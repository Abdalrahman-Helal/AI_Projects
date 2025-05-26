import pygame
import random
import heapq

# Maze settings - Larger maze
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 15, 15  # More cells
CELL_SIZE = WIDTH // COLS

# Rose-themed Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEP_ROSE = (180, 20, 90)      # Start position - deep rose
LIGHT_PINK = (255, 182, 193)   # Goal position
ROSE = (255, 85, 125)          # Walls
BABY_PINK = (255, 192, 203)    # Visited cells
HOT_PINK = (255, 105, 180)     # Current search node
MAUVE = (224, 176, 255)        # Solution path color

# Player movement directions
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def generate_maze(rows, cols):
    maze = [[1] * cols for _ in range(rows)]
    stack = [(0, 0)]
    visited = set(stack)

    while stack:
        x, y = stack[-1]
        neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS
                     if 0 <= x + dx < cols and 0 <= y + dy < rows]
        neighbors = [(nx, ny) for nx, ny in neighbors if (nx, ny) not in visited]

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[y][x] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
            visited.add((nx, ny))
        else:
            stack.pop()

    # Add more walls for complexity
    for _ in range((rows * cols) // 4):
        while True:
            ox, oy = random.randint(0, cols - 1), random.randint(0, rows - 1)
            if (ox, oy) not in [(0, 0), (cols - 1, rows - 1)] and \
               (ox, oy) not in [(0, 1), (1, 0), (cols - 2, rows - 1), (cols - 1, rows - 2)]:
                maze[oy][ox] = 1
                break

    return maze

def draw_maze(screen, maze, path, current=None, solution_path=None):
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) == (0, 0):
                color = DEEP_ROSE  # Start position
            elif (x, y) == (COLS - 1, ROWS - 1):
                color = LIGHT_PINK  # Goal position
            elif solution_path and (x, y) in solution_path:
                color = MAUVE  # Highlight solution path
            elif (x, y) in path:
                color = BABY_PINK
            elif maze[y][x] == 1:
                color = ROSE
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

    if current:
        pygame.draw.rect(screen, HOT_PINK, (current[0] * CELL_SIZE, current[1] * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

    pygame.display.flip()
    pygame.time.delay(50)  # Faster animation

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_solve(screen, maze):
    start, goal = (0, 0), (COLS - 1, ROWS - 1)
    pq = [(0 + heuristic(start, goal), 0, start, [start])]
    visited = set()

    while pq:
        f, g, (x, y), path = heapq.heappop(pq)

        if (x, y) in visited:
            continue
        visited.add((x, y))
        draw_maze(screen, maze, visited, current=(x, y))

        if (x, y) == goal:
            print("Maze Solved with A*!")
            return path

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
                new_g = g + 1
                new_f = new_g + heuristic((nx, ny), goal)
                heapq.heappush(pq, (new_f, new_g, (nx, ny), path + [(nx, ny)]))

    return None

def greedy_solve(screen, maze):
    start, goal = (0, 0), (COLS - 1, ROWS - 1)
    pq = [(heuristic(start, goal), start, [start])]
    visited = set()

    while pq:
        h, (x, y), path = heapq.heappop(pq)

        if (x, y) in visited:
            continue
        visited.add((x, y))
        draw_maze(screen, maze, visited, current=(x, y))

        if (x, y) == goal:
            print("Maze Solved with Greedy Search!")
            return path

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
                heapq.heappush(pq, (heuristic((nx, ny), goal), (nx, ny), path + [(nx, ny)]))

    return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Helal's Maze - Rose Theme")

    maze = generate_maze(ROWS, COLS)

    # Toggle between algorithms here
    use_astar = True   # Set False to use Greedy instead

    if use_astar:
        solution_path = a_star_solve(screen, maze)
    else:
        solution_path = greedy_solve(screen, maze)

    draw_maze(screen, maze, path=[], solution_path=solution_path)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
