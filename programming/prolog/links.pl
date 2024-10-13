% Links entre lenguajes

link(fortran, algol60).
link(algol60, cpl).
link(cpl, bcpl).
link(bcpl, c).
link(c, cplusplus).
link(algol60, simula67).
link(simula67, cplusplus).
link(simula67, smalltalk80).

path(L, L).
path(L, M) :- link(L, X), path(X, M).
