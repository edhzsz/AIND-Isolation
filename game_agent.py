"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from isolation import Board

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def get_cached_legal_moves(self, player=None):
    """
    Return the list of all legal moves for the specified player.

    Parameters
    ----------
    player : object (optional)
        An object registered as a player in the current game. If None,
        return the legal moves for the active player on the board.

    Returns
    ----------
    list<(int, int)>
        The list of coordinate pairs (row, column) of all legal moves
        for the player constrained by the current game state.
    """
    if not hasattr(self, 'moves_cache'):
        self.moves_cache = {}

    if player is None:
        player = self.active_player

    valid_moves = self.moves_cache.get(player, None)

    if valid_moves:
        return valid_moves

    valid_moves = self.__get_moves__(self.__last_player_move__[player])

    self.moves_cache[player] = valid_moves

    return valid_moves

def cached_apply_move(self, move):
    """
    Move the active player to a specified location.

    Parameters
    ----------
    move : (int, int)
        A coordinate pair (row, column) indicating the next position for
        the active player on the board.

    Returns
    ----------
    None
    """
    row, col = move
    self.__last_player_move__[self.active_player] = move
    self.__board_state__[row][col] = self.__player_symbols__[self.active_player]
    self.__active_player__, self.__inactive_player__ = self.__inactive_player__, self.__active_player__
    self.move_count += 1
    # clean the valid moves cache
    self.moves_cache = {}

Board.get_legal_moves = get_cached_legal_moves
Board.apply_move = cached_apply_move

def parametrized_moves_score(game, player, a, b, c):
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

    moves = game.get_legal_moves(player)
    opponent = game.get_opponent(player)
    opponent_moves = game.get_legal_moves(opponent)

    return  a * len(moves) + b * len(opponent_moves) + c

def common_moves_score(game, player):
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

    moves = set(game.get_legal_moves(player))

    opponent = game.get_opponent(player)
    opponent_moves = set(game.get_legal_moves(opponent))

    # intersection of common moves
    common_moves = moves & opponent_moves
    return len(common_moves)

def distance_score(game, player):
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

    opponent = game.get_opponent(player)

    location = game.get_player_location(player)
    opponent_location = game.get_player_location(opponent)

    # distance from players
    distance = (abs(location[0] - opponent_location[0])
                + abs(location[1] - opponent_location[1]))
    return distance

def generate_custom_score(a, b, c):
    def __score__(game, player):
        return parametrized_moves_score(game, player, a, b, c)

    return __score__

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
    return (
        parametrized_moves_score(game, player, 2, -3, 16)
        + distance_score(game, player)
        #+ common_moves_score(game, player)
        )

class CustomPlayer(object):
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
                 iterative=True, method='minimax', timeout=20., verbose=False):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.used_score_fn = False
        self.verbose = verbose

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
        score = 0.12345

        if not legal_moves:
            return move

        search_method = (self.minimax
                         if self.method == 'minimax'
                         else self.alphabeta)
        max_depth = (
            game.width * game.height if self.iterative
            else self.search_depth
            )
        start_depth = 1 if self.iterative else self.search_depth

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            depth = start_depth
            while depth <= max_depth:
                self.used_score_fn = False
                # reset the board score cache on each iteration as the score
                # will be updated with the values from the new depth
                score, move = search_method(game, depth)
                depth = depth + 1

                if not self.used_score_fn:
                    break

        except Timeout:
            pass

        # if move is invalid (i.e (-1, -1)) after timeout or not found good move
        # select randomly one of the legal moves
        if move == (-1, -1):
            move = legal_moves[random.randint(0, len(legal_moves) - 1)]
        
        # Return the best move from the last completed search iteration
        return move

    def minimax(self, game, depth, maximizing_player=True):
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

        best_score = float("-inf") if maximizing_player else float("inf")
        best_move = (-1, -1)

        legal_moves = game.get_legal_moves()

        if not legal_moves or depth == 0:
            return self.score(game, self), best_move

        for move in legal_moves:
            score, _ = self.minimax(
                game.forecast_move(move), depth - 1, not maximizing_player)

            if maximizing_player:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return (best_score, best_move)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"),
                  maximizing_player=True):
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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        best_score = float("-inf") if maximizing_player else float("inf")
        best_move = (-1, -1)

        # if alpha or beta are maxed up, just give up early
        if maximizing_player and beta == float("-inf"):
            return (best_score, best_move)

        if not maximizing_player and alpha == float("inf"):
            return (best_score, best_move)

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return self.score(game, self), best_move

        if depth == 0:
            self.used_score_fn = True
            return self.score(game, self), best_move

        for move in legal_moves:
            branch_score, _ = self.alphabeta(
                game.forecast_move(move), depth - 1, alpha, beta, not maximizing_player)

            if maximizing_player:
                if branch_score > best_score:
                    best_score = branch_score
                    best_move = move

                if best_score >= beta:
                    break

                alpha = max(alpha, best_score)
            else:
                if branch_score < best_score:
                    best_score = branch_score
                    best_move = move

                if best_score <= alpha:
                    break

                beta = min(beta, best_score)

        return best_score, best_move


