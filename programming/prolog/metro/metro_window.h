local_station(Wagon, Station, Semaphore):-
  station(yes, _, Station, Semaphore, _, _),
  Wagon =< Station+28000,
  Wagon >= Station-28000.

visible_station(N, Station, Semaphore, Distance, big):-
  station(yes, N, Station, Semaphore, _, _),
  G_PosX =< Station+Distance,
  G_PosX+G_Xsize/G_Zoom >= Station-Distance.
visible_station(N, Station, Semaphore, Distance, small):-
  station(yes, N, Station, Semaphore, _, _),
  G_PosSmall-80000 =< Station+Distance,
  G_PosSmall+530000 >= Station-Distance.

visible_wagon(Wagon, big):-
  G_PosX =< Wagon+1000,
  G_PosX+G_Xsize/G_Zoom >= Wagon-1000.
visible_wagon(Wagon, small):-
  G_PosSmall-30000 =< Wagon+1000,
  G_PosSmall+530000 >= Wagon-1000.

menu_pause(press) :-
  G_Pause := 1 - G_Pause.

menu_fast_speed(press) :-
  G_FastSpeed:=(G_FastSpeed=:=1 -> 0 else 1),
  change_speed.
menu_normal_speed(press) :-
  (G_FastSpeed=\=0->
    G_FastSpeed:=0,
    change_speed
  ).
menu_slow_motion(press) :-
  G_FastSpeed:=(G_FastSpeed=:= -1 -> 0 else -1),
  change_speed.

change_speed:-
  set_main_window_text,
  Interval := (G_FastSpeed =:= 1 -> 0.01 else (G_FastSpeed =:= 0 -> 0.1 else 0.5)),
  kill_timer(_, G_Timer),
  G_Timer := set_timer(_, Interval, time_func).

