# CSCI-6511-Project-2

For this project, we were required to color given graph, Constraint Satisfaction Problem. Input is txt file with list of edges (from vertex to vertex).
Program should color vertices in a given number of colors with preserving constraint of no adjacent vertices can have same color.

For coloring, I implemented backtracking algorithm. The idea is to assign colors one by one to different vertices, starting from the particular vertex.
Before assigning a color, it checks for safety by considering already assigned colors to the adjacent vertices.
If there is any color assignment that does not violate the conditions, it marks the color assignment as a part of the solution.
If no assignment of color is possible, then it backtrack and return false.

Decision of which vertex need to be colored first or next is very important in the scope of performance. For this purpose I have implemented 2 heuristic functions.

First one is Minimum Remaining Values which is heuristic of selecting unassigned variable. MRV is the idea of choosing the variable with the fewest value.
It picks a variable that is most likely to cause a failure soon thereby pruning the search tree.
If some variable X has no legal values left, the MRV heuristic will select X and failure will be detected immediately—avoiding pointless searches through other variables.

Another heuristic is Least Constraining Value which is ordering domain value heuristic.
LCV prefers the value that rules out the fewest choice for the neighboring variables in the constraint graph.
It helps in deciding which value to try first for a given variable. In other words, MRV selects the variable that fail first, and LCV selects value fail last.

Arc Consistency is also implemented in this project as a constraint propagation algorithm.
Arc Consistency (AC-3) eliminates values from domain of variable that can never be part of a consistent solution.
A variable in a CSP is arc-consistent if every value in its domain satisfies the variable’s binary constraints.
What AC-3 does is it selects an arc A->B, for each value of “a” that A can takes try to check if there's a value “b” that B can take respecting the restriction.
If so, the domain of A keeps the same, if not removes the value “a” from the domain of A.
