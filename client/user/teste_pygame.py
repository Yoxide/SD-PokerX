import pygame
import sys

class GridGame:
    def __init__(self):
        # --- Game configuration ---
        self.window_size = 400
        self.grid_size = 4
        self.cell_size = self.window_size // self.grid_size

        # --- Colors ---
        self.white = (255, 255, 255)
        self.grey = (200, 200, 200)
        self.red = (255, 0, 0)
        self.blue =(0,0,255)
        self.other = (130,50,200)

        # --- Pygame setup ---
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("4x4 Grid Game (Class-based)")
        self.clock = pygame.time.Clock()

        # --- Game state ---
        self.running = True
        self.piece_x = 0
        self.piece_y = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.piece_x > 0:
                    self.piece_x -= 1
                elif event.key == pygame.K_RIGHT and self.piece_x < self.grid_size - 1:
                    self.piece_x += 1
                elif event.key == pygame.K_UP and self.piece_y > 0:
                    self.piece_y -= 1
                elif event.key == pygame.K_DOWN and self.piece_y < self.grid_size - 1:
                    self.piece_y += 1

    def update(self):
        # Placeholder for future logic (animations, AI, game rules, etc.)
        pass

    def draw(self):
        self.screen.fill(self.white)

        # Draw grid
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.grey, rect, width=1)

        # Draw piece
        piece_rect = pygame.Rect(
            self.piece_x * self.cell_size,
            self.piece_y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.screen, self.other, piece_rect)

        pygame.display.flip()


# Run the game
if __name__ == "__main__":
    game = GridGame()
    game.run()
