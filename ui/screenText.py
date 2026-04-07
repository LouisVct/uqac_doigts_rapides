import pygame


class ScreenText:
    # initialise l'affichage texte: surface, zone, police et couleurs
    def __init__(
        self,
        surface,
        zone_rect,
        font_path="assets/fonts/OpenDyslexic-Regular.otf",
        font_size=50,
        background_color="#FAF9F6",
        font_color="black",
        text_pos=(20, 30),
    ):
        self.surface = surface
        self.zone_rect = zone_rect
        self.background_color = background_color
        self.font_color = font_color
        self.font_path = font_path
        self.font_size = font_size
        self.font = pygame.font.Font(font_path, font_size)
        self.text_pos = text_pos

    # affiche le texte et le curseur; découpe en lignes et rend les caractères
    def draw(self, moteur, display_mode="classic"):
        pygame.draw.rect(self.surface, self.background_color, self.zone_rect)

        if display_mode == "focus":
            self._draw_focus(moteur)
        else:
            self._draw_classic(moteur)

    def _draw_classic(self, moteur):
        texte = moteur.texte
        index = moteur.index

        left_x = self.zone_rect.x + self.text_pos[0]
        top_y = self.zone_rect.y + self.text_pos[1]
        line_height = self.font.get_linesize()
        max_x = self.zone_rect.right - self.text_pos[0]

        # si l'exercice est terminé, on affiche le score final et on quitte l'affichage
        if moteur.est_termine:
            self._draw_score(moteur)
            return

        # on découpe le texte en lignes, en essayant de couper sur les espaces
        # ça évite d'avoir des mots cassés et des retours à la ligne bizarres
        # on va découper le texte en lignes en parcourant chaque caractère
        lines = []
        line_start = 0
        cursor_x = left_x
        last_space = -1
        i = 0
        n = len(texte)
        # boucle principale: parcourir tout le texte
        while i < n:
            ch = texte[i]
            # si on rencontre un retour à la ligne explicite, terminer la ligne
            if ch == "\n":
                lines.append((line_start, i + 1))
                line_start = i + 1
                cursor_x = left_x
                last_space = -1
                i += 1
                continue

            # mesurer la largeur du caractère
            ch_width = self.font.size(ch)[0]
            # si le caractère dépasse la largeur de la zone, il faut couper la ligne
            if cursor_x + ch_width > max_x and i > line_start:
                # si on a trouvé un espace sur la ligne, couper après cet espace
                if last_space >= line_start:
                    # couper après l'espace trouvé pour ne pas casser le mot
                    lines.append((line_start, last_space + 1))
                    line_start = last_space + 1
                    i = line_start
                else:
                    # pas d'espace: couper à la position courante
                    lines.append((line_start, i))
                    line_start = i
                cursor_x = left_x
                last_space = -1
                continue

            # mémoriser la position du dernier espace vu (utile pour couper proprement)
            if ch == " ":
                last_space = i

            cursor_x += ch_width
            i += 1

        # si du texte reste après la dernière coupe, l'ajouter comme dernière ligne
        if line_start <= n:
            lines.append((line_start, n))

        # déterminer sur quelle ligne se trouve le curseur (index)
        if not lines:
            # pas de lignes => texte vide
            current_line = 0
        else:
            safe_index = min(index, len(texte))
            current_line = 0
            for li, (start_i, end_i) in enumerate(lines):
                if start_i <= safe_index < end_i:
                    current_line = li
                    break
                if safe_index >= end_i:
                    current_line = li

        available_height = self.zone_rect.height - self.text_pos[1]
        max_lines = max(1, available_height // line_height)

        # on affiche la ligne du curseur en haut, puis les suivantes
        start_line = current_line
        end_line = min(len(lines), start_line + max_lines)

        prev_clip = self.surface.get_clip()
        self.surface.set_clip(self.zone_rect)

        # on dessine seulement les lignes visibles (celles qui tiennent dans la zone)
        for line_no in range(start_line, min(end_line, len(lines))):
            line_start, line_end = lines[line_no]
            cursor_x = left_x
            cursor_y = top_y + (line_no - start_line) * line_height

            # parcourir les caractères de la ligne pour les afficher
            i = line_start
            while i < line_end:
                ch = texte[i]
                # ignorer les sauts de ligne lors du rendu
                if ch == "\n":
                    i += 1
                    continue

                ch_width = self.font.size(ch)[0]

                # choisir couleur/arriére-plan selon l'état du caractère
                if i < index:
                    fg = (0, 140, 0)
                    bg = self.background_color
                elif i == index:
                    fg = (0, 0, 0)
                    bg = (200, 200, 200)
                else:
                    fg = (0, 0, 0)
                    bg = self.background_color

                txt_surf = self.font.render(ch, True, fg, bg)
                self.surface.blit(txt_surf, (cursor_x, cursor_y))
                cursor_x += ch_width
                i += 1

        self.surface.set_clip(prev_clip)

    def _draw_focus(self, moteur):
        if moteur.est_termine:
            self._draw_score(moteur)
            return

        texte = moteur.texte
        index = moteur.index
        deja_tape = texte[:index]
        reste = texte[index:]

        max_font_size = int(self.zone_rect.height * 0.68)
        max_font_size = max(max_font_size, self.font_size)
        font_size = max_font_size
        font_focus = pygame.font.Font(self.font_path, font_size)

        marge_x = 40
        max_width = self.zone_rect.width - (2 * marge_x)
        while font_size > self.font_size and font_focus.size(texte)[0] > max_width:
            font_size -= 4
            font_focus = pygame.font.Font(self.font_path, font_size)

        partie_ok = font_focus.render(deja_tape, True, (0, 140, 0), self.background_color)
        partie_ko = font_focus.render(reste, True, (0, 0, 0), self.background_color)

        total_width = partie_ok.get_width() + partie_ko.get_width()
        x_depart = self.zone_rect.centerx - (total_width // 2)
        y = self.zone_rect.centery - (font_focus.get_linesize() // 2)

        self.surface.blit(partie_ok, (x_depart, y))
        self.surface.blit(partie_ko, (x_depart + partie_ok.get_width(), y))

    # affiche l'écran de score final (fautes, temps)
    def _draw_score(self, moteur):
        prev_clip = self.surface.get_clip()
        self.surface.set_clip(self.zone_rect)

        lines = [
            "Score final",
            f"Fautes: {moteur.fautes}",
            f"Temps: {moteur.temps_ecoule:.1f} s",
        ]

        line_height = self.font.get_linesize()
        total_height = line_height * len(lines)
        start_y = self.zone_rect.centery - (total_height // 2)

        for i, line in enumerate(lines):
            txt_surf = self.font.render(line, True, (0, 0, 0), self.background_color)
            rect = txt_surf.get_rect(centerx=self.zone_rect.centerx, y=start_y + i * line_height)
            self.surface.blit(txt_surf, rect)

        self.surface.set_clip(prev_clip)
