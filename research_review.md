# Research review

## Paper: [Game Tree Searching by Min / Max Approximation](https://people.csail.mit.edu/rivest/pubs/Riv87c.pdf)

When performing a tree search using the _minimax_ algorithm with _Alpha-Beta pruning_
the amount of nodes being pruned depend on the order in which the nodes are
visited. Usually the selection of the child node to explore next is done in an
arbitrary way and there is no guarantee that the selected node is "the node that
is expected to have largest effect on the value".

The key idea presented in the paper is to use the generalized _p-mean_ functions,
defined as

<img src="https://latex.codecogs.com/gif.latex?M_p(a)=\left(\frac{1}{n}\sum_{i=1}^na_i^p\right)^{1/p}" title="p-mean" />

to approximate the "min" and "max" operators of _minimax_ by using the facts that

<img src="https://latex.codecogs.com/gif.latex?\lim_{p&space;\rightarrow&space;\infty&space;}M_p(a)=\max(a_1,...,a_n)" title="max aproximation" /></a>

and

<img src="https://latex.codecogs.com/gif.latex?\lim_{p&space;\rightarrow&space;-\infty&space;}M_p(a)=\min(a_1,...,a_n)" title="min aproximation" /></a>

This allows to identify "in an interesting way that leaf in a game tree upon whose
value the value at the root depends most strongly".

The algorithm presented is an example of a penalty based iterative search heuristic
method. This means that a non-negative value, called penalty, is assigned to each
node and the search tree is iteratively grown one step a time by expanding the tip
node with the least penalty. The estimated value of each node (the heuristic) is
updated each time the search tree grows.

In the algorithm presented the derivatives of the _p-mean_ functions are used to
calculate the "sensivity" of the root node to changes in the values of each tip
node. This sensitivity, in turn, is used to calculate the value of the penalty.

Calculating the generalized p-means is computational difficult beause of the large
computational cost involved in taking powers and roots but it may allow an improve
in the play because the min/max approximation favors moves whose min/max value
can be achieved in several ways over a move whose min/max value can be achieved
in only one way.

"Another approach is to skip the computation of the generalized mean values altogether, and use the appropriate min or max values instead. (I.e. use bE instead of ~E everywhere.) Since the generalized mean values are intended to approximate the min and max functions anyway, this may not introduce very much error. The main point of using the generalized mean values was for their derivatives, not for the values themselves. We call this variation the "reverse approximation" idea."

An implementation of the algorithm using "reverse aproximation" was compared
against a straigth forward implementation of
_iterative deepening minimax search with alpha-beta pruning_ by playing the game
_Connect-Four_. each strategy was allocated a fixed amount of resources to use
in computing its move: elapsed CPU time (measured in seconds), and calls to the
basic "move" subroutine (measured in thousands of calls).

For each experiment, considered 49 different starting positions. For each starting position, two games were played--one with alpha-beta (AB) moving first, and one with min/max approximation (MM) moving firs. it was recorded how many times each strategy won, and how many ties occured. One experiment was run for each of five posible time bounds (1 second to 5 seconds, in one-second intervals), and for five possible move bounds (1000 moves to 5000 moves, in 1000-move increments). Thus, 490 games were played for each resource bound, and 980 games played altogether.

based on time usage alone, alpha-beta seems to be superior to our implementation of the min/max approximation approach.
However, if we base our comparison on move-based resource limits, the story is reversed: min/max approximation is definitely superior.

Unlike depth-first search schemes (e.g. minimax search with alpha-beta pruning), penalty-based schemes may not perform well unless they are given a large amount of memory
to work with.