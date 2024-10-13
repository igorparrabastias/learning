R is wagons_in_use :- R:= 72.
R is time_period :- R:=1000. % minimum 1000
R is end_map :- R:= 0.

finish_station(Where, I, Posoka):-
  Where=14, wPosoka(I)=:=Posoka; Where=19, wPosoka(I)=:= -1*Posoka.

station(no, 35, _, _, "Business", "Park").
station(no, 34, _, _, "Balan", "").
station(no, 33, _, _, "Alexander", "Malinov").

station(no, 32, _, _, "Sofia", "Airport").
station(no, 31, _, _, "Sofiyska", "Sveta Gora").
station(no, 30, _, _, "Iskarsko", "Shose").
station(no, 29, _, _, "Druzhba", "").
station(no, 28, _, _, "Tsarigradsko", "Shose").
station(no, 27, _, _, "Mladost 3", "").
 
station(no, 26, _, _, "Mladost 1", "").
station(no, 25, _, _, "Musagenitsa", "").
station(no, 24, _, _, "G.M.", "Dimitrov").
station(no, 23, _, _, "Joliot", "Curie").
station(no, 22, _, _, "Vasil Levski", "Stadium").
station(no, 21, _, _, "Kliment", "Ohridski").
station(no, 20, _, _, "Serdika", "").

station(yes, 19, 500000, 100, "Opalchenska", "").
station(yes, 18, 400000,  80, "Konstantin", "Velichkov").
station(yes, 17, 300000,  60, "Vardar", "").
station(yes, 16, 200000,  40, "Zapaden", "Park").
station(yes, 15, 100000,  20, "Lyulin", "").
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
metro_line(508000, 1520,518000, 1520, no, no). % +20 for beauty

metro_line(-8000, 1010,  -5000, 1010,  12, no).
metro_line(505000, 1520, 508000, 1520, no,  4).

metro_arc( -8000, 1000,  1, -6500, 1250, 4625, 12).
metro_arc( -5000, 1500,  1, -6500, 1250, 4625, no).

metro_arc(505000, 1000,  1,  506500, 1250, 4625, no).
metro_arc(508000, 1500,  1,  506500, 1250, 4625, 4).

