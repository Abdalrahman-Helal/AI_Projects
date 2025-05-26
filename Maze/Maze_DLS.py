import pygame
import random
import time

# Maze settings
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH // COLS

# Colors - Neon Theme
BACKGROUND = (10, 10, 30)
WALL = (255, 0, 128)  # Neon Pink
PATH = (50, 50, 80)  # Dark Gray-Blue
CURRENT = (0, 255, 255)  # Cyan
START = (0, 255, 128)  # Neon Green
END = (255, 128, 0)  # Neon Orange
VISITED = (80, 0, 120)  # Dark Purple

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


def dls_solve(screen, maze, depth_limit):
    start = (0, 0)
    goal = (COLS - 1, ROWS - 1)

    # Stack now contains (path, current_position, current_depth)
    stack = [([start], start, 0)]
    visited = set([start])
    path = set()

    while stack:
        current_path, (x, y), depth = stack.pop()

        # Update screen each step
        path.update(current_path)
        draw_maze(screen, maze, path, current=(x, y))
        pygame.display.flip()
        pygame.time.delay(100)  # Animation delay

        if (x, y) == goal:
            return current_path  # Final path to goal

        # If we've reached the depth limit, don't explore further from this node
        if depth >= depth_limit:
            continue

        # Check neighbors
        for dx, dy in DIRECTIONS[::-1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((current_path + [(nx, ny)], (nx, ny), depth + 1))

    return None  # No solution found


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Maze Solver")

    # Calculate a reasonable depth limit based on maze size
    # For a square maze, the Manhattan distance to any point can't exceed (ROWS + COLS - 2)
    default_depth_limit = (ROWS + COLS) * 2  # Using a higher limit to ensure solvability

    maze = generate_maze(ROWS, COLS)
    screen.fill(BACKGROUND)

    path = dls_solve(screen, maze, default_depth_limit)

    running = True
    message = f"Solved with DLS! (Depth Limit: {default_depth_limit})" if path else "No Solution Found!"

    depth_limit = default_depth_limit

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
                    path = dls_solve(screen, maze, depth_limit)
                    message = f"Solved with DLS! (Depth Limit: {depth_limit})" if path else "No Solution Found!"
                elif event.key == pygame.K_UP:  # Press Up to increase depth limit
                    depth_limit += 5
                    path = dls_solve(screen, maze, depth_limit)
                    message = f"Solved with DLS! (Depth Limit: {depth_limit})" if path else "No Solution Found!"
                elif event.key == pygame.K_DOWN and depth_limit > 5:  # Press Down to decrease depth limit
                    depth_limit -= 5
                    path = dls_solve(screen, maze, depth_limit)
                    message = f"Solved with DLS! (Depth Limit: {depth_limit})" if path else "No Solution Found!"

    pygame.quit()


if __name__ == "__main__":
    main()