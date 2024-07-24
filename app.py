import time

from mastermind import Game
from assets import INTRO, countdown

if __name__ == "__main__":
    print(INTRO)
    game = Game(countdown)
    game.play()



    



    