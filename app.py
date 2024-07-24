from mastermind import Game
from assets import MENU

if __name__ == "__main__":
    print(MENU)

    game = Game()
    while game.countdown > 0:
        game.guess = game.prompt_guess()
        game.evaluate_guess()
        game.show_guess_result()
        game.countdown -= 1

    



    