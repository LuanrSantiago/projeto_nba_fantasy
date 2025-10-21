PROJETO NBA ANALYST

Criei esse projeto afim de aprimorar meus conhecimentos técnicos em Data Science junto a minha paixão com a NBA.
Para primeira versão, meu objetivo é praticar meus aprendizados e entender mais sobre a base de dados que possuo.

Quero estabelecer conexões cruas entre estátisticas dos jogadores por temporada e prever o comportamento dele através do seu histórico.

Exemplo: um jogador A com médias 20ppg, 5apg e 8rpg irá melhorar na próxima temporada? Ele terá mais ppg? Outro estátistica irá melhorar?
Esse tipo de perguntar que estou em mente que posso prever com o estudo em questão.


OBJETIVO
Prever o percentual de mudança (aumento ou queda) nas principais estatísticas (PPG, RPG, APG)
do jogador na próxima temporada (T+1) em relação à atual (T).

Classificar o jogador em categorias na próxima temporada: (1) Regressão (quedas significativas em stats),
(2) Estável (mudança mínima) ou (3) Progressão (aumento significativo em stats).

FEATURE ENGINEERING
Melhoria, Ação Necessária e Valor em DS
Histórico Temporal: "Para cada jogador/temporada, você precisará de todas as estatísticas dos anos anteriores.",
"Modelos precisam de sequências (ex: o jogador melhorou dos 20 para 21 anos, mas estagnou nos 22)."

Variáveis de Contexto:"Adicione colunas como: Idade, AnosDeLiga (carreira), e Posição (PG, SG, PF, etc.).",
A progressão de um Rookie é diferente da de um Veterano. Idade é o preditor mais forte de progressão.

Métricas Avançadas: "Calcule estatísticas avançadas, mesmo que não estejam diretamente na API: USG% (taxa de uso),
TS% (percentual de arremessos verdadeiros), +/- (plus/minus).", "Essas métricas avançadas são preditores mais fortes 
do que as estatísticas básicas (PPG, RPG)."

Criação do Alvo (Target): Crie a variável que você quer prever. Ex: Target_PPG_Proxima_Temporada 
(o valor real da próxima temporada) ou Mudanca_PPG = PPG(T+1) - PPG(T), Essencial para Treinamento de Modelos Supervisionados.


MODELAGEM
Exploração (EDA): Gere gráficos de dispersão: PPG vs. Idade; Mudanca_PPG vs. AnosDeLiga,
Entender se a base de dados confirma a curva de progressão do jogador (o pico geralmente ocorre por volta dos 27 anos).

Modelagem Inicial: Regressão Linear Múltipla ou Random Forest Regressor,Fornece uma linha de base (baseline) para a 
performance do seu modelo e é simples de interpretar.
Modelagem Avançada: Modelos de Série Temporal (se você estruturar os dados como sequências temporais) ou Gradient Boosting 
(XGBoost/LightGBM), Estes modelos são poderosos para capturar interações complexas entre as estatísticas de um jogador 
ao longo do tempo.