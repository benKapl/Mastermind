COLORS = {
    "1": "\033[93m",
    "2": "\033[0;34m",
    "3": "\033[91m",
    "4": "\033[0;32m",
    "5": "\033[97m",
    "6": "\033[95m"
}

COLOR_RESET = "\033[00m"

SQUARE = "\u25A0" # correspondant à ■
DOT = "\u25CF" # correspondant à ●

combination_account = {
    f"{COLORS['1']} {SQUARE} {COLOR_RESET}": 0,
    f"{COLORS['2']} {SQUARE} {COLOR_RESET}": 0,
    f"{COLORS['3']} {SQUARE} {COLOR_RESET}": 0,
    f"{COLORS['4']} {SQUARE} {COLOR_RESET}": 0,
    f"{COLORS['5']} {SQUARE} {COLOR_RESET}": 0,
    f"{COLORS['6']} {SQUARE} {COLOR_RESET}": 0
}

WHITE_DOT = f"{COLORS['5']} {DOT} {COLOR_RESET}"
RED_DOT = f"{COLORS['3']} {DOT} {COLOR_RESET}"

DELIMITER = '*' * 29
countdown = 10

INTRO = (f"{COLORS['1']}{DOT} {COLORS['2']}{DOT} {COLORS['3']}{DOT}{COLOR_RESET} "
         f"JEU DU MASTERMIND {COLORS['4']}{DOT} {COLORS['5']}{DOT} {COLORS['6']}{DOT}{COLOR_RESET}\n"
f"""{DELIMITER}

Trouvez la bonne combinaison de quatre couleurs secrètes que notre 'IA' aura généré.
A chaque couleur bien positionnée, vous aurez en retour un indicateur rouge.
A chaque couleur présente mais mal positionnée, vous aurez en retour un indicateur blanc.
Vous avez {countdown} tentatives.""")

MENU = f"\nEntrez votre combinaison secrète en utilisant les chiffres des couleurs disponibles." + \
f"\n[1]:{COLORS['1']} Jaune {COLOR_RESET}   [2]:{COLORS['2']} Bleu {COLOR_RESET}"\
f"   [3]:{COLORS['3']} Rouge {COLOR_RESET}   [4]:{COLORS['4']} Vert {COLOR_RESET}" \
f"   [5]:{COLORS['5']} Blanc {COLOR_RESET}   [6]:{COLORS['6']} Magenta {COLOR_RESET}\n"

if __name__ == "__main__":
    print(f"{COLORS['3']}{SQUARE}", f"{COLORS['2']}{DOT}{COLOR_RESET}")
    print(INTRO)