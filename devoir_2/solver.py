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
    current_solution_cost = 0
    current_state_main_station_cost = 0

    for i in range(problem.n_main_station):
        if s[0][i] == 1:
            current_solution_cost += problem.main_stations_opening_cost[i]
        for j in range(problem.n_satellite_station):
            current_solution_cost += problem.satellite_stations_connection_cost[i][j]
    print("solution initiale : ", s)
    print("cout de la solution initiale : ", current_solution_cost)
    
    s_star = s
    """for k in range(5000):
        neighbors = getVoisins(s)
        # print("nombre de voisin : ", len(neighbors))
        # print("voisins : ", neighbors)
        valid_neighbors, valid_neighbors_cost = validate(neighbors, current_solution_cost, problem)
        # maybe valid neighbors is empty, check it
        # print("voisins valides : ", valid_neighbors)
        # print("valid neighbors cost : ", valid_neighbors_cost)
        s, best_neighbor_cost = select_Neighbor(valid_neighbors, valid_neighbors_cost)
        # print("best neighbor : ", s)
        # print("best neighbor cost : ", best_neighbor_cost)
        # print("current cost : ", current_solution_cost)
        if (best_neighbor_cost < current_solution_cost):
            s_star = s
    return s_star"""

    begin = time.time()
    for k in range (1000) : 
        for i in range(0, problem.n_main_station):
            if s[0][i] == 1:
                current_state_main_station_cost += problem.main_stations_opening_cost[i]

        neighbors = getVoisins(s_star)
        validNeighbors, neighbors_cost = validate(neighbors, current_state_main_station_cost, problem)
        if len(validNeighbors) == 0:
            print("plus de voisins valide")
            break
        s, nextNeighbour_cost = select_Neighbor(validNeighbors, neighbors_cost)
        if (nextNeighbour_cost < current_state_main_station_cost):
            s_star = s
    end = time.time() - begin
    print("delta en seconde : ", end)

    print("gares principales : ", s_star[0])
    print("gares satellites : ", s_star[1])
    begin = time.time()
    for j in range(0, problem.n_satellite_station):
        # print("j : ", j)
        for i in range(0, problem.n_main_station):
            # print("i : ", i)
            if s_star[0][i] == 1:
                current_cost = problem.satellite_stations_connection_cost[s_star[1][j]][j] # something wrong here with index ?
                # print("current cost : ", current_cost)
                # print("cost to compare : ", problem.satellite_stations_connection_cost[i][j])
                if current_cost > problem.satellite_stations_connection_cost[i][j]:
                    s_star[1][j] = i
    print("s star : ", s_star)
    end = time.time() - begin
    print("delta pour le calcul final : ", end)
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
    return ([0, 1, 0, 0], [1, 1, 1, 1, 1, 1])


def getVoisins(state: Tuple[List[int], List[int]]):
    main_stations, satellites_stations = state
    neighbors = []

    for i in range(len(main_stations)):
        if not (main_stations.count(1) == 1 and main_stations[i] == 1):
            neighbor = (main_stations[:i] + [1 - main_stations[i]] + main_stations[i + 1:], satellites_stations)
            indices=[i for i in range(len(main_stations)) if neighbor[0][i] == 1 ]
            satellites = [random.choice(indices) for i in range (len(satellites_stations))]
            neighbor = (neighbor[0], satellites)
            neighbors.append(neighbor)
    
    # voisinage changer l'association d'une gare satellite
    # for j in range(len(satellites_stations)):
    #     for i in range(len(main_stations)):
    #         if main_stations[i] == 1:
    #             neighbor = (main_stations, satellites_stations[:j] + [i] + satellites_stations[j + 1:])
    #             neighbors.append(neighbor)
    
    return neighbors

    # Voisins = []
    # GaresOuvertes = state[0]
    # Satellites = state[1]
    # for i in range (len(GaresOuvertes)) :
    #     Voisins.append(state)
    #     # Modifier les gares ouvertes
    #     if GaresOuvertes[i] == 0 :
    #         Voisins[-1][0][i] == 1 # = pas == et same 2 lignes plus bas
    #     else :
    #         Voisins[-1][0][i] == 0
    # return Voisins

def validate(voisins: List[Tuple[List[int], List[int]]], current_cost: float, problem: UFLP):
    """neighbors_cost = [0 for i in range(len(voisins))]
    for i in range(len(voisins)):
        for j in range(problem.n_main_station):
            if voisins[i][0][j] == 1:
                neighbors_cost[i] += problem.main_stations_opening_cost[j]
            for k in range(problem.n_satellite_station):
                neighbors_cost[i] += problem.satellite_stations_connection_cost[j][k]
    
    valid_neighbors = []
    valid_neighbors_cost = []
    for i in range(len(voisins)):
        if neighbors_cost[i] <= current_cost:
            valid_neighbors.append(voisins[i])
            valid_neighbors_cost.append(neighbors_cost[i])
    return valid_neighbors, valid_neighbors_cost"""

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

    valid_neighbors = []
    valid_neighbors_cost = []
    for i in range(0, len(voisins)):
        if neighbours_main_station_cost[i] <= current_cost:
            valid_neighbors.append(voisins[i])
            valid_neighbors_cost.append(neighbours_main_station_cost[i])
    return valid_neighbors, valid_neighbors_cost

def select_Neighbor(voisins: List[Tuple[List[int], List[int]]], cost: List[int]):
    index = cost.index(min(cost))
    return voisins[index], cost[index]
