% Should give the correct output for an input of complete([], X).
% Puzzle with 1 given is currently ready to go. Comment out inits
% and uncomment the other set of inits to switch to the other 
% puzzle. Both should work.

% init(2,3,46).
% init(2,4,45).
% init(2,6,55).
% init(2,7,74).
% init(3,2,38).
% init(3,5,43).
% init(3,8,78).
% init(4,2,35).
% init(4,8,71).
% init(5,3,33).
% init(5,7,59).
% init(6,2,17).
% init(6,8,67).
% init(7,2,18).
% init(7,8,64).
% init(8,3,24).
% init(8,4,21).
% init(8,6,1).
% init(8,7,2).

init(1,1,13).
init(1,5,27).
init(1,9,39).
init(2,2,11).
init(2,5,24).
init(2,8,37).
init(5,1,71).
init(5,2,70).
init(5,8,34).
init(5,9,43).
init(8,2,81).
init(8,5,62).
init(8,8,53).
init(9,1,79).
init(9,5,63).
init(9,9,51).

withinOne([X, Y1], [X, Y2]) :-
    Y2 is Y1+1,
    Y2 < 10.

withinOne([X, Y1], [X, Y2]) :-
    Y2 is Y1-1,
    Y2 > 0.

withinOne([X1, Y], [X2, Y]) :-
    X2 is X1+1,
    X2 < 10.

withinOne([X1, Y], [X2, Y]) :-
    X2 is X1-1,
    X2 > 0.

elementOf(E, [E | _]).
elementOf(E, [_ | T]) :-
    elementOf(E, T).

complete([], Finished) :-
    init(X1, Y1, 1),
    complete([[X1, Y1]], Finished).
complete([], Finished) :-
    elementOf(X1, [1,2,3,4,5,6,7,8,9]),
    elementOf(Y1, [1,2,3,4,5,6,7,8,9]),
    \+ init(X1, Y1, _),
    \+ init(_, _, 1),
    complete([[X1, Y1]], Finished).
complete(X, X) :-
    length(X, 81).
complete([[X, Y] | T], Finished) :-
    withinOne([X, Y], [X2, Y2]),
    \+ elementOf([X2, Y2], T),
    length(T, Length),
    NewLength is Length + 2,
    init(X2, Y2, NewLength),
    complete([[X2, Y2], [X, Y] | T], Finished).
complete([[X, Y] | T], Finished) :-
    withinOne([X, Y], [X2, Y2]),
    \+ elementOf([X2, Y2], T),
    length(T, Length),
    NewLength is Length + 2,
    \+ init(X2, Y2, _),
    \+ init(_, _, NewLength),
    complete([[X2, Y2], [X, Y] | T], Finished).

show(Soln) :- reverse(Soln,Forwards), write('\n'),
              member(Row,[1,2,3,4,5,6,7,8,9]),
              write('\n'),
              member(Col,[1,2,3,4,5,6,7,8,9]),
              nth1(Value,Forwards,[Row,Col]),
              write(Value),write('\t'),
              fail.
