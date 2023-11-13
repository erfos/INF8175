include "globals.mzn";

var 1000..9999: nombre;

array[1..4] of var 1..9: chiffres;

var int: product = product([chiffres[i] | i in 2..4]); % produit des trois dernier chiffres

constraint chiffres[4] mod 2 == 0; % c'est un nombre pair
constraint forall(c in chiffres) (c != 0); % le nombre ne contient pas de 0
constraint all_different(chiffres); % tous les chiffres sont différents
constraint chiffres[1] > chiffres[2]; % le chiffre des milliers > celui des centaines
constraint chiffres[3] < chiffres[4]; % le chiffre des dizaines < celui des unités
constraint chiffres[2] > chiffres[4]; % le chiffre des centaines > celui des unités
constraint sum(i in 1..4) (chiffres[i]) = 15; % la somme des chiffres = 15

nombre = chiffres[1] * 1000 + chiffres[2] * 100 + chiffres[3] * 10 + chiffres[4];

%minimize product; % minimise le produit des 3 derniers chiffres
solve minimize product; % minimise le produit des 3 derniers chiffres
%solve satisfy;

output [
  show(nombre)
];

/*
1. C’est un nombre pair.
2. Le chiffre 0 n’est pas présent dans le nombre.
3. Les 4 chiffres sont différents.
4. Le chiffre à la position des milliers est supérieur à celui à la position des centaines.
5. Le chiffre à la position des dizaines est inférieur à celui à la position des unités.
6. Le chiffre à la position des centaines est supérieur à celui à la position des unités.
7. La somme des 4 chiffres est supérieure à 15.
8. Le produit des 3 derniers chiffres (chiffre à la position des centaines×chiffre à la position des dizaines × chiffre à la position des unités) doit être minimisé.
*/