"""
    Thaïs Genisson (2315046)
    Erika Fossouo (1943831)
"""
import math
from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError
from typing import Tuple #Any, List,


class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float=60*15,*args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type,name,time_limit,*args)
        self.opponent_piece_type = 'W' if piece_type == 'B' else 'B'


    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        print("les scores : ", current_state.scores)
        # player = current_state.get_next_player()
        score_avant = self.center_control_heuristic(current_state)
        # current_state.convert_light_action_to_action(data={'from':(6,2),'to':(7,3)})
        # score_apres = self.center_control_heuristic(current_state)
        # print("le score avant : ", score_avant)
        # print("le score apres : ", score_apres)



        # print("piece : ", current_state.get_rep().get_pieces_player(player)[1])
        # print("type des coordonnes : ", type(current_state.get_rep().get_pieces_player(player)[1][0]))
        # print("dimension du plateau : ", current_state.rep.dimensions)
        # for x in current_state.get_rep().get_grid():
        #     print(*x)
        # for a,b in current_state.get_rep().env.items():
        #     print(a,b.__dict__)
        print("on joue avec : ", self.get_piece_type())
        print("l'adversaire joue avec : ", self.opponent_piece_type)

        print("score avant : ", score_avant)
        result = self.h_alphabeta_search(current_state)
        # score_apres = self.center_control_heuristic(result[1].get_next_game_state())
        # print("score apres : ", score_apres)
        print("result : ", result[0])
        print("move : ", result[1])
        return result[1]
        # return self.h_alphabeta_search(current_state)
        raise MethodNotImplementedError()

    def cutoff_depth(self, depth, d):
        """A cutoff function that searches to depth d."""
        return depth > d

    # TODO: le contenu plusieurs heuristique fait une boucle sur les pièce.
    # Pour économiser du temps, on peut mélanger tout ça dans la même boucle
    # for piece in player_pieces:
    #     fonction pour le centre
    #     fonction pour les bords
    #     etc ..
    # Ce ne serait pas les fonction tel quel, ce serait le contenu des boucles
    # for de chaque fonction (vérifier la logique quand même)
    def heuristic(self, action):
        # previous_state = action.get_current_game_state()
        current_state = action.get_next_game_state()
        score = 0
        score += self.center_control_heuristic(current_state)
        score += self.border_control_heuristic(current_state)
        score += self.avoid_encirclement_heuristic(current_state)
        score += self.isolation_heuristic(current_state)

        dico = dict()
        players = current_state.players
        dico[players[0].get_id()] = 0
        dico[players[1].get_id()] = 0
        dico[self.get_id()] = score

        # EST CE QUE JE DOIS TOUCHER AU SCORE ? LE RESULTAT DE L HEURISTIQUE VA OÙ ?
        return dico
    
    def h_alphabeta_search(self, state: GameState):
        """Search game to determine best action; use alpha-beta pruning."""

        infinity = math.inf
        # player = current_state.get_next_player()
        # print("id du joueur : ", player.get_id())
        print("id du joueur : ", self.get_id())
       
        def max_value(action: Action, alpha, beta, depth):
            current_state = action.get_next_game_state()
            if current_state.is_done():
                # TODO: revoir ce qu'on fait si on arrive à un état final
                # Je pense que puisque l'état final indique la fin du jeu,
                # on peut vraiment savoir qui a gagné et pas estimer.
                # Donc on pourrait voir qui a le plus de pions.
                return current_state.scores, None
                # return current_state.compute_scores(self.get_id()), None
            if self.cutoff_depth(depth, 3):
                return self.heuristic(action), None
            v, move = -infinity, None
            v_dict = dict()
            n_actions = current_state.generate_possible_actions()
            for a in n_actions:
                if self.action_removing_pieces(a) == False:
                    v2, _ = min_value(a, alpha, beta, depth+1)
                    score = v2[self.get_id()]
                    if score > v:
                        v, move = score, a
                        v_dict = v2
                        alpha = max(alpha, score)
                    if v >= beta:
                        return v_dict, move
                # else:
                #     print("des pions sont retirés (MAX)")
                #     # print("l'action en question : ", a)
            return v_dict, move

        def min_value(action: Action, alpha, beta, depth):
            current_state = action.get_next_game_state()
            if current_state.is_done():
                # TODO: see max value
                return current_state.scores, None
                # return current_state.compute_scores(self.get_id()), None
            if self.cutoff_depth(depth, 3):
                return self.heuristic(action), None
            v, move = +infinity, None
            v_dict = dict()
            n_actions = current_state.generate_possible_actions()
            for a in n_actions:
                if self.action_removing_pieces(a) == False:
                    v2,_ = max_value(a, alpha, beta, depth+1)
                    score = v2[self.get_id()]
                    if score < v:
                        v, move = score, a
                        v_dict = v2
                        beta = min(beta, v)
                    if v <= alpha:
                        return v_dict, move
                # else:
                #     print("des pions sont retirés (MIN)")
                #     # print("l'action en question : ", a)
            return v_dict, move

        # Action avec les mêmes états juste pour avoir les deux états dans le minimax
        action = Action(state, state)
        return max_value(action, -infinity, +infinity, 0)
    
    # si on élimine l'adversaire c est parfait
    def elimination_heuristic(self, current_state: GameState) -> float:
        players = current_state.players
        pieces_number_player_1 = current_state.get_rep().get_pieces_player(players[0])[0]
        pieces_number_player_2 = current_state.get_rep().get_pieces_player(players[1])[0]

        elimination_score = 0
        if self.get_id() == players[0].get_id():
            elimination_score = pieces_number_player_1 - pieces_number_player_2
        else:
            elimination_score = pieces_number_player_2 - pieces_number_player_1
        return float(elimination_score)
    
    def isolation_heuristic(self, current_state: GameState) -> float:
        player_pieces = current_state.get_rep().get_pieces_player(self)[1]
        isolation_score = 0

        for piece in player_pieces:
            # Récupérer les positions voisines du pion
            neighbors = current_state.get_rep().get_neighbours(piece[0], piece[1])
            empty_neighbor = sum(1 for neighbor_type, _ in neighbors.values() if neighbor_type == "EMPTY")
            # plus de 2 cases vides, il est surement isolé
            if empty_neighbor > 2:
                isolation_score -= 0.1

        return isolation_score

    def avoid_encirclement_heuristic(self, current_state: GameState) -> float:
        player_pieces = current_state.get_rep().get_pieces_player(self)[1]
        encirclement_score = 0
        # neighbour = current_state.get_rep().get_neighbours(player_pieces[0][0], player_pieces[0][1])
        # print("neighbour : ", neighbour.values())

        for piece in player_pieces:
            neighbors = current_state.get_rep().get_neighbours(piece[0], piece[1])
            opponent_neighbors = sum(0.1 for neighbor_type, _ in neighbors.values() if neighbor_type == self.opponent_piece_type)
            encirclement_score -= opponent_neighbors + 0.1  # Diminuer le score en cas de voisin mais pas s'il n y en a qu'un

        return encirclement_score

    def action_removing_pieces(self, action: Action) -> bool:
        previous_state = action.get_current_game_state()
        current_state = action.get_next_game_state()
        # player = current_state.get_next_player()
        # print("player id dans action removing pieces : ", player.get_id())
        # print("avec self : ", self.get_id())

        pieces_number_before = previous_state.get_rep().get_pieces_player(self)[0]
        pieces_number_after = current_state.get_rep().get_pieces_player(self)[0]
        # print("nombre pieces avant : ", pieces_number_before)
        # print("nombre pieces apres : ", pieces_number_after)

        # print("pieces : ", current_state.get_rep().get_pieces_player(player)[1])
        # grid = current_state.get_rep().get_grid()
        
        # print("plateau : ", current_state.get_rep().env)

        # piece = current_state.get_rep().get_pieces_player(player)[1][0]
        # print("piece en hexa : ", piece)
        # print('piece en grid : ', grid_piece)

        # print("nous jouons avec les pions : ", self.piece_type)

        return pieces_number_after < pieces_number_before
    
    def border_control_heuristic(self, current_state: GameState) -> float:
        borders = [(0, 4), (1, 5), (2, 6), (3, 7),
                   (4, 8), (6, 8), (8, 8), (10, 8),
                   (12, 8), (13, 7), (14, 6), (15, 5),
                   (16, 4), (15, 3), (14, 2), (13, 1),
                   (12, 0), (10, 0), (8, 0), (6, 0),
                   (4, 0), (3, 1), (2, 2), (1, 3)
                   ]
        # Je ne peux pas vraiment utiliser ça comme ça parce que l'état initial a un score
        # de 0 donc dès que je vais appliquer ça, n'importe quel autre état sera pire
        # Mais combiner avec l heuristique de controle de centre, est ce que ça équilibre
        penalty = 0
        player_pieces = current_state.get_rep().get_pieces_player(self)[1]
        for piece in player_pieces:
            if piece in borders:
                penalty -= 0.1 # TODO: revoir les valeurs
        return penalty

    def center_control_heuristic(self, current_state: GameState) -> float:
        #TODO: les dimensions en attributs, en constante ou en parametre ? or just keep it like this
        center = (8, 4)
        # max_distance = 4
        max_gain = 1 #TODO: à ajuster
        # la variation = max_gain / max distance
        variation = -0.25 #TODO: à ajuster

        player_pieces = current_state.get_rep().get_pieces_player(self)[1]

        bonus = 0
        # la distance maximale au centre vaut 4
        for piece in player_pieces:
            distance = self.manhattan_distance(center, piece)
            gain = variation * distance + max_gain
            bonus += gain
        return bonus
    
    def manhattan_distance(self, position1: Tuple[int, int], position2: Tuple[int, int]) -> int:
        """
            pour aller de (3,1) à (8, 4) ou de (13, 3) à (8, 4) c est bon mais par exemple,
            de (3,1) à (2, 4), ma logique ne fonctionne pas (ou plutôt ce n est pas le chemin le plus court)
            de (5, 1) à (8, 4) non plus d ailleurs. de (3, 1) à (4, 2) non plus ..
            Bon, il me faut une autre methode
        """
        # x = 0 # dist absolue divisé par deux, floor
        # y = abs(position1[1] - position2[1])

        """Bon, ça a l air de fonctionner"""
        # distance = 0
        # la même position
        if position1 == position2:
            distance = 0
        # sur la même colonne
        elif position1[1] == position2[1]:
            distance = abs(position1[0] - position2[0]) / 2
        # sur la même ligne
        elif position1[0] == position2[0]:
            distance = abs(position1[1] - position2[1])
        # sur la même diagonale
        elif abs(position1[0] - position2[0]) == abs(position1[1] - position2[1]):
            distance = abs(position1[0] - position2[0])
        # ex : (10, 2) ou (10. 0) et (7, 7)
        else:
            distance = abs(position1[1] - position2[1])
        
        return distance
 
