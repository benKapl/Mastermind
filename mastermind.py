import random
import logging

from assets import COLORS, COLOR_RESET, CARRE, PASTILLE

logging.basicConfig(level=logging.WARNING,
					format='%(asctime)s - %(levelname)s - %(message)s')

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

    def __init__(self) -> None:
        self.combination = self.generate_combination()
        self.guess = ""
        self.evaluation = []
        self.countdown = 10
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
                    print("Votre saisie est incorrecte...")   
            else:
                print("Votre saisie est incorrecte...")
    
    def evaluate_guess(self) -> None:
        """ Indicates the player how close from the combination his guess is
        """
        self.evaluation.clear()      
        # Map colors to compare pairs  
        color_mapping = list(zip(self.combination, self.guess))

        for color_combination, color_guess in color_mapping:
            if color_combination == color_guess:
                logging.info(f"PERFECT MATCH : {display_colors(color_combination)} {display_colors(color_guess)}")
                self.evaluation.append(f"{COLORS['3']} {PASTILLE} {COLOR_RESET}")

            elif color_guess in self.combination:
                logging.info(f"Simple match: {display_colors(color_guess)}")
                self.evaluation.append(f"{COLORS['5']} {PASTILLE} {COLOR_RESET}")

            else:
                logging.info("NO MATCH")
                
        # Sort indications to return the red dot first and display the result
        self.evaluation = sorted(self.evaluation)
        # return f"Indicateurs: {'' ''.join(sorted(evaluation))}"

    def show_guess_result(self) -> None:
        if self.evaluation:
            print(f"{display_colors(self.guess)}   Indicateurs : {'' ''.join(self.evaluation)}")
        else:
            print(f"{display_colors(self.guess)}  Aucune correspondance trouvée")





if __name__ == "__main__":

    game = Game()

    combination = display_colors(game.combination)
    print(combination)


    game.guess = game.prompt_guess()
    game.evaluate_guess()
    print(game.guess)
    game.show_guess_result()


    # guess = ['\x1b[95m ■ \x1b[00m', '\x1b[95m ■ \x1b[00m', '\x1b[91m ■ \x1b[00m', '\x1b[97m ■ \x1b[00m']

    # combination = display_colors(game.combination)
    # b = display_colors(guess)


    # print(combination)
    # print(b)
                              
    # evaluation = game.evaluate_guess(guess)
    # print(display_colors(evaluation))