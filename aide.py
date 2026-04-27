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

    def _touche_maj(self):
        for nom in ("maj gauche", "maj droit", "fix maj"):
            touche = self.clavier.get_touche(nom)
            if touche is not None:
                return touche
        return None

    def _touches_aide_pour_lettre(self, lettre: str):
        if not lettre:
            return []

        if lettre.isalpha() and lettre.isupper():
            touche_maj = self._touche_maj()
            touche_lettre = self.clavier.get_touche(lettre.lower())

            touches = []
            if touche_maj is not None:
                touches.append(touche_maj)
            if touche_lettre is not None:
                touches.append(touche_lettre)

            if touches:
                return touches

        return self.clavier.get_touches_aide(lettre)

    def erreur(self, lettre: str):
        if self.level != Level.EASY:
            return False

        couleur_principale, couleur_secondaire = self._couleurs_aide()
        touches = self._touches_aide_pour_lettre(lettre)
        if not touches:
            return False

        touches[0].background_color = couleur_principale

        for touche in touches[1:]:
            touche.background_color = couleur_secondaire

        return True

        
        

    def reset_erreur(self, lettre: str):
        touches = self._touches_aide_pour_lettre(lettre)
        if not touches:
            return False

        for touche in touches:
            touche.background_color = touche.default_background_color
        return True

