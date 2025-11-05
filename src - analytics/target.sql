WITH tb_join AS (
    SELECT 
        t1.Temporada,
        t1.playerId,
        t1.name,
        t1.fantasyScore,
        t2.fantasyScore AS nextFantasyScore,
        t2.fantasyScore - t1.fantasyScore AS scoreChange,
        CASE WHEN t2.fantasyScore > t1.fantasyScore THEN 1 ELSE 0 END AS flagFsGrow
        --ROW_NUMBER() OVER (PARTITION BY t1.playerId ORDER BY random()) AS RandomCol
    FROM ft_gameStats AS t1
    LEFT JOIN ft_gameStats AS t2
    ON t1.playerId = t2.playerId AND t1.Temporada + 1 = t2.Temporada
)

SELECT * 
FROM tb_join
--WHERE RandomCol <= 2
ORDER BY playerId, Temporada
