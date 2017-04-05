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

The first derivative of the p-mean function could be