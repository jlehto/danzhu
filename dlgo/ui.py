import pygame
from dlgo.gotypes import Point
from dlgo.goboard import Move
# adapted from https://github.com/lxucs/go-game-easy/blob/master/game/ui.py

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
        self.player_color = None #holds color if interactive mode
        self.player_moved = False
        self.hover_stone = None
        self.game = None  # TODO extract most of these vars from game

    def initialize(self, game, board_type, player_color=None):
        """This method should only be called once, when initializing the board."""
        pygame.init()
        pygame.display.set_caption('Danzhu Go')
        self.game = game
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
        self.player_color = player_color 
    
        

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif self.player_color and event.type == pygame.MOUSEMOTION:
                # Get the mouse position
                if self.hover_stone and not self.player_moved:
                    self.remove(self.hover_stone)
                mouse_pos = pygame.mouse.get_pos()
                # Calculate the nearest intersection point
                nearest_point = self.get_nearest_intersection(mouse_pos)
                # Store the position of the hovered stone
              
                if self.is_valid(nearest_point) and not self.player_moved:
                    self.hover_stone = nearest_point
                    self.draw_hover_stone()
            elif self.player_color and event.type == pygame.MOUSEBUTTONDOWN:
                # Handle stone placement when mouse button is clicked
                if event.button == 1 and self.hover_stone is not None:
                    # Place stone at the selected intersection
                    #self.draw(self.hover_stone, get_rbg(self.player_color))  # Assuming black stone for player
                  
                    if self.is_valid(self.hover_stone):
                        self.player_moved = True
                    #pygame.display.update()


    def get_nearest_intersection(self, mouse_pos):
        # Calculate the nearest intersection point based on the mouse position
        a = 45
        x = round((mouse_pos[0] - a) / self.lines_size)
        y = round((mouse_pos[1] - a) / self.lines_size)
        return (x+1, y+1)

    def draw_hover_stone(self):
        # Draw a semi-transparent stone at the nearest intersection point while hovering
        if self.hover_stone is not None:
            #color = get_rbg(self.player_color)
            color = (128,128,128, 50)  # Add transparency (alpha value)
            pygame.draw.circle(self.screen, color, self.coords(self.hover_stone), self.stone_size, 0)
            pygame.display.update()
    

    def save_image(self, path_to_save):
        pygame.image.save(self.screen, path_to_save)

    def make_move(self):
        # make that move, right now baby
        self.hover_stone = None 
        self.player_moved = False
        while self.player_moved is not True:
            self.handle_events()  # Handle pygame events
        return self.hover_stone    

    def is_valid(self,ui_point):
        #print(ui_point)
        candidate = Point(ui_point[0], ui_point[1])
        #print(self.game.is_valid_move(Move.play(candidate))) 
        return self.game.is_valid_move(Move.play(candidate)) 