WITH dataPlayersFantasy AS (    
    SELECT 
        playerId,
        PlayerName_Limpo AS name,
        Temporada,
        games,
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
        fieldPercent
    FROM player_totals_seasons
), 

tableFantasyPoints AS (
    SELECT
        t1.playerId,
        t1.Temporada,
        t1.PlayerName_Limpo,
        
        -- Colunas de Estatísticas da Tabela Principal (t1)
        -- As subconsultas (SELECT Pontos...) garantem o peso correto de cada regra (r)
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

    ORDER BY
        t1.Temporada ASC, t1.PlayerName_Limpo ASC
)

SELECT
    d.*,
    t2.fantasyScore    
FROM dataPlayersFantasy AS d
LEFT JOIN tableFantasyPoints AS t2
ON d.playerId = t2.playerId AND d.Temporada = t2.Temporada
GROUP BY
    d.playerId,
    d.Temporada,
    d.name
ORDER BY d.name ASC, d.Temporada ASC
