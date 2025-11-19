WITH dataPlayersFantasy AS (    
    SELECT
        playerId,
        PlayerName_Limpo AS name,
        position,
        Temporada,
        team,
        age,
        games,
        gamesStarted,
        minutesPg,
        points,
        assists,
        totalRb as rebounds,
        steals,
        blocks,
        turnovers,
        personalFouls,
        ftPercent,
        twoPercent,
        threePercent,
        fieldPercent,
        
        -- Coluna que identifica se existe a linha 'TOT' para este jogador/temporada
        MAX(CASE WHEN team = 'TOT' THEN 1 ELSE 0 END) 
            OVER (PARTITION BY playerId, Temporada) AS HasTotLine
            
    FROM player_totals_seasons
), 
-- CTE para selecionar APENAS a linha consolidada (TOT) ou a única linha
dataPlayersFantasyClean AS (
    SELECT
        playerId,
        name,
        position,
        Temporada,
        team,
        age,
        games,
        gamesStarted,
        minutesPg,
        points,
        assists,
        rebounds,
        steals,
        blocks,
        turnovers,
        personalFouls,
        ftPercent,
        twoPercent,
        threePercent,
        fieldPercent
        
    FROM dataPlayersFantasy
    
    -- FILTRO PRINCIPAL: Seleciona APENAS a linha consolidada (TOT) se ela existir,
    -- OU a única linha se a linha TOT não existir (jogadores que não trocaram de time).
    WHERE 
        (HasTotLine = 1 AND team = 'TOT') -- Se tem linha TOT, pega só a TOT
        OR 
        (HasTotLine = 0)                     -- Se não tem linha TOT, pega a única linha
    
), 

tableFantasyPoints AS (
    SELECT
        t1.playerId,
        t1.Temporada,
        t1.PlayerName_Limpo,
        t1.team,
        -- Coluna para identificar se existe a linha 'TOT' (necessário para o filtro)
        MAX(CASE WHEN t1.team = 'TOT' THEN 1 ELSE 0 END) 
            OVER (PARTITION BY t1.playerId, t1.Temporada) AS HasTotLineForFantasy,
        (
            IFNULL (t1.twoFg * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'twoFg') ,0)+
            IFNULL(t1.twoAttempts * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'twoAttemps') ,0)+
            IFNULL(t1.ft * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'ft') ,0)+
            IFNULL(t1.ftAttempts * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'ftAttemps') ,0)+
            IFNULL(t1.threeFg * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'threeFg') ,0)+
            IFNULL(t1.totalRb * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'totalRb') ,0)+
            IFNULL(t1.assists * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'assists') ,0)+
            IFNULL(t1.steals * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'steals') ,0)+
            IFNULL(t1.blocks * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'blocks') ,0)+
            IFNULL(t1.turnovers * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'turnovers') ,0)+
            IFNULL(t1.points * (SELECT Pontos FROM regras_fantasy WHERE Estatistica = 'points'), 0)
        ) AS fantasyScore
        
    FROM 
        player_totals_seasons t1
)

SELECT
    d.playerId,
    d.name,
    d.position,
    d.Temporada,
    d.team,
    d.age,
    d.games,
    d.gamesStarted,
    d.minutesPg,
    d.points,
    d.assists,
    d.rebounds,
    d.steals,
    d.blocks,
    d.turnovers,
    d.personalFouls,
    d.ftPercent,
    d.twoPercent,
    d.threePercent,
    d.fieldPercent,
    t2.fantasyScore
FROM dataPlayersFantasyClean AS d 
LEFT JOIN (
    -- Subquery para aplicar o filtro de consolidação na tabela de Fantasy Points
    SELECT 
        playerId,
        Temporada,
        fantasyScore 
    FROM tableFantasyPoints
    WHERE 
        (HasTotLineForFantasy = 1 AND team = 'TOT') -- Filtra pela linha TOT
        OR 
        (HasTotLineForFantasy = 0)                               -- OU pela única linha
) AS t2
ON d.playerId = t2.playerId AND d.Temporada = t2.Temporada
ORDER BY d.name ASC, d.Temporada ASC