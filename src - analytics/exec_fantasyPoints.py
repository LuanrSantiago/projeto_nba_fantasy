# %%

import pandas as pd
import sqlalchemy

# %%

def import_query(path):
    with open(path) as open_file:
        query = open_file.read()
    return query

query = import_query("fantasyPoints.sql")

engine_app = sqlalchemy.create_engine("sqlite:///../data/nba_fantasy/nba_analytics_rest.db")

engine_analytical = sqlalchemy.create_engine("sqlite:///../data/analytics/nba_analytics.db")

# %%

df = pd.read_sql(query, engine_app)
df.to_sql("fantasyPoints", engine_analytical, index=False, if_exists="append")

# %%
