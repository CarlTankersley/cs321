partition([], _, [], []).
partition([H | T], V, [H | A], B) :- 
    H < V,
    partition(T, V, A, B).
partition([H | T], V, A, [H | B]) :- 
    H > V,
    partition(T, V, A, B).
partition([H | T], V, A, B) :- 
    H is V,
    partition(T, V, A, B).

equalLength([], []).
equalLength([_ | T1], [_ | T2]) :-
    equalLength(T1, T2).

elementOf(E, [H | _]) :-
    E is H.
elementOf(E, [_ | T]) :-
    elementOf(E, T).

median(L, M) :-
    elementOf(M, L),
    partition(L, M, A, B),
    equalLength(A, B).

