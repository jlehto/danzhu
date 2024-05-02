import pygame
"""
This file is the GUI on top of the game backend.
# adapted from https://github.com/lxucs/go-game-easy/blob/master/game/ui.py
"""

BACKGROUND = 'dlgo/img/ramin.jpg'
BOARD_SIZE = (820, 820)
BLACK = (0, 0, 0)
BOARD_TYPE=9
RSIZE = 720/(BOARD_TYPE-1)

if BOARD_TYPE < 13:
    S_SIZE = 30
elif BOARD_TYPE == 13:
    S_SIZE = 24
else:
    S_SIZE = 20

def get_rbg(color):
    if color == 'WHITE':
        return 255, 255, 255
    elif color == 'BLACK':
        return 0, 0, 0
    else:
        return 0, 133, 211


def coords(point):
    """Return the coordinate of a stone drawn on board"""
    # since dlgo coords start with (1,1), decrement here
    col = point[0] - 1
    row = point[1] - 1
    return 45 + col * RSIZE, 45 + row * RSIZE

class UI:
    def __init__(self):
        """Create, initialize and draw an empty board."""
        self.outline = pygame.Rect(45, 45, 720, 720)
        self.screen = None
        self.background = None

    def initialize(self):
        """This method should only be called once, when initializing the board."""
        pygame.init()
        pygame.display.set_caption('Danzhu Go')
        self.screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
        self.background = pygame.image.load(BACKGROUND).convert()

        pygame.draw.rect(self.background, BLACK, self.outline, 3)
        # Outline is inflated here for future use as a collidebox for the mouse
        self.outline.inflate_ip(20, 20)
        
        for i in range(BOARD_TYPE-1):
            for j in range(BOARD_TYPE-1):
                rect = pygame.Rect(45 + (RSIZE * i), 45 + (RSIZE * j), RSIZE, RSIZE)
                pygame.draw.rect(self.background, BLACK, rect, 1)
        if BOARD_TYPE==19:
            # too lazy to mark these out for smaller boards
            for i in range(3):
                for j in range(3):
                    coords = (165 + (240 * i), 165 + (240 * j))
                    pygame.draw.circle(self.background, BLACK, coords, 5, 0)
        
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def draw(self, point, color, size=S_SIZE):
        color = get_rbg(color)
        pygame.draw.circle(self.screen, color, coords(point), size, 0)
        pygame.display.update()

    def remove(self, point, size=S_SIZE):
        center = coords(point)
        blit_coords = (center[0] - size, center[1] - size)
        area_rect = pygame.Rect(blit_coords, (2 * size, 2 * size))
        self.screen.blit(self.background, blit_coords, area_rect)
        pygame.display.update()

    def save_image(self, path_to_save):
        pygame.image.save(self.screen, path_to_save)
