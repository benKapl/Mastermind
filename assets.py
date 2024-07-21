# def print_red(text): print(f"\033[91m {text}\033[00m")
# def print_green(text): print(f"\033[92m {text}\033[00m")
# def print_yellow(text): print(f"\033[93m {text}\033[00m")
# def print_purple(text): print(f"\033[95m {text}\033[00m")
# def print_cyan(text): print(f"\033[96m {text}\033[00m")
# def print_white(text): print(f"\033[97m {text}\033[00m")

COLOR_RESET = "\033[00m"

RED = "\033[91m"
GREEN = "\033[0;32m"
YELLOW = "\033[93m"
PURPLE = "\033[95m" 
BLUE = "\033[0;34m"
WHITE = "\033[97m"

COLORS = (RED, GREEN, YELLOW, PURPLE, BLUE, WHITE)

CARRE = "\u25A0" # correspondant à ■
PASTILLE = "\u25CF" # correspondant à ●


MENU = """

"""

if __name__ == "__main__":
    print(f"{RED}{CARRE}", f"{BLUE}{PASTILLE}{COLOR_RESET}")
    print(COLORS)

