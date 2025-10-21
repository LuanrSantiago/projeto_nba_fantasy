# %%
import requests
import json
import pandas as pd
import sqlite3
from datetime import datetime
from unidecode import unidecode

# %%

# --- 1. CONFIGURAÇÃO DA NOVA API (rest.nbaapi.com) ---
# A nova API não usa RapidAPI Key. Ela usa uma estrutura de URL mais direta.
BASE_URL = "http://rest.nbaapi.com/api/PlayerDataTotals/season/"

# A API rest.nbaapi.com não precisa de headers de autenticação como a RapidAPI.
# O método GET que usaremos é: /api/PlayerDataTotals/season/{season}

# --- 2. FUNÇÃO DE EXTRAÇÃO (E) para rest.nbaapi.com ---
def extrair_estatisticas_jogadores_nova_api(temporada: int, base_url: str):
    """
    Extrai as estatísticas dos jogadores da API: rest.nbaapi.com
    Endpoint: /api/PlayerDataTotals/season/{season}
    """
    
    url_completa = f"{base_url}{temporada}"
    print(f"Fazendo requisição para: {url_completa}...")
    
    try:
        # Não precisa de 'headers' ou 'params' como a RapidAPI
        response = requests.get(url_completa)
        response.raise_for_status() 

        # A resposta desta API retorna um JSON que é uma lista de objetos
        dados_jogadores = response.json()
        
        if not dados_jogadores:
            print("Nenhum dado encontrado para a temporada.")
            return pd.DataFrame()

        df = pd.json_normalize(dados_jogadores)
        # Adiciona a coluna de temporada para facilitar a análise posterior
        df['Temporada'] = temporada 
        print(f"Dados extraídos. Total de linhas: {len(df)}")
        
        return df

    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição da API ({url_completa}): {err}")
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON. A resposta pode não ser válida.")
    
    return pd.DataFrame()


# --- 3. FUNÇÃO DE CARGA (L) ---
# Esta função permanece a mesma.
def carregar_para_sqlite(df: pd.DataFrame, db_file: str, nome_tabela: str, if_exists: str = 'append'):
    """Carrega o DataFrame para uma tabela SQLite."""
    print(f"Iniciando conexão com o banco de dados: {db_file}")
    
    try:
        conn = sqlite3.connect(db_file)
        # Usamos 'append' para adicionar os dados de cada temporada
        df.to_sql(
            nome_tabela, 
            conn, 
            if_exists=if_exists, 
            index=False 
        )
        print(f"Sucesso! {len(df)} linhas carregadas na tabela '{nome_tabela}'.")
        
    except Exception as e:
        print(f"Erro ao carregar dados para o SQLite: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

#--- NOVA FUNÇÃO DE TRANSFORMAÇÃO (T) ---
def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza a limpeza de dados, focando em remover acentos e caracteres especiais, 
    além de converter os nomes para CAIXA ALTA (UPPERCASE).
    """
    print("Iniciando a etapa de transformação de dados...")
    
    # Coluna do nome do jogador
    COLUNA_NOME = 'playerName' 
    
    if COLUNA_NOME not in df.columns:
        print(f"Aviso: Coluna '{COLUNA_NOME}' não encontrada. Pulando limpeza de nomes.")
        return df
        
    # Lógica de Limpeza e Padronização:
    # 1. Aplica unidecode para remover acentos (é, ç, etc.)
    # 2. Converte o nome para string (caso não seja)
    # 3. Converte o resultado para CAIXA ALTA
    df['PlayerName_Limpo'] = (
        df[COLUNA_NOME]
        .apply(lambda name: unidecode(str(name)).upper())
    )
    
    print("Nomes dos jogadores limpos, sem acentos e em CAIXA ALTA ('PlayerName_Limpo').")
    return df


# --- Pipeline E+L para as Últimas 5 Temporadas ---
if __name__ == '__main__':
    
    NOME_DO_BANCO = 'nba_analytics_rest.db'
    NOME_DA_TABELA = 'player_totals_5_seasons'
    
    # Define as últimas 5 temporadas. (Ajuste conforme o ano atual)
    ano_atual = datetime.now().year
    # Assumindo que a temporada é nomeada pelo ano de início (ex: 2022-2023 é '2022')
    # A API rest.nbaapi.com usa o formato '2023-24' para a temporada. Vamos usar o ano de início.
    # Ex: 2023 = 2023-2024
    
    # Ex: As 5 temporadas mais recentes (assumindo a temporada 2023-2024 é a mais atual)
    # Se for Outubro/2025, o ano final completo pode ser 2024 (2024-2025).
    # Vamos usar as 5 temporadas anteriores ao ano atual:
    ultimas_5_temporadas = range(ano_atual - 5, ano_atual) 
    # Ex: Se ano_atual é 2025, vai de 2020 a 2024.

    # Lista para armazenar todos os DataFrames (opcional, mas bom para debug)
    todos_dfs_limpos = []
    
    # 1. Loop sobre as temporadas para Extração (E) e Carga (L)
    # A tabela será recriada na primeira temporada e 'appended' nas seguintes
    if_exists_mode = 'replace'
    
    for temporada in ultimas_5_temporadas:
            print("-" * 50)
            
            # 1. Extração (E)
            df_dados_brutos = extrair_estatisticas_jogadores_nova_api(
                temporada=temporada,
                base_url=BASE_URL 
            )
            
            if not df_dados_brutos.empty:
                
                # 2. Transformação (T)
                df_dados_limpos = transformar_dados(df_dados_brutos)
                todos_dfs_limpos.append(df_dados_limpos)
                
                # 3. Carga (L)
                carregar_para_sqlite(
                    df=df_dados_limpos, # <--- Carregando o DF LIMPO
                    db_file=NOME_DO_BANCO, 
                    nome_tabela=NOME_DA_TABELA,
                    if_exists=if_exists_mode 
                )
                if_exists_mode = 'append' 
            else:
                print(f"Pulando a temporada {temporada} devido à falha na extração.")

    print("\n" + "=" * 50)
    print("Pipeline E+T+L de 5 temporadas concluído.")
        
    # Opcional: Combinar todos os dados em um DataFrame final na memória
    if todos_dfs_limpos:
        df_final_memoria = pd.concat(todos_dfs_limpos, ignore_index=True)
        print(f"Total de linhas salvas no DB: {len(df_final_memoria)}")
    else:
        print("Nenhum dado foi extraído com sucesso.")

# %%
