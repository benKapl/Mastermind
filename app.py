
def print_red(skk): print(f"\033[91m {skk}\033[00m")
def print_green(skk): print("\033[92m {}\033[00m" .format(skk))
def print_yellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def print_purple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))

if __name__ == "__main__":
    prCyan("Hello World, ")
    print_yellow("coucou")
    print_purple("It's")
    prLightPurple("Geeks")


    