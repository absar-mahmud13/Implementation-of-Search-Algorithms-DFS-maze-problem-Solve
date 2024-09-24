### Problem Overview ##
In this maze-solving problem, the goal is to find a path from a starting point (`A`) to a goal point (`B`) through a grid of cells, where some cells are walls that cannot be crossed.

### Depth-First Search (DFS)
DFS is an algorithm used for traversing or searching tree or graph data structures. It explores as far down a branch as possible before backtracking. This is well-suited for maze solving because it will explore potential paths until it either finds a solution or exhausts all possibilities.

### Code Breakdown of DFS in the Maze Solver

1. **Initialization**
   - The maze is read from a text file, which defines walls, open paths, and the start and goal points.
   - The `Maze` class is initialized with attributes like `walls`, `start`, `goal`, and a placeholder for the solution.

2. **Node Class**
   - Each state in the maze is represented by a `Node` that contains:
     - The current state (coordinates),
     - A reference to its parent node (to trace back the path),
     - The action taken to reach that state.

3. **StackFrontier**
   - This class manages the nodes to explore. It uses a stack to implement the DFS behavior:
     - Nodes are added to the end of the stack and removed from the end, which ensures that the most recently added node is explored next.

4. **Solving the Maze**
   - The `solve()` method executes the DFS:
     - It starts by initializing the frontier with the starting node.
     - It also maintains a set of explored nodes to avoid revisiting them.
     - The algorithm enters a loop where it continuously checks the frontier:
       - If the frontier is empty, it raises an exception indicating no solution exists.
       - It removes the last node added (the most recently explored).
       - If this node is the goal, it backtracks to construct the solution.
       - If it’s not the goal, it marks the node as explored and adds its valid neighbors to the frontier.
       - Neighbors are generated based on possible movements (up, down, left, right), checking for walls and bounds.
5. **Backtracking for Solution Path**
   - When the goal is reached, the path is constructed by following parent nodes back to the start, recording actions and states along the way.
### Visual Output
- The maze can be printed in the console, and an image can be generated to visualize the maze, solution path, and explored states.
### Summary
The DFS maze-solving implementation explores possible paths systematically until it finds a solution. It uses a stack to manage the nodes, ensuring that it always goes as deep as possible into the maze before backtracking. This method can be effective for finding a solution, but it may not always be the most efficient in terms of time or space, especially for large mazes.
