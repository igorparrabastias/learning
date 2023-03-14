likes(wallace, cheese).
likes(grommit, cheese).
likes(wendolene, sheep).

% So, our rule means X is a friend of Y if X and Y are not the same and X and Y like the same Z.
friend(X,Y) :- \+(X = Y), likes(X, Z), likes(Y,Z).

loves(X,Y):- likes(X,Y), \+ (( likes(X,Z), Z \= Y )). 
