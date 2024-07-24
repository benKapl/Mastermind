import logging
import random
import sys
import time

from assets import COLORS, combination_account, COLOR_RESET, SQUARE, WHITE_DOT, RED_DOT, DELIMITER, countdown, MENU

logging.basicConfig(level=logging.DEBUG)

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
        self.combination = []
        self.combination_state = combination_account
        self.generate_combination()
        self.combination_balance = combination_account
        self.guess = ""
        self.evaluation = []
        self.countdown = countdown

    @property
    def attempts(self):
        return 10 - self.countdown

    def generate_combination(self) -> None:
        """ Generate 4 random colors

        Returns:
            list: 4 colors
        """
        for _ in range(4):
            color = f"{random.choice(list(COLORS.values()))} {SQUARE} {COLOR_RESET}"
            self.combination.append(color)
            self.combination_state[color] += 1

        print(self.combination_state)
    
    def prompt_guess(self) -> str:
        """ Ask the player 4 digits, return the digits converted to colors
        """
        while True:
            self.guess = input("Veuillez saisir vos 4 chiffres pour les couleurs : ")
            if len(self.guess) == 4 and self.guess.isdigit():
                try:
                    return [f"{COLORS[number]} {SQUARE} {COLOR_RESET}" for number in self.guess] # type: ignore
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
                # In case of perfect match, add a red dot to self.evaluation
                self.evaluation.append(RED_DOT)
                self.combination_balance[color_guess] += 1

                if self.combination_balance[color_guess] > self.combination_state[color_guess]:
                    self.combination_balance[color_guess] -= 1
                    self.evaluation.remove(WHITE_DOT)

            elif color_guess in self.combination:
                logging.debug(f" Simple match: {display_colors(color_guess)}")

                if self.combination_balance[color_guess] < self.combination_state[color_guess]:
                     # In case of simple match, add a white dot to self.evaluation
                    self.evaluation.append(WHITE_DOT)

            else:
                logging.debug(" NO MATCH")
                
        # Sort indications to return the red dot first and display the result
        self.evaluation = sorted(self.evaluation)

        # If self evalutation contains 4 red dots, the game is won
        if self.evaluation == [RED_DOT, RED_DOT, RED_DOT, RED_DOT]:
            return True
        else:
            return False

    def show_guess_result(self) -> None:
        """ Display colors chosen by the player at each attemps and the result of evaluation
        """
        if self.evaluation:
            print(f"{display_colors(self.guess)}   Indicateurs : {'' ''.join(self.evaluation)}")
        else:
            print(f"{display_colors(self.guess)}  Aucune correspondance trouvée")

    def show_remaining_attemps(self) -> None:
        """ Display the number of remaining attemps
        """
        if self.countdown > 0:
            print(f"Il vous reste {self.countdown} tentative{'s.' if self.countdown > 1 else ' 😱'}\n")
        else:
            print("Vous n'avez plus de tentative 💀\n")

    def won(self) -> None:
        """ Display a message in case of win. The message depends on the number of attemps before winning
        Then propose the user to retry
        """
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
        self.retry()

    def failed(self) -> None:
        """ Display a message in case of failure 
        and prompt player to retry.
        """ 
        print(f"""{DELIMITER}
PERDU !
La bonne combinaison était {display_colors(self.combination)}
T'es MAUVAIS Jack 👎
{DELIMITER}""")
        time.sleep(3)
        self.retry()

    def retry(self) -> None:
        """ Prompt the user to retry the game. 
        If positive : creates a new game instance and start playing
        If negative : exit the program
        """
        retry = input("Souhaitez-vous rejouer ? [Y/n] ").lower()
        if retry in ["y", "yes"]:
            game = Game(countdown)
            game.play()
        elif retry in ["n", "no"]:
            print("A bientôt 👋")
            sys.exit()
        else:
            print("Entrée incorrecte...")
            self.retry()

    def play(self) -> None:
        """ Manage game workflow """

        print(MENU)
        while self.countdown > 0:
            # Display the expected result (change logging parameters to WARNING for a functionning program) 
            logging.info(f" Combinaison gagnante : {display_colors(self.combination)}")
            # Prompt the user to choose 4 colors
            self.guess = self.prompt_guess()

            # Evaluate proposal, display result and update countdown
            evaluation = self.evaluate_guess()
            self.show_guess_result()
            self.countdown -= 1

            # If the game is won
            if evaluation:
                time.sleep(1)
                self.won()
            
            remaining_attemps = self.show_remaining_attemps()

        # When countdown < 1, the game is lost
        time.sleep(2)
        self.failed()


if __name__ == "__main__":
    pass
