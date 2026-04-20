import time

import pygame

from aide import Aide, Couleur
from app.constants import (
    DISPLAY_CLASSIC,
    DISPLAY_FOCUS,
    MODE_FILE,
    MODE_RANDOM_LETTERS,
    MODE_RANDOM_WORDS,
    RANDOM_MODES,
)
from modes import FournisseurLettresUniques, FournisseurMotsUniques, charger_texte_fichier
from moteur import MoteurExercice


IDLE_HELP_DELAY_SECONDS = 5


def display_mode_for(mode):
    if mode == MODE_FILE:
        return DISPLAY_CLASSIC
    return DISPLAY_FOCUS


class ModeTextProvider:
    def __init__(self, mode, text_file, words_file, random_words_limit):
        self.mode = mode
        self.text_file = text_file
        self.words_provider = None
        self.letters_provider = None

        if mode == MODE_RANDOM_WORDS:
            self.words_provider = FournisseurMotsUniques(words_file, limite=random_words_limit)
        elif mode == MODE_RANDOM_LETTERS:
            self.letters_provider = FournisseurLettresUniques()
        elif mode != MODE_FILE:
            raise ValueError(f"Mode inconnu: {mode}")

    def next_text(self):
        if self.mode == MODE_FILE:
            return charger_texte_fichier(self.text_file)
        if self.mode == MODE_RANDOM_WORDS:
            if self.words_provider is None:
                raise ValueError("Fournisseur de mots non initialise.")
            return self.words_provider.prochain()
        if self.mode == MODE_RANDOM_LETTERS:
            if self.letters_provider is None:
                raise ValueError("Fournisseur de lettres non initialise.")
            return self.letters_provider.prochain()
        raise ValueError(f"Mode inconnu: {self.mode}")


class SessionController:
    def __init__(
        self,
        surface,
        keyboard_zone,
        clock,
        screen_text,
        screen_keyboard,
        mode,
        aide_level,
        modele,
        text_provider,
        error_sound,
        finish_sound,
        font_path,
    ):
        self.surface = surface
        self.keyboard_zone = keyboard_zone
        self.clock = clock
        self.screen_text = screen_text
        self.screen_keyboard = screen_keyboard
        self.mode = mode
        self.text_provider = text_provider
        self.error_sound = error_sound
        self.finish_sound = finish_sound

        self.aide = Aide(aide_level, modele, Couleur.VERTE)
        self.display_mode = display_mode_for(mode)
        self.font_fin = pygame.font.Font(font_path, 22)

        self.moteur = MoteurExercice(self.text_provider.next_text())
        self.derniere_entree = time.monotonic()
        self.lettre_aide_active = None

        self.sequence_random_terminee = False
        self.element_random_comptabilise = False
        self.fautes_globales_random = 0
        self.temps_global_random = 0.0
        self.son_fin_joue = False

    def _on_erreur_saisie(self, attendu):
        if self.error_sound is not None:
            self.error_sound.play()

        if self.lettre_aide_active is not None and self.lettre_aide_active != attendu:
            self.aide.reset_erreur(self.lettre_aide_active)

        if self.aide.erreur(attendu):
            self.lettre_aide_active = attendu
            return

        self.lettre_aide_active = None

    def _handle_text_input(self, raw_entry):
        attendu_avant = self.moteur.caractere_attendu
        entry = raw_entry.lower() if self.mode in RANDOM_MODES else raw_entry

        self.moteur.traiter_entree(entry)
        self.derniere_entree = time.monotonic()

        if attendu_avant is None:
            return

        if entry == attendu_avant:
            if self.lettre_aide_active is not None:
                self.aide.reset_erreur(self.lettre_aide_active)
                self.lettre_aide_active = None
            return

        self._on_erreur_saisie(attendu_avant)

    def _update_idle_help(self):
        if self.moteur.est_termine:
            return

        if (time.monotonic() - self.derniere_entree) <= IDLE_HELP_DELAY_SECONDS:
            return

        attendu = self.moteur.caractere_attendu
        if attendu is None or self.lettre_aide_active == attendu:
            return

        if self.lettre_aide_active is not None:
            self.aide.reset_erreur(self.lettre_aide_active)

        if self.aide.erreur(attendu):
            self.lettre_aide_active = attendu
            return

        self.lettre_aide_active = None

    def _advance_random_sequence(self):
        if self.mode not in RANDOM_MODES:
            return
        if not self.moteur.est_termine or self.sequence_random_terminee:
            return

        if not self.element_random_comptabilise:
            self.fautes_globales_random += self.moteur.fautes
            self.temps_global_random += self.moteur.temps_ecoule
            self.element_random_comptabilise = True

        if self.lettre_aide_active is not None:
            self.aide.reset_erreur(self.lettre_aide_active)
            self.lettre_aide_active = None

        try:
            self.moteur = MoteurExercice(self.text_provider.next_text())
            self.derniere_entree = time.monotonic()
            self.element_random_comptabilise = False
        except StopIteration:
            self.sequence_random_terminee = True
            moteur_final = MoteurExercice("")
            moteur_final.fautes = self.fautes_globales_random
            moteur_final.start_time = 0.0
            moteur_final.end_time = self.temps_global_random
            self.moteur = moteur_final

    def _draw(self):
        screen_width, screen_height = self.surface.get_size()

        self.surface.fill((245, 243, 236))
        pygame.draw.rect(self.surface, (245, 243, 236), self.keyboard_zone)

        self.screen_text.draw(self.moteur, display_mode=self.display_mode)
        self.screen_keyboard.draw()

        if self.moteur.est_termine and not self.son_fin_joue:
            if self.finish_sound is not None:
                self.finish_sound.play()
            self.son_fin_joue = True

        if self.moteur.est_termine:
            msg = "Entree ou Espace: retour au hub"
            msg_fin = self.font_fin.render(msg, True, (60, 60, 60))
            self.surface.blit(msg_fin, msg_fin.get_rect(center=(screen_width // 2, int(screen_height * 0.46))))

        pygame.display.flip()

    def run(self):
        session_active = True
        application_active = True

        while session_active and application_active:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    application_active = False
                    session_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        application_active = False
                        session_active = False
                    elif self.moteur.est_termine and event.key in (
                        pygame.K_RETURN,
                        pygame.K_KP_ENTER,
                        pygame.K_SPACE,
                    ):
                        session_active = False
                elif event.type == pygame.TEXTINPUT and not self.moteur.est_termine:
                    self._handle_text_input(event.text)

            self._update_idle_help()
            self._advance_random_sequence()
            self._draw()

        return application_active
