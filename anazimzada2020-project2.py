import time
from collections import deque

# Backtracking algorithm assign colors one by one to different vertices
# Function also uses 2 heuristics (Minimum Remaining Value, Least Constraining Value) and Arc Consistency
def Backtracking(res, adjacency, domain, assignment): 
    
    if -1 not in assignment:
        return res
    
    vertex = MRV(domain, assignment)
    color_order = LCV(vertex, adjacency, domain)
    
    for c in color_order:
        domain2 = domain
        
        if (Is_Safe(vertex, c, res, adjacency)):
            domain2[vertex] = [dom for dom in domain[vertex] if dom == c]
            arc = []
            
            for j in adjacency[vertex]:
                temp = [j, vertex]
                
                if assignment[j] != 1:
                    arc.append(temp)
                
                queue = deque(arc)
            
            [flag, domain_list] = AC3(vertex, queue, adjacency, domain2, assignment)
            if flag == 1:
                res[vertex] = c
                assignment[vertex] = 1
                domain2 = domain_list
                result = Backtracking(res, adjacency, domain2, assignment)
                
                if result != 0:
                    return result
        
        res[vertex] = -1
        assignment[vertex] = -1

    return 0


# Backtracking uses this function to check whether it is safe to assign color to particular vertex
# Function checks particular vertex's neighbors whether there is vertex with same color
def Is_Safe(vertex, cur_color, res, adjacency):
    
    for j in adjacency[vertex]:
        if cur_color == res[j]:
            return 0  
    
    return 1


# This function chooses the variable with the fewest possible values
# Backtracking uses this function to get the next vertex to be colored
def MRV(domain, assignment):
    
    minimum = 1000
    next = -1

    for i in range(N):
        if (len(domain[i]) < minimum and assignment[i] != 1):
            minimum = len(domain[i])
            next = i
    
    return next


# This function chooses a value that rules out the smallest number of values 
# in variables connected to the current variable by constraints.
def LCV(vertex, adjacency, domain):
    
    lcv = []
    for dom in domain[vertex]:
        minimum = 100
        
        for i in adjacency[vertex]:
            temp = len(domain[i])
            if dom in domain[i]:
                temp = temp - 1
            if(temp < minimum):
                minimum = temp
        
        lcv.append([dom, minimum])
        ind = sorted(lcv, key=lambda res: res[1], reverse = True)
        color = [col[0] for col in ind]
    
    return color


# Arc consistency eliminates values from domain of variable that can never be part of a consistent solution
# AC3 function returns the CSP with reduced domains
# Function is being called by the Backtracking function
def AC3(res, queue, adjacency, domain2, assignment):
    
    while len(queue) != 0:
        popped = queue.popleft()
        [removed, domain2] = Remove_Arcs(popped, domain2)

        if removed == 1:
            global arcs_pruned
            arcs_pruned = arcs_pruned + 1
            
            if len(domain2[popped[0]]) == 0:
                return (0, domain2)
            
            adjacency2 = [adj for adj in adjacency[popped[0]] if adj != popped[1]]

            for j in adjacency2:
                added = [j, popped[0]]
                
                if assignment[j] != 1:
                    queue.append(added)
    
    return (1, domain2)


# This is the function which removes inconsistent values
# Function is called by AC3
def Remove_Arcs(popped, domain2):
    
    removed = 0
    if len(domain2[popped[1]]) == 1:
        c = domain2[popped[1]][0]
        
        if c in domain2[popped[0]]:
            domain2[popped[0]].remove(c)
            removed = 1
    
    return (removed, domain2)


# Here, program reads input file, creates adjacency list, and initialize other data types that will be used
# Then, backtracking function is called. If there is no solution, it return error message
# If it founds solution, it prints corresponding color of each vertex and number of arcs reduced by AC3
# There is also timer, which shows the time it took to run backtracing function.
# At the end, it double checks whether constraints are preserved or not
def CSP(input_file):
    
    file = open(input_file, 'r')
    lines = file.readlines()

    global N, M, C 
    global arcs_pruned
    
    arcs_pruned = 0
    N = 0
    M = 0
    mode = 1
    sub = 1
    
    for line in lines:
        if line[0] != "#" and line[0] != 'c' and line[0] != 'C':
            M = M + 1
            b = line.strip().split(",")
            if int(b[0]) > N:
                N = int(b[0])
            if int(b[1]) > N:
                N = int(b[1])
            if int(b[0]) == 0 or int(b[1]) == 0:
                mode = 0
    
    if mode == 0:
        N = N + 1
        sub = 0
    
    adjacency = []
    for i in range(N):
        adjacency.append([])
    
    for line in lines:
        if line[0] == 'c' or line[0] == 'C':
            a = line.strip().split("=")
            C = int(a[1])
        elif line[0] != "#":
            b = line.strip().split(",")
            x = int(b[0]) - sub
            y = int(b[1]) - sub
            adjacency[x].append(y)
            adjacency[y].append(x)
    
    res = []
    for i in range(N):
        res.append(-1)

    assignment = []
    for i in range(N):
        assignment.append(-1)
    
    domain = []
    for i in range(N):
        domain.append([])
    
    for i in range(0, N):
        for j in range(1, C + 1):
            domain[i].append(j)
    
    start_time = time.time()
    output = Backtracking(res, adjacency, domain, assignment)
    finish_time = time.time()
    
    if output == 0:
        print(f"There is no solution with C={C}. Try to increase number of colors")
    else:
        print("SOLUTION FOUND!\n")
        print(f"There are {N} vertices and {M} edges. Number of colors to be used is {C}\n")
        print(f"Program took {finish_time - start_time} seconds to complete!\n")
        print("Here are the solution:")
        print(output)
        print("\nNumber of Arcs pruned by AC3:", arcs_pruned)
    
    flag = 1
    for i in range(N):
        for j in adjacency[i]:
            if output[i] == output[j]:
                flag = 0
    
    print("\nSolution being checked according to constraints...")
    if flag:
        print("All Constraints are Satisfied!")
    else:
        print("ERROR! Solution violates constraints!")


# Main Function
if __name__ == "__main__":
    
    CSP("input1.txt")
    CSP("input2.txt")
    CSP("input3.txt")
    CSP("input4.txt")