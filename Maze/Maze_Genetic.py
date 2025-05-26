import pygame
import random
import heapq
import numpy as np

# Maze settings
WIDTH, HEIGHT = 800, 800  # Increased from 600x600 to 800x800
ROWS, COLS = 15, 15      # Increased from 10x10 to 15x15
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 240, 240)      # Slightly off-white background
BLACK = (0, 0, 0)
BLUE = (65, 105, 225)        # Royal Blue for start position
GREEN = (34, 139, 34)        # Forest Green for goal position
RED = (178, 34, 34)          # Firebrick Red for walls
GRAY = (169, 169, 169)       # Darker gray for path
YELLOW = (255, 215, 0)       # Gold for current node
PURPLE = (147, 112, 219)     # Medium Purple for solution path

# Player movement directions
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
DIR_KEYS = ['U', 'D', 'L', 'R']
DIR_MAP = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

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

    for _ in range((rows * cols) // 5):
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
                color = BLUE  # Start position
            elif (x, y) == (COLS - 1, ROWS - 1):
                color = GREEN  # Goal position
            elif solution_path and (x, y) in solution_path:
                color = PURPLE  # Highlight solution path
            elif (x, y) in path:
                color = GRAY
            elif maze[y][x] == 1:
                color = RED
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if current:
        pygame.draw.rect(screen, YELLOW, (current[0] * CELL_SIZE, current[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    pygame.time.delay(200)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def evaluate_fitness(maze, moves):
    x, y = 0, 0
    for move in moves:
        dx, dy = DIR_MAP[move]
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
            x, y = nx, ny
    return -heuristic((x, y), (COLS - 1, ROWS - 1))

def generate_individual(length):
    return [random.choice(DIR_KEYS) for _ in range(length)]

def mutate(individual, mutation_rate=0.1):
    return [gene if random.random() > mutation_rate else random.choice(DIR_KEYS) for gene in individual]

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

def genetic_solve(screen, maze, pop_size=100, generations=100, path_len=2 * (ROWS + COLS)):
    population = [generate_individual(path_len) for _ in range(pop_size)]
    goal = (COLS - 1, ROWS - 1)

    for generation in range(generations):
        scored = sorted([(evaluate_fitness(maze, ind), ind) for ind in population], reverse=True)
        best_score, best_path = scored[0]
        print(f"Generation {generation}: Best Score {best_score}")

        path_coords = [(0, 0)]
        x, y = 0, 0
        for move in best_path:
            dx, dy = DIR_MAP[move]
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0:
                x, y = nx, ny
                path_coords.append((x, y))
                if (x, y) == goal:
                    print("Maze Solved with Genetic Algorithm!")
                    return path_coords
        draw_maze(screen, maze, path_coords)

        top_half = [ind for _, ind in scored[:pop_size // 2]]
        population = [mutate(crossover(random.choice(top_half), random.choice(top_half))) for _ in range(pop_size)]

    return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game - Genetic Algorithm")

    maze = generate_maze(ROWS, COLS)
    solution_path = genetic_solve(screen, maze)

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