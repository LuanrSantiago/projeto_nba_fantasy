# %%

import pandas as pd
import sqlalchemy
from sklearn import model_selection, tree, metrics, pipeline
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

# SAMPLE - TESTE E TREINO

target = 'flagFsGrow'
features_to_exclude = ['flagFsGrow', 'nextFantasyScore', 'scoreChange', 'playerId', 'name', 'Temporada', 'team', 'position']
features = [col for col in df.columns if col not in features_to_exclude]
#features = df.columns.tolist()[5:]

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

# EXPLORE - BIVARIADA

cat_features = X_train.dtypes[X_train.dtypes == 'object'].index.tolist()
num_features = list(set(features) - set(cat_features))

df_train = X_train.copy()
df_train[target] = y_train.copy()
df_train[num_features] = df_train[num_features].astype(float)

bivariada = df_train.groupby(target)[num_features].median().T
bivariada['ratio'] = (bivariada[1] + 0.001) / (bivariada[0] + 0.001) 
bivariada.sort_values(by='ratio', ascending=False)

bivariada_cat = df_train.groupby('groupPerformance')[target].mean()

# %%

# MODIFY - DROP

# to_remove = bivariada[bivariada['ratio']==1].index.tolist()
# if len(to_remove) > 0:
#     drop_feat = selection.DropFeatures(to_remove)
#     X_train_transform = drop_feat.fit_transform(X_train)
# else:
#     X_train_transform = X_train.copy()


# %%

# MODIFY - FILL MISSING

fill_0 = ['ftPercent', 'twoPercent', 'threePercent', 'fieldPercent'] 
imput_0 = imputation.ArbitraryNumberImputer(arbitrary_number=0,variables=fill_0)

fill_9999 = ['careerPeak','deltaCareerPeak']
imput_9999 = imputation.ArbitraryNumberImputer(arbitrary_number=-9999, variables=fill_9999)

# %%

# MODIFY - ONEHOT

onehot = encoding.OneHotEncoder(variables=['groupPerformance'])

# %%

# MODEL

model = tree.DecisionTreeClassifier(random_state=42, min_samples_leaf=50)


# %%

# CRIANDO PIPELINE

model_pipeline = pipeline.Pipeline(steps=[
    ('Imputação de Zeros', imput_0),
    ('Imputação de -9999', imput_9999),
    ('OneHot Encoding', onehot),
    ('Algoritmo', model)
])

model_pipeline.fit(X_train, y_train)

# %%

# ASSESS - TREINOS

y_pred_train = model_pipeline.predict(X_train)
y_proba_train = model_pipeline.predict_proba(X_train)

acc_train = metrics.accuracy_score(y_train, y_pred_train)
auc_train = metrics.roc_auc_score(y_train, y_proba_train[:,1])

print('Acurácia Treino:', acc_train)
print('AUC Treino:', auc_train)

# %%

# ASSESS - TESTE

y_pred_test = model_pipeline.predict(X_test)
y_proba_test = model_pipeline.predict_proba(X_test)

acc_test = metrics.accuracy_score(y_test, y_pred_test)
auc_test = metrics.roc_auc_score(y_test, y_proba_test[:,1])

print('Acurácia Teste:', acc_test)
print('AUC Teste:', auc_test)

# %%

features_names = X_train_transform.columns.tolist()

feature_importance = pd.Series(model.feature_importances_, index=features_names)
feature_importance.sort_values(ascending=False)

# %%
