import logging
import random
import sys
import time

from assets import COLORS, COLOR_RESET, CARRE, PASTILLE, DELIMITER, COUNTDOWN, MENU

logging.basicConfig(level=logging.WARNING)

def display_colors(colors_unicode) -> str:
    """Display a iterable of color_codes into a string to represent the colors in terminal

    Args:
        colors_unicode (iterable): iterable of color unicodes

    Returns:
        str: All colors in a single string
    """
    display = ""
    for color in colors_unicode:
        display += color
    return display

class Game:

    def __init__(self, countdown) -> None:
        self.combination = self.generate_combination()
        self.guess = ""
        self.evaluation = []
        self.countdown = countdown
        self.attempts = 10 - self.countdown
        # self.combination = ['\x1b[95m ■ \x1b[00m', '\x1b[95m ■ \x1b[00m', '\x1b[91m ■ \x1b[00m', '\x1b[97m ■ \x1b[00m']

    def generate_combination(self) -> list:
        """ Generate 4 random colors

        Returns:
            list: 4 colors
        """
        return [f"{random.choice(list(COLORS.values()))} {CARRE} {COLOR_RESET}" for _ in range(4)]
    
    def prompt_guess(self) -> str:
        """ Ask the player 4 digits, return the digits converted to colors
        """
        while True:
            self.guess = input("Veuillez saisir vos 4 chiffres pour les couleurs : ")
            if len(self.guess) == 4 and self.guess.isdigit():
                try:
                    return [f"{COLORS[number]} {CARRE} {COLOR_RESET}" for number in self.guess] # type: ignore
                except KeyError:
                    print("Votre saisie est incorrecte...\n")   
            else:
                print("Votre saisie est incorrecte...\n")
    
    def evaluate_guess(self) -> bool:
        """ Indicates the player how close from the combination his guess is
        """
        self.evaluation.clear()      
        # Map colors to compare pairs  
        color_mapping = list(zip(self.combination, self.guess))

        for color_combination, color_guess in color_mapping:
            if color_combination == color_guess:
                logging.debug(f" PERFECT MATCH : {display_colors(color_guess)}")
                self.evaluation.append(f"{COLORS['3']} {PASTILLE} {COLOR_RESET}")

            elif color_guess in self.combination:
                logging.debug(f" Simple match: {display_colors(color_guess)}")
                self.evaluation.append(f"{COLORS['5']} {PASTILLE} {COLOR_RESET}")

            else:
                logging.debug(" NO MATCH")
                
        # Sort indications to return the red dot first and display the result
        self.evaluation = sorted(self.evaluation)

        if self.evaluation == [f"{COLORS['3']} {PASTILLE} {COLOR_RESET}", 
                               f"{COLORS['3']} {PASTILLE} {COLOR_RESET}", 
                               f"{COLORS['3']} {PASTILLE} {COLOR_RESET}", 
                               f"{COLORS['3']} {PASTILLE} {COLOR_RESET}"]:
            return True
        else:
            return False

    def show_guess_result(self) -> None:
        if self.evaluation:
            print(f"{display_colors(self.guess)}   Indicateurs : {'' ''.join(self.evaluation)}")
        else:
            print(f"{display_colors(self.guess)}  Aucune correspondance trouvée")

    def show_remaining_attemps(self) -> None:
        if self.countdown > 0:
            print(f"Il vous reste {self.countdown} tentative{'s.' if self.countdown > 1 else ' 😱'}\n")
        else:
            print("Vous n'avez plus de tentative 💀\n")



    def won(self) -> None:
        if self.attempts == 1:
            display = f"""{DELIMITER}
FELICITATIONS 👏👏👏
Vous avez gagné du premier coup 😮
{DELIMITER}"""
        elif 2 <= self.attempts < 10:
            display = f"""{DELIMITER}
Bravo !
Vous avez gagné en {self.attempts} tentatives 🎉
{DELIMITER}"""
        else:
            display = f"{DELIMITER}\nIl s'en est fallu de peu !\nVous avez gagné en 10 tentatives 😅\n{DELIMITER}"

        print(display)

        time.sleep(3)
        self.retry()

    def failed(self) -> None:
        print(f"""{DELIMITER}
PERDU !
La bonne combinaison était {display_colors(self.combination)}
T'es MAUVAIS Jack 👎
{DELIMITER}""")
        time.sleep(3)
        self.retry()

    def retry(self) -> None:
        retry = input("Souhaitez-vous rejouer ? [Y/n] ").lower()
        if retry in ["y", "yes"]:
            game = Game(COUNTDOWN)
            game.play()
        elif retry in ["n", "no"]:
            print("A bientôt 👋")
            sys.exit()
        else:
            print("Entrée incorrecte...")
            self.retry()

    def play(self):
        print(MENU)
        while self.countdown > 0:
            logging.info(f" Combinaison gagnante : {display_colors(self.combination)}")
            self.guess = self.prompt_guess()
            evaluation = self.evaluate_guess()
            self.show_guess_result()
            self.countdown -= 1
            if evaluation:
                time.sleep(1)
                self.won()
            
            remaining_attemps = self.show_remaining_attemps()

        time.sleep(2)
        self.failed()


if __name__ == "__main__":
    pass
