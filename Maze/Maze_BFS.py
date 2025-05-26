import pygame
import random
import time
from collections import deque

# Maze settings
WIDTH, HEIGHT = 300, 300
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH // COLS

# Improved Colors - High Contrast
BACKGROUND = (255, 255, 255)       # white background
WALL = (255, 75, 75)            # Bright red walls
PATH = (100, 200, 255)          # Sky blue path
CURRENT = (255, 255, 100)       # Yellow current position
START = (100, 255, 100)         # Bright green start
END = (255, 150, 50)            # Orange end
VISITED = (0, 255, 0)         #green for visited areas

# Directions (Right, Down, Left, Up)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def generate_maze(rows, cols):
    maze = [[1] * cols for _ in range(rows)]
    stack = [(0, 0)]
    visited = set(stack)

    while stack:
        x, y = stack[-1]
        neighbors = [(x + dx, y + dy) for dx, dy in DIRECTIONS
                     if 0 <= x + dx < cols and 0 <= y + dy < rows]
        unvisited_neighbors = [(nx, ny) for nx, ny in neighbors if (nx, ny) not in visited]

        if unvisited_neighbors:
            nx, ny = random.choice(unvisited_neighbors)
            maze[y][x] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
            visited.add((nx, ny))
        else:
            stack.pop()

    # Add random obstacles (about 20% of the free cells)
    for _ in range((rows * cols) // 8):
        while True:
            ox, oy = random.randint(0, cols - 1), random.randint(0, rows - 1)
            if (ox, oy) not in [(0, 0), (cols - 1, rows - 1)] and \
               (ox, oy) not in [(0, 1), (1, 0), (cols - 2, rows - 1), (cols - 1, rows - 2)]:
                maze[oy][ox] = 1
                break

    return maze

def draw_maze(screen, maze, path, current=None):
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) == (0, 0):
                color = START  # Start position
            elif (x, y) == (COLS - 1, ROWS - 1):
                color = END  # End position
            elif (x, y) == current:
                color = CURRENT  # Node being processed
            elif (x, y) in path:
                color = PATH  # Explored path
            elif maze[y][x] == 1:
                color = WALL  # Obstacle
            else:
                color = VISITED  # Open space
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Add grid lines
            pygame.draw.rect(screen, BACKGROUND, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_text(screen, text, x, y):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))  # White text
    screen.blit(text_surface, (x, y))

def bfs_solve(screen, maze):
    start = (0, 0)
    goal = (COLS - 1, ROWS - 1)

    queue = deque([([start], start)])
    visited = set([start])
    path = set()

    while queue:
        current_path, (x, y) = queue.popleft()

        # Update screen each step
        path.update(current_path)
        draw_maze(screen, maze, path, current=(x, y))
        pygame.display.flip()
        pygame.time.delay(100)  # Faster animation

        if (x, y) == goal:
            return current_path  # Final path to goal

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((current_path + [(nx, ny)], (nx, ny)))

    return None  # No solution found

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Solver - High Contrast")

    maze = generate_maze(ROWS, COLS)
    screen.fill(BACKGROUND)

    path = bfs_solve(screen, maze)

    running = True
    message = "Solved with BFS!" if path else "No Solution Found!"

    while running:
        screen.fill(BACKGROUND)

        draw_maze(screen, maze, path)
        draw_text(screen, message, 10, HEIGHT - 40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press R to regenerate maze
                    maze = generate_maze(ROWS, COLS)
                    path = bfs_solve(screen, maze)

    pygame.quit()

if __name__ == "__main__":
    main()