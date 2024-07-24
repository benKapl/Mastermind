import time

from mastermind import Game
from assets import INTRO, COUNTDOWN

if __name__ == "__main__":
    print(INTRO)
    game = Game(COUNTDOWN)
    time.sleep(5)
    game.play()
    game.retry()


    



    