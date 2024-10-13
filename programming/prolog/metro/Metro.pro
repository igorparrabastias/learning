% Metro.pro, version 2.0
% 22 May, 2017
% Patent Application #112419 from 1 December, 2016

% Metro.pro, version 1.0 is on the address:
% http://dobrev.com/software/Metro_v1_0.zip

include("metro_map.h"). % try 1, 2, 3
include("metro_data.h").
include("metro_window.h").
include("metro_tools.h").


?-
  initialisation,
  % H is open("test.metro", "rb"),  read_metro(H),  close(H),
  window(title("Metro"), pos(0, 100), size(1900,740), backgr(rgb(0, 200, 200)), paint_indirectly, h_scroll,v_scroll).
  % change_speed.

in_group(0).
in_group(T) :- T > 30, T =< 32.
in_group(T) :- T > 62, T =< 65.
in_group(T) :- T > 95, T =< 99.

time_func(end):-
  G_Pause =:= 0,
  start_random_from(G_Time), % make the random deterministic
  (G_Time mod 10 =:= 0, G_WagonNum<G_Wagons_in_use ->
    T:=(G_Time mod time_period)//10,
    (T =:= 0 -> % (time_period/2)
      G_NextColor := (G_NextColor+1) mod 8
    ),
    (in_group(T) ->
      semaphore(8+4):=1,
      wagon_color(G_NextColor, Color),
      wColor(G_WagonNum) := Color,
      wPosoka(G_WagonNum) := 1,
      G_Number := (G_Number+1) mod 10,
      wagonY(G_WagonNum) := 1250+G_Posoka*250-500, % +500
      (G_WagonNum=:=0 ->
        wPrevious(G_WagonNum) := -1
      else
        wNext(G_WagonNum-1) := G_WagonNum,
        wPrevious(G_WagonNum) := G_WagonNum-1
      ),
      wNext(G_WagonNum) := -1,
      next_stop(G_Number, Jump, Stop, Speed),
      wagonX(G_WagonNum) := -35000-10*Stop*Speed, % 500000-2000
      %wagonX(G_WagonNum) := 0-20*Number*(5-Speed),
      wNumber(G_WagonNum) := G_Number,
      wJump(G_WagonNum) := Jump,
      wStop(G_WagonNum) := Stop,
      stop_at_pos(G_WagonNum, Stop-1),
      wSpeed(G_WagonNum) := G_Posoka*(main_speed+Speed),
      wTargetSpeed2(G_WagonNum) := G_Posoka*(main_speed+Speed),
      wFlags(G_WagonNum) := true_value(Jump=\=Stop),
      (G_WagonNum>0->
        Distance := wagonX(G_WagonNum-1)-2000,
        (Jump=\=Stop->
          wSpeed(G_WagonNum) := wSpeed(G_WagonNum-1),
          wAcceleration(G_WagonNum) := wAcceleration(G_WagonNum-1)
        else
          Distance := Distance-0.5*(wSpeed(G_WagonNum)**2-wSpeed(G_WagonNum-1)**2)
        ),
        wagonX(G_WagonNum):= min(wagonX(G_WagonNum), Distance)
      ),
      G_WagonNum := G_WagonNum + 1
    )
  ),
  G_Time := G_Time + 1,
  (G_Time mod 600=:=0 -> write("One minute for "+chronometer()/60), nl),
  move_wagons,
  (G_Time mod 10=:=0; G_FastSpeed=:= -1 ->
    set_main_window_text
  ),
  update_window(_).

next_stop(0, 1, 1, 0).
next_stop(1, 2, 2, 0).
next_stop(2, 2, 1, 0).
next_stop(3, 3, 3, 0).
next_stop(4, 3, 2, 0).
next_stop(5, 3, 1, 0).
next_stop(6, 4, 4, 0).
next_stop(7, 4, 3, 0).
next_stop(8, 4, 2, 0).
next_stop(9, 4, 1, 0).

