from enum import Enum

class Level(Enum):
    EASY = "level_1"
    MEDIUM = "level_2"
    HARD = "level_3"

class Couleur(Enum):
    VERTE = (48, 209, 88)
    ORANGE = (255, 170, 90)
    ROUGE = (255, 110, 110)

class Aide:
    def __init__(self, level: Level, clavier, couleur: Couleur):
        self.level = level
        self.clavier = clavier
        self.couleur = couleur

    def erreur(self, lettre: str):
        if self.level == Level.EASY:
            self.clavier.set_touche_background(lettre, Couleur.VERTE.value)
        elif self.level == Level.MEDIUM:
            self.clavier.set_touche_background(lettre, Couleur.ORANGE.value)
        else:
            self.clavier.set_touche_background(lettre, Couleur.ROUGE.value)
        

    def reset_erreur(self, lettre: str):
        self.clavier.reset_touche_background(lettre)

