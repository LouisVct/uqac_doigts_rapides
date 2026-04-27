import pygame

from aide import Level
from app.constants import MODE_FILE, MODE_RANDOM_LETTERS, MODE_RANDOM_WORDS


def _build_font(font_path, size):
    try:
        return pygame.font.Font(font_path, size)
    except (FileNotFoundError, OSError):
        return pygame.font.Font(None, size)


def _wrap_text(text, font, max_width):
    if not text:
        return [""]

    words = text.split()
    if not words:
        return [""]

    lines = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
            continue
        lines.append(current)
        current = word
    lines.append(current)
    return lines


def run_configuration_screen(surface, clock, font_path):
    screen_width, screen_height = surface.get_size()

    font_titre = _build_font(font_path, 56)
    font_sous_titre = _build_font(font_path, 24)
    font_section = _build_font(font_path, 30)
    font_option = _build_font(font_path, 24)
    font_info = _build_font(font_path, 21)

    mode_options = [
        (MODE_FILE, "Texte du fichier"),
        (MODE_RANDOM_WORDS, "Mots aleatoires"),
        (MODE_RANDOM_LETTERS, "Lettres aleatoires"),
    ]
    aide_options = [
        (Level.EASY, "Niveau 1 (aide active)"),
        (Level.MEDIUM, "Niveau 2"),
        (Level.HARD, "Niveau 3"),
    ]

    selection_ligne = 0
    mode_index = 0
    aide_index = 0

    def dessiner_fond_hub():
        surface.fill((243, 240, 231))
        en_tete = pygame.Rect(0, 0, screen_width, int(screen_height * 0.22))
        pygame.draw.rect(surface, (232, 227, 214), en_tete)

    def dessiner_groupe_options(y_top, titre, options, index_selection, groupe_actif):
        titre_couleur = (20, 110, 56) if groupe_actif else (58, 58, 58)
        titre_surf = font_section.render(titre, True, titre_couleur)
        surface.blit(titre_surf, (int(screen_width * 0.08), y_top))

        marge_x = int(screen_width * 0.08)
        largeur_zone = int(screen_width * 0.84)
        y_cartes = y_top + 48
        nb_options = len(options)
        espace = max(12, int(screen_width * 0.015))
        largeur_carte = (largeur_zone - (espace * (nb_options - 1))) // nb_options
        hauteur_carte = int(screen_height * 0.12)

        for index_option, (_, libelle) in enumerate(options):
            rect = pygame.Rect(
                marge_x + index_option * (largeur_carte + espace),
                y_cartes,
                largeur_carte,
                hauteur_carte,
            )

            est_selection = index_option == index_selection
            if est_selection:
                fond = (28, 127, 67)
                bord = (23, 94, 51)
                texte = (248, 248, 248)
            elif groupe_actif:
                fond = (252, 251, 246)
                bord = (118, 155, 126)
                texte = (36, 36, 36)
            else:
                fond = (248, 245, 237)
                bord = (190, 185, 172)
                texte = (60, 60, 60)

            pygame.draw.rect(surface, fond, rect, border_radius=14)
            pygame.draw.rect(surface, bord, rect, width=3, border_radius=14)

            label = font_option.render(libelle, True, texte)
            surface.blit(label, label.get_rect(center=rect.center))

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key in (pygame.K_UP, pygame.K_w):
                    selection_ligne = (selection_ligne - 1) % 2
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    selection_ligne = (selection_ligne + 1) % 2
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    if selection_ligne == 0:
                        mode_index = (mode_index - 1) % len(mode_options)
                    else:
                        aide_index = (aide_index - 1) % len(aide_options)
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    if selection_ligne == 0:
                        mode_index = (mode_index + 1) % len(mode_options)
                    else:
                        aide_index = (aide_index + 1) % len(aide_options)
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    return mode_options[mode_index][0], aide_options[aide_index][0]

        dessiner_fond_hub()

        titre = font_titre.render("Bienvenue", True, (28, 28, 28))
        sous_titre = font_sous_titre.render("Selectionne un mode puis un niveau d'aide", True, (88, 88, 88))
        surface.blit(titre, titre.get_rect(center=(screen_width // 2, int(screen_height * 0.10))))
        surface.blit(sous_titre, sous_titre.get_rect(center=(screen_width // 2, int(screen_height * 0.17))))

        dessiner_groupe_options(
            y_top=int(screen_height * 0.30),
            titre="Mode",
            options=mode_options,
            index_selection=mode_index,
            groupe_actif=(selection_ligne == 0),
        )

        dessiner_groupe_options(
            y_top=int(screen_height * 0.56),
            titre="Niveau d'aide",
            options=aide_options,
            index_selection=aide_index,
            groupe_actif=(selection_ligne == 1),
        )

        info_1 = font_info.render("Haut/Bas: changer de section   Gauche/Droite: choisir", True, (68, 68, 68))
        info_2 = font_info.render("Entree/Espace: lancer   Esc: quitter", True, (68, 68, 68))
        surface.blit(info_1, info_1.get_rect(center=(screen_width // 2, int(screen_height * 0.90))))
        surface.blit(info_2, info_2.get_rect(center=(screen_width // 2, int(screen_height * 0.94))))

        pygame.display.flip()


def show_blocking_message(surface, clock, font_path, title, message):
    screen_width, screen_height = surface.get_size()
    font_titre = _build_font(font_path, 42)
    font_message = _build_font(font_path, 24)
    font_info = _build_font(font_path, 21)

    message_lines = []
    max_width = int(screen_width * 0.70)
    for paragraph in message.splitlines() or [message]:
        message_lines.extend(_wrap_text(paragraph, font_message, max_width))

    if not message_lines:
        message_lines = ["Une erreur inconnue est survenue."]

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    return True

        surface.fill((243, 240, 231))
        panel = pygame.Rect(
            int(screen_width * 0.12),
            int(screen_height * 0.20),
            int(screen_width * 0.76),
            int(screen_height * 0.58),
        )
        pygame.draw.rect(surface, (252, 251, 246), panel, border_radius=16)
        pygame.draw.rect(surface, (190, 185, 172), panel, width=3, border_radius=16)

        titre_surface = font_titre.render(title, True, (130, 28, 28))
        surface.blit(titre_surface, titre_surface.get_rect(center=(screen_width // 2, int(screen_height * 0.31))))

        line_height = font_message.get_linesize()
        block_height = line_height * len(message_lines)
        start_y = int(screen_height * 0.40) - (block_height // 2)
        for line_number, line in enumerate(message_lines):
            text_surface = font_message.render(line, True, (40, 40, 40))
            y = start_y + line_number * line_height
            surface.blit(text_surface, text_surface.get_rect(center=(screen_width // 2, y)))

        info_text = "Entree/Espace: retour au hub   Esc: quitter"
        info_surface = font_info.render(info_text, True, (68, 68, 68))
        surface.blit(info_surface, info_surface.get_rect(center=(screen_width // 2, int(screen_height * 0.70))))

        pygame.display.flip()
