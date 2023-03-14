%domains

lista=char*

%predicates

%inicial(symbol)
%final(symbol)
%delta(symbol, char, symbol)
%aceptar(lista, symbol)
%acepto(lista)

%clauses

inicial(q0).
final(q0).
delta(q0, 'a', q1).
delta(q1, 'b', q0).
acepto(L):-inicial(Q), aceptar(L,Q).
aceptar([X|Y], Q):-delta(Q, X, Q1), aceptar(Y, Q1).
aceptar([],Q):-final(Q).

%goal

write("Dame lista de símbolos: "), readterm(lista, L),
acepto(L),
nl,
write("Pertenece al lenguaje").