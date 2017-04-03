# Heuristic Analysis

## Objective

The objective of this work is to generate, implement, analyze, and compare
three custom heuristic functions used to calculate the value of an _Isolation_
board. These functions are compared against the _Improved_ heuristic while being
executed by an agent using the _Iterative deepening_ search algorithm. This agent
is called the __ID_Improved__ agent.

Both agents are excuted in a tournament against other three agents each of them
using a different search algorithm and with three different heuristic functions:

- **Random agent**: It is an agent that choses randomly. This agent is not executed
with any herustic function (as it does not uses any).
- **Minimax Agent (MM)**: It is an agent that implements a fixed-depth minimax search algorithm.
- **Alpha-Beta agent (AB)**: It is an agent that implements the fixed-depth Alpha-Beta pruning
search algorithm.

The __AB__ and __MM__ agents are evaluated with three different heuristics:

- **Null heuristic**: This heuristic presumes no knowledge for non-terminal states,
and returns the same uninformative value for all other states.
- **Open move heuristic**: This heuristic implements the basic evaluation function
described in lecture that outputs a score equal to the number of available moves
for the player.
- **Improved heuristic**: This heuristic calculates the difference of available
moves between the two players.

The tournament estimates the strength rating of the student-agent with iterative
deepening and a custom heuristic evaluation function against the __AB__ and __MM__
test agents by running a round-robin tournament.

The _student agent_ and the *ID_Improved* agents play 20 "fair" matches against
each test agent. The matches are fair because, for each match, the board is
initialized randomly for both players, and the players play each match twice --
switching the player order between games. This helps to correct for imbalances
in the game due to both starting position and initiative.

The results for the *ID_Improved* agent were pretty stable on the computer used
to exeuted the tournaments. An example of a tipical result is the following:

Playing Matches:
----------
  Match 1: ID_Improved vs   Random      Result: 40 to 0
  Match 2: ID_Improved vs   MM_Null     Result: 38 to 2
  Match 3: ID_Improved vs   MM_Open     Result: 30 to 10
  Match 4: ID_Improved vs MM_Improved   Result: 25 to 15
  Match 5: ID_Improved vs   AB_Null     Result: 31 to 9
  Match 6: ID_Improved vs   AB_Open     Result: 28 to 12
  Match 7: ID_Improved vs AB_Improved   Result: 26 to 14
ID_Improved         77.86%

This agent played in total 4200 games and won 3257 of them giving it a total
score of 77.54%

## Heuristics Analyzed


### Available moves in common

This heuristic function calculates the size of the intersection of the sets of
open moves of each player. The board score is positive if the active player
is the current player and negative otherwise.

The rationale behind this heuristic is that the moves in common are the moves
were the active agent can close options for the opponent possibly creating a
partition. Thus, when the active player is our agent the score is positive
meaning that from this board some good moves can be possible done and viceversa.

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 35 to 5
  Match 2:   Student   vs   MM_Null     Result: 27 to 13
  Match 3:   Student   vs   MM_Open     Result: 15 to 25
  Match 4:   Student   vs MM_Improved   Result: 18 to 22
  Match 5:   Student   vs   AB_Null     Result: 26 to 14
  Match 6:   Student   vs   AB_Open     Result: 23 to 17
  Match 7:   Student   vs AB_Improved   Result: 17 to 23
Student             57.50%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 36 to 4
  Match 2:   Student   vs   MM_Null     Result: 27 to 13
  Match 3:   Student   vs   MM_Open     Result: 19 to 21
  Match 4:   Student   vs MM_Improved   Result: 17 to 23
  Match 5:   Student   vs   AB_Null     Result: 22 to 18
  Match 6:   Student   vs   AB_Open     Result: 20 to 20
  Match 7:   Student   vs AB_Improved   Result: 17 to 23
Student             56.43%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 31 to 9
  Match 2:   Student   vs   MM_Null     Result: 26 to 14
  Match 3:   Student   vs   MM_Open     Result: 21 to 19
  Match 4:   Student   vs MM_Improved   Result: 19 to 21
  Match 5:   Student   vs   AB_Null     Result: 25 to 15
  Match 6:   Student   vs   AB_Open     Result: 17 to 23
  Match 7:   Student   vs AB_Improved   Result: 19 to 21
Student             56.43%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 37 to 3
  Match 2:   Student   vs   MM_Null     Result: 27 to 13
  Match 3:   Student   vs   MM_Open     Result: 15 to 25
  Match 4:   Student   vs MM_Improved   Result: 20 to 20
  Match 5:   Student   vs   AB_Null     Result: 21 to 19
  Match 6:   Student   vs   AB_Open     Result: 16 to 24
  Match 7:   Student   vs AB_Improved   Result: 11 to 29
Student             52.50%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 37 to 3
  Match 2:   Student   vs   MM_Null     Result: 26 to 14
  Match 3:   Student   vs   MM_Open     Result: 21 to 19
  Match 4:   Student   vs MM_Improved   Result: 18 to 22
  Match 5:   Student   vs   AB_Null     Result: 28 to 12
  Match 6:   Student   vs   AB_Open     Result: 16 to 24
  Match 7:   Student   vs AB_Improved   Result: 13 to 27
