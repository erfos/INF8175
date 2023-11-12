import math
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
    limit_timestamp = 110 - 1
    begin = time.time()
    best_solution = solutionInitiale(problem)
    best_solution_cost = math.inf

    while time.time() - begin < limit_timestamp:
        s = solutionInitiale(problem)
            
        s_star = s
        s_star_cost = calculate_cost(problem, s_star)
        for k in range (2000):
            neighbors = getVoisins(s)
            validNeighbors, neighbors_cost = validate(neighbors, problem)
            if len(validNeighbors) == 0:
                break
            s, nextNeighbour_cost = select_Neighbor(validNeighbors, neighbors_cost)
            if (nextNeighbour_cost < s_star_cost):
                s_star = s
                s_star_cost = nextNeighbour_cost

        if best_solution_cost > s_star_cost:
            best_solution = s_star
            best_solution_cost = s_star_cost

    return best_solution

def solutionInitiale(problem: UFLP):
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
    
    return neighbors

def validate(voisins: List[Tuple[List[int], List[int]]], problem: UFLP):
    associated_neighbors = []
    associated_neighbors_cost = []
    for i in range(len(voisins)):
        right_neighbor = associate_satellite_to_main(problem, voisins[i])
        associated_neighbors.append(right_neighbor)
        associated_neighbors_cost.append(calculate_cost(problem, right_neighbor))
    return associated_neighbors, associated_neighbors_cost

def select_Neighbor(voisins: List[Tuple[List[int], List[int]]], cost: List[int]):
    index = cost.index(min(cost))
    return voisins[index], cost[index]

def associate_satellite_to_main(problem: UFLP, solution: Tuple[List[int], List[int]]):
    for j in range(problem.n_satellite_station):
        min_connection_cost = math.inf
        for i in range(problem.n_main_station):
            if solution[0][i] == 1:
                connection_cost = problem.satellite_stations_connection_cost[i][j]
                if connection_cost < min_connection_cost:
                    min_connection_cost = connection_cost
                    solution[1][j] = i
    
    return solution

def calculate_cost(problem: UFLP, solution: Tuple[List[int], List[int]]):
    cost = 0
    for i in range(problem.n_main_station):
        if solution[0][i] == 1:
            cost += problem.main_stations_opening_cost[i]
            for j in range(problem.n_satellite_station):
                if solution[1][j] == i: # station j connectée à la station i qui est ouverte
                    cost += problem.satellite_stations_connection_cost[i][j]
    
    return cost
