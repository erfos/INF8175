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
        self.h_alphabeta_search(current_state)
        raise MethodNotImplementedError()

    def cutoff_depth(self,depth,d):
        """A cutoff function that searches to depth d."""
        return depth > d

    def h_alphabeta_search(self, current_state, h=lambda s, p: 0):
        """Search game to determine best action; use alpha-beta pruning.
        As in [Figure 5.7], this version searches all the way to the leaves."""

        infinity = math.inf
        player = current_state.get_next_player()
        print(player.get_id())
        
        def max_value(current_state, alpha, beta,depth):
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            print(self.cutoff_depth(depth,20))
            if self.cutoff_depth(depth,20):
                print("ici")
                return 4,None
            v, move = -infinity, None
            v_dict = dict()
            for a in current_state.generate_possible_actions():
                print(min_value(a.get_next_game_state(), alpha, beta,depth+1))
                v2, _ = min_value(a.get_next_game_state(), alpha, beta,depth+1)  
                #v_dict=v2
                score=v2[player.get_id()] 
                print("v2=",v2)
                print("v=",v)
                if score > v:
                    v, move = score, a
                    v_dict=v2
                    alpha = max(alpha, score)
                if v >= beta:
                    return v_dict, move
            return v_dict, move

        def min_value(current_state, alpha, beta,depth):
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            if self.cutoff_depth(depth,20):
                return 4,None # il faut retourner un dictionaire 
            v, move = +infinity, None
            v_dict=dict()
            for a in current_state.generate_possible_actions():
                v2,_ = max_value(a.get_next_game_state(), alpha, beta,depth+1)
                score=v2[player.get_id()]
                if score < v:
                    v, move = score, a
                    v_dict=v2
                    beta = min(beta, v)
                if v <= alpha:
                    return v_dict, move
            return v_dict, move

        return max_value(current_state, -infinity, +infinity,0)
        

    def alphabeta_search(self, current_state):
        """Search game to determine best action; use alpha-beta pruning.
        As in [Figure 5.7], this version searches all the way to the leaves."""

        infinity = math.inf
        player = current_state.get_next_player()
        print(player.get_id())
        
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