# %%

import pandas as pd
import sqlalchemy
import mlflow

con = sqlalchemy.create_engine("sqlite:///../data/analytics/nba_analytics.db")

mlflow.set_tracking_uri("http://127.0.0.1:5000")

model = mlflow.sklearn.load_model("models:///model_fsGrow/1")

# %%
model

# %%

data = pd.read_sql("SELECT * FROM abt_FsGrow WHERE Temporada = '2024'", con)

predict = model.predict_proba(data[model.feature_names_in_])[:,1]

data["predict"] = predict

data_ordenada = data.sort_values(by='predict', ascending=False)

top_50 = data_ordenada.head(50)

top_50.to_excel("top_50_previsoes.xlsx", index=False)

# %%