Student             56.79%
----------

### Distance to the opponent

This heuristic function calculates the distance between the two players.

The rationale behind this heuristic is that it is better to be further away from
the opponent 

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 33 to 7
  Match 2:   Student   vs   MM_Null     Result: 24 to 16
  Match 3:   Student   vs   MM_Open     Result: 19 to 21
  Match 4:   Student   vs MM_Improved   Result: 23 to 17
  Match 5:   Student   vs   AB_Null     Result: 17 to 23
  Match 6:   Student   vs   AB_Open     Result: 23 to 17
  Match 7:   Student   vs AB_Improved   Result: 15 to 25
Student             55.00%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 31 to 9
  Match 2:   Student   vs   MM_Null     Result: 27 to 13
  Match 3:   Student   vs   MM_Open     Result: 19 to 21
  Match 4:   Student   vs MM_Improved   Result: 22 to 18
  Match 5:   Student   vs   AB_Null     Result: 28 to 12
  Match 6:   Student   vs   AB_Open     Result: 21 to 19
  Match 7:   Student   vs AB_Improved   Result: 16 to 24
Student             58.57%
----------


Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 34 to 6
  Match 2:   Student   vs   MM_Null     Result: 28 to 12
  Match 3:   Student   vs   MM_Open     Result: 18 to 22
  Match 4:   Student   vs MM_Improved   Result: 18 to 22
  Match 5:   Student   vs   AB_Null     Result: 22 to 18
  Match 6:   Student   vs   AB_Open     Result: 18 to 22
  Match 7:   Student   vs AB_Improved   Result: 22 to 18
Student             57.14%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 30 to 10
  Match 2:   Student   vs   MM_Null     Result: 29 to 11
  Match 3:   Student   vs   MM_Open     Result: 20 to 20
  Match 4:   Student   vs MM_Improved   Result: 17 to 23
  Match 5:   Student   vs   AB_Null     Result: 22 to 18
  Match 6:   Student   vs   AB_Open     Result: 20 to 20
  Match 7:   Student   vs AB_Improved   Result: 23 to 17
Student             57.50%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 35 to 5
  Match 2:   Student   vs   MM_Null     Result: 28 to 12
  Match 3:   Student   vs   MM_Open     Result: 20 to 20
  Match 4:   Student   vs MM_Improved   Result: 19 to 21
  Match 5:   Student   vs   AB_Null     Result: 23 to 17
  Match 6:   Student   vs   AB_Open     Result: 21 to 19
  Match 7:   Student   vs AB_Improved   Result: 18 to 22
Student             58.57%
----------

### Linear combination of moves

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 38 to 2
  Match 2:   Student   vs   MM_Null     Result: 35 to 5
  Match 3:   Student   vs   MM_Open     Result: 30 to 10
  Match 4:   Student   vs MM_Improved   Result: 31 to 9
  Match 5:   Student   vs   AB_Null     Result: 33 to 7
  Match 6:   Student   vs   AB_Open     Result: 27 to 13
  Match 7:   Student   vs AB_Improved   Result: 26 to 14
Student             78.57%
----------


Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 39 to 1
  Match 2:   Student   vs   MM_Null     Result: 35 to 5
  Match 3:   Student   vs   MM_Open     Result: 32 to 8
  Match 4:   Student   vs MM_Improved   Result: 33 to 7
  Match 5:   Student   vs   AB_Null     Result: 35 to 5
  Match 6:   Student   vs   AB_Open     Result: 27 to 13
  Match 7:   Student   vs AB_Improved   Result: 27 to 13
Student             81.43%
----------


Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 40 to 0
  Match 2:   Student   vs   MM_Null     Result: 37 to 3
  Match 3:   Student   vs   MM_Open     Result: 28 to 12
  Match 4:   Student   vs MM_Improved   Result: 30 to 10
  Match 5:   Student   vs   AB_Null     Result: 29 to 11
  Match 6:   Student   vs   AB_Open     Result: 27 to 13
  Match 7:   Student   vs AB_Improved   Result: 30 to 10
Student             78.93%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 38 to 2
  Match 2:   Student   vs   MM_Null     Result: 38 to 2
  Match 3:   Student   vs   MM_Open     Result: 31 to 9
  Match 4:   Student   vs MM_Improved   Result: 31 to 9
  Match 5:   Student   vs   AB_Null     Result: 32 to 8
  Match 6:   Student   vs   AB_Open     Result: 26 to 14
  Match 7:   Student   vs AB_Improved   Result: 29 to 11
Student             80.36%
----------

Playing Matches:
----------
  Match 1:   Student   vs   Random      Result: 37 to 3
  Match 2:   Student   vs   MM_Null     Result: 37 to 3
  Match 3:   Student   vs   MM_Open     Result: 31 to 9
  Match 4:   Student   vs MM_Improved   Result: 29 to 11
  Match 5:   Student   vs   AB_Null     Result: 35 to 5
  Match 6:   Student   vs   AB_Open     Result: 27 to 13
  Match 7:   Student   vs AB_Improved   Result: 29 to 11
Student             80.36%
----------
