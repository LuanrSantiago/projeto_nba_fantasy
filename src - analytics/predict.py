# %%

import pandas as pd
import sqlalchemy

con = sqlalchemy.create_engine("sqlite:///../data/analytics/nba_analytics.db")

model = pd.read_pickle("model_fsGrow.pkl")

# %%

data = pd.read_sql("SELECT * FROM abt_FsGrow", con)

predict = model['model'].predict_proba(data[model["features"]])[:,1]

data["predict"] = predict

data

# %%
