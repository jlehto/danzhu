from dlgo import agent
from dlgo import goboard_slow as goboard
from dlgo import gotypes

from dlgo.ui import UI
import pygame
import time


def main():
    ui = UI()

    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: agent.naive.RandomBot(),
        gotypes.Player.white: agent.naive.RandomBot(),
    }
    
    ui.initialize()

    while not game.is_over():
        time.sleep(0.5)

        bot_move = bots[game.next_player].select_move(game)
        color = game.next_player.color
        game = game.apply_move(bot_move)
        #print(f"last move: {game.last_move.point}")
        if game.last_move.point is not None:
            ui.draw(game.last_move.point,color)
        if len(game.removed) > 0:     
            for point in game.removed:
                ui.remove(point)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()    


if __name__ == '__main__':
    main()


