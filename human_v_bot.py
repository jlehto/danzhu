from dlgo import agent
from dlgo import goboard
from dlgo import gotypes
from dlgo.ui import UI

def main():
    board_size = 9
    ui = UI()
    game = goboard.GameState.new_game(board_size)
    bot = agent.RandomBot()
    ui.initialize(game, board_size,'BLACK')

    while not game.is_over():
        if game.next_player == gotypes.Player.black:
            
            ui_move = ui.make_move()
            print(ui_move)
            point = gotypes.Point(ui_move[0],ui_move[1])
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        color = game.next_player.color    
        game = game.apply_move(move)
        if game.last_move.point is not None:
            print(game.last_move.point)
            ui.draw(game.last_move.point,color)
        if len(game.removed) > 0:     
            for point in game.removed:
                ui.remove(point)
        

if __name__ == '__main__':
    main()