move_wagons:-
  for(I, 0, G_WagonNum-1),
  wOldX(I) := wagonX(I),
  (wCount(I)>0->
    (wAcceleration(I) =:=0, G_Unexpected_Delay=:=1->
      Delay := random(frequency_fild),
      (Delay =< 2*unexpected_delay->
        (Delay=:=unexpected_delay->
          % write("Big problem i="+I), nl,
          wCount(I) := wCount(I) + random(1+big_problem)
        else
          wCount(I) := wCount(I) + Delay - unexpected_delay,
          (wCount(I)<1 -> wCount(I):=1)
        )
      )
    ),
    wCount(I) := wCount(I)-1
  else (wAcceleration(I)>0->
    change_speed(I, 1)
  else (wAcceleration(I)<0->
    change_speed(I, -1)
  ))),
  (in_curve(I, X, Y, Sign, R)->
    Alfa := arccos((wagonX(I)-X)/R),
    %write(wagonX(I)+"="+Alfa+"="+cos(Alfa - wSpeed(I)/4625)*4625), nl,
    wagonX(I) := X+cos(Alfa - wSpeed(I)/R)*R,
    wagonY(I) := Y+wPosoka(I)*Sign*(R-sin(Alfa - wSpeed(I)/R)*R)
  else
    wagonX(I) := wagonX(I) + wSpeed(I)
  ),
  % (I=9, wSpeed(I)<200-> write("speed="+wSpeed(I)+" "+G_Time), nl),
  fail.
move_wagons:-
  for(I, 0, G_WagonNum-1),
  NextSpeed := wSpeed(I) + (wPosoka(I)*wAcceleration(I)>0 -> wAcceleration(I) else 0),
  (2*wPosoka(I)*(wStopAt(I)-wagonX(I)-wSpeed(I)-wAcceleration(I))<NextSpeed**2->
    wFlags(I):=(wFlags(I)\/64)/\0xffce,
    (wPosoka(I)*wSpeed(I)>0->
      Acceleration := -1*wPosoka(I), % 0.5*wSpeed(I)**2/(wagonX(I)-wStopAt(I)),
      wTargetSpeed2(I) := 0,
      move_train(I, Acceleration, 0)
    )
  else (wFlags(I)/\32=\=0->
    (wPrevious(I)=\= -1, wPosoka(I)=:=wPosoka(wPrevious(I))->
      calc_Distanse(Distanse, Limit, I),
      (abs(wSpeed(wPrevious(I)))<abs(wSpeed(I))->
        (Distanse<Limit->
          move_train(I, -1*wPosoka(I), 0)
        else (0.8*Distanse>Limit-> % 0.8 coef.
          end_of_slowdown(I)
        else
          move_train(I, 0, 0)
        )),
        (wFlags(wPrevious(I))/\16=\=0->
          (0.97*Distanse<Limit-> % 0.97 coef.
            (wAcceleration(wPrevious(I))=:=0, abs(wSpeed(wPrevious(I)))<abs(wTargetSpeed2(I))->
              wAcceleration(wPrevious(I)) := wPosoka(I),
              wTargetSpeed(wPrevious(I)) := wTargetSpeed2(I)
            )
          else (abs(wSpeed(I))<abs(wTargetSpeed2(I))->
            move_train(I, wPosoka(I), wTargetSpeed2(I))
          ))
        )
      else (wPosoka(I)*(wagonX(wPrevious(I))-wagonX(I))<2000+100-> % 100 coef.
        move_train(I, 0, 0),
        (wSpeed(wPrevious(I))=:=wSpeed(I), wAcceleration(wPrevious(I)) =:= 0->
          wFlags(I):=1
        )
      else
        end_of_slowdown(I)
      ))
    else
      end_of_slowdown(I)
    )
  else (wFlags(I)/\7=:=0, wPrevious(I)=\= -1, wPosoka(I)=:=wPosoka(wPrevious(I))->
    calc_Distanse(Distanse, Limit, I),
    (Distanse<Limit->
      wFlags(I):=(wFlags(I)\/32)/\0xffef,
      move_train(I, -1*wPosoka(I), 0)
    else (wFlags(I)/\64=\=0->
      wFlags(I):=wFlags(I)/\0xffbf,
      move_train(I, 0, 0)
    )),
    (0.97*Distanse<Limit, wFlags(wPrevious(I))/\16=\=0, abs(wSpeed(wPrevious(I)))<abs(wTargetSpeed2(I))-> % 0.97 coef.
      wFlags(I):=(wFlags(I)\/32)/\0xffef,
      wAcceleration(wPrevious(I)) := wPosoka(I),
      wTargetSpeed(wPrevious(I)) := wTargetSpeed2(I)
    )
  else (wFlags(I)/\64=\=0->
    wFlags(I):=wFlags(I)/\0xffbf,
    move_train(I, 0, 0)
  )))),
  fail.
