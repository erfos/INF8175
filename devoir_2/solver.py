import random
from uflp import UFLP
from typing import List, Tuple
import time

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

    #print("main station coordinates : ", problem.main_stations_coordinates)
    #print("main stations opening cost : ", problem.main_stations_opening_cost)
    #print("satellite station coordinates : ", problem.satellite_stations_connection_coordinates)
    #print("satellites stations connection cost : ", problem.satellite_stations_connection_cost)


    s = SolutionInitiale(problem)
    current_state_main_station_cost = 0
    
    s_star = s
    for k in range (90000) : 
        for i in range(0, problem.n_main_station):
            if s[0][i] == 1:
                current_state_main_station_cost += problem.main_stations_opening_cost[i]

        neighbours = getVoisins(s_star)
        validNeighbours, neighbours_cost = validate(neighbours, current_state_main_station_cost, problem)
        s, nextNeighbour_cost = select_Neighbour(validNeighbours, neighbours_cost)
        if (nextNeighbour_cost < current_state_main_station_cost):
            s_star = s

    print("gares principales : ", s_star[0])
    print("gares satellites : ", s_star[1])
    for j in range(0, problem.n_satellite_station):
        print("j : ", j)
        for i in range(0, problem.n_main_station):
            print("i : ", i)
            if s_star[0][i] == 1:
                current_cost = problem.satellite_stations_connection_cost[s_star[1][j]][j] # something wrong here with index ?
                print("current cost : ", current_cost)
                print("cost to compare : ", problem.satellite_stations_connection_cost[i][j])
                if current_cost > problem.satellite_stations_connection_cost[i][j]:
                    s_star[1][j] = i
    print("s star : ", s_star)
    return s_star
    """
    𝖫𝗈𝖼𝖺𝗅𝖲𝖾𝖺𝗋𝖼𝗁(N, L, Q, f, Θ) :
        s = 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾𝖨𝗇𝗂𝗍𝗂𝖺𝗅𝖲𝗈𝗅𝗎𝗍𝗂𝗈𝗇()
        s⋆ = s
        𝖿𝗈𝗋 k ∈ 1 𝗍𝗈 Θ :
            G = [n ∈ N(s)]
            V = [n ∈ L(G,s)]
            s = Q(V,s)
            𝗂𝖿 f(s) < f(s⋆) :
                s⋆ = s
        return s*
    for k ∈ 1 𝗍𝗈 Θ :
        G = [n ∈ N(s)] V = [n ∈ L(G, s)]
        s = Q(V, s)
        𝗂𝖿 f(s) < f(s⋆) :
        s⋆ = s 𝗋𝖾𝗍𝗎𝗋𝗇 s⋆

    return None, None """

def SolutionInitiale(problem: UFLP):
    # Initialisation aléatoire de la liste représentant les stations principales ouvertes 
    GaresOuvertes = [random.choice([0,1]) for _ in range(problem.n_main_station)]
    # Les gares satellites doivent être ratachées à au moins une station ouverte 
    if sum(GaresOuvertes) == 0:
        GaresOuvertes[random.choice(range(problem.n_main_station))] = 1 

    # Initialisation aléatoire de la liste représentant les associations des stations satellites
    indices=[i for i in range(len(GaresOuvertes)) if GaresOuvertes[i] == 1 ]
    Satellites = [random.choice(indices) for i in range (problem.n_satellite_station)]
    return (GaresOuvertes, Satellites)


def getVoisins(state: Tuple[List[int], List[int]]): 
    Voisins = []
    GaresOuvertes = state[0]
    Satellites = state[1]
    for i in range (len(GaresOuvertes)) :
        Voisins.append(state)
        # Modifier les gares ouvertes
        """print("voisins[-1] : ", Voisins[-1])
        print("voisins : ", Voisins)
        print("len(voisins) : ", len(Voisins))
        print("voisins[len(voisins)] : ", Voisins[len(Voisins)])
        print("voisins[len(voisins)][0] : ", Voisins[len(Voisins)][0])
        print("voisins[len(voisins)][0][i] : ", Voisins[len(Voisins)][0][i])"""
        if GaresOuvertes[i] == 0 :
            Voisins[-1][0][i] == 1
        else :
            Voisins[-1][0][i] == 0
    return Voisins

def validate(voisins: List[Tuple[List[int], List[int]]], current_cost: float, problem: UFLP):
    neighbours_main_station_cost = [0 for i in range(0, len(voisins))]
    """cost_current_state = 0
    for i in range(0, len(problem.n_main_station)):
        if state[0][i] == 1:
            cost_current_state += problem.main_stations_opening_cost[i]
        
        for j in range(0, len(voisins)):
            if voisins[j][0][i] == 1:
                neighbours_main_station_cost[j] += problem.main_stations_opening_cost[i]
    """
    for i in range(0, len(voisins)):
        for j in range(0, problem.n_main_station):
            if voisins[i][0][j] == 1:
                neighbours_main_station_cost[i] += problem.main_stations_opening_cost[j]

    valid_neighbours = []
    for i in range(0, len(voisins)):
        if neighbours_main_station_cost[i] <= current_cost:
            valid_neighbours.append(voisins[i])
    return valid_neighbours, neighbours_main_station_cost

def select_Neighbour(voisins: List[Tuple[List[int], List[int]]], cost: List[int]):
    index = cost.index(min(cost))
    return voisins[index], cost[index]
