R is wagons_in_use :- R:= 200.
R is time_period :- R:=2000. % minimum 1000
R is end_map :- R:= 2200000.

finish_station(Where, I, Posoka):-
  Where=1, wPosoka(I)=:=Posoka; Where=32, wPosoka(I)=:= -1*Posoka.

station(no, 35, _, _, "Business", "Park").
station(no, 34, _, _, "Balan", "").
station(no, 33, _, _, "Alexander", "Malinov").

station(yes, 32, 2700000, _, "Sofia", "Airport").
station(yes, 31, 2650000, _, "Sofiyska", "Sveta Gora").
station(yes, 30, 2520000, _, "Iskarsko", "Shose").
station(yes, 29, 2430000, _, "Druzhba", "").
station(yes, 28, 2300000, _, "Tsarigradsko", "Shose").
station(yes, 27, 2250000, _, "Mladost 3", "").
 
station(yes, 26, 2130000, _, "Mladost 1", "").
station(yes, 25, 2060000, _, "Musagenitsa", "").
station(yes, 24, 1960000, _, "G.M.", "Dimitrov").
station(yes, 23, 1840000, _, "Joliot", "Curie").
station(yes, 22, 1790000, _, "Vasil Levski", "Stadium").
station(yes, 21, 1610000, _, "Kliment", "Ohridski").

station(yes, 20, 1500000, 120, "Serdika", "").
station(yes, 19, 1410000, 100, "Opalchenska", "").
station(yes, 18, 1290000,  80, "Konstantin", "Velichkov").
station(yes, 17, 1210000,  60, "Vardar", "").
station(yes, 16, 1180000,  40, "Zapaden", "Park").
station(yes, 15, 1050000,  20, "Lyulin", "").
station(yes, 14, 1000000,   0, "Slivnitsa", "").

station(yes, 13,  910000, _, "Obelya", "").
station(yes, 12,  820000, _, "Lomsko", "Shose").
station(yes, 11,  780000, _, "Beli", "Dunav").
station(yes, 10,  720000, _, "Nadezhda", "").
station(yes, 9,   680000, _, "Han", "Kubrat").
station(yes, 8,   480000, _, "Knyaginya", "Maria Luiza").
station(yes, 7,   440000, _, "Central", "Rail Station").
station(yes, 6,   370000, _, "Lavov", "Most").
station(yes, 5,   280000, _, "Serdika 2", "").
station(yes, 4,   180000, _, "Palace", "of Culture").
station(yes, 3,   140000, _, "European", "Union").
station(yes, 2,    60000, _, "James", "Baucher").
station(yes, 1,        0, _, "Vitosha", "").

local_metro_line(-5000, 1520, 5000, 1520, no, no).
local_metro_line(-5000, 1010, 5000, 1010, no, no).

metro_line(-18000, 1010, -8000, 1010, no, no). % +10 for beauty
metro_line(2708000, 1520,2718000, 1520, no, no). % +20 for beauty

metro_line(-8000, 1010,  -5000, 1010,  12, no).
metro_line(2705000, 1520, 2708000, 1520, no,  4).

metro_arc( -8000, 1000,  1, -6500, 1250, 4625, 12).
metro_arc( -5000, 1500,  1, -6500, 1250, 4625, no).

metro_arc(2705000, 1000,  1,  2706500, 1250, 4625, no).
metro_arc(2708000, 1500,  1,  2706500, 1250, 4625, 4).

