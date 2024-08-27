from enum import Enum
import logging
import random
import sys
import time

from colorama import Fore

logging.basicConfig(level=logging.WARNING)

class Constant(Enum):
    SQUARE = "\u25A0" # correspondant à ■
    DOT = "\u25CF" # correspondant à ●
    RED_DOT = Fore.RED + '\u25CF' + Fore.RESET
    DELIMITER = '*' * 29
    COUNTDOWN = "10"
    COLORS_NUMBER = "4"

class Message(Enum):
    INTRO = (f"{Fore.YELLOW}{Constant.DOT.value} {Fore.BLUE}{Constant.DOT.value} {Fore.RED}{Constant.DOT.value}{Fore.RESET} "
         f"JEU DU MASTERMIND {Fore.GREEN}{Constant.DOT.value} {Fore.WHITE}{Constant.DOT.value} {Fore.MAGENTA}{Constant.DOT.value}{Fore.RESET}\n"
f"""{Constant.DELIMITER.value}

Trouvez la bonne combinaison de {Constant.COLORS_NUMBER.value} couleurs secrètes que notre 'IA' aura généré.
A chaque couleur bien positionnée, vous aurez en retour un indicateur rouge.
A chaque couleur présente mais mal positionnée, vous aurez en retour un indicateur blanc.
Vous avez {Constant.COUNTDOWN.value} tentatives.""")

    MENU = f"\nEntrez votre combinaison secrète en utilisant les chiffres des couleurs disponibles." + \
