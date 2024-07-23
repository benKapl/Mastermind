YELLOW_1 = "\033[93m"
BLUE_2 = "\033[0;34m"
RED_3 = "\033[91m"
GREEN_4 = "\033[0;32m"

PURPLE_6 = "\033[95m" 

WHITE_5 = "\033[97m"

COLORS = {
    "1": "\033[93m",
    "2": "\033[0;34m",
    "3": "\033[91m",
    "4": "\033[0;32m",
    "5": "\033[97m",
    "6": "\033[95m"
}

COLOR_RESET = "\033[00m"

CARRE = "\u25A0" # correspondant à ■
PASTILLE = "\u25CF" # correspondant à ●


MENU = f"""JEU DU MASTERMIND
Trouvez la bonne combinaison de quatre couleurs secrètes que notre 'IA' aura généré.
A chaque couleur bien postionnée, vous aurez en retour un indicateur rouge.
A chaque couleur présente mais mal positionnée, vous aurez en retour un indicateur blanc.
Entrez votre combinaison secrète en utilisant les chiffres des couleurs disponibles.""" + \
f"\n[1]:{COLORS['1']} Jaune {COLOR_RESET}   [2]:{COLORS['2']} Bleu {COLOR_RESET}"\
f"   [3]:{COLORS['3']} Rouge {COLOR_RESET}   [4]:{COLORS['4']} Vert {COLOR_RESET}" \
f"   [5]:{COLORS['5']} Blanc {COLOR_RESET}   [6]:{COLORS['6']} Magenta {COLOR_RESET}\n"

if __name__ == "__main__":
    print(f"{COLORS['3']}{CARRE}", f"{COLORS['2']}{PASTILLE}{COLOR_RESET}")
    print(MENU)