DROP TABLE IF EXISTS abt_FsGrow;

CREATE TABLE abt_FsGrow AS

WITH tb_target AS (
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

SELECT 
    t1.playerId,
    t1.name,
    t1.position,
    t1.Temporada,
    t1.team,
    t2.flagFsGrow,
    t1.age,
    t1.games,
    t1.gamesStarted,
    t1.minutesPg,
    t1.points,
    t1.assists,
    t1.rebounds,
    t1.steals,
    t1.blocks,
    t1.turnovers,
    t1.personalFouls,
    t1.ftPercent,
    t1.twoPercent,
    t1.threePercent,
    t1.fieldPercent,
    t1.fantasyScore,
    t1.fantasyPointsGame,
    t1.fantasyPointsMinute,
    t1.fantasyPointsStarted,
    t1.percentPointFantasyTeam,
    t1.fantasyPointsPer36,
    t1.pointsAssistRatio,
    t1.groupPerformance,
    t1.careerPeak,
    t1.deltaCareerPeak,
    t2.nextFantasyScore,
    t2.scoreChange
FROM ft_join AS t1
LEFT JOIN tb_target AS t2
ON t1.playerId = t2.playerId AND t1.Temporada= t2.Temporada

--WHERE RandomCol <= 2
ORDER BY t1.playerId, t1.Temporada;