f"\n[1]:{Fore.YELLOW} Jaune {Fore.RESET}   [2]:{Fore.BLUE} Bleu {Fore.RESET}"\
f"   [3]:{Fore.RED} Rouge {Fore.RESET}   [4]:{Fore.GREEN} Vert {Fore.RESET}" \
f"   [5]:{Fore.WHITE} Blanc {Fore.RESET}   [6]:{Fore.MAGENTA} Magenta {Fore.RESET}\n"
    

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
    COUNTDOWN = int(Constant.COUNTDOWN.value)
    COLORS_NUMBER = int(Constant.COLORS_NUMBER.value)
    
    COLORS = {
    "1": Fore.YELLOW,
    "2": Fore.BLUE,
    "3": Fore.RED,
    "4": Fore.GREEN,
    "5": Fore.WHITE,
    "6": Fore.MAGENTA
}

    def __init__(self) -> None:
        self.combination = self.generate_combination()
        self.guess = ""
        self.evaluation = []
        self.countdown = Game.COUNTDOWN
        self.finished = False

    @property
    def attempts(self):
        return 10 - self.countdown

    def generate_combination(self) -> list:
        """ Generate random colors equal to Game.COLORS_NUMBER

        Returns:
            list: N colors (N is equal to Game.COLORS_NUMBER)
        """
        return [f"{random.choice(list(Game.COLORS.values()))} {Constant.SQUARE.value} {Fore.RESET}" for _ in range(Game.COLORS_NUMBER)]
    
    def prompt_guess(self) -> str:
        """ Ask the player a number of digits equal to Game.COLORS_NUMBER, return the digits converted to colors
        """
        while True:
            self.guess = input(f"Veuillez saisir vos {Game.COLORS_NUMBER} chiffres pour les couleurs : ")
            # Check that user guess contains 4 digit characters all strictly below 7
            if len(self.guess) == Game.COLORS_NUMBER and self.guess.isdigit() and all(int(digit) < 7 for digit in self.guess):
                return [f"{Game.COLORS[number]} {Constant.SQUARE.value} {Fore.RESET}" for number in self.guess] # type: ignore
            else:
                print("Votre saisie est incorrecte...\n")

    def count_perfect_matches(self) -> list:
        """ Count perfect matches and return a list of the remaning colors to evaluate

        Returns:
            list: A list of two tuples : the colors of the combination and the colors of the guess 
                                         without the colors that perfectly matched
        """
        no_perfect_matches = []
        color_mapping = list(zip(self.combination, self.guess))

        for color_pair in color_mapping:
            if color_pair[0] == color_pair[1]:
                logging.debug(f" PERFECT MATCH : {display_colors(color_pair[1])}")
                # In case of perfect match, add a red dot to self.evaluation
                self.evaluation.append(Constant.RED_DOT.value)
            else:
                no_perfect_matches.append(color_pair)
        
        # Unzip no_perfect_matches to get the two original list without the colors that perfectly matched
        return list(zip(*no_perfect_matches))

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
                self.evaluation.append(Constant.DOT.value)
                # remove color to avoir counting it twice
                remaining_combination.remove(color)
    
    def evaluate_guess(self) -> bool:
        """ Indicates the player how close from the combination his guess is
        Returns True if the guess equals the combination
        Returns False otherwise

        """
        # Empty self.evaluation that might be filled with previous guessing attempts
        self.evaluation.clear()

        # Count perfect matches and store the remaining_colors in a variable
        remaining_colors = self.count_perfect_matches()

        # If self evalutation contains 4 red dots, the game is won
        if "".join(self.evaluation) == Constant.RED_DOT.value*4:
            return True
        else:
            # If not all matches are perfect, count simple ones
            self.count_simple_matches(remaining_colors)
            return False

    def show_guess_result(self) -> None:
        """ Display colors chosen by the player at each attemps and the result of evaluation
        """
        print(f"{display_colors(self.guess)}   Indicateurs : {'' ''.join(self.evaluation)}" if self.evaluation else f"{display_colors(self.guess)}  Aucune correspondance trouvée")

    def show_remaining_attemps(self) -> None:
        """ Display the number of remaining attemps
        """
        print(f"Il vous reste {self.countdown} tentative{'s.' if self.countdown > 1 else ' 😱'}\n" if self.countdown > 0 else "Vous n'avez plus de tentative 💀")

    def won(self) -> None:
        """ Displays a message in case of win. The message depends on the number of attemps before winning
        """
        if self.attempts == 1:
            display = f"""\n{Constant.DELIMITER.value}
FELICITATIONS 👏👏👏
Vous avez gagné du premier coup 😮
{Constant.DELIMITER.value}\n"""
        elif 2 <= self.attempts < 10:
            display = f"""\n{Constant.DELIMITER.value}
Bravo !
Vous avez gagné en {self.attempts} tentatives 🎉
{Constant.DELIMITER.value}\n"""
        else:
            display = f"\n{Constant.DELIMITER.value}\nIl s'en est fallu de peu !\nVous avez gagné en 10 tentatives 😅\n{Constant.DELIMITER.value}\n"

        print(display)

    def failed(self) -> None:
        """ Displays a message in case of failure.
        """ 
        print(f"""\n{Constant.DELIMITER.value}
PERDU !
La bonne combinaison était {display_colors(self.combination)}
T'es MAUVAIS Jack 👎
{Constant.DELIMITER.value}\n""")
        time.sleep(3)

    def play(self) -> None:
        """ Manage game workflow """

        print(Message.MENU.value)
        while self.countdown > 0:
            # Displays the expected result (change logging parameters to WARNING for a functionning program) 
            logging.info(f" Combinaison gagnante : {display_colors(self.combination)}")
            # Prompt the user to choose 4 colors
            self.guess = self.prompt_guess()

            # Evaluates proposal, displays result and updates countdown
            evaluation = self.evaluate_guess()
            self.show_guess_result()
            self.countdown -= 1

            # If the game is won
            if evaluation:
                time.sleep(1)
                self.won()
                break
            
            self.show_remaining_attemps()

        # if the combination was not found and the countdown < 1, the game is lost
        if not evaluation:
            time.sleep(2)
            self.failed()


if __name__ == "__main__":
    print(Message.INTRO.value)
    while True:
        game = Game().play()

        while True:
            retry = input("Souhaitez-vous rejouer ? [Y/n] ").lower()
            if retry in ["y", "yes"]:
                break
            elif retry in ["n", "no"]:
                print("A bientôt 👋")
                time.sleep(2)
                sys.exit()
            else:
                print("Entrée incorrecte...")
                continue
