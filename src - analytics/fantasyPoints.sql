WITH dataPlayersFantasy AS (    
    SELECT 
        playerId,
        PlayerName_Limpo AS name,
        position,
        Temporada,
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
        age,
        team

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
        ) AS fantasyScore,
        t1.team
        
    FROM 
        player_totals_seasons t1

    ORDER BY
        t1.Temporada ASC, t1.PlayerName_Limpo ASC
),

tableFantasyPointsTeam AS (
    SELECT 
        team,
        Temporada,
        SUM(fantasyScore) AS fpTeam 
    FROM tableFantasyPoints 
    GROUP BY team, Temporada
)

SELECT
    d.*,
    t2.fantasyScore,
    ROUND(t2.fantasyScore / d.games,2) AS fantasyPointsGame,
    ROUND(t2.fantasyScore / d.minutesPg,2) AS fantasyPointsMinute,
    IFNULL(ROUND(t2.fantasyScore / d.gamesStarted,2),0) AS fantasyPointsStarted,
    ROUND((t2.fantasyScore / t3.fpTeam),2) AS percentPointFantasyTeam,
    CASE 
        WHEN d.minutesPg > 0 THEN ROUND((t2.fantasyScore / d.minutesPg) * 36, 2) ELSE 0 
    END AS fantasyPointsPer36,
    CASE
        WHEN d.assists > 0 THEN ROUND(d.points * 1.0 / d.assists, 2)
        ELSE 0 
    END AS pointsAssistRatio
FROM dataPlayersFantasy AS d
LEFT JOIN tableFantasyPoints AS t2
ON d.playerId = t2.playerId AND d.Temporada = t2.Temporada
LEFT JOIN tableFantasyPointsTeam as t3
ON d.team = t3.team
GROUP BY
    d.playerId,
    d.Temporada,
    d.name
ORDER BY d.name ASC, d.Temporada ASC
