from dlgo import agent
from dlgo import goboard
from dlgo import gotypes

from dlgo.ui import UI
import pygame
import time


def main():
   
    board_size = 9

    ui = UI()
    game = goboard.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: agent.naive.RandomBot(),
        gotypes.Player.white: agent.naive.RandomBot(),
    }
    
    ui.initialize(game, board_size)

    while not game.is_over():
        time.sleep(0.5)
        ui.handle_events()
        bot_move = bots[game.next_player].select_move(game)
        color = game.next_player.color
        game = game.apply_move(bot_move)
        #print(f"last move: {game.last_move.point}")
        if game.last_move.point is not None:
            ui.draw(game.last_move.point,color)
        if len(game.removed) > 0:     
            for point in game.removed:
                ui.remove(point)
        


if __name__ == '__main__':
    main()


