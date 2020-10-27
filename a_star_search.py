# A* Tree Search Example for Robot Navigation
# R. Shekhar
# August 10, 2017

# Define the start and goal nodes
start = (3,2)
goal = (2,5)

# Define the obstacle coordinates
obstacles = set([(2,2),(6,2),(1,3),(2,4),(3,4),(4,4),(5,4),(6,4)])

# Define the heuristic functions here

# A sample heuristic (makes A* behave like uniform-cost search)
def hnull(coord): return 0

# [Insert  your own heuristic functions here, defining new functions like hnull above.]

#def h1(node, goal_node=goal):
  #  a = goal[0]-node[0]
 #   b = goal[1]-node[1]
  #  c = (a**2 + b**2)**0.5
 #   return c

def h2(node, goal_node=goal):
    x_axis = goal[0] - node[0]
    y_axis = goal[1] - node[1]
    man_distance = abs(x_axis) + abs(y_axis)
    return man_distance
    
def h1(node, goal_node=goal):
    x_axis = goal[0] - node[0]
    y_axis = goal[1] - node[1]
    distance = (x_axis**2 + y_axis**2)**0.5
    return distance
    
def f(node, heur=h2, goal_node=goal):
   	return h2(node) + h2(node, goal_node=start)

#Current heuristic function. Change the handle cur_heur to point to the heuristic function you want to test
########################## Adjust this ##########################
cur_heur = f
##########################  END ADJUST ##########################


# Define the data structure for A* search node
class AStarNode:
    # Class constructor
    def __init__(self,coord,fval,gval,parent=None):
        self.coord = coord
        self.fval = fval
        self.gval = gval
        self.parent = parent
        self.pruned = False

    # Comparison function based on f cost
    def __lt__(self,other):
        return self.fval < other.fval

    # Convert to string
    def __str__(self):
        return str(self.coord)

# Start node
start_node = AStarNode(start,cur_heur(start),0)

# Dictionary with current cost to reach all visited nodes
costs_db = {start:start_node}

# Frontier, stored as a Priority Queue to maintain ordering
from queue import PriorityQueue

frontier = PriorityQueue()
frontier.put(start_node)

# next moves
moves_orth = ((1,0),(0,1),(-1,0),(0,-1))

# Begin A* Tree Search
step_counter = 0

while not frontier.empty():
    # Take the next available node from the priority queue
    cur_node = frontier.get()

    if cur_node.pruned:
        continue # Skip if this node has been marked for removal

    # Check if we are at the goal
    if cur_node.coord == goal: break

    # Expand the node in the orthogonal and diagonal directions
    for m in moves_orth:
        next_coord = tuple(sum(x) for x in zip(cur_node.coord,m))

        # Can only move in this direction if there is no obstacle there
        if next_coord not in obstacles:
            step_counter += 1 # Each valid child node generated is another step
            gval = cur_node.gval + 1 # Tentative cost value for child

            # If the child node is already in the cost database (i.e. explored) then see if we need to update the path.  In a graph search, we wouldn't even bother exploring it again.
            if next_coord in costs_db:
                if costs_db[next_coord].gval > gval:
                    costs_db[next_coord].pruned = True # Mark existing value for deletion from frontier
                else:
                    continue # ignore this child, since a better path has already been found previously.

            hval = cur_heur(next_coord) # Heuristic cost from next node to goal
            next_node = AStarNode(next_coord,gval+hval,gval,cur_node) # Create new node for child
            frontier.put(next_node)
            costs_db[next_coord] = next_node #Mark the node as explored

# Reconstruct the optimal path
optimal_path = [cur_node.coord]
while cur_node.parent:
    optimal_path.append((cur_node.parent).coord)
    cur_node = cur_node.parent
optimal_path = optimal_path[::-1]
print(f"A* search completed in {step_counter} steps\n")
print(f"A* path length: {len(optimal_path)-1} steps\n")
print(f"A* path to goal:\n")
print(optimal_path)