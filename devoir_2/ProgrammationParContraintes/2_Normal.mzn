% Thaïs Genisson (2315046)
% Erika Fossouo (1943831)

include "globals.mzn";

% États possibles pour une case du terrain
% V = Vide
% B = Tour bleue
% R = Tour rouge
enum etat = {V, B, R};

% Dimension du terrain (carré)
int: n;
set of int: dim = 1..n;

% État du terrain
array[dim, dim] of var etat: terrain;

% Variable objectif à maximiser
var int: total_commun;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
total_commun = count(terrain, B);
solve maximize total_commun;


constraint count(terrain, B) == count(terrain, R); % autant de B que de R
constraint forall(d in dim) (
  not exists(b in dim) (terrain[b, d] == B /\ exists(r in dim) (terrain[r, d] == R))
); % pas de B et de R sur la meme colonne
constraint forall(d in dim) (
  not exists(b in dim) (terrain[d, b] == B /\ exists(r in dim) (terrain[d, r] == R))
); % pas de B et de R sur la meme ligne
% les B et R ne sont pas sur la même diagonale
constraint forall(i in 1..n, j in 1..n where terrain[i, j] == B) (
  forall(k in 1..n, l in 1..n where terrain[k, l] == R) (
    abs(i - k) != abs(j - l)
  )
);
constraint exists(d in dim) (terrain[1, d] == B); % briser une symétrie (interchager bleu et rouge pas possible)
%-----------------------------------------------------------------------------%
output 
["Terrain :\n"]
++
[if j = 1 then "["  endif ++ if fix(terrain[i,j]) == V then "_" else show(terrain[i,j]) endif ++ if j = n then "]\n" else "," endif | i in 1..n, j in 1..n]
++
["\n"]
++
["Total de tours commun: " ++ show(total_commun)]