"""
TODO: heurisctic
    HEURISTIQUES DÉJÀ IMPLÉMENTÉES ET INCORPORÉES:
    - Conservation des billes : Encouragez la conservation des billes en pénalisant les mouvements qui pourraient
    rendre une bille vulnérable. (DONE -> action_removing_pieces)

    - Contrôle du centre du plateau : Les billes au centre du plateau peuvent être plus stratégiques.
    Vous pourriez attribuer un bonus pour les billes situées au centre. (DONE -> center_control_heuristic)

    - Contrôle des bords : Les billes près des bords peuvent être plus vulnérables. Vous pourriez attribuer
    des pénalités pour les billes près des bords. (DONE -> border_control_heuristic)
    (Ajouter à l'heuristique "controle du centre du plateau ?")

    - Éviter encerclement : Éviter de se faire encercler par l'adversaire. (DONE -> avoid_encirclement_heuristic)
    (faire attention à ce que ça n'empêche pas d'aller vers l'adversaire pour le pousser)

    - l'isolation des pions (better s'il sont regroupés) (idée perso) (DONE -> isolation_heuristic)
    (À FAIRE, ça à l'air important/intéressant et faisable)
    

    HEURISTIQUES IMPLÉMENTÉES MAIS PAS INCORPORÉES:
    - Évaluation simple de la position : Considérez le nombre de billes ou de groupes de billes pour chaque joueur.
    Un joueur avec plus de billes sur le plateau peut être dans une position plus forte. (DONE -> elimination_heuristic)
    (simple à faire mais efficace une fois que d'autres heuristiques nous permettront de nous retrouver
    plus facilement dans cette situation)

    

    LE RESTE:
    - Mobilité : Plus un joueur a d'options de déplacement, mieux c'est. Vous pourriez évaluer la mobilité
    en comptant le nombre de déplacements légaux possibles pour chaque joueur.
    (oui mais et la qualité des déplacements ? Peut être accorder un mini bonus pour ça)    

    - Évaluation de la stabilité : Évaluez la stabilité des groupes de billes. Un groupe stable est moins
    susceptible d'être poussé par l'adversaire. (ça a l'air d'aller avec isolation comme center_control va avec border_control)
    (À FAIRE, ça à l'air faisable, logique et intéressant)

    - Encerclement (encercler l'autre) : Considérez si un joueur peut encercler les billes de l'adversaire. Cela peut être une position forte.
    (ça n'a pas l''air trivial)

    - Stratégie offensive/défensive : L'algorithme pourrait encourager des stratégies plus offensives ou défensives
    en fonction de la phase du jeu.
    (on dirait un peu l'idée des tables donc on va laisser faire pour l'instant)

    - Évaluation dynamique : L'heuristique pourrait être dynamique et changer en fonction de la phase du jeu.
    Par exemple, en début de partie, la mobilité peut être plus importante.
    (rejoint aussi l'idée des tables mais peut être implémenté plus facilement. Par exemple, dependemment de la phase
    du jeu, changer la pondération accordé à chaque heuristique)

    - Adaptation à l'adversaire : Apprenez du style de jeu de l'adversaire et ajustez l'heuristique en conséquence.
    (on va laisser ça aux experts de Slack la)

    - une heuristique qui évite les états où il y a plus de pions adverses sur la même diagonale (idée perso) (si on a moins de
    3 pions sur une diagonale il ne faut pas que l'adversaire en ai plus sinon il peut nous pousser)
"""