set_main_window_text:-
  (G_FastSpeed=:= -1 ->
    Slow:= (G_Time mod 10=:=0 -> ".0" else ""),
    set_text("Metro "+G_Time/10+Slow, _)
  else
    Fast:= (G_FastSpeed=:=1 -> " (fast)" else ""),
    set_text("Metro "+G_Time//10+Fast, _)
  ).

menu_unexpected_delay(press) :-
  G_Unexpected_Delay := 1-G_Unexpected_Delay.

menu_number(press) :-
  G_MenuNumber := (G_MenuNumber-1) mod 8,
  update_window(_).
menu_minus(press) :-
  G_MenuNumber := (G_MenuNumber+1) mod 8,
  update_window(_).

make_flags_text(Text, I, 1):- !, Text := (wFlags(I)/\1=:=0-> "." else "*").
make_flags_text(Text, I, Flag):-
  NextFlag := Flag//2,
  make_flags_text(Text, I, NextFlag),
  Text := (wFlags(I)/\Flag=:=0-> ".  " else "*  ") + Text.

make_text(0, I, Text):- Text := wJump(I)+" : "+wStop(I).
make_text(1, I, Text):- Text := "#"+I. % "line "+(wNumber(I)+1).
make_text(2, I, Text):- Text := "x="+wagonX(I)/100.
make_text(3, I, Text):- make_flags_text(Text, I, 64).
make_text(4, I, Text):- Text := "s="+wSpeed(I)+" + "+wAcceleration(I).
make_text(5, I, Text):- Text := "<"+wTargetSpeed(I)+", "+wTargetSpeed2(I)+">".
make_text(6, I, Text):- Text := "at "+wStopAt(I)/100+", c="+wCount(I).
make_text(7, I, Text):- 
  Text := (wPosoka(I)=:=1 -> wNext(I)+"<"+I+">"+wPrevious(I) else wPrevious(I)+"<"+I+">"+wNext(I)).

menu_zoom_in(press):- client_size(_,W,H), zoom(-1, W//2, H//2).
menu_zoom_out(press):- client_size(_,W,H), zoom(1, W//2, H//2).
menu_help(press):-
  message("Metro",
  "Metro where every wagon has its own opinion. We present a new scheme for the wagon movement which will increase the capacity of the metro tube with 17%. This will decrease the traveling time by 10% and the power consumption by 20%.

At every station is posted a scheme. At different stations the schemes are slightly different. These schemes will help to the passengers to choose the right wagon.

You can zoom in and out by the buttons + and -. You can drag the field with the mouse. Also you can move by the arrows. Other possibility to move and zoom is by the mouse wheel.",i).

menu_file(init) :-
  menu( normal, action(menu_file_open), text("&Load") ), % Open
  menu( normal, action(menu_file_save), text("&Save") ). % &As

menu_show(init) :-
  menu(normal, action(menu_number), text("Next Label\t<, >") ).

menu_time(init) :-
  menu(normal, action(menu_pause), text("&Pause\tP") ),
  menu(separator),
  menu(normal, action(menu_slow_motion), text("&Slow Motion\tS") ),
  menu(normal, action(menu_normal_speed), text("&Normal Speed") ),
  menu(normal, action(menu_fast_speed), text("&Fast Speed\tF") ),
  menu(separator),
  menu(normal, action(menu_unexpected_delay), text("Unexpected Delay") ).

menu_file_open(press) :-
  %kill_timer(_, G_Timer),
  % F is select_file(o, _, "Metro Files (*.metro)\0*.metro\0All Files (*.*)\0*.*\0"),
  % write(F), nl,
  H is open("test.metro", "rb"),
  read_metro(H),
  close(H),
  change_speed,
  fix_scroll_bar_v,
  fix_scroll_bar_h.
  %G_Timer := set_timer(_, 0.1, time_func).

menu_file_save(press) :-
  % kill_timer(_, G_Timer),
  % F is select_file(s, _, "Metro Files (*.metro)\0*.metro\0All Files (*.*)\0*.*\0"),
  H is open("test.metro", "wb"),
  save_metro(H),
  close(H).
  % G_Timer := set_timer(_, 0.1, time_func).

read_metro(H) :-
  G_Posoka := get(H, l),
  G_PosX := get(H, l),
  G_PosY := get(H, l),
  G_PosSmall := get(H, l),
  G_Zoom := get(H, l)/1000,
  G_ScrollRange := get(H, l),
  G_Time := get(H, l),
  G_WagonNum := get(H, l),
  G_NextColor := get(H, l),
  G_Unexpected_Delay := get(H, l),
  G_Pause := get(H, l),
  G_FastSpeed := get(H, l),
  G_MenuNumber := get(H, l),
  G_Number := get(H, l),
  G_Statistic_Course:= get(H, l),
  G_Statistic_Last:= get(H, l),
  G_Statistic_Time:= get(H, l),
  get_array(wagonX, H, max_wagons, 1),
  get_array(wagonY, H, max_wagons, 1),
  get_array(wPosoka, H, max_wagons, 1),
  get_array(wOldX, H, max_wagons, 1),
  get_array(wJump, H, max_wagons, 1),
  get_array(wStop, H, max_wagons, 1),
  get_array(wNumber, H, max_wagons, 1),
  get_array(wSpeed, H, max_wagons, 1000),
  get_array(wTargetSpeed, H, max_wagons, 1000),
  get_array(wTargetSpeed2, H, max_wagons, 1000),
  get_array(wStopAt, H, max_wagons, 1),
  get_array(wAcceleration, H, max_wagons, 1000),
  get_array(wCount, H, max_wagons, 1),
  get_array(wColor, H, max_wagons, 1),
  get_array(wNext, H, max_wagons, 1),
  get_array(wPrevious, H, max_wagons, 1),
  get_array(wFlags, H, max_wagons, 1),

  get_array(semaphore, H, 400, 1).

save_metro(H) :-
  put2(G_Posoka, H, l),
  put2(G_PosX, H, l),
  put2(G_PosY, H, l),
  put2(G_PosSmall, H, l),
  put2(1000*G_Zoom, H, l),
  put2(G_ScrollRange, H, l),
  put2(G_Time, H, l),
  put2(G_WagonNum, H, l),
  put2(G_NextColor, H, l),
  put2(G_Unexpected_Delay, H, l),
  put2(G_Pause, H, l),
  put2(G_FastSpeed, H, l),
  put2(G_MenuNumber, H, l),
  put2(G_Number, H, l),
  put2(G_Statistic_Course, H, l),
  put2(G_Statistic_Last, H, l),
  put2(G_Statistic_Time, H, l),

  put_array(wagonX, H, max_wagons, 1),
  put_array(wagonY, H, max_wagons, 1),
  put_array(wPosoka, H, max_wagons, 1),
  put_array(wOldX, H, max_wagons, 1),
  put_array(wJump, H, max_wagons, 1),
  put_array(wStop, H, max_wagons, 1),
  put_array(wNumber, H, max_wagons, 1),
  put_array(wSpeed, H, max_wagons, 1000),
  put_array(wTargetSpeed, H, max_wagons, 1000),
  put_array(wTargetSpeed2, H, max_wagons, 1000),
  put_array(wStopAt, H, max_wagons, 1),
  put_array(wAcceleration, H, max_wagons, 1000),
  put_array(wCount, H, max_wagons, 1),
  put_array(wColor, H, max_wagons, 1),
  put_array(wNext, H, max_wagons, 1),
  put_array(wPrevious, H, max_wagons, 1),
  put_array(wFlags, H, max_wagons, 1),

  put_array(semaphore, H, 400, 1).

*** put2(int W, obj(H), T) :- 47.

get_array(Array, H, Size, D):-
  for(I, 0, Size),
  Array(I) := get(H, l)/D,
  fail.
get_array(_, _, _, _).

put_array(Array, H, Size, D):-
  for(I, 0, Size),
  put2(D*Array(I), H, l),
  fail.
put_array(_, _, _, _).

my_paint(PosX, PosY, ZoomX, ZoomY, small):-
  pen(0, 0),
  brush(rgb(0, 180, 180)),
  rect(0, 0, G_Xsize+10, 100),
  pen(1, 0),
  X1 := (G_PosX-PosX)*ZoomX,
  X2 := (G_PosX-PosX+G_Xsize/G_Zoom)*ZoomX,
  Y1 := (G_PosY-PosY+100/G_Zoom)*ZoomY,
  Y2 := (G_PosY-PosY+G_Ysize/G_Zoom)*ZoomY,
  line(X1, Y1, X1, Y2, X2, Y2, X2, Y1, X1, Y1),
  fail.

my_paint(PosX, PosY, ZoomX, ZoomY, Variant):-
  ZoomY>=0.02,
  (ZoomX>0.08->
    pen(1+10*ZoomX, rgb(255, 0, 0)),
    Add:=72
  else
    pen(1+2*10*ZoomX, rgb(255, 0, 0)),
    Add:=0
  ),
  get_metro_line(X1, Y1, X2, Y2, Sem1, Sem2, Variant),
  X1p := (Sem1\=no, semaphore(Sem1)=:=1 -> X1+1200 else X1),
  X2p := (Sem2\=no, semaphore(Sem2)=:=1 -> X2-1200 else X2),
  line((X1p-PosX)*ZoomX, (Y1+Add-PosY)*ZoomY, (X2p-PosX)*ZoomX, (Y2+Add-PosY)*ZoomY),
  put_grid(X2, Y2, X1, Y1, PosX, PosY, ZoomX, ZoomY, Variant),
  (ZoomX>0.08->
    line((X1p-PosX)*ZoomX, (Y1-Add-PosY)*ZoomY, (X2p-PosX)*ZoomX, (Y2-Add-PosY)*ZoomY)
  ),
  fail.

my_paint(PosX, PosY, ZoomX, ZoomY, Variant):-
  ZoomY>=0.02,
  (ZoomX>0.08->
    Add:=72
  else
    Add:=0
  ),
  get_visible_arc(X, Y, Sign, Q1, Q2, Semaphore),
  D := (Q2-Y)+(Q1-X)**2/(Q2-Y),
  % write(" R="+D/2), nl,
  (Sign*X>Sign*Q1 -> Y := Y+30, Q2 := Q2 + 10), % +10, +30 for beauty
  (Semaphore\=no, semaphore(Semaphore)=:=0 ->
    Open := (X>Q1 -> -1200 else 1200)
  else
    Open := 0
  ),
  my_draw_arc(X, Y+Add, D, Q1, Q2+Add, Open, Sign, PosX, PosY, ZoomX, ZoomY, Variant),
  (ZoomX>0.08->
    my_draw_arc(X, Y-Add, D, Q1, Q2-Add, Open, Sign, PosX, PosY, ZoomX, ZoomY, Variant)
  ),
  fail.

my_paint(PosX, PosY, ZoomX, ZoomY, Variant):-
  ZoomY>=0.02,
  pen(4+80*ZoomY, rgb(0, 127, 0)),
  make_station(0, PosX, PosY, ZoomX, ZoomY, Variant).
my_paint(PosX, PosY, ZoomX, ZoomY, Variant):-
  ZoomY>=0.02,
  pen(4+80*ZoomY, rgb(0, 0, 255)),
  make_station(2000, PosX, PosY, ZoomX, ZoomY, Variant).
my_paint(PosX, PosY, ZoomX, ZoomY, Variant):-
  ZoomY>=0.02,
  pen(4+80*ZoomY, rgb(255, 0, 0)),
  make_station(4000, PosX, PosY, ZoomX, ZoomY, Variant).
my_paint(PosX, PosY, ZoomX, ZoomY, Variant):-
  ZoomY>=0.02,
  pen(4+80*ZoomY, rgb(255, 255, 0)),
  make_station(6000, PosX, PosY, ZoomX, ZoomY, Variant).

my_paint(PosX, PosY, ZoomX, ZoomY, Variant):-
  font(10,25,_),
  pen(10*ZoomX, 0),
  for(I, 0, G_WagonNum-1),
  visible_wagon(wagonX(I), Variant),
  brush(wColor(I)),
  X := (wagonX(I)-PosX)*ZoomX,
  Y := (wagonY(I)-PosY)*ZoomY,
  (in_curve(I, Xc, Yc, Sign, R)->
    Alfa := arccos((wagonX(I)-Xc)/R),
    Cx := (sin(Alfa)*1000-wPosoka(I)*Sign*cos(Alfa)*150)*ZoomX,
    Cy := (sin(Alfa)*150+wPosoka(I)*Sign*cos(Alfa)*1000)*ZoomY,
    Cx2 := (sin(Alfa)*1000+wPosoka(I)*Sign*cos(Alfa)*150)*ZoomX,
    Cy2 := (sin(Alfa)*150-wPosoka(I)*Sign*cos(Alfa)*1000)*ZoomY,
    fill_polygon( X - Cx, Y - Cy, X - Cx2, Y + Cy2, X + Cx, Y + Cy, X + Cx2, Y - Cy2)
  else
    SizeX := 1000*ZoomX,
    SizeY := 150*ZoomY,
    (wFlags(I)/\4=:=0->
      rect(X - SizeX, Y - SizeY, X + SizeX, Y + SizeY)
    else (wPosoka(I)=:=1->
      rect(X - SizeX, Y - SizeY, X + SizeX, Y + SizeY+120*ZoomY)
    else
      rect(X - SizeX, Y - SizeY - 120*ZoomY, X + SizeX, Y + SizeY)
    ))
  ),
  (Variant=big, ZoomX>0.08->
    make_text(G_MenuNumber, I, Text),
    text_out(Text, pos(X-25, Y-10))
  ),
  fail.

my_paint(PosX, PosY, ZoomX, ZoomY, Variant):-
  font(ZoomY*300,ZoomY*750,_),
  visible_station(N, Station, _, 8000, Variant),
  station(yes, N, Station, _, Text, Text2),
  X := Station-2000,
  Y := -500,
  text_out(N+". "+Text+" "+Text2, pos((X-PosX)*ZoomX-5, (Y-PosY)*ZoomY-10)),
  fail.

my_paint(PosX, PosY, ZoomX, ZoomY, big):-
  G_Zoom>0.08,
  font(10,25,_),
  visible_station(N, Station, _, 8000, big),
  pen(10*G_Zoom, 0),
  make_brush(12),
  % when_will_arrive(Station),
  X := Station-1500,
  Y := 2870,
  Rx := 200,
  Ry := 550,
  ellipse((X+Rx-G_PosX)*G_Zoom, (Y+Ry-G_PosY)*G_Zoom, (X-Rx-G_PosX)*G_Zoom, (Y-Ry-G_PosY)*G_Zoom),
  pen(20*G_Zoom, rgb(0, 0, 255)),
  Y0:=2500,
  Y := 3250,
  Y1 := 4000,
  X1 := Station-5500,
  X2 := Station,
  line((X1-G_PosX)*G_Zoom, (Y0-G_PosY)*G_Zoom, (X2+500-G_PosX)*G_Zoom, (Y0-G_PosY)*G_Zoom),
  line((X1-G_PosX)*G_Zoom, (Y-G_PosY)*G_Zoom, (X2-4500-G_PosX)*G_Zoom, (Y-G_PosY)*G_Zoom),
  D:=750,
  draw_arc((X1-D/2-G_PosX)*G_Zoom, (Y0-G_PosY)*G_Zoom, (X1+D/2-G_PosX)*G_Zoom, (Y0+D-G_PosY)*G_Zoom, (X1-G_PosX)*G_Zoom, (Y0-G_PosY)*G_Zoom, (X1-G_PosX)*G_Zoom, (Y-G_PosY)*G_Zoom),
  pen(20*G_Zoom, rgb(255, 0, 0)),
  X1 := Station-4500,
  X2 := Station+4500,
  line((X1-G_PosX)*G_Zoom, (Y-G_PosY)*G_Zoom, (X2-G_PosX)*G_Zoom, (Y-G_PosY)*G_Zoom),
  X1 := Station+2250,
  X2 := Station+1500,
  line((X1-G_PosX)*G_Zoom, (Y1-G_PosY)*G_Zoom, (X2-G_PosX)*G_Zoom, (Y-G_PosY)*G_Zoom),
  X2 := Station+3250,
  line((X1-G_PosX)*G_Zoom, (Y1-G_PosY)*G_Zoom, (X2-G_PosX)*G_Zoom, (Y1-G_PosY)*G_Zoom),
  pen(10*G_Zoom, 0),
  Add :=5500, Y:=2500, Sign:= -1,
  for(I, 1, 35),
  (I=:=14-> Y :=3250, Add := -7000, Sign:=1),
  (I=:=33-> Y :=4000, Add := -9750),
  R := (I=:=N -> 200 else 100),
  N1 := (32<N -> N-6 else N),
  (I<26->
    Brush := (N=:=I -> 0 else 1+(abs(N1-I)-1) mod 10)
  else (I<33->
    Brush := (N=:=I; 32<N -> 0 else 1+(abs(N-I)-1) mod 10)
  else
    Brush := (N=:=I; 25<N, N<33 -> 0 else 1+(abs(N1-I+6)-1) mod 10)
  )),
  X := Station-4500 + Sign*I*500+Add,
  more_variants(X, Y, R, Brush),
  (G_Zoom>0.2->
    text_out(I, pos((X-G_PosX)*G_Zoom-5, (Y-G_PosY)*G_Zoom-10)),
    station(_, I, _, _, Text, Text2),
    text_out(Text, pos((X-150-G_PosX)*G_Zoom-5, (Y+300-G_PosY)*G_Zoom-10)),
    text_out(Text2, pos((X-150-G_PosX)*G_Zoom-5, (Y+300-G_PosY)*G_Zoom+15))
  ),
  fail.

when_will_arrive(Station):-
  X := Station-2000+900-4000,
  Y := 2000,
  text_out("Arrive at: ", pos((X-G_PosX)*G_Zoom-5, (Y-G_PosY)*G_Zoom-10)),
  X := X+2000,
  find_wagon(Wagon, Station),
  text_out(Wagon, pos((X-G_PosX)*G_Zoom-5, (Y-G_PosY)*G_Zoom-10)).

find_wagon(Wagon, Station) :-
  Wagon := (G_WagonNum>0 -> 0 else -1),
  for(I, 1, G_WagonNum-1),
  (wPosoka(Wagon)=:= -1->
    (wPosoka(I)=:= -1->
      (wagonX(Wagon)>wagonX(I)-> Wagon:=I)
    else
      (wagonX(I)=<Station+3000-> Wagon:=I)
    )
  else (wagonX(Wagon)>Station+3000->
    (wPosoka(I)=:= -1; wagonX(I)=<Station+3000; wagonX(Wagon)<wagonX(I)-> Wagon:=I)
  else
    (wPosoka(I)=:= 1, wagonX(I)=<Station+3000, wagonX(Wagon)<wagonX(I)-> Wagon:=I)
  )),
  fail.
find_wagon(_, _).

win_func(paint):-
  my_paint(G_PosX, G_PosY, G_Zoom, G_Zoom, big);
  ZoomX := 0.0034*G_Xsize/1863,
  my_paint(-25000+G_PosSmall, -2000, ZoomX, 0.02, small).

win_func(init):-
  menu( pop_up, action(menu_file), text("&File") ),
  menu( pop_up, action(menu_show), text("&Show") ),
  menu( pop_up, action(menu_time), text("&Time") ),
  menu(right, action(menu_zoom_in), text("Zoom &In") ),
  menu(right, action(menu_zoom_out), text("Zoom &Out") ),
  menu( right, action(menu_help), text("&Help") ),
  G_Timer := set_timer(_, 0.1, time_func),
  set_scroll_range(_,vertical,0,G_ScrollRange),
  set_scroll_range(_,horizontal,0,G_ScrollRange),
  fix_scroll_bar_v,
  fix_scroll_bar_h.

%win_func(key_down(Ch, Rep)):-
%  write(Ch), nl,
%  fail.

win_func(key_down(67, Rep)):- % C
  menu_crash(press). 
win_func(key_down(83, Rep)):- % S
  menu_slow_motion(press). 
win_func(key_down(70, Rep)):- % F
  menu_fast_speed(press). 
win_func(key_down(80, Rep)):- % P
  menu_pause(press).
win_func(key_down(190, Rep)):- % >
  menu_minus(press).
win_func(key_down(188, Rep)):- % <
  menu_number(press).
win_func(key_down(187, Rep)):- % +
  menu_zoom_in(press).
win_func(key_down(189, Rep)):- % -
  menu_zoom_out(press).
 
win_func(key_down(36, Rep)):- % home
  G_PosSmall := 0, fix_scroll_bar_h.
win_func(key_down(35, Rep)):- % end
  G_PosSmall := end_map, fix_scroll_bar_h.
win_func(key_down(45, Rep)):- % insert
  G_PosSmall := max(0, G_PosSmall-Rep*10000), fix_scroll_bar_h.
win_func(key_down(33, Rep)):- % page Up
  G_PosSmall := min(end_map, G_PosSmall+Rep*10000), fix_scroll_bar_h.
win_func(key_down(46, Rep)):- % del
  G_PosSmall := max(0, G_PosSmall-Rep*50000), fix_scroll_bar_h.
win_func(key_down(34, Rep)):- % page Down
  G_PosSmall := min(end_map, G_PosSmall+Rep*50000), fix_scroll_bar_h.

win_func(key_down(Char, Rep)):-
  Xold:=G_PosX,
  Yold:=G_PosY,
  (Char=37-> % left
    G_PosX:= G_PosX - G_Xsize*0.02*Rep/G_Zoom
  ),
  (Char=39-> % right
    G_PosX:= G_PosX + G_Xsize*0.02*Rep/G_Zoom
  ),
  (Char=38-> % up
    G_PosY:= G_PosY - G_Ysize*0.02*Rep/G_Zoom
  ),
  (Char=40-> % down
    G_PosY:= G_PosY + G_Ysize*0.02*Rep/G_Zoom
  ),
  move(Xold, Yold).

win_func(size(X,Y)):-
  G_Xsize:=X,
  G_Ysize:=Y,
  update_window(_).

win_func(mouse_click(X, Y)):-
  (Y<100->
    G_Variant:= small,
    Xold:=G_PosX,
    Yold:=G_PosY,
    ZoomX := 0.0034*G_Xsize/1863,
    ZoomY:= 0.02,
    G_PosX:= -25000+G_PosSmall+X/ZoomX-0.5*G_Xsize/G_Zoom,
    G_PosY:= -2000+Y/ZoomY-100/G_Zoom-0.25*(G_Ysize-100)/G_Zoom,
    move(Xold, Yold)
  else
    G_Variant:= big
  ),
  G_moveX:=X,
  G_moveY:=Y,
  set_capture(_).

win_func(mouse_click_up(X, Y)):-
  release_capture.

win_func(mouse_move(X, Y)):-
  (message_flags(left)->
    Xold:=G_PosX,
    Yold:=G_PosY,
    (G_Variant=big->
      ZoomX:=G_Zoom,
      ZoomY:=G_Zoom
    else
      ZoomX := -0.0034*G_Xsize/1863,
      ZoomY:= -0.02
    ),
    G_PosX:= G_PosX + (G_moveX-X)/ZoomX,
    G_PosY:= G_PosY + (G_moveY-Y)/ZoomY,
    move(Xold, Yold),
    G_moveX:=X,
    G_moveY:=Y
  ).

win_func(scroll(horizontal,Type,Val)):-
  (Type=line->
    Step := 10000
  else (Type=page->
    Step := 100000
  else (Type=thumb_track->
    Step := (end_map+500000)/G_ScrollRange,
    Old := Val,
    Val := Val - G_Scroll_h,
    G_Scroll_h := Old
  else % thumb_moved_to
    G_Scroll_h := G_ScrollRange*(G_PosSmall/(end_map+500000)),
    fail
  ))),
  G_PosSmall := G_PosSmall + Step*Val,
  (G_PosSmall<0 -> G_PosSmall := 0),
  (G_PosSmall>end_map -> G_PosSmall := end_map),
  fix_scroll_bar_h.

win_func(scroll(vertical,Type,Val)):-
  Xold:=G_PosX,
  Yold:=G_PosY,
  (Type=line->
    Step := 0.02
  else (Type=page->
    Step := 0.3
  else (Type=thumb_track->
    Step := 0.02,
    Old := Val,
    Val := Val - G_Scroll_v,
    G_Scroll_v := Old
  else % thumb_moved_to
    G_Scroll_v := (G_ScrollRange-G_ScrollPage)//2,
    fail
  ))),
  G_PosY:= G_PosY + G_Ysize*Step*Val/G_Zoom,
  move(Xold, Yold).

win_func(mouse_wheel(Delta, X, Y)):-
  (message_flags(left); message_flags(middle); message_flags(ctrl)->
    client_pos(_,A,B),
    zoom(0-Delta, X-A, Y-B)
  else
    Yold:=G_PosY,
    G_PosY:= G_PosY - 3*G_Ysize*0.02*Delta/G_Zoom,
    move(G_PosX, Yold)
  ).

win_func(r_mouse_click(X, Y)):-
  (message_flags(ctrl)->
    zoom( 7, X, Y)
  else
    zoom(-7, X, Y)
  ). 

zoom(Delta, X, Y):-
  G_Zoom:=G_Zoom*0.9**Delta,
  G_PosX:= G_PosX - X* (1 - 0.9**Delta)/G_Zoom,
  G_PosY:= G_PosY - Y* (1 - 0.9**Delta)/G_Zoom,
  fix_scroll_bar_v,
  update_window(_).

fix_scroll_bar_v:-
  G_ScrollPage := (G_Zoom=<0.25 -> 1000*G_Zoom else 1500+1000*log(G_Zoom)/log(0.25)),
  G_Scroll_v := (G_ScrollRange-G_ScrollPage)//2,
  set_scroll_page(_,vertical,G_ScrollPage),
  set_scroll_pos(_,vertical,G_Scroll_v).

fix_scroll_bar_h:-
  G_Scroll_h := G_ScrollRange*(G_PosSmall/(end_map+500000)),
  set_scroll_page(_,horizontal,G_ScrollRange*500000/(end_map+500000)),
  set_scroll_pos(_,horizontal,G_Scroll_h),
  update_window(_).

move(Xold, Yold):-
  update_window(_).
  %scroll_window(_, floor(Xold*G_Zoom)-floor(G_PosX*G_Zoom), floor(Yold*G_Zoom)-floor(G_PosY*G_Zoom), 1).

put_grid(X2, Y2, X1, Y1, PosX, PosY, ZoomX, ZoomY, big):-
  (X1<X2-> A:=X1, B:=X2 else A:=X2, B:=X1),
  for(X, A, B, step(5000)),
  line((X-PosX)*ZoomX, (Y1-72-PosY)*ZoomY, (X-PosX)*ZoomX, (Y1+72-PosY)*ZoomY),
  fail.
put_grid(X2, Y2, X1, Y1, PosX, PosY, ZoomX, ZoomY, Variant).

get_local_arc(Wagon, X, Y, Sign, Q1, Q2, R, Semaphore):-
  metro_arc(X, Y, Sign, Q1, Q2, R, Semaphore).
get_local_arc(Wagon, X+Point, Y, Sign, Q1+Point, Q2, R, Semaphore2):-
  local_station(Wagon, Point, FirstSemaphore),
  local_metro_arc(X, Y, Sign, Q1, Q2, R, Semaphore),
  Semaphore2 := (Semaphore=no-> no else Semaphore+FirstSemaphore).

get_visible_arc(X, Y, Sign, Q1, Q2, Semaphore):-
  metro_arc(X, Y, Sign, Q1, Q2, _, Semaphore).
get_visible_arc(X+Point, Y, Sign, Q1+Point, Q2, Semaphore2):-
  visible_station(_, Point, FirstSemaphore, 20000, big),
  local_metro_arc(X, Y, Sign, Q1, Q2, _, Semaphore),
  Semaphore2 := (Semaphore=no-> no else Semaphore+FirstSemaphore).

get_metro_line(X1, Y1, X2, Y2, Sem1, Sem2, Variant):-
  metro_line(X1, Y1, X2, Y2, Sem1, Sem2).
get_metro_line(X1+Point, Y1, X2+Point, Y2, NewSem1, NewSem2, Variant):-
  visible_station(_, Point, FirstSemaphore, 20000, Variant),
  local_metro_line(X1, Y1, X2, Y2, Sem1, Sem2),
  NewSem1 := (Sem1=no-> no else Sem1+FirstSemaphore),
  NewSem2 := (Sem2=no-> no else Sem2+FirstSemaphore).
get_metro_line(X1+5000, Y, X2-5000, Y, no, no, Variant):-
  visible_station(Where, X1, _, 300000, Variant), % increase if distance between stations is more than 3 km 
  NextSt := Where+1,
  station(yes, NextSt, X2, _, _, _),
  (Y=1010; Y=1520).

my_draw_arc(X, Y, D, Q1, Q2, Open, Sign, PosX, PosY, ZoomX, ZoomY, Variant):-
  (Sign=:=1->
    draw_arc((X-D/2-PosX)*ZoomX, (Y-PosY)*ZoomY, (X+D/2-PosX)*ZoomX, (Y+D-PosY)*ZoomY, (Q1-PosX)*ZoomX, (Q2-PosY)*ZoomY, (X+Open-PosX)*ZoomX, (Y-PosY)*ZoomY)
  else
    draw_arc((X-D/2-PosX)*ZoomX, (Y-PosY)*ZoomY, (X+D/2-PosX)*ZoomX, (Y+D-PosY)*ZoomY, (X+Open-PosX)*ZoomX, (Y-PosY)*ZoomY, (Q1-PosX)*ZoomX, (Q2-PosY)*ZoomY)
  ).

make_station(Shift, PosX, PosY, ZoomX, ZoomY, Variant):-
  visible_station(_, Station, _, 4000, Variant),
  X1 := Station-4000+Shift,
  Y := 750,
  X2 := Station-2000+Shift,
  line((X1-PosX)*ZoomX, (Y-PosY)*ZoomY, (X2-PosX)*ZoomX, (Y-PosY)*ZoomY),
  X1 := Station+4000-Shift,
  Y := 1750,
  X2 := Station+2000-Shift,
  line((X1-PosX)*ZoomX, (Y-PosY)*ZoomY, (X2-PosX)*ZoomX, (Y-PosY)*ZoomY),
  fail.

more_variants(X, Y, R, Brush):-
  Y1:=Y-50,
  R1:=R-10,
  (Brush=:=3 -> draw_ellipse(X, Y1, R1, 1)),
  (Brush=:=5 -> draw_ellipse(X, Y1, R1, 2)),
  (Brush=:=7 -> draw_ellipse(X, Y1, R1, 4)),
  (Brush=:=10 ->
    draw_ellipse(X, Y1-100, R1-20, 2),
    draw_ellipse(X, Y1-50, R1-10, 3),
    draw_ellipse(X, Y1, R1, 4)
  ),
  draw_ellipse(X, Y, R, Brush).

draw_ellipse(X, Y, R, Brush):-
  make_brush(Brush),
  ellipse((X+R-G_PosX)*G_Zoom, (Y+R-G_PosY)*G_Zoom, (X-R-G_PosX)*G_Zoom, (Y-R-G_PosY)*G_Zoom).

