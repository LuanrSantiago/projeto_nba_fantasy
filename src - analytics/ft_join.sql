SELECT 
    t1.playerId,
    t1.name,
    t1.position,
    t1.Temporada,
    t1.team,
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
    t2.fantasyPointsGame,
    t2.fantasyPointsMinute,
    t2.fantasyPointsStarted,
    t2.percentPointFantasyTeam,
    t2.fantasyPointsPer36,
    t2.pointsAssistRatio,
    t3.groupPerformance,
    t3.careerPeak,
    t3.deltaCareerPeak

FROM fantasyPoints AS t1

LEFT JOIN ft_gameStats AS t2
ON t1.playerId = t2.playerId AND t1.Temporada = t2.Temporada

LEFT JOIN ft_classification AS t3
ON t1.playerId = t3.playerId AND t1.Temporada = t3.Temporada

