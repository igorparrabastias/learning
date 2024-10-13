R is main_speed :- R:=200.0.  % 200 cm/ds = 20 m/s = 72 km/h
R is change_speed :- R:=40.0.  % 40 cm/ds = 4 m/s = 14.4 km/h
R is wait_time :- R:=100. % 10 seconds = 100 deciseconds (ds)
R is plus_minus :- R:=50. % 5 seconds
R is big_problem :- R:=1000. % big_problem < 2*frequency_fild
R is unexpected_delay :- R:=20.
R is frequency_fild :- R:=2000.
 % big problem frequency = 1/frequency_fild 
 % unexpected delay frequency = (2*unexpected_delay)/frequency_fild 
R is max_wagons :- R:=400.
R is add :- R:= 2*(arcsin(1500/4625)*4625-1500).

initialisation:-
  G_Wagons_in_use := 10*(wagons_in_use//10)+(2*count_successes(station(yes, _, _, _, _, _))) mod 10,
  max_wagons>=G_Wagons_in_use,
  G_Posoka := 1,
  G_PosX := -14000.0,
  G_PosY := -2000.0,
  G_PosSmall := 0,
  G_Zoom := 0.1,
  G_ScrollRange := 1000,
  G_Time := 0,
  G_WagonNum := 0,
  G_NextColor := 0,
  G_Unexpected_Delay := 0,
  G_Pause := 0,
  G_FastSpeed := 0,
  G_MenuNumber := 0,
  G_Number := 9,
  G_Statistic_Course:=0,
  G_Statistic_Last:=0,
  G_Statistic_Time:=0,

  array(wagonX, max_wagons, -33000),
  array(wagonY, max_wagons, 1000),
  array(wPosoka, max_wagons, 1),
  array(wOldX, max_wagons, 0),
  array(wJump, max_wagons, 0),
  array(wStop, max_wagons, 0),
  array(wNumber, max_wagons, 0),
  array(wSpeed, max_wagons, main_speed),
  array(wTargetSpeed, max_wagons, 0.0),
  array(wTargetSpeed2, max_wagons, 0.0),
  array(wStopAt, max_wagons, 0),
  array(wAcceleration, max_wagons, 0.0), % 1 = 1 m/s2
  array(wCount, max_wagons, 0),
  array(wColor, max_wagons, rgb(0, 255, 0)),
  array(wNext, max_wagons, -1),
  array(wPrevious, max_wagons, -1),
  array(wFlags, max_wagons, 0),
  %  1 - the next in the train (this wagon will stop together with the previous one)
  %  2 - wait the semaphore to switch
  %  4 - the door is open
  %  8 - return this wagon
  % 16 - run forward to prevent crash
  % 32 - stopping to prevent crash
  % 64 - stopping to stop

  array(semaphore, 400, 0),
  _ is chronometer().

make_brush(0):- brush(rgb(255, 255, 255)).
make_brush(1):- brush(rgb(0, 127, 0)).
make_brush(2):- brush(rgb(0, 0, 255)).
make_brush(3):- brush(rgb(255, 255, 0)).
make_brush(4):- brush(rgb(255, 0, 0)).
make_brush(5):- brush(rgb(255, 0, 0)).
make_brush(6):- brush(rgb(0, 127, 0)).
make_brush(7):- brush(rgb(255, 255, 0)).
make_brush(8):- brush(rgb(255, 255, 0)).
make_brush(9):- brush(rgb(0, 0, 255)).
make_brush(10):- brush(rgb(0, 127, 0)).
make_brush(12):- brush(rgb(255, 200, 200)).
  
wagon_color(1, rgb(255, 255, 0)).
wagon_color(2, rgb(255, 0, 0)).
wagon_color(3, rgb(0, 255, 255)).
wagon_color(4, rgb(0, 0, 255)).
wagon_color(5, rgb(255, 255, 255)).
wagon_color(6, rgb(128, 0, 128)).
wagon_color(7, rgb(0, 255, 0)).
wagon_color(0, rgb(255, 0, 255)).

