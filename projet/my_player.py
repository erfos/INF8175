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
        result = self.h_alphabeta_search(current_state)
        print("move : ", result[1])
        return result[1]
        # return self.h_alphabeta_search(current_state)
        raise MethodNotImplementedError()

    def cutoff_depth(self,depth,d):
        """A cutoff function that searches to depth d."""
        return depth > d

    def heuristic(action):
        # previous_state = action.get_current_game_state()
        current_state = action.get_next_game_state()
        # player = current_state.get_next_player()

        # pieces_number_before = previous_state.get_rep().get_pieces_player(player)
        # pieces_number_after = current_state.get_rep().get_pieces_player(player)

        dico = dict()
        players = current_state.players
        dico[players[0].get_id()] = 0
        dico[players[1].get_id()] = 0

        # if pieces_number_after < pieces_number_before:
        #     dico[player.get_id()] = -1

        return dico
    
    def h_alphabeta_search(self, current_state, h=heuristic):
        """Search game to determine best action; use alpha-beta pruning.
        As in [Figure 5.7], this version searches all the way to the leaves."""

        # TODO : retirer les actions qui retirent un pion

        infinity = math.inf
        player = current_state.get_next_player()
        print("id du joueur : ",player.get_id())
       
        def max_value(action, alpha, beta,depth):
            current_state = action.get_next_game_state()
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            # print('on peut entrer dans le cutoff max ? ', self.cutoff_depth(depth, 4))
            if self.cutoff_depth(depth, 4):
                # print("DANS LE CUTOFF DU MAX VALUE")
                return h(action), None
            v, move = -infinity, None
            v_dict = dict()
            n_actions = current_state.generate_possible_actions()
            for a in n_actions:
                if not self.action_removing_pieces(a):
                    v2, _ = min_value(a, alpha, beta, depth+1)
                    score = v2[player.get_id()]
                    if score > v:
                        v, move = score, a
                        v_dict = v2
                        alpha = max(alpha, score)
                    if v >= beta:
                        return v_dict, move
            return v_dict, move

        def min_value(action, alpha, beta,depth):
            current_state = action.get_next_game_state()
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            if self.cutoff_depth(depth,4):
                # print("DANS LE CUTOFF DU MIN VALUE")
                # print("resultat de h : ", h(current_state))
                return h(action), None
            v, move = +infinity, None
            v_dict = dict()
            n_actions = current_state.generate_possible_actions()
            for a in n_actions:
                if  not self.action_removing_pieces(a):
                    v2,_ = max_value(a, alpha, beta, depth+1)
                    score = v2[player.get_id()]
                    if score < v:
                        v, move = score, a
                        v_dict = v2
                        beta = min(beta, v)
                    if v <= alpha:
                        return v_dict, move
            return v_dict, move

        # Action avec les mêmes états juste pour avoir les deux états dans le minimax
        action = Action(current_state, current_state)
        return max_value(action, -infinity, +infinity, 0)

    def action_removing_pieces(self, action) -> bool:
        previous_state = action.get_current_game_state()
        current_state = action.get_next_game_state()
        player = current_state.get_next_player()

        pieces_number_before = previous_state.get_rep().get_pieces_player(player)[0]
        pieces_number_after = current_state.get_rep().get_pieces_player(player)[0]

        # print("pieces : ", current_state.get_rep().get_pieces_player(player)[1])
        # grid = current_state.get_rep().get_grid()
        # print("grid : ", grid)
        piece = current_state.get_rep().get_pieces_player(player)[1][0]
        grid_piece = current_state.get_rep().get_env().get(piece)
        print("piece en hexa : ", piece)
        print('piece en grid : ', grid_piece)

        return pieces_number_after < pieces_number_before


    # def h_alphabeta_search(self, current_state, h=heuristic):
        """Search game to determine best action; use alpha-beta pruning.
        As in [Figure 5.7], this version searches all the way to the leaves."""
"""
        # TODO : retirer les actions qui retirent un pion

        infinity = math.inf
        player = current_state.get_next_player()
        print("id du joueur : ",player.get_id())
       
        def max_value(current_state, alpha, beta,depth):
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            # print('on peut entrer dans le cutoff max ? ', self.cutoff_depth(depth, 4))
            if self.cutoff_depth(depth, 4):
                # print("DANS LE CUTOFF DU MAX VALUE")
                return h(current_state), None
            v, move = -infinity, None
            v_dict = dict()
            n_actions = current_state.generate_possible_actions()
            for a in n_actions:
                v2, _ = min_value(a.get_next_game_state(), alpha, beta, depth+1)
                score = v2[player.get_id()]
                if score > v:
                    v, move = score, a
                    v_dict = v2
                    alpha = max(alpha, score)
                if v >= beta:
                    return v_dict, move
            return v_dict, move

        def min_value(current_state, alpha, beta,depth):
            if current_state.is_done():
                return current_state.compute_scores(player.get_id()), None
            if self.cutoff_depth(depth,4):
                # print("DANS LE CUTOFF DU MIN VALUE")
                # print("resultat de h : ", h(current_state))
                return h(current_state), None
            v, move = +infinity, None
            v_dict = dict()
            n_actions = current_state.generate_possible_actions()
            for a in n_actions:
                v2,_ = max_value(a.get_next_game_state(), alpha, beta, depth+1)
                score = v2[player.get_id()]
                if score < v:
                    v, move = score, a
                    v_dict = v2
                    beta = min(beta, v)
                if v <= alpha:
                    return v_dict, move
            return v_dict, move

        # Action avec les mêmes états juste pour avoir les deux états dans le minimax
        action = Action(current_state, current_state)
        return max_value(current_state, -infinity, +infinity, 0)
"""        

    # def alphabeta_search(self, current_state):
    #     """Search game to determine best action; use alpha-beta pruning.
    #     As in [Figure 5.7], this version searches all the way to the leaves."""

    #     infinity = math.inf
    #     player = current_state.get_next_player()
        
    #     def max_value(current_state, alpha, beta):
    #         if current_state.is_done():
    #             return current_state.compute_scores(player.get_id()), None
    #         v, move = -infinity, None
    #         v_dict = dict()
    #         for a in current_state.generate_possible_actions():
    #             v2, _ = min_value(a.get_next_game_state(), alpha, beta)  
    #             #v_dict=v2
    #             score=v2[player.get_id()] 
    #             print(min_value(a.get_next_game_state(), alpha, beta) )
    #             print("v2=",v2)
    #             print("v=",v)
    #             if score > v:
    #                 v, move = score, a
    #                 v_dict=v2
    #                 alpha = max(alpha, score)
    #             if v >= beta:
    #                 return v_dict, move
    #         return v_dict, move

    #     def min_value(current_state, alpha, beta):
    #         if current_state.is_done():
    #             return current_state.compute_scores(player.get_id()), None
    #         v, move = +infinity, None
    #         v_dict=dict()
    #         for a in current_state.generate_possible_actions():
    #             v2,_ = max_value(a.get_next_game_state(), alpha, beta)
    #             score=v2[player.get_id()]
    #             if score < v:
    #                 v, move = score, a
    #                 v_dict=v2
    #                 beta = min(beta, v)
    #             if v <= alpha:
    #                 return v_dict, move
    #         return v_dict, move

    #     return max_value(current_state, -infinity, +infinity)
    

