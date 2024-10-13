llueve(X):-nublado(X),frio(X).
frio(X):-temperatura(X,baja).
nublado(X):-sin_sol(X).

temperatura(jueves,baja).
sin_sol(jueves).