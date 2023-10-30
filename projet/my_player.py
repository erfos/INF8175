import math
from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError


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


    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        return self.h_alphabeta_search(current_state)
        raise MethodNotImplementedError()

    def cutoff_depth(self,depth,d):
        """A cutoff function that searches to depth d."""
        return depth > d

    def heuristic(current_state):
        dico = dict()
        players = current_state.players
        dico[players[0].get_id()] = 0
        dico[players[1].get_id()] = 0
        return dico

    def h_alphabeta_search(self, current_state, h=heuristic):
        """Search game to determine best action; use alpha-beta pruning.
        As in [Figure 5.7], this version searches all the way to the leaves."""

        infinity = math.inf
        player = current_state.get_next_player()
        print(player.get_id())
       
        def max_value(current_state, alpha, beta,depth):
            print("depth max =", depth)
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            print('on peut entrer dans le cutoff max ? ', self.cutoff_depth(depth, 4))
            if self.cutoff_depth(depth, 4):
                print("DANS LE CUTOFF DU MAX VALUE")
                return h(current_state), None
            v, move = -infinity, None
            v_dict = dict()
            for a in current_state.generate_possible_actions():
                print("DANS LA BOUCLE FOR MAX VALUE")
                v2, _ = min_value(a.get_next_game_state(), alpha, beta, depth+1)  
                #v_dict=v2
                print("v2 dans max value =",v2)
                score = v2[player.get_id()]
                if score > v:
                    print("Cas score > v dans max value : ")
                    v, move = score, a
                    v_dict = v2
                    alpha = max(alpha, score)
                if v >= beta:
                    print( "Cas v >= beta : dans max value")
                    return v_dict, move
            return v_dict, move

        def min_value(current_state, alpha, beta,depth):
            print("depth min =", depth)
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            print('on peut entrer dans le cutoff min ? ', self.cutoff_depth(depth, 4))
            if self.cutoff_depth(depth,4):
                print("DANS LE CUTOFF DU MIN VALUE")
                print("resultat de h : ", h(current_state))
                return h(current_state), None
            v, move = +infinity, None
            v_dict = dict()
            for a in current_state.generate_possible_actions():
                print("DANS LA BOUCLE FOR MIN VALUE")
                v2,_ = max_value(a.get_next_game_state(), alpha, beta, depth+1)
                score = v2[player.get_id()]
                if score < v:
                    print("Cas score < v dans min : ")
                    v, move = score, a
                    v_dict = v2
                    beta = min(beta, v)
                if v <= alpha:
                    print( "Cas v <= alpha dans min : ")
                    return v_dict, move
            return v_dict, move

        return max_value(current_state, -infinity, +infinity, 0)
        

    def alphabeta_search(self, current_state):
        """Search game to determine best action; use alpha-beta pruning.
        As in [Figure 5.7], this version searches all the way to the leaves."""

        infinity = math.inf
        player = current_state.get_next_player()
        
        def max_value(current_state, alpha, beta):
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            v, move = -infinity, None
            v_dict = dict()
            for a in current_state.generate_possible_actions():
                v2, _ = min_value(a.get_next_game_state(), alpha, beta)  
                #v_dict=v2
                score=v2[player.get_id()] 
                print(min_value(a.get_next_game_state(), alpha, beta) )
                print("v2=",v2)
                print("v=",v)
                if score > v:
                    v, move = score, a
                    v_dict=v2
                    alpha = max(alpha, score)
                if v >= beta:
                    return v_dict, move
            return v_dict, move

        def min_value(current_state, alpha, beta):
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            v, move = +infinity, None
            v_dict=dict()
            for a in current_state.generate_possible_actions():
                v2,_ = max_value(a.get_next_game_state(), alpha, beta)
                score=v2[player.get_id()]
                if score < v:
                    v, move = score, a
                    v_dict=v2
                    beta = min(beta, v)
                if v <= alpha:
                    return v_dict, move
            return v_dict, move

        return max_value(current_state, -infinity, +infinity)