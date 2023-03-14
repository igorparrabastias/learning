statistic(I):-
  (I=:=0->
    G_Statistic_Course:=G_Statistic_Course+1,
    G_Statistic_Last:=G_Time-G_Statistic_Time,
    G_Statistic_Time:=G_Time, nl,
    write("     Course "+G_Statistic_Course),
    write(". (Length "+(end_map+500000)/100000+" km, "+G_Wagons_in_use+" wagons in use)"), nl, nl,
    write("This Course:"), nl,
    write("      Duration = "+G_Statistic_Last//10+" s ("+G_Statistic_Last/36000+" h)"),
    write("  aver. "+(G_Time/G_Statistic_Course)//10+" s"), nl,
    write("         Speed = "+(0.36*(end_map+500000)/G_Statistic_Last)+" km/h"),
    write("       aver. "+(G_Statistic_Course*0.36*(end_map+500000)/G_Statistic_Time)+" km/h"), nl,
    write("       Dencity = "+(600*0.5*G_Wagons_in_use/G_Statistic_Last)+" wagons/min"),
    write(" aver. "+(600*0.5*G_Wagons_in_use*G_Statistic_Course/G_Statistic_Time)+" wagons/min"), nl,
    write("Wait for wagon = "+integer(1/(0.5*G_Wagons_in_use/G_Statistic_Last))+" s"),
    write("              aver. "+integer(1/(0.5*G_Wagons_in_use*G_Statistic_Course/G_Statistic_Time))+" s"), nl, nl
  ).

move_train(I, A, S):-
  wAcceleration(I) := A,
  wTargetSpeed(I) := S,
  (wNext(I)=\= -1, wFlags(wNext(I))/\1=\=0->
    move_train(wNext(I), A, S)
  ).

calc_Distanse(Distanse, Limit, I):-
  Distanse := 0.8*(2*abs(wagonX(wPrevious(I))-wagonX(I))-4000), % 0.8 coef.
   % -(abs(wSpeed(I)-wSpeed(wPrevious(I)))>40; wAcceleration(wPrevious(I)) =:= -1*wPosoka(I)-> 800 else 0),  % 40, 800 coef.
  Limit := wSpeed(I)**2-wSpeed(wPrevious(I))**2.

end_of_slowdown(I):-
  wFlags(I):=wFlags(I)/\0xff9f,
  (abs(wSpeed(I))<abs(wTargetSpeed2(I))-> 
    move_train(I, wPosoka(I), wTargetSpeed2(I))
  else
    move_train(I, 0, 0)
  ),
  (wFlags(wPrevious(I))/\16=\=0->
    wAcceleration(wPrevious(I)) := 0
  ).

in_curve(I, X, Y, Sign, R):-
  get_local_arc(wagonX(I), X, Y, Sign, Q1, Q2, R, Semaphore),
  (wPosoka(I)*X<wPosoka(I)*Q1->
    (abs(X-wagonX(I))<600, abs(Y-wagonY(I))<200, Semaphore\=no->
      (semaphore(Semaphore)=:=0 -> fail)
    else
      wagonY(I)>1010, wagonY(I)<1490
    ),
    wPosoka(I)*wagonX(I)>=wPosoka(I)*X,
    wPosoka(I)*wagonX(I)<wPosoka(I)*Q1
  else
    wagonY(I)>1010, wagonY(I)<1490,
    wPosoka(I)*wagonX(I)>=wPosoka(I)*Q1,
    wPosoka(I)*wagonX(I)<wPosoka(I)*X,
    Sign := -1*Sign
  ).

start_wagon(I):-
  wFlags(I):=8,
  (wPrevious(I)=:= -1, wPosoka(I)=:= -1->
    wPrevious(I):=G_WagonNum-1,
    wNext(G_WagonNum-1):=I
  ),
  move_train(I, wPosoka(I), wPosoka(I)*main_speed).

the_next_is_coming(I):-
  wNext(I)=\= -1,
  Value := wJump(I),
  next_point(Value, Pos),
  BreakPos := abs(wagonX(wNext(I))-wagonX(I))+Pos-22000,
    % write(Value+" "+wSpeed(wNext(I))+" "+abs(wagonX(wNext(I))-wagonX(I))), nl,
  (BreakPos=<0 ->
    % abs(wSpeed(wNext(I)))+wCount(wNext(I))<2*sqrt(Pos)
    wSpeed(wNext(I))**2 < 4*Pos
  else
    200+BreakPos/200<2*sqrt(Pos)
  ).

next_point(1, 6000).
next_point(2, 10000).
next_point(3, 16000).
next_point(4, 16000).

init_wagon(I):-
  wJump(I) := 1 + wJump(I) mod 4,
  (finish_point(I)->
    stop_at_pos(I, wJump(I)),
    (wJump(I)=:=2, wPrevious(I)=\= -1->
      wStop(I) := 2,
      wFlags(I):= 0,
      move_train(I, wPosoka(I), wPosoka(I)*main_speed),
      wTargetSpeed2(I) := wPosoka(I)*main_speed
    else
      wFlags(I):= 2
    )
  else
    Speed := main_speed+(wJump(I)>3-> -40 else (wJump(I)<3-> 40 else 10)),
    wStop(I) := wJump(I),
    stop_at_pos(I, wStop(I)-1),
    (wJump(I)=:=1->
      wFlags(I):=0,
      Speed := Speed+10
    else (wNext(I)=\= -1, wFlags(wNext(I))/\1=\=0->
      wFlags(I):=0,
      Speed := Speed+10
    else
      wFlags(I):=16,
      Speed := Speed-40
    )),
    move_train(I, wPosoka(I), wPosoka(I)*Speed),
    wTargetSpeed2(I) := wPosoka(I)*Speed
  ).

return_wagon(I):-
  All := (wStop(I)>0 -> wStop(I) else (wJump(I)=:=1 -> 3 else wJump(I))),
  all_are_stopped(I, All),
  wStop(I):=1,
  (wJump(I)=:=1-> wJump(I):=2),
  semaphore(8-4*wPosoka(I)):=1,
  wPosoka(I):= -1*wPosoka(I),
  wAcceleration(I):= wPosoka(I),

  stop_at_pos(I, wStop(I)-1),
  wTargetSpeed(I) := wPosoka(I)*main_speed,
  wTargetSpeed2(I) := wPosoka(I)*main_speed,
  First:=wPrevious(I),
  return_all(I, All, 2, First, I, Last),
  wFlags(I):= 1,
  wFlags(Last):= 0.

all_are_stopped(_, 1):- !.
all_are_stopped(Previous, All):-
  I := wNext(Previous),
  I =\= -1,
  wSpeed(I)=:=0,
  wPosoka(I)=:=wPosoka(Previous),
  wPosoka(I)*(wagonX(Previous)-wagonX(I))<2000+150, % 150 coef.
  All2:= All-1,
  all_are_stopped(I, All2).

return_all(Previous, All, Num, First, Second, Last):-
  statistic(Previous),
  I := wNext(Previous),
  I =\= -1,
  (All>1->
    All2:= All-1,
    Num2:= Num+1,
    return_all(I, All2, Num2, First, Second, Last),
    wPosoka(I):= -1*wPosoka(I),
    wAcceleration(I):= wPosoka(I),

    wFlags(I):= 1,
    (wJump(I)>2->
      wStop(I) := Num
    else (Num=:=2->
      wStop(I) := 2
    else
      wJump(I) := 1
    )),
    stop_at_pos(I, wStop(I)-1),
    wTargetSpeed(I) := wPosoka(I)*main_speed,
    wTargetSpeed2(I) := wPosoka(I)*main_speed,
    wPrevious(Previous):=I,
    wNext(I):=Previous
  else
    Last:=Previous,
    % write("Last="+Last+" First="+First+" Second="+Second),nl,
    (First =\= -1 -> wNext(First):=Last),
    wPrevious(Last):=First,
    wNext(Second):=I,
    (I =\= -1 -> wPrevious(I):=Second)
  ).

finish_point(I):-
  station(yes, Where, X, _, _, _),
  X-25000<wagonX(I), wagonX(I)<X+25000,
  finish_station(Where, I, -1).

where_is_now(I, Where, X, Semaphore):-
  station(yes, Where, X, Semaphore, _, _),
  X-4000<wagonX(I), wagonX(I)<X+4000.

pos_point(4,  3000).
pos_point(1,  1000).
pos_point(3, -1000).
pos_point(2, -3000).

stop_at_pos(Wagon, Stop):-
  (between_stations(Wagon, N)->
    stop_at_pos2(Wagon, Stop, N)
  else
    local_station(wagonX(Wagon), StationX, _),
    (wJump(Wagon)=:=1-> 
      wStopAt(Wagon):= 13000*wPosoka(Wagon)+StationX
    else
      wStopAt(Wagon):= (Stop*2000+7000)*wPosoka(Wagon)+StationX
    )
  ).
  % write("Wagon="+Wagon+" StopAt="+wStopAt(Wagon)), nl.

stop_at_pos2(Wagon, Stop, N):-
  (Stop=:=0->
    station(yes, N, StationX, _, _, _),
    Jump := wJump(Wagon),
    pos_point(Jump, Where),
    wStopAt(Wagon):= Where*wPosoka(Wagon)+StationX
  else (next_station(Wagon, N, Next)->
    stop_at_pos2(Wagon, Stop-1, Next)
  else
    station(yes, N, StationX, _, _, _),
    (wPrevious(Wagon)=\= -1-> 
      wStopAt(Wagon):= (Stop*2000+7000)*wPosoka(Wagon)+StationX
    else
      wStopAt(Wagon):= 4000*wPosoka(Wagon)+StationX
    )
  )).

between_stations(Wagon, N):-
  station(yes, N, Station, _, _, _),
  wPosoka(Wagon)*wagonX(Wagon) =< wPosoka(Wagon)*Station-4000,
  (previus_station(Wagon, N, Previus)->
    station(yes, Previus, Station2, _, _, _),
    wPosoka(Wagon)*wagonX(Wagon) > wPosoka(Wagon)*Station2-4000
  ).

previus_station(Wagon, N, Previus):-
  not(finish_station(N, Wagon, 1)),
  Previus := N-wPosoka(Wagon).

next_station(Wagon, N, Next):-
  not(finish_station(N, Wagon, -1)),
  Next := N+wPosoka(Wagon).
