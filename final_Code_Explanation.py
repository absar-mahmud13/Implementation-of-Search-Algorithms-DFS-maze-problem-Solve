import sys  # Import the sys module for command-line arguments

class Node():
    def __init__(self, state, parent, action):
        self.state = state  # The current position in the maze (row, column)
        self.parent = parent  # The previous node in the path
        self.action = action  # The action taken to reach this node

class StackFrontier():
    def __init__(self):
        self.frontier = []  # Initialize an empty list to hold nodes

    def add(self, node):
        self.frontier.append(node)  # Add a node to the frontier

    def contains_state(self, state):
        # Check if a state is already in the frontier
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0  # Check if the frontier is empty

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")  # Raise error if frontier is empty
        else:
            node = self.frontier[-1]  # Get the last node added (DFS behavior)
            self.frontier = self.frontier[:-1]  # Remove it from the frontier
            return node  # Return the removed node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")  # Raise error if frontier is empty
        else:
            node = self.frontier[0]  # Get the first node added (BFS behavior)
            self.frontier = self.frontier[1:]  # Remove it from the frontier
            return node  # Return the removed node

class Maze():
    def __init__(self, filename):
        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()  # Read the maze contents from the file

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")  # Ensure exactly one start point
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")  # Ensure exactly one goal

        # Determine height and width of maze
        contents = contents.splitlines()  # Split contents into lines
        self.height = len(contents)  # Set the height of the maze
        self.width = max(len(line) for line in contents)  # Set the width of the maze

        # Keep track of walls
        self.walls = []  # Initialize a list for wall positions
        for i in range(self.height):
            row = []  # Initialize a row for the current line
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)  # Set start position
                        row.append(False)  # Mark as open space
                    elif contents[i][j] == "B":
                        self.goal = (i, j)  # Set goal position
                        row.append(False)  # Mark as open space
                    elif contents[i][j] == " ":
                        row.append(False)  # Mark as open space
                    else:
                        row.append(True)  # Mark as a wall
                except IndexError:
                    row.append(False)  # Handle index error (out of bounds)
            self.walls.append(row)  # Add the row to the walls list

        self.solution = None  # Initialize the solution attribute

    def print(self):
        solution = self.solution[1] if self.solution is not None else None  # Get the solution path
        print()  # Print a newline
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")  # Print wall
                elif (i, j) == self.start:
                    print("A", end="")  # Print start point
                elif (i, j) == self.goal:
                    print("B", end="")  # Print goal point
                elif solution is not None and (i, j) in solution:
                    print("*", end="")  # Print solution path
                else:
                    print(" ", end="")  # Print empty space
            print()  # Newline for the next row
        print()  # Print a newline after the maze

    def neighbors(self, state):
        row, col = state  # Unpack the current state
        candidates = [  # List potential moves
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []  # Initialize a list for valid neighbors
        for action, (r, c) in candidates:
            # Check if the neighbor is within bounds and not a wall
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))  # Add valid neighbor
        return result  # Return the list of valid neighbors

    def solve(self):
        """Finds a solution to the maze, if one exists."""

        self.num_explored = 0  # Initialize the number of states explored
        start = Node(state=self.start, parent=None, action=None)  # Create the start node
        frontier = StackFrontier()  # Initialize the frontier
        frontier.add(start)  # Add the start node to the frontier

        self.explored = set()  # Initialize an empty explored set

        while True:
            if frontier.empty():
                raise Exception("no solution")  # Raise error if no path found

            node = frontier.remove()  # Remove a node from the frontier
            self.num_explored += 1  # Increment explored states count

            if node.state == self.goal:
                actions = []  # List to store actions taken to reach the goal
                cells = []  # List to store cells in the solution path
                while node.parent is not None:
                    actions.append(node.action)  # Add action to the list
                    cells.append(node.state)  # Add state to the list
                    node = node.parent  # Move to the parent node
                actions.reverse()  # Reverse actions to get the correct order
                cells.reverse()  # Reverse cells to get the correct order
                self.solution = (actions, cells)  # Store the solution
                return  # Exit the function

            self.explored.add(node.state)  # Mark the node as explored

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)  # Create a child node
                    frontier.add(child)  # Add child node to the frontier

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw  # Import image libraries
        cell_size = 50  # Size of each cell in the image
        cell_border = 2  # Border size for each cell

        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"  # Create a new image with black background
        )
        draw = ImageDraw.Draw(img)  # Prepare to draw on the image

        solution = self.solution[1] if self.solution is not None else None  # Get solution cells
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                # Determine the fill color based on the cell type
                if col:
                    fill = (40, 40, 40)  # Wall color
                elif (i, j) == self.start:
                    fill = (255, 0, 0)  # Start color (red)
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)  # Goal color (green)
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)  # Solution path color
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)  # Explored cell color
                else:
                    fill = (237, 240, 252)  # Empty cell color

                # Draw the cell as a rectangle on the image
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)  # Save the generated image

# Main execution logic
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")  # Check for correct command-line usage

m = Maze(sys.argv[1])  # Create a Maze object from the provided filename
print("Maze:")  # Indicate the maze is being printed
m.print()  # Print the maze
print("Solving...")  # Indicate the solving process is starting
m.solve()  # Attempt to solve the maze
print("
