SELECT 
    t1.*,
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

