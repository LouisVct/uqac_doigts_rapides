from enum import Enum
from clavier import ModeleClavier

class Level(Enum):
    EASY = "level_1"
    MEDIUM = "level_2"
    HARD = "level_3"

class Couleur(Enum):
    VERTE = (48, 209, 88)
    VERTE_CLAIRE = (120, 230, 145)

class Aide:
    def __init__(self, level: Level, clavier: ModeleClavier, couleur: Couleur):
        self.level = level
        self.clavier = clavier
        self.couleur = couleur

    def _couleurs_aide(self):
        return Couleur.VERTE.value, Couleur.VERTE_CLAIRE.value

    def erreur(self, lettre: str):
        if self.level != Level.EASY:
            return False

        couleur_principale, couleur_secondaire = self._couleurs_aide()
        touches = self.clavier.get_touches_aide(lettre)
        if not touches:
            return False

        touches[0].background_color = couleur_principale

        for touche in touches[1:]:
            touche.background_color = couleur_secondaire

        return True

        
        

    def reset_erreur(self, lettre: str):
        return self.clavier.reset_touches_background_pour_caractere(lettre)

