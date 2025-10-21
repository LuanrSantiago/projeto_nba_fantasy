    
WITH data_filter AS (    
    SELECT playerId,
        PlayerName_Limpo AS name,
        Temporada,
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
    FROM player_totals_5_seasons
)

SELECT * FROM data_filter 
WHERE name = "STEVEN ADAMS"