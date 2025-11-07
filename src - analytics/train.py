# %%

import pandas as pd
import sqlalchemy
from sklearn import model_selection
from feature_engine import selection, imputation, encoding

con = sqlalchemy.create_engine("sqlite:///../data/analytics/nba_analytics.db")

# %%

# SAMPLE - IMPORT DE DADOS

df = pd.read_sql("SELECT * FROM abt_FsGrow", con)
df.head()

# %%

# SAMPLE - OOT

df_oot = df[df['Temporada']==df['Temporada'].max()].reset_index(drop=True)
df_oot

# %%

# SAMPLE - Teste e Treino

target = 'flagFsGrow'
features_to_exclude = ['flagFsGrow', 'nextFantasyScore', 'scoreChange']
features = [col for col in df.columns if col not in features_to_exclude]

df_train_test = df[df['Temporada']<df['Temporada'].max()].reset_index(drop=True)

X = df_train_test[features]
y = df_train_test[target]

X_train, X_test, y_train, y_test = model_selection.train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Base Treino: {y_train.shape[0]} Unid. | Tx. Target {100*y_train.mean():.2f}%")
print(f"Base Test: {y_test.shape[0]} Unid. | Tx. Target {100*y_test.mean():.2f}%")


# %%

# EXPLORE - MISSING

s_nas = X_train.isna().mean()
s_nas = s_nas[s_nas>0]
s_nas


# %%

cat_features = X_train.dtypes[X_train.dtypes == 'object'].index.tolist()
num_features = list(set(features) - set(cat_features))
num_features

df_train = X_train.copy()
df_train[target] = y_train.copy()
df_train[num_features] = df_train[num_features].astype(float)

bivariada = df_train.groupby(target)[num_features].median().T
bivariada['ratio'] = (bivariada[1] + 0.001) / (bivariada[0] + 0.001) 
bivariada.sort_values(by='ratio', ascending=False)

bivariada_cat = df_train.groupby('groupPerformance')[target].mean()


# %%

# MODIFY - DROP

to_remove = bivariada[bivariada['ratio']==1].index.tolist()

if len(to_remove) > 0:
    drop_features = selection.DropFeatures(to_remove)
    X_train_transform = drop_features.fit_transform(X_train)
else:
    X_train_transform = X_train.copy()



# %%

# MODIFY - FILL MISSING

fill_0 = ['ftPercent', 'twoPercent', 'threePercent', 'fieldPercent'] 
imput_0 = imputation.ArbitraryNumberImputer(arbitrary_number=0,variables=fill_0)

fill_9999 = ['careerPeak','deltaCareerPeak']
imput_9999 = imputation.ArbitraryNumberImputer(arbitrary_number=-9999, variables=fill_9999)


# %%

# MODIFY - ONEHOT

onehot = encoding.OneHotEncoder(variables=['groupPerformance'])

#%%

# MODIFY - APLICANDO TRANSFORMAÇÕES NO DATASET

X_train_transform = imput_0.fit_transform(X_train_transform)
X_train_transform = imput_9999.fit_transform(X_train_transform)
X_train_transform = onehot.fit_transform(X_train_transform)
X_train_transform

# %%

# MODEL

from sklearn import tree, metrics, ensemble

model = tree.DecisionTreeClassifier(random_state=42, min_samples_leaf=50)
model.fit(X_train_transform, y_train)


# %%

# ASSESS

y_pred_train = model.predict(X_train_transform)
y_proba_train = model.predict_proba(X_train_transform)

acc_train = metrics.accuracy_score(y_train, y_pred_train)
auc_train = metrics.roc_auc_score(y_train, y_proba_train[:,1])

print('Acurácia Treino:', acc_train)
print('AUC Treino:', auc_train)

# %%

if len(to_remove) > 0:
    X_test_transform = drop_features.transform(X_test)
else:
    X_test_transform = X_test.copy()

X_test_transform = imput_0.transform(X_test_transform)
X_test_transform = imput_9999.transform(X_test_transform)
X_test_transform = onehot.transform(X_test_transform)

y_pred_test = model.predict(X_test_transform)
y_proba_test = model.predict_proba(X_test_transform)

acc_test = metrics.accuracy_score(y_test, y_pred_test)
auc_test = metrics.roc_auc_score(y_test, y_proba_test[:,1])

print('Acurácia Teste:', acc_test)
print('AUC Teste:', auc_test)

# %%

# y_pred_fodace = pd.Series([0]*y_test.shape[0])
# y_proba_fodace = pd.Series([y_train.mean()]*y_test.shape[0])

# acc_fodace = metrics.accuracy_score(y_test, y_pred_fodace)
# auc_fodace = metrics.roc_auc_score(y_test, y_proba_fodace)

# print('Acurácia fodace:', acc_fodace)
# print('AUC fodace:', auc_fodace)

# %%

features_names = X_train_transform.columns.tolist()

feature_importance = pd.Series(model.feature_importances_, index=features_names)
feature_importance.sort_values(ascending=False)

# %%
