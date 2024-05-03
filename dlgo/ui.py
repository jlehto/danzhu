import pygame
"""
This file is the GUI on top of the game backend.
# adapted from https://github.com/lxucs/go-game-easy/blob/master/game/ui.py
"""

BACKGROUND = 'dlgo/img/ramin.jpg'
BOARD_SIZE = (820, 820)
BLACK = (0, 0, 0)

def get_rbg(color):
    if color == 'WHITE':
        return 255, 255, 255
    elif color == 'BLACK':
        return 0, 0, 0
    else:
        return 0, 133, 211

class UI:
    def __init__(self):
        """Create, initialize and draw an empty board."""
        self.outline = pygame.Rect(45, 45, 720, 720)
        self.screen = None
        self.background = None
        self.board_dim = None
        self.stone_size = None
        self.lines_size = None
        

    def initialize(self, board_type):
        """This method should only be called once, when initializing the board."""
        pygame.init()
        pygame.display.set_caption('Danzhu Go')
        self.screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
        self.background = pygame.image.load(BACKGROUND).convert()
        if board_type < 13:
            self.stone_size = 30
        elif board_type == 13:
            self.stone_size = 24
        else:
            self.stone_size = 20
        self.board_dim = board_type - 1        
        self.lines_size = 720/(self.board_dim)       
        

        pygame.draw.rect(self.background, BLACK, self.outline, 3)
        # Outline is inflated here for future use as a collidebox for the mouse
        self.outline.inflate_ip(20, 20)
        
        for i in range(self.board_dim):
            for j in range(self.board_dim):
                rect = pygame.Rect(45 + (self.lines_size * i), 45 + (self.lines_size * j), self.lines_size, self.lines_size)
                pygame.draw.rect(self.background, BLACK, rect, 1)
        if board_type==19:
            # too lazy to mark these out for smaller boards
            for i in range(3):
                for j in range(3):
                    coords = (165 + (240 * i), 165 + (240 * j))
                    pygame.draw.circle(self.background, BLACK, coords, 5, 0)
        
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def coords(self, point):
        """Return the coordinate of a stone drawn on board"""
        # since dlgo coords start with (1,1), decrement here
        col = point[0] - 1
        row = point[1] - 1
        return 45 + col * self.lines_size, 45 + row * self.lines_size  

    def draw(self, point, color):
        color = get_rbg(color)
        pygame.draw.circle(self.screen, color, self.coords(point), self.stone_size, 0)
        pygame.display.update()

    def remove(self, point):
        center = self.coords(point)
        blit_coords = (center[0] - self.stone_size, center[1] - self.stone_size)
        area_rect = pygame.Rect(blit_coords, (2 * self.stone_size, 2 * self.stone_size))
        self.screen.blit(self.background, blit_coords, area_rect)
        pygame.display.update()

    def save_image(self, path_to_save):
        pygame.image.save(self.screen, path_to_save)
