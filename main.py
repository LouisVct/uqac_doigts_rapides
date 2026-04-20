from pathlib import Path

import pygame

from app.configuration_screen import run_configuration_screen, show_blocking_message
from app.session_controller import ModeTextProvider, SessionController
from clavier import ModeleClavier
from screenKeyboard import ScreenKeyboard
from screenText import ScreenText


PROJECT_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
SONGS_DIR = ASSETS_DIR / "songs"
CONTENTS_DIR = ASSETS_DIR / "contents"

FONT_REGULAR = FONTS_DIR / "OpenDyslexic-Regular.otf"
KEYBOARD_LAYOUT_FILE = PROJECT_ROOT / "clavier.json"
TEXT_FILE = CONTENTS_DIR / "texte.txt"
WORDS_FILE = CONTENTS_DIR / "mots.txt"
ERROR_SOUND_FILE = SONGS_DIR / "error.wav"
FINISH_SOUND_FILE = SONGS_DIR / "aplause.wav"

WINDOW_TITLE = "Doigts rapide - test saisie"
RANDOM_WORDS_PER_SESSION = 30


def init_pygame():
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass


def create_fullscreen_window():
    info_screen = pygame.display.Info()
    screen_width = info_screen.current_w
    screen_height = info_screen.current_h
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption(WINDOW_TITLE)
    return screen, screen_width, screen_height


def load_sound(path, volume=0.7):
    try:
        sound = pygame.mixer.Sound(str(path))
        sound.set_volume(volume)
        return sound
    except (pygame.error, FileNotFoundError):
        return None


def main():
    init_pygame()
    screen, screen_width, screen_height = create_fullscreen_window()
    clock = pygame.time.Clock()

    font_path = str(FONT_REGULAR) if FONT_REGULAR.exists() else None

    text_height = int(screen_height * 0.4)
    keyboard_height = screen_height - text_height
    text_zone = pygame.Rect(0, 0, screen_width, text_height)
    keyboard_zone = pygame.Rect(0, text_height, screen_width, keyboard_height)

    screen_text = ScreenText(surface=screen, zone_rect=text_zone, font_path=font_path)
    modele = ModeleClavier(str(KEYBOARD_LAYOUT_FILE))
    screen_keyboard = ScreenKeyboard(surface=screen, modele_clavier=modele)

    son_erreur = load_sound(ERROR_SOUND_FILE)
    son_fin = load_sound(FINISH_SOUND_FILE)

    application_active = True
    while application_active:
        selection = run_configuration_screen(screen, clock, font_path)
        if selection is None:
            break

        mode, aide_level = selection
        try:
            fournisseur_texte = ModeTextProvider(
                mode=mode,
                text_file=TEXT_FILE,
                words_file=WORDS_FILE,
                random_words_limit=RANDOM_WORDS_PER_SESSION,
            )
            session = SessionController(
                surface=screen,
                keyboard_zone=keyboard_zone,
                clock=clock,
                screen_text=screen_text,
                screen_keyboard=screen_keyboard,
                mode=mode,
                aide_level=aide_level,
                modele=modele,
                text_provider=fournisseur_texte,
                error_sound=son_erreur,
                finish_sound=son_fin,
                font_path=font_path,
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            application_active = show_blocking_message(
                surface=screen,
                clock=clock,
                font_path=font_path,
                title="Erreur de configuration",
                message=str(exc),
            )
            continue

        application_active = session.run()

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
