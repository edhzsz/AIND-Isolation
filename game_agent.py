"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def null_score(game, player):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return 0.


def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


def improved_score(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    return improved_score(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=15., use_cache=False):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.board_representations_cache = {}
        self.board_score_cache = {}
        self.use_cache = use_cache

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        move = (-1, -1)
        search_method = (self.minimax
                         if self.method == 'minimax'
                         else self.alphabeta)
        max_depth = 10000 if self.iterative else self.search_depth
        start_depth = 0 if self.iterative else self.search_depth

        if not legal_moves:
            return move

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            depth = start_depth
            while depth <= max_depth:
                # reset the board score cache on each iteration as the score
                # will be updated with the values from the new depth
                self.board_score_cache = {}
                _, move = search_method(game, depth, first_call=True, original_depth=depth)
                depth = depth + 1

        except Timeout:
            # if move is invalid (i.e (-1, -1)) after timeout select randomly
            #  one of the legal moves
            if move == (-1, -1):
                move = legal_moves[random.randint(0, len(legal_moves) - 1)]

        # Return the best move from the last completed search iteration
        return move

    def __get_proyections__(self, game):
        row_proyection = [game.height for i in range(game.width)]
        col_proyection = [game.width for i in range(game.height)]

        for clean_pos in game.get_blank_spaces():
            cp_r, cp_c = clean_pos
            row_proyection[cp_c] -= 1
            col_proyection[cp_r] -= 1

        if game.get_player_location(self):
            p1_r, p1_c = game.get_player_location(self)
            col_proyection[p1_r] += 99
            row_proyection[p1_c] += 99

        if game.get_player_location(game.get_opponent(self)):
            p2_r, p2_c = game.get_player_location(game.get_opponent(self))
            row_proyection[p2_c] += 199
            col_proyection[p2_r] += 199

        return row_proyection, col_proyection

    def __get_representations__(self, game, maximizing_player):
        cache_key = (game)
        if self.board_representations_cache.get(cache_key):
            return self.board_representations_cache.get(cache_key)

        sufix = "#1" if maximizing_player else "#2"
        r_proyection, c_proyection = self.__get_proyections__(game)

        sr_proyection = ','.join(str(x) for x in r_proyection)
        sc_proyection = ','.join(str(x) for x in c_proyection)
        srr_proyection = ','.join(str(x) for x in reversed(r_proyection))
        src_proyection = ','.join(str(x) for x in reversed(c_proyection))

        representations = [
            sr_proyection + '#' + sc_proyection + sufix#,
            #sc_proyection + '#' + sr_proyection + sufix,
            #sr_proyection + '#' + src_proyection + sufix,
            #src_proyection + '#' + sr_proyection + sufix,
            #srr_proyection + '#' + sc_proyection + sufix,
            #sc_proyection + '#' + srr_proyection + sufix,
            #srr_proyection + '#' + src_proyection + sufix,
            #src_proyection + '#' + srr_proyection + sufix
            ]

        self.board_representations_cache[cache_key] = representations

        return representations

    def __get_cached_score__(self, game, maximizing_player, print_hit=False):
        representations = self.__get_representations__(game, maximizing_player)
        main_rep = representations[0]

        for rep in representations:
            if self.board_score_cache.get(rep, False) != False:
                c_score, c_move = self.board_score_cache.get(rep)
                if print_hit:
                    print(main_rep, rep, c_score, c_move)
                return True, c_score, c_move, main_rep

        return False, 0, (-1, -1), main_rep

    def minimax(self, game, depth, maximizing_player=True, first_call=False, original_depth=0):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if self.use_cache:
            found, c_score, c_move, move_rep = self.__get_cached_score__(game, maximizing_player)

            if found:
                return c_score, c_move

        best_score = float("-inf") if maximizing_player else float("inf")
        best_move = (-1, -1)

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return game.utility(game.active_player), best_move

        if depth == 0:
            return self.score(game, self), best_move

        aggregate_fn = max if maximizing_player else min

        for move in legal_moves:
            score, _ = self.minimax(
                game.forecast_move(move), depth - 1, not maximizing_player)

            if score != best_score and score == aggregate_fn(score, best_score):
                best_score = score
                best_move = move

        if self.use_cache:
            # cache the score for this branch
            self.board_score_cache[move_rep] = (best_score, best_move)

        return (best_score, best_move)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"),
                  maximizing_player=True, first_call=False, original_depth=0):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        cache_score, cache_mov = None, None
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if self.use_cache:
            found, c_score, c_move, board_rep = self.__get_cached_score__(game, maximizing_player)

            if found:
                #return c_score, c_move
                cache_score, cache_mov = c_score, c_move

        best_score = float("-inf") if maximizing_player else float("inf")
        best_move = (-1, -1)

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return game.utility(game.active_player), best_move

        if depth == 0:
            return self.score(game, self), best_move

        for move in legal_moves:
            branch_score, _ = self.alphabeta(
                game.forecast_move(move), depth - 1, alpha, beta, not maximizing_player, original_depth=original_depth)

            if maximizing_player:
                if branch_score > best_score:
                    best_score = branch_score
                    best_move = move

                if best_score >= beta:
                    return (best_score, best_move)

                alpha = max(alpha, best_score)
            else:
                if branch_score < best_score:
                    best_score = branch_score
                    best_move = move

                if best_score <= alpha:
                    return (best_score, best_move)

                beta = min(beta, best_score)

        if self.use_cache:
            if cache_score != None:
                if cache_score != best_score:
                    print ("--------------------------")
                    print("Failed cache for {} with cached score {} and actual score {}".format(board_rep, cache_score, best_score))
                    print(game.print_board())
                    print("cached move: {}".format(cache_mov))
                    print("best move: {}".format(best_move))
                    self.__get_cached_score__(game, maximizing_player, True)
                    print(depth, len(self.board_score_cache), original_depth)

            # cache the score for this branch
            self.board_score_cache[board_rep] = (best_score, best_move)


        return best_score, best_move
