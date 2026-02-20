import pygame


class ScreenKeyboard:
    CLAVIER_DESIGN = [
        [("A", 1), ("Z", 1), ("E", 1), ("R", 1), ("T", 1), ("Y", 1), ("U", 1), ("I", 1), ("O", 1), ("P", 1)],
        [("Q", 1), ("S", 1), ("D", 1), ("F", 1), ("G", 1), ("H", 1), ("J", 1), ("K", 1), ("L", 1), ("M", 1)],
        [("MAJ", 1.5), ("W", 1), ("X", 1), ("C", 1), ("V", 1), ("B", 1), ("N", 1), ("ENTRÉE", 2)],
        [("ESPACE", 7)],
    ]

    def __init__(
        self,
        surface,
        zone_rect,
        key_color=(50, 50, 55),
        text_color=(255, 255, 255),
    ):
        self.surface = surface
        self.zone_rect = zone_rect
        self.key_color = key_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def draw(self):
        y_actuel = self.zone_rect.y
        hauteur_ligne = self.zone_rect.height / len(self.CLAVIER_DESIGN)

        for ligne in self.CLAVIER_DESIGN:
            total_tailles = sum(poids for _, poids in ligne)
            unite = self.zone_rect.width / total_tailles

            x_actuel = self.zone_rect.x
            for nom, taille in ligne:
                largeur_touche = unite * taille
                rect = pygame.Rect(x_actuel + 2, y_actuel + 2, largeur_touche - 4, hauteur_ligne - 4)

                pygame.draw.rect(self.surface, self.key_color, rect, border_radius=5)

                texte_surface = self.font.render(nom, True, self.text_color)
                texte_rect = texte_surface.get_rect(center=rect.center)
                self.surface.blit(texte_surface, texte_rect)

                x_actuel += largeur_touche

            y_actuel += hauteur_ligne