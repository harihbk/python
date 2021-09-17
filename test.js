test = IF(StandardContinuous="Standard",
(Round((IF(PairSingle="Pair",
WidthsPerCurtain*2,WidthsPerCurtain)*(IF(StandardContinuous="Standard",
(FabricWidth/10),
(FabricDrop/10))))/if(Measurement="mm",WidthofTrackPole/10,
if(Measurement="inch",(WidthofTrackPole*25.4)/10,
if(Measurement="cm",
(WidthofTrackPole*10)/10,WidthofTrackPole*100))),1)),
DefaultFullness)


test1 =IF(StandardContinuous="Standard",
(Round((IF(PairSingle="Pair",
WidthsPerCurtain*2,WidthsPerCurtain)*(IF(StandardContinuous="Standard",
(FabricWidth/10),
(FabricDrop/10))))/if(Measurement="mm",WidthofTrackPole/10,
if(Measurement="inch",(WidthofTrackPole*25.4)/10,
if(Measurement="cm",
(WidthofTrackPole*10)/10,WidthofTrackPole*100))),1)),
DefaultFullness)+test



test2 =if(test1 = '10',12,test)

params = [
   {A1 : 1},
   {A2 : 1},
   {A2 : 1}
]

formula = [
    """=IF(A1 = 1 , 3 ,4)""",
    """=IF(A2 = 3 , A2 , 4) + A2""",
    """=IF(A2 = 6 , 12 ,14)"""
]

A2 = "=IF(A1 = 1 , 3 ,4)"
B2 = "=IF(A2 = 3 , A2 , 4) + A2"
C2 = "=IF(A2 = 6 , 12 ,14)"