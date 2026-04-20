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
        self._font_cache = {font_size: self.font}
        self.text_pos = text_pos

    # affiche le texte et le curseur; découpe en lignes et rend les caractères
    def draw(self, moteur, display_mode="classic"):
        pygame.draw.rect(self.surface, self.background_color, self.zone_rect)

        if display_mode == "focus":
            self._draw_focus(moteur)
        else:
            self._draw_classic(moteur)

    def _get_font(self, size):
        font = self._font_cache.get(size)
        if font is None:
            font = pygame.font.Font(self.font_path, size)
            self._font_cache[size] = font
        return font

    def _zone_textuelle(self):
        left_x = self.zone_rect.x + self.text_pos[0]
        top_y = self.zone_rect.y + self.text_pos[1]
        line_height = self.font.get_linesize()
        max_x = self.zone_rect.right - self.text_pos[0]
        return left_x, top_y, line_height, max_x

    def _decouper_lignes(self, texte, left_x, max_x):
        lines = []
        line_start = 0
        cursor_x = left_x
        last_space = -1
        i = 0
        n = len(texte)

        while i < n:
            ch = texte[i]
            if ch == "\n":
                lines.append((line_start, i + 1))
                line_start = i + 1
                cursor_x = left_x
                last_space = -1
                i += 1
                continue

            ch_width = self.font.size(ch)[0]
            if cursor_x + ch_width > max_x and i > line_start:
                if last_space >= line_start:
                    lines.append((line_start, last_space + 1))
                    line_start = last_space + 1
                    i = line_start
                else:
                    lines.append((line_start, i))
                    line_start = i
                cursor_x = left_x
                last_space = -1
                continue

            if ch == " ":
                last_space = i

            cursor_x += ch_width
            i += 1

        if line_start <= n:
            lines.append((line_start, n))

        return lines

    def _ligne_courante(self, lines, index, texte_len):
        if not lines:
            return 0

        safe_index = min(index, texte_len)
        current_line = 0
        for line_number, (line_start, line_end) in enumerate(lines):
            if line_start <= safe_index < line_end:
                return line_number
            if safe_index >= line_end:
                current_line = line_number

        return current_line

    def _couleurs_caractere(self, char_index, typed_index):
        if char_index < typed_index:
            return (0, 140, 0), self.background_color
        if char_index == typed_index:
            return (0, 0, 0), (200, 200, 200)
        return (0, 0, 0), self.background_color

    def _draw_classic(self, moteur):
        texte = moteur.texte
        index = moteur.index

        left_x, top_y, line_height, max_x = self._zone_textuelle()

        # si l'exercice est terminé, on affiche le score final et on quitte l'affichage
        if moteur.est_termine:
            self._draw_score(moteur)
            return

        lines = self._decouper_lignes(texte, left_x, max_x)
        current_line = self._ligne_courante(lines, index, len(texte))

        available_height = self.zone_rect.height - self.text_pos[1]
        max_lines = max(1, available_height // line_height)

        # on affiche la ligne du curseur en haut, puis les suivantes
        start_line = current_line
        end_line = min(len(lines), start_line + max_lines)

        prev_clip = self.surface.get_clip()
        self.surface.set_clip(self.zone_rect)

        # on dessine seulement les lignes visibles (celles qui tiennent dans la zone)
        for line_no in range(start_line, end_line):
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

                fg, bg = self._couleurs_caractere(i, index)
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
        font_focus = self._get_font(font_size)

        marge_x = 40
        max_width = self.zone_rect.width - (2 * marge_x)
        while font_size > self.font_size and font_focus.size(texte)[0] > max_width:
            font_size -= 4
            font_focus = self._get_font(font_size)

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
