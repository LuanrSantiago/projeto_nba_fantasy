# %%

import pandas as pd
import sqlalchemy

# %%

def import_query(path):
    with open(path) as open_file:
        query = open_file.read()
    return query

query = import_query("fantasyPoints.sql")

engine = sqlalchemy.create_engine("sqlite:/nba_analytics_rest.db")

# %%
