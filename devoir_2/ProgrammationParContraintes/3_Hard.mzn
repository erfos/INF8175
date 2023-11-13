% Thaïs Genisson (2315046)
% Erika Fossouo (1943831)

include "globals.mzn";

% Énumérations des équipes participant au tournoi
enum equipes = {CO, TA, HO, DA, NA, MU, AL, UT};

% Lieux de rencontres des equipes (0 = pas de rencontre).
% Tout lieu i, tel que 0 < i <= card(equipes), 
% est designé comme le domicile de l'équipe associée par la relation to_enum(equipe, i)
set of int: terrains = 0..card(equipes);

% Étendue du tournoi (en jours)
int: d = 16;
set of int: jours = 1..d;

% Calendrier de placement des matchs
array[equipes, jours] of var terrains: calendrier;

% Nombres de rencontres entre deux equipes
array[equipes, equipes] of var 0..2: rencontres;

% Tuples des dates de match entre deux équipes
array[equipes, equipes] of var tuple (0..d, 0..d): dates;

% Variable objectif à maximiser
var int: objectif_match_espaces;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%




% Lier calendrier et dates
constraint forall(e1 in equipes, e2 in equipes) (
  if (e1 != e2) then
    forall(j in jours, k in jours where j < k) (
      calendrier[e1, j] == calendrier[e2, j] /\ calendrier[e1, k] == calendrier[e2, k] /\ calendrier[e1, j] != 0 /\ calendrier[e1, k] != 0 ->
      dates[e1, e2] == dates[e2, e1] /\ dates[e1, e2] = (j, k)
    )
   else % Si c'est la même équipe, mettre (0, 0), c'est à dire aucun jour
    dates[e1, e2] = (0, 0)
   endif
);

% Lier calendrier et rencontres
constraint forall(e1 in equipes, e2 in equipes) (
  if (e1 != e2) then
    rencontres[e1, e2] = sum(j in jours) (bool2int(calendrier[e1, j] == calendrier[e2, j] /\ calendrier[e1, j] != 0))
   else
    rencontres[e1, e2] = 0
   endif
);

% Contrainte 1 et contrainte 3 (l'unicité d'une autre équipe sur le même terrain assure qu'il n y en ait que deux)
constraint forall(j in jours) (
  forall(e1 in equipes) (
    if (calendrier[e1, j] != 0) then
      count(e2 in equipes where e1 != e2) (
        calendrier[e1, j] == calendrier[e2, j]
      ) == 1
    endif
  )
);

% Contrainte 2
constraint forall(j in jours) (
  forall(e1 in equipes, e2 in equipes where e1 != e2) (
    if (calendrier[e1, j] != 0) then
      e1 == to_enum(equipes, calendrier[e1, j]) \/ e2 == to_enum(equipes, calendrier[e2, j])
    endif
  )
);

% 4. Si une équipe ne joue pas lors d’une période elle est placée sur le terrain n°0.
% Comment on sait qu'une équipe ne joue pas.

% Contrainte 5
constraint forall(e in equipes) (
 sum(j in jours) (bool2int(to_enum(equipes, calendrier[e, j]) == e)) <= 7
);

% Contrainte 6
constraint forall(e1 in equipes, e2 in equipes where e1 != e2) (
  rencontres[e1, e2] == 2
);

% Contrainte 7
constraint forall(e1 in equipes, e2 in equipes where e1 != e2) (
  abs(dates[e1, e2].1 - dates[e1, e2].2) >= 3
);

% Contrainte 8
constraint forall(e1 in equipes, e2 in equipes where e1 != e2) (
  calendrier[e1, dates[e1, e2].1] != calendrier[e1, dates[e1, e2].2]
);

% Le nombre de matchs espacés de plus de 6 jours
objectif_match_espaces = sum(e1, e2 in equipes where e1 < e2) (
  bool2int(abs(dates[e1, e2].1 - dates[e1, e2].2) >= 6)
);
solve maximize objectif_match_espaces;

%-----------------------------------------------------------------------------%

% Affichage du calendrier par equipes et par jours puis du résultat de la fonction objectif.
% Lorsqu'une équipe ne joue pas, l'emplacement de match reste vide sinon elle contient le nom de l'équipie adverse.
% Si une équipe ne joue pas à domicile, un "@" précède le nom de l'équipe adverse.
output 
["Calendrier:\n"]
++
[if j = 1 then "   " else "" endif ++ if j < 10 then "  j" ++ show(j) else " j" ++ show(j) endif ++ if j = d then "\n" else "" endif | j in jours ]
++
[if j = 1 then show(e1) ++ ":" else "" endif ++ if fix(calendrier[e1,j]) = 0 then "    " else if fix(calendrier[e1,j]) = e1 then "  " ++ concat([if e1 != e2 /\ fix(calendrier[e2,j]) = e1 then show(e2) else "" endif | e2 in equipes])  else " @" ++ show(to_enum(equipes, calendrier[e1,j])) endif endif ++ if j = d then "\n" else "" endif | e1 in equipes, j in jours ]
++
["\nMatchs retour espacés de 6 jours ou plus = " ++ show(objectif_match_espaces) ++ "\n"]
++
["\nTableau calendrier : ", show(dates)]
;
