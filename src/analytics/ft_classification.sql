WITH rankedPlayers AS (
    SELECT
        *,
        NTILE(4) OVER (ORDER BY fantasyPointsPer36 ASC) AS Performance_Rank_Num
    FROM 
        ft_gameStats
),

groupPerformance AS (
    SELECT
        playerId,
        Temporada,
        CASE Performance_Rank_Num
            WHEN 1 THEN 'Nivel 1: Below Average'
            WHEN 2 THEN 'Nivel 2: Average'
            WHEN 3 THEN 'Nivel 3: Above Average'
            WHEN 4 THEN 'Nivel 4: Elite'
            ELSE NULL 
        END AS groupPerformance
        
    FROM 
        rankedPlayers ),

careerPeak AS (
    SELECT
        *,
        MAX(fantasyScore) OVER (PARTITION BY playerId ORDER BY Temporada 
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
                ) AS careerPeak

    FROM ft_gameStats 
),

careerPeakTotal AS (
    SELECT
        *,
        (fantasyScore - careerPeak) AS deltaCareerPeak 
        
    FROM careerPeak
)

SELECT 
    t1.playerId,
    t1.Temporada,
    t2.groupPerformance,
    t3.careerPeak,
    t4.deltaCareerPeak

FROM rankedPlayers AS t1

LEFT JOIN groupPerformance AS t2
ON t1.playerId = t2.playerId AND t1.Temporada = t2.Temporada

LEFT JOIN careerPeak AS t3
ON t1.playerId = t3.playerId AND t1.Temporada = t3.Temporada

LEFT JOIN careerPeakTotal AS t4
ON t1.playerId = t4.playerId AND t1.Temporada = t4.Temporada


ORDER BY t1.playerId, t1.Temporada
