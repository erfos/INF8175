from uflp import UFLP
from typing import List, Tuple

def solve(problem: UFLP) -> Tuple[List[int], List[int]]:
    """
    Votre implementation, doit resoudre le probleme via recherche locale.

    Args:
        problem (UFLP): L'instance du probleme à résoudre

    Returns:
        Tuple[List[int], List[int]]: 
        La premiere valeur est une liste représentant les stations principales ouvertes au format [0, 1, 0] qui indique que seule la station 1 est ouverte
        La seconde valeur est une liste représentant les associations des stations satellites au format [1 , 4] qui indique que la premiere station est associée à la station pricipale d'indice 1 et la deuxieme à celle d'indice 4
    """

    s = SolutionInitiale(problem)
    s_star = s 
    for k in range (100) : 
        Voisinage = getVoisins(s_star)
   
   """
    for k ∈ 1 𝗍𝗈 Θ :
G = [n ∈ N(s)] V = [n ∈ L(G, s)]
s = Q(V, s)
𝗂𝖿 f(s) < f(s⋆) :
s⋆ = s 𝗋𝖾𝗍𝗎𝗋𝗇 s⋆

    return None, None """

def SolutionInitiale(problem) :
    # Initialisation aléatoire de la liste représentant les stations principales ouvertes 
    GaresOuvertes = [random.choice([0,1]) for _ in range(problem.n_main_station)]
    # Les gares satellites doivent être ratachées à au moins une station ouverte 
    if sum(GaresOuvertes) == 0:
        GaresOuvertes[random.choice(range(problem.n_main_station))] = 1 

    # Initialisation aléatoire de la liste représentant les associations des stations satellites
    indices=[i for i in range(len(GaresOuvertes)) if GaresOuvertes[i]==1 ]
    Satellites = [random.choice(indices) for i in range (problem.n_station_stallites)]
    return (GaresOuvertes, Satellites)


def getVoisins(state) : 
    Voisins = []
    GaresOuvertes = state[0]
    Satellites = state[1]
    for i in range (len(GaresOuvertes)) :
        Voisins.append(state)
        # Modifier les gares ouvertes 
        if GaresOuvertes[i] == 0 :
            Voisins[-1][0][i] == 1 
        else : 
            Voisins[-1][i][0] ==0 

    return Voisins 

def validite (voisin,state) : 

    return 
