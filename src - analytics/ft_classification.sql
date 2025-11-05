WITH RankedPlayers AS (
    SELECT
        *,
        NTILE(4) OVER (ORDER BY fantasyPointsPer36 ASC) AS Performance_Rank_Num
    FROM 
        ft_gameStats
),

groupPerformance AS (
    SELECT
        t1.playerId,
        t1.Temporada,
        CASE t1.Performance_Rank_Num
            WHEN 1 THEN 'Nível 1: Below Average'
            WHEN 2 THEN 'Nível 2: Average'
            WHEN 3 THEN 'Nível 3: Above Average'
            WHEN 4 THEN 'Nível 4: Elite'
            ELSE NULL 
        END AS groupPerformance
        
    FROM 
        RankedPlayers t1
)    

SELECT * FROM groupPerformance