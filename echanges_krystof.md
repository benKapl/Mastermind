kapkap — 24/07/2024 21:28
Bon c'est un gros casse-tête cette règle ! 

Je ne vais pas avoir le temps de continuer davantage ce soir mais j'ai commit certains changements. J'ai commencé avec 2 dictionnaires combination_state, combination_balance (oui les noms de variable sont horribles,). Que je compare pour savoir si j'ajoute ou enlvèe des indicateurs blancs, mais pour l'instant ça ne fonctionne pas (j'ai bien les indicateurs rouge mais les indicateurs blancs ne sont pas systématiquement présent lorsque nécessaire).

J'y retourne demain.

Bonne soirée !

------------------------------------------

кяуѕтσƒ26 — 24/07/2024 22:23
En effet il y a un truc qui ne fonctionne pas dans le code

кяуѕтσƒ26 — 24/07/2024 22:45
L'idée de séparer les données (les constantes) du code à proprement parler est une bonne idée, mais pourquoi ne pas utiliser une classe qui hérite de enum.EnumStr ou bien des dataclasses, ou bien d'utiliser des instances de classe dans ta classe Game ?

De même pour la séparation entre app.py et mastermind.py, le if __main__ dans mastermind.py peut suffire. Bon, après ce n'est pas un gros problème, mais le code final peut tenir en une centaine de lignes, donc pas besoin d'avoir autant de fichiers.

кяуѕтσƒ26 — 24/07/2024 22:59
Pour les couleurs, je t'invite à voir de ce côté là : https://pypi.org/project/colorama/ . Cela va te permettre de créer un dictionnaire de couleurs, et de pouvoir gérer tes affichages avec à l'aide de la méthode join() quand tu travailleras sur tes listes.

Comment pourrais-tu éviter la répétition qui suit :
                except KeyError:
                    print("Votre saisie est incorrecte...\n")
            else:
                print("Votre saisie est incorrecte...\n")

кяуѕтσƒ26 — 24/07/2024 23:12
Le problème se situe bien à ce niveau :
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

L'idée serait d'évaluer si les pastilles de couleurs de l'utilisateur sont bien positionnées, puis d'évaluer si elles sont mal positionées. Mais Attention aux doublons

Allez un petit ternaire pour réduire tout ce qui suit : 😉 
# Sort indications to return the red dot first and display the result
        self.evaluation = sorted(self.evaluation)

        # If self evalutation contains 4 red dots, the game is won
        if self.evaluation == [RED_DOT, RED_DOT, RED_DOT, RED_DOT]:
            return True
        else:
            return False

Idem avec show_guess_result() et show_remaining_attemps() 

кяуѕтσƒ26 — 24/07/2024 23:19
A la place de :
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

je verrais plus simplement une boucle dans le if __main__
Je ne comprends pas ce que tu as voulu faire avec cette variable :
remaining_attemps = self.show_remaining_attemps()

car je ne la vois utilisée nulle part
Ceci peut se réduire à une seule instruction :
game = Game(countdown)
game.play()

Bon, voilà le retour global que je peux te faire. Si des choses ne te paraissent pas claires dans mes explications, n'hésite pas à me solliciter

--------------------------------------------

kapkap — 25/07/2024 13:06
Super merci pour tout tes retours, je vais modifier tout ça.

Pour info je suis en plein déménagement puis départ en vacances, donc je ne sais pas si j'arriverais à tout modifier d'ici la fin du challenge. Mais je vais conserver tout ça quelque part pour reprendre à mon retour si jamais.
Seul élément que j'ai n'ai pas totalement compris, ton premier retour : 

L'idée de séparer les données (les constantes) du code à proprement parler est une bonne idée, mais pourquoi ne pas utiliser une classe qui hérite de enum.EnumStr ou bien des dataclasses, ou bien d'utiliser des instances de classe dans ta classe Game ?
Je n'ai pas compris la partie sur enum.EnumStr ou l'utilisation des instances de classe. Tu veux dire créer plusieurs instances de Game ? 


---------------------------------------------

кяуѕтσƒ26 — 25/07/2024 13:16
EnumStr est une classe du module enum. Je t'invite à te renseigner. Cela peut-être intéressant pour des constantes de type chaînes de caractères.

Instances de classe... pardon, je voulais dire attributs de classe.

L'idée, pour ce code serait d'avoir les constantes dans le même fichier. Comme je disais, le code peut-être écrit en une centaine de lignes (constantes comprises), il  n'y a donc pas nécessité à démultiplier les fichiers. Autant faire simple  : Simple is better than complex dit le zen de Python 😉

Pas de souci par rapport au temps. A l'issue de cette quinzaine nous enchaînons avec les codes passés, donc si tu le souhaites nous pourrons poursuivre 15 jours de plus