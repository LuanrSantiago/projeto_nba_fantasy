WITH tableFantasyPointsTeam AS (
    SELECT 
        team,
        Temporada,
        SUM(fantasyScore) AS fpTeam 
    FROM fantasyPoints 
    GROUP BY team, Temporada
)

SELECT 
    t1.*,
    1. *(t1.fantasyScore / t1.games) AS fantasyPointsGame,
    1. *(t1.fantasyScore / t1.minutesPg) AS fantasyPointsMinute,
    IFNULL (1. *(t1.fantasyScore / t1.gamesStarted),0) AS fantasyPointsStarted,
   1. *(t1.fantasyScore / t2.fpTeam) AS percentPointFantasyTeam,
    CASE 
        WHEN t1.minutesPg > 0 THEN 1. *(t1.fantasyScore / t1.minutesPg) * 36 ELSE 0 
        END AS fantasyPointsPer36,
    CASE
        WHEN t1.assists > 0 THEN 1. *(t1.points * 1.0 / t1.assists)
        ELSE 0 
    END AS pointsAssistRatio
FROM 
    fantasyPoints AS t1
LEFT JOIN tableFantasyPointsTeam AS t2
ON t1.team = t2.team AND t1.Temporada = t2.Temporada
ORDER BY t1.Temporada, t1.name


