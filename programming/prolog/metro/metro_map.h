R is wagons_in_use :- R:= 248.
R is time_period :- R:=1000. % minimum 1000
R is end_map :- R:= 1200000.

finish_station(Where, I, Posoka):-
  Where=14, wPosoka(I)=:=Posoka; Where=32, wPosoka(I)=:= -1*Posoka.

station(no, 35, _, _, "Business", "Park").
station(no, 34, _, _, "Balan", "").
station(no, 33, _, _, "Alexander", "Malinov").

station(yes, 32, 1700000, _, "Sofia", "Airport").
station(yes, 31, 1650000, _, "Sofiyska", "Sveta Gora").
station(yes, 30, 1520000, _, "Iskarsko", "Shose").
station(yes, 29, 1430000, _, "Druzhba", "").
station(yes, 28, 1300000, _, "Tsarigradsko", "Shose").
station(yes, 27, 1250000, _, "Mladost 3", "").
 
station(yes, 26, 1130000, _, "Mladost 1", "").
station(yes, 25, 1060000, _, "Musagenitsa", "").
station(yes, 24,  960000, _, "G.M.", "Dimitrov").
station(yes, 23,  840000, _, "Joliot", "Curie").
station(yes, 22,  790000, _, "Vasil Levski", "Stadium").
station(yes, 21,  610000, _, "Kliment", "Ohridski").

station(yes, 20, 500000, 120, "Serdika", "").
station(yes, 19, 410000, 100, "Opalchenska", "").
station(yes, 18, 290000,  80, "Konstantin", "Velichkov").
station(yes, 17, 210000,  60, "Vardar", "").
station(yes, 16, 180000,  40, "Zapaden", "Park").
station(yes, 15,  50000,  20, "Lyulin", "").
station(yes, 14,      0,   0, "Slivnitsa", "").

station(no, 13, _, _, "Obelya", "").
station(no, 12, _, _, "Lomsko", "Shose").
station(no, 11, _, _, "Beli", "Dunav").
station(no, 10, _, _, "Nadezhda", "").
station(no, 9, _, _, "Han", "Kubrat").
station(no, 8, _, _, "Knyaginya", "Maria Luiza").
station(no, 7, _, _, "Central", "Rail Station").
station(no, 6, _, _, "Lavov", "Most").
station(no, 5, _, _, "Serdika 2", "").
station(no, 4, _, _, "Palace", "of Culture").
station(no, 3, _, _, "European", "Union").
station(no, 2, _, _, "James", "Baucher").
station(no, 1, _, _, "Vitosha", "").

local_metro_line(-5000, 1520, 5000, 1520, no, no).
local_metro_line(-5000, 1010, 5000, 1010, no, no).

metro_line(-18000, 1010, -8000, 1010, no, no). % +10 for beauty
metro_line(1708000, 1520,1718000, 1520, no, no). % +20 for beauty

metro_line(-8000, 1010,  -5000, 1010,  12, no).
metro_line(1705000, 1520, 1708000, 1520, no,  4).

metro_arc( -8000, 1000,  1, -6500, 1250, 4625, 12).
metro_arc( -5000, 1500,  1, -6500, 1250, 4625, no).

metro_arc(1705000, 1000,  1,  1706500, 1250, 4625, no).
metro_arc(1708000, 1500,  1,  1706500, 1250, 4625, 4).

