import logging
import random
import sys
import time

from assets import INTRO, COLORS, COLOR_RESET, SQUARE, WHITE_DOT, RED_DOT, DELIMITER, countdown, MENU

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

    @property
    def attempts(self):
        return 10 - self.countdown

    def generate_combination(self) -> list:
        """ Generate 4 random colors

        Returns:
            list: 4 colors
        """
        return [f"{random.choice(list(COLORS.values()))} {SQUARE} {COLOR_RESET}" for _ in range(4)]
    
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

    def count_perfect_matches(self) -> list:
        """ Count perfect match and return a list of the remaning colors to evaluate

        Returns:
            list: A list of two tuples : the remaning colors of the combination and the remaning colors of the guess
        """
        unperfect_matches = []
        color_mapping = list(zip(self.combination, self.guess))

        for color_pair in color_mapping:
            if color_pair[0] == color_pair[1]:
                logging.debug(f" PERFECT MATCH : {display_colors(color_pair[1])}")
                # In case of perfect match, add a red dot to self.evaluation
                self.evaluation.append(RED_DOT)
            else:
                unperfect_matches.append(color_pair)
        
        # Unzip unperfect_matches to get the two original list with the perfect matches removed
        return list(zip(*unperfect_matches))

    def count_simple_matches(self, remaining_colors: list) -> None:
        """Count simple matches from a list where color matching perfectly were removed

        Args:
            remaining_colors (list): colors that do not match perfectly
        """
        remaining_combination = list(remaining_colors[0])
        remaining_guess = list(remaining_colors[1])

        for color in remaining_guess:
            if color in remaining_combination:
                logging.debug(f" SIMPLE MATCH : {display_colors(color)}")                
                self.evaluation.append(WHITE_DOT)
                # remove color to avoir counting it twice
                remaining_combination.remove(color)
    
    def evaluate_guess(self) -> bool:
        """ Indicates the player how close from the combination his guess is
        Returns True if the guess equals the combination
        Returns False otherwise

        """
        self.evaluation.clear()    
        # Count perfect matches
        remaining_colors = self.count_perfect_matches()

        # If self evalutation contains 4 red dots, the game is won
        if self.evaluation == [RED_DOT, RED_DOT, RED_DOT, RED_DOT]:
            return True
        else:
            # If not all matches are perfect, count simple ones
            self.count_simple_matches(remaining_colors)
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
    print(INTRO)
    game = Game(countdown)
    game.play()