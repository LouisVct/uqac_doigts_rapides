import pygame

class ScreenKeyboard:
    def __init__(self, surface, modele_clavier):
        self.surface = surface
        self.modele = modele_clavier
        

        self.font_principale = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_secondaire = pygame.font.SysFont("Arial", 14, bold=True)
        
        # couleurs par défaut (si non présentes dans le fichier JSON)
        self.default_bg = (50, 50, 55)
        self.default_text = (255, 255, 255)

    def _calculer_geometrie(self):
        """
        C'est ici qu'on applique l'algorithme de tes photos !
        """
        largeur_ecran = self.surface.get_width()
        hauteur_ecran = self.surface.get_height()

        # le ratio physique
        ratio = self.modele.w_reel / self.modele.h_reel 

        # les dimensions maximales autorisées
        largeur_clavier_max = largeur_ecran * 0.97
        hauteur_clavier_max = hauteur_ecran * 0.60

        # ajuste le clavier à la zone disponible
        self.largeur_clavier = min(largeur_clavier_max, hauteur_clavier_max * ratio)
        self.hauteur_clavier = self.largeur_clavier / ratio

        # calcul du point de départ (X, Y) pour centrer le clavier en bas
        self.offset_x = (largeur_ecran - self.largeur_clavier) / 2
        self.offset_y = hauteur_ecran - self.hauteur_clavier - 20 # le 20 est pour la marge

        # Calcule la taille d'une unité en pixels
        self.unite_w = self.largeur_clavier / self.modele.w_reel
        self.unite_h = self.hauteur_clavier / self.modele.h_reel

    def draw(self):
        # On recalcule les dimensions à chaque frame 
        # pour s'adapter si la fenêtre change de taille !
        self._calculer_geometrie()

        y_actuel = self.offset_y

        # boucle sur la liste des lignes (pas sur dictionnaire)
        for ligne in self.modele.lignes_touches:
            x_actuel = self.offset_x
            
            # hauteur de la ligne (en pixels)
            h_ligne_reel = max(t.hauteur for t in ligne)
            hauteur_ligne_px = h_ligne_reel * self.unite_h

            for touche in ligne:
                
                largeur_px = touche.largeur * self.unite_w
                hauteur_px = touche.hauteur * self.unite_h

                est_enter = any(c.lower() == "enter" for c in touche.caracteres)
                padding_x = 2
                padding_y = 2
                if est_enter and touche.frame_color == 0:
                    padding_y = 0

                # création du rectangle (avec un padding de 2px pour séparer les touches)
                rect = pygame.Rect(
                    x_actuel + padding_x,
                    y_actuel + padding_y,
                    largeur_px - (2 * padding_x),
                    hauteur_px - (2 * padding_y)
                )
                
                # en vue d'une futur utiliation je sauvegarde le rectangle dans l'objet touche
                touche.rect = rect

                # couleur de fond
                couleur_fond = touche.background_color if touche.background_color else self.default_bg
                pygame.draw.rect(self.surface, couleur_fond, rect, border_radius=6)

                # bordure de la touche
                if touche.frame_color != 0:
                    c_bord = touche.frame_color if isinstance(touche.frame_color, tuple) else (20, 20, 25)
                    pygame.draw.rect(self.surface, c_bord, rect, width=2, border_radius=6)

                # affichage du texte
                c_texte = touche.text_color if touche.text_color != (0,0,0) else self.default_text
                
                if len(touche.caracteres) == 1:
                    # touche avec 1 caractère
                    txt_surf = self.font_principale.render(touche.caracteres[0].upper(), True, c_texte)
                    self.surface.blit(txt_surf, txt_surf.get_rect(center=rect.center))
                    
                elif len(touche.caracteres) == 2:
                    # touche avec + de 1 caractère
                    txt_bas = self.font_principale.render(touche.caracteres[0], True, c_texte)
                    self.surface.blit(txt_bas, txt_bas.get_rect(bottomleft=(rect.x + 8, rect.bottom - 5)))
                    
                    txt_haut = self.font_secondaire.render(touche.caracteres[1], True, c_texte)
                    self.surface.blit(txt_haut, txt_haut.get_rect(topleft=(rect.x + 8, rect.top + 5)))

                # la touche est poussé à droite
                x_actuel += largeur_px
            
            # on passe à la ligne suivante
            y_actuel += hauteur_ligne_px