move_wagons:-
  for(I, 0, G_WagonNum-1),
  (wSpeed(I)=:=0, wCount(I)=:=0, wAcceleration(I)=:=0 ->
    %write("i="+I+", "+G_Time+"="+wFlags(I)+"="+wAcceleration(I)), nl,
    (wFlags(I)/\8=\=0->
      return_wagon(I)
    else (wFlags(I)/\4=\=0->
      init_wagon(I)
    else (wFlags(I)/\2=\=0, semaphore(8-4*wPosoka(I))=:=0,
          not(wPrevious(I) =\= -1, wPosoka(I)=:=wPosoka(wPrevious(I)), wPosoka(I)*(wagonX(wPrevious(I))-wagonX(I))>0),
          not(wPosoka(I)=:= -1, G_WagonNum<G_Wagons_in_use)->
      start_wagon(I)
    )))
  ),
  fail.
move_wagons:-
  for(I, 0, G_WagonNum-1),
  where_to_stop(Type, I, N, StationX, Semaphore),
  cross_point(Type, I, N, StationX, Semaphore),
  fail.
move_wagons.

change_speed(I, Sing):-
  (Sing*wTargetSpeed(I)>Sing*(wSpeed(I)+wAcceleration(I))->
    wSpeed(I) := wSpeed(I)+wAcceleration(I)
  else
    %write("i="+I+", "+G_Time+"=="+wFlags(I)+"="+wAcceleration(I)), nl,
    (abs(wTargetSpeed(I)-wSpeed(I))>abs(wAcceleration(I))-> write("Opposite acceleration! i="+I+" speed=("+wSpeed(I)+","+wTargetSpeed(I)+") Acceleration="+wAcceleration(I)+" now="+G_Time), nl),
    wSpeed(I) := wTargetSpeed(I),
    wAcceleration(I) :=0,
    (wTargetSpeed(I)=:=0 ->
      (wFlags(I)/\8=:=0, abs(wStopAt(I)-wagonX(I))<500 -> % 500 coef.
        (wStop(I)=:=0->
          wFlags(I):=4,
          % wCount(I):= 100
          wCount(I):=wait_time+random(1+2*plus_minus)-plus_minus
        else (local_station(wagonX(I), StationX, _), wStopAt(I)=:=4000*wPosoka(I)+StationX->
          stop_at_pos(I, wStop(I)),
          wFlags(I):=2
        ))
      )      
    )
  ).

where_to_stop(Type, I, N, StationX, Semaphore):-
  station(yes, N, StationX, Semaphore, _, _),
  abs(StationX-wagonX(I))<43000,
  stop_point(Type, Point),
  (wPosoka(I)=:=1->
    wOldX(I) =< Point+StationX, Point+StationX< wagonX(I)
  else
    wOldX(I) >= -1*Point+StationX, -1*Point+StationX> wagonX(I)
  ).

stop_point(enter, -8000).
stop_point(switch, -5000).

cross_point(switch, I, N, StationX, _):-
  finish_station(N, I, 1),
  not(wNext(I)=\= -1, wPosoka(I)=:=wPosoka(wNext(I)), wPosoka(I)*(wagonX(I)-wagonX(wNext(I)))>0),
  % (wStop(I)=:=0, wJump(I)>1; wNext(I)=:= -1),
  semaphore(8+4*wPosoka(I)):=0.

cross_point(enter, I, N, StationX, _):-
  wStop(I) := wStop(I)-1,
  % stop_at_pos(I, wStop(I)),
  wFlags(I):=wFlags(I)/\0xffef,
  (wStop(I)>0, 2*wPosoka(I)*(wStopAt(I)-wagonX(I))>wSpeed(I)**2->
    Speed := main_speed+(wJump(I)>3-> -40 else (wJump(I)<3-> 40 else 10)),
    wTargetSpeed2(I):= wPosoka(I)*Speed,
    (wFlags(I)/\1=:=0->
      (abs(wSpeed(I))<abs(wTargetSpeed2(I)) ->
        move_train(I, wPosoka(I), wTargetSpeed2(I))
      else (abs(wSpeed(I))>abs(wTargetSpeed2(I))->
        move_train(I, -1*wPosoka(I), wTargetSpeed2(I))
      ))
    )
  ).

