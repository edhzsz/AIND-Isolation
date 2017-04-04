# Research review

## Paper: [Game Tree Searching by Min / Max Approximation][1]

One of the problems of _Alpha-Beta pruning_ is that the amount of nodes being
pruned depends on the order in which the nodes are visited so it is worth
investing into calculating "the node that is expected to have largest effect on
the value".

The key idea presented in the paper is to approximate the "min" and "max"
operators with generalized mean-value operators which not only are good aproximations
of min and max, but also have continuous derivatives with respect to all arguments.



[1]: (https://people.csail.mit.edu/rivest/pubs/Riv87c.pdf)