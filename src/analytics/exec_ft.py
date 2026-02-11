# %%

import pandas as pd
import sqlalchemy
import argparse
from pathlib import Path

# %%

def import_query(path):

    with open(path) as open_file:
        query = open_file.read()
    return query

def exec_query(table, db_target):

    base_dir = Path(__file__).resolve().parent.parent

    db_path_analytical = base_dir.joinpath('data', db_target, 'nba_analytics.db')
    
    engine_analytical = sqlalchemy.create_engine(f"sqlite:///{db_path_analytical}")

    query = import_query(f"{table}.sql")

    df = pd.read_sql(query, engine_analytical)
    df.to_sql(table, engine_analytical, index=False, if_exists="replace")

    print(f"Dados carregados com sucesso! Tabela '{table}' atualizada.")

# %%
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--db_target", default = 'analytics')
    parser.add_argument("--table", type=str, help= "Tabela que será processada com o mesmo nome do arquivo")

    args = parser.parse_args()

    exec_query(args.table, args.db_target)

if __name__ == "__main__":
    main()