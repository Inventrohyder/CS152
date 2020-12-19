% Prolog Sudoku Solver (C) 2007 Markus Triska (triska@gmx.at)
% Modified by Rohan Shekhar.
% Modified by Haitham Alhad Hyder to solve for diagonal sudokus.
% Public domain code.

% We need this module to use some of the constraint programming extensions to Prolog
:- use_module(library(clpfd)).

% Pss is a list of lists representing the game board.

sudoku(Pss) :-
    flatten(Pss, Ps),
    Ps ins 1..9,
    maplist(all_distinct, Pss),
    Pss = [R1,R2,R3,R4,R5,R6,R7,R8,R9],
    columns(R1, R2, R3, R4, R5, R6, R7, R8, R9),
    diagonals(R1, R2, R3, R4, R5, R6, R7, R8, R9),
    blocks(R1, R2, R3), blocks(R4, R5, R6), blocks(R7, R8, R9),
    label(Ps).

columns([], [], [], [], [], [], [], [], []).
columns([A|As],[B|Bs],[C|Cs],[D|Ds],[E|Es],[F|Fs],[G|Gs],[H|Hs],[I|Is]) :-
    all_distinct([A,B,C,D,E,F,G,H,I]),
    columns(As, Bs, Cs, Ds, Es, Fs, Gs, Hs, Is).

blocks([], [], []).
blocks([X1,X2,X3|R1], [X4,X5,X6|R2], [X7,X8,X9|R3]) :-
    all_distinct([X1,X2,X3,X4,X5,X6,X7,X8,X9]),
    blocks(R1, R2, R3).

diagonals([], [], [], [], [], [], [], [], []).
diagonals(
    [A1,_, _, _, _, _, _, _, A9],
    [_, B2, _, _, _, _, _, B8, _],
    [_, _, C3, _, _, _, C7, _, _],
    [_, _, _, D4, _, D6, _, _, _],
    [_, _, _, _, E5, _, _, _, _],
    [_, _, _, F4, _, F6, _, _, _],
    [_, _, G3, _, _, _ ,G7, _, _],
    [_, H2, _, _, _, _ , _, H8, _],
    [I1, _, _, _, _, _ , _, _, I9]) :-
    all_distinct([A1,B2,C3,D4,E5,F6,G7,H8,I9]),
    all_distinct([A9, B8, C7, D6, E5, F4, G3, H2, I1]).

problem(1, [[_,8,_, 4,_,7, _,9,_],
            [3,_,4, _,_,_, 8,_,2],
            [_,6,_, _,_,_, _,7,_],

            [6,_,_, _,_,_, _,_,1],
            [_,_,_, _,_,_, _,_,_],
            [8,_,_, _,_,_, _,_,9],

            [_,1,_, _,_,_, _,3,_],
            [2,_,5, _,_,_, 1,_,7],
            [_,3,_, 8,_,9, _,5,_]]).


:- problem(1, Rows), sudoku(Rows), maplist(writeln,Rows), halt.

