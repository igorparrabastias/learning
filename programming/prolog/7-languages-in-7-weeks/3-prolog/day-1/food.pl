food_type(velveeta, cheese).
food_type(ritz, cracker).
food_type(spam, meat).
food_type(sausage, meat).
food_type(jolt, soda).
food_type(twinkie, dessert).
flavor(sweet, dessert).
flavor(savory, meat).
flavor(savory, cheese).
flavor(sweet, soda).
food_flavor(X, Y) :- food_type(X, Z), flavor(Y, Z).

%% Prolog can give you information sooner, it will. Try a few more:
%% | ?- food_flavor(sausage, sweet).
%% no
%% | ?- flavor(sweet, What).
%% What = dessert ? ;
%% What = soda
%% yes
%%
%% No, sausage is not sweet. What food types are sweet? dessert and soda.
