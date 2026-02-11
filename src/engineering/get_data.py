# %%

import os
import requests
import json
import pandas as pd
import sqlite3
from datetime import datetime
from unidecode import unidecode
from nba_api.stats.endpoints import leaguedashplayerstats

# --- CONFIGURAÇÕES DE CAMINHOS (Igual à estrutura da aula) ---
# Define onde o banco de dados será salvo. 
# "../.." sobe duas pastas, entra em "data", cria uma pasta "nba_fantasy" e salva o arquivo.
DATA_DIR = os.path.join("..", "..", "data", "nba_fantasy")
DB_NAME = "nba_analytics.db"
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

# --- 1. FUNÇÕES DE SUPORTE (Sua lógica original) ---

def extrair_estatisticas_jogadores_nova_api(temporada: int):
    """
    Extrai dados usando a biblioteca oficial nba_api.
    A temporada deve ser no formato '2021-22'.
    """
    # Converte 2021 para '2021-22'
    season_str = f"{temporada}-{str(temporada + 1)[-2:]}"
    print(f"Extraindo dados oficiais da NBA para a temporada: {season_str}...")
    
    try:
        # Pega as estatísticas totais da temporada
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season_str,
            per_mode_detailed='Totals' # Pega os totais, não média por jogo
        )
        
        df = stats.get_data_frames()[0]
        
        # A biblioteca retorna colunas em CAIXA ALTA e nomes ligeiramente diferentes.
        # Vamos renomear para manter compatibilidade com seu código antigo se necessário
        # Mas para o Fantasy, as colunas principais são:
        # PLAYER_NAME, PTS, AST, REB, STL, BLK, TOV, FGM, FGA, FG3M, FTM, FTA
        
        df['Temporada'] = temporada
        
        # Pequeno ajuste para garantir que sua função de transformação encontre o nome
        if 'PLAYER_NAME' in df.columns:
            df.rename(columns={'PLAYER_NAME': 'playerName'}, inplace=True)
            
        return df

    except Exception as err:
        print(f"Erro ao extrair da NBA API ({season_str}): {err}")
        return pd.DataFrame()

def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:
    print("Transformando dados...")
    coluna_nome = 'playerName'
    if coluna_nome in df.columns:
        df['PlayerName_Limpo'] = (
            df[coluna_nome]
            .apply(lambda name: unidecode(str(name)).upper())
        )
    return df

def carregar_para_sqlite(df: pd.DataFrame, db_path: str, nome_tabela: str, if_exists: str = 'append'):
    try:
        # Conecta diretamente no caminho final
        conn = sqlite3.connect(db_path)
        df.to_sql(nome_tabela, conn, if_exists=if_exists, index=False)
        print(f"Sucesso! {len(df)} linhas salvas em {db_path}.")
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def carregar_regras_fantasy(db_path: str):
    regras = {
        'twoFg': 2.0, 'twoAttemps': -1.0, 'ft': 1.0, 'ftAttemps': -1.0, 
        'threeFg': 1.0, 'totalRb': 1.0, 'assists': 2.0, 'steals': 4.0, 
        'blocks': 4.0, 'turnovers': -2.0, 'points': 1.0
    }
    df_regras = pd.DataFrame(list(regras.items()), columns=['Estatistica', 'Pontos'])
    
    conn = sqlite3.connect(db_path)
    df_regras.to_sql('regras_fantasy', conn, if_exists='replace', index=False)
    conn.close()
    print("Tabela de regras atualizada.")

# --- 2. EXECUÇÃO DO PIPELINE (Onde a mágica acontece) ---

if __name__ == '__main__':
    
    # 1. Garante que a pasta existe (similar ao mkdir)
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Diretório criado: {DATA_DIR}")

    # 2. Define o período de extração
    ano_atual = datetime.now().year
    # Pegando as ultimas 5 temporadas completas
    ultimas_temporadas = range(ano_atual - 5, ano_atual) 

    print(f"Iniciando atualização do banco de dados em: {DB_PATH}")
    print(f"Temporadas alvo: {list(ultimas_temporadas)}")

    # 3. Carrega as regras primeiro
    carregar_regras_fantasy(DB_PATH)

    # 4. Loop de Extração e Carga
    # Na primeira passada, usamos 'replace' para limpar dados antigos da tabela.
    # Nas seguintes, usamos 'append'.
    modo_escrita = 'replace' 

    for temporada in ultimas_temporadas:
        print(f"\n--- Processando temporada {temporada} ---")
        
        # E (Extract)
        df_bruto = extrair_estatisticas_jogadores_nova_api(temporada)
        
        if not df_bruto.empty:
            # T (Transform)
            df_limpo = transformar_dados(df_bruto)
            
            # L (Load)
            carregar_para_sqlite(
                df=df_limpo, 
                db_path=DB_PATH, 
                nome_tabela='player_totals_seasons', 
                if_exists=modo_escrita
            )
            
            # Depois da primeira temporada, mudamos para append para não apagar o que acabamos de salvar
            modo_escrita = 'append' 
        else:
            print(f"Sem dados para a temporada {temporada}.")

    print("\n" + "="*50)
    print("ATUALIZAÇÃO CONCLUÍDA COM SUCESSO")
    print("="*50)
# %%
