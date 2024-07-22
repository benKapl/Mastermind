import random

from assets import COLORS, COLOR_RESET, CARRE, PASTILLE, RED, WHITE

def display_colors(colors_unicode: list) -> str:
    display = ""
    for color in colors_unicode:
        display += color
    return display

class Game:
    def __init__(self) -> None:
        self.computer_combination = self.generate_combination()

    def generate_combination(self) -> list:
        """ Generate 4 random colors

        Returns:
            list: 4 colors
        """
        return [f"{random.choice(COLORS)} {CARRE} {COLOR_RESET}" for _ in range(4)]
    
    def evaluate_guess(self, guess):
    ### ATTENTION ###
    # Ne fonctionne pas lorsqu'il y a plusieurs fois la même couleur identiquement placée
    # exemple combinaison : rouge, rouge , noir, blanc
    # exemple tentative :   rouge, rouge, blanc, bleu
    # retournera :          pastille rouge, pastille blanc
    # AURAIT DU RETOURNER : pastille rouge, pastille rouge, pastille blanc


    # je zip la combinaison et le guess
        zipped_list = list(zip(self.computer_combination, guess))
        # je crée une liste dans laquelle j'incluerai les informations
        evaluation = []
        for color_combination, color_guess in zipped_list:
            # si j'ai la bonne couleur au bon endroit
            if color_combination == color_guess:
                print(f"PERFECT MATCH : {display_colors(color_combination)}, {display_colors(color_guess)}")
                # j'ajoute une pastille rouge dans ``information``
                evaluation.append(f"{RED} {PASTILLE} {COLOR_RESET}")
                # je retire la paire qui match parfaitement
                zipped_list.remove((color_combination, color_guess))
                print(f"Mise à jour des couleurs : {zipped_list}")
                continue
            else: 
                print("NO PERFECT MATCH")
        # je dezip les tuples pour comparer les couleurs restants
        self.computer_combination, guess = zip(*zipped_list)
        for color in guess:
            if color in self.computer_combination:
                print(f"Simple match: {display_colors(color)}")
                evaluation.append(f"{WHITE} {PASTILLE} {COLOR_RESET}")
        
        return evaluation




if __name__ == "__main__":

    game = Game()

    guess = ['\x1b[95m ■ \x1b[00m', '\x1b[95m ■ \x1b[00m', '\x1b[91m ■ \x1b[00m', '\x1b[97m ■ \x1b[00m']

    a = display_colors(game.computer_combination)
    b = display_colors(guess)


    print(a)
    print(b)
                              
    evaluation = game.evaluate_guess(guess)
    print(display_colors(evaluation))