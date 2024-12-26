import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = {
    'I': (0, 255, 255),   # Cyan
    'O': (255, 255, 0),   # Yellow
    'T': (128, 0, 128),   # Purple
    'S': (0, 255, 0),     # Green
    'Z': (255, 0, 0),     # Red
    'J': (0, 0, 255),     # Blue
    'L': (255, 128, 0)    # Orange
}

# Tetromino shapes
SHAPES = {
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, 1), (1, 0), (1, 1), (1, 2)],
    'S': [(0, 1), (0, 2), (1, 0), (1, 1)],
    'Z': [(0, 0), (0, 1), (1, 1), (1, 2)],
    'J': [(0, 0), (1, 0), (1, 1), (1, 2)],
    'L': [(0, 2), (1, 0), (1, 1), (1, 2)]
}

class SandParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.settled = False

    def update(self, grid):
        if self.settled:
            return

        # Check if particle can fall
        if self.y + 1 < GRID_HEIGHT and grid[self.y + 1][self.x] is None:
            self.y += 1
        # Check if particle can slide down-left or down-right
        elif self.y + 1 < GRID_HEIGHT:
            if self.x > 0 and grid[self.y + 1][self.x - 1] is None:
                self.x -= 1
                self.y += 1
            elif self.x < GRID_WIDTH - 1 and grid[self.y + 1][self.x + 1] is None:
                self.x += 1
                self.y += 1
            else:
                self.settled = True

class Tetromino:
    def __init__(self):
        self.shape = random.choice(list(SHAPES.keys()))
        self.color = COLORS[self.shape]
        self.blocks = SHAPES[self.shape].copy()
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0

    def move(self, dx, dy, grid):
        for x, y in self.blocks:
            new_x = x + self.x + dx
            new_y = y + self.y + dy
            if not (0 <= new_x < GRID_WIDTH and new_y < GRID_HEIGHT):
                return False
            if new_y >= 0 and grid[new_y][new_x] is not None:
                return False
        self.x += dx
        self.y += dy
        return True

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sand Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.particles = []
        self.game_over = False

    def convert_to_sand(self):
        for x, y in self.current_piece.blocks:
            world_x = x + self.current_piece.x
            world_y = y + self.current_piece.y
            if world_y >= 0:
                particle = SandParticle(world_x, world_y, self.current_piece.color)
                self.particles.append(particle)
                self.grid[world_y][world_x] = particle

    def update(self):
        if not self.current_piece.move(0, 1, self.grid):
            self.convert_to_sand()
            self.current_piece = Tetromino()
            if not self.current_piece.move(0, 0, self.grid):
                self.game_over = True

        # Update sand particles
        for particle in self.particles:
            if particle.settled:
                continue
            old_x, old_y = particle.x, particle.y
            self.grid[old_y][old_x] = None
            particle.update(self.grid)
            self.grid[particle.y][particle.x] = particle

    def draw(self):
        self.screen.fill(BLACK)

        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] is not None:
                    pygame.draw.rect(self.screen, self.grid[y][x].color,
                                  (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw current piece
        for x, y in self.current_piece.blocks:
            world_x = (x + self.current_piece.x) * GRID_SIZE
            world_y = (y + self.current_piece.y) * GRID_SIZE
            if world_y >= 0:
                pygame.draw.rect(self.screen, self.current_piece.color,
                              (world_x, world_y, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.move(-1, 0, self.grid)
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.move(1, 0, self.grid)
                    elif event.key == pygame.K_DOWN:
                        self.current_piece.move(0, 1, self.grid)

            self.update()
            self.draw()
            self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()