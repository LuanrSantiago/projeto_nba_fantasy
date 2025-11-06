# %%

import pandas as pd
import sqlalchemy
from sklearn import model_selection

con = sqlalchemy.create_engine("sqlite:///../data/analytics/nba_analytics.db")

# %%

# SAMPLE - IMPORT DE DADOS

df = pd.read_sql("abt_FsGrow", con)
df.head()

# %%

# SAMPLE - OOT

df_oot = df[df['Temporada']==df['Temporada'].max()].reset_index(drop=True)
df_oot

# %%

# SAMPLE - Teste e Treino

target = 'flagFsGrow'
features = df.columns.tolist()[6:]

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

# %%

bivariada_cat = df_train.groupby('groupPerformance')[target].mean()
bivariada_cat
# %%
