import random

from assets import COLORS, COLOR_RESET, CARRE 

class Mastermind:
    def __init__(self) -> None:
        self.computer_combination = self.generate_combination()

    def generate_combination(self) -> tuple:
        """ Generate 4 random colors

        Returns:
            tuple: 4 ordered colors
        """
        return tuple([f"{random.choice(COLORS)} {CARRE} {COLOR_RESET}" for _ in range(4)])
    
    def display_combination(self, combination: tuple) -> str:
        display = ""
        for color in combination:
            display += color
        return display



if __name__ == "__main__":

    m = Mastermind()
    a = m.display_combination(m.computer_combination)
    print(a)