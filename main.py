import pygame
import sys
import time
import os
from core.clavier import ModeleClavier
from ui.screenText import ScreenText
from ui.screenKeyboard import ScreenKeyboard
from core.moteur import MoteurExercice
from app.modes import (
	charger_texte_fichier,
	FournisseurLettresUniques,
	FournisseurMotsUniques,
)
from core.aide import Aide, Level, Couleur


pygame.init()

try:
	pygame.mixer.init()
except pygame.error:
	pass

info_screen = pygame.display.Info()

screen_width = info_screen.current_w

screen_height = info_screen.current_h

pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Doigts rapide - test saisie")

DISPLAY_CLASSIC = "classic"
DISPLAY_FOCUS = "focus"
ASSETS_DIR = "assets"
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
SONGS_DIR = os.path.join(ASSETS_DIR, "songs")
CONTENTS_DIR = os.path.join(ASSETS_DIR, "contents")
FONT_REGULAR = os.path.join(FONTS_DIR, "OpenDyslexic-Regular.otf")


def ecran_configuration(surface, clock):
	font_titre = pygame.font.Font(FONT_REGULAR, 56)
	font_sous_titre = pygame.font.Font(FONT_REGULAR, 24)
	font_section = pygame.font.Font(FONT_REGULAR, 30)
	font_option = pygame.font.Font(FONT_REGULAR, 24)
	font_info = pygame.font.Font(FONT_REGULAR, 21)

	mode_options = [
		("file", "Texte du fichier"),
		("random_words", "Mots aleatoires"),
		("random_letters", "Lettres aleatoires"),
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

		for i, (_, libelle) in enumerate(options):
			rect = pygame.Rect(
				marge_x + i * (largeur_carte + espace),
				y_cartes,
				largeur_carte,
				hauteur_carte,
			)

			est_selection = i == index_selection
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
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
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

		titre = font_titre.render("Hub de demarrage", True, (28, 28, 28))
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

text_height = int(screen_height * 0.4)
keyboard_height = screen_height - text_height

text_zone = pygame.Rect(0, 0, screen_width, text_height)
keyboard_zone = pygame.Rect(0, text_height, screen_width, keyboard_height)

screen_text = ScreenText(surface=screen, zone_rect=text_zone)
modele = ModeleClavier("clavier.json")
screen_keyboard = ScreenKeyboard(surface=screen, modele_clavier=modele)

clock = pygame.time.Clock()
TEXT_FILE = os.path.join(CONTENTS_DIR, "texte.txt")
WORDS_FILE = os.path.join(CONTENTS_DIR, "mots.txt")
RANDOM_WORDS_PER_SESSION = 30


def affichage_actif(mode):
	if mode == "file":
		return DISPLAY_CLASSIC
	return DISPLAY_FOCUS

son_erreur = None
son_fin = None
try:
	chemin_son_erreur = os.path.join(SONGS_DIR, "error.wav")
	son_erreur = pygame.mixer.Sound(chemin_son_erreur)
	son_erreur.set_volume(0.7)
except (pygame.error, FileNotFoundError):
	son_erreur = None

try:
	chemin_son_fin = os.path.join(SONGS_DIR, "aplause.wav")
	son_fin = pygame.mixer.Sound(chemin_son_fin)
	son_fin.set_volume(0.7)
except (pygame.error, FileNotFoundError):
	son_fin = None

application_active = True

while application_active:
	MODE, AIDE_LEVEL = ecran_configuration(screen, clock)
	fournisseur_mots = None
	fournisseur_lettres = None

	if MODE == "random_words":
		fournisseur_mots = FournisseurMotsUniques(WORDS_FILE, limite=RANDOM_WORDS_PER_SESSION)
	elif MODE == "random_letters":
		fournisseur_lettres = FournisseurLettresUniques()

	def generer_texte_pour_mode(mode):
		if mode == "file":
			return charger_texte_fichier(TEXT_FILE)
		if mode == "random_words":
			if fournisseur_mots is None:
				raise ValueError("Fournisseur de mots non initialise.")
			return fournisseur_mots.prochain()
		if mode == "random_letters":
			if fournisseur_lettres is None:
				raise ValueError("Fournisseur de lettres non initialise.")
			return fournisseur_lettres.prochain()
		raise ValueError(f"Mode inconnu: {mode}")

	texte = generer_texte_pour_mode(MODE)
	moteur = MoteurExercice(texte)
	aide = Aide(AIDE_LEVEL, modele, Couleur.VERTE)

	derniere_entree = time.monotonic()
	lettre_aide_active = None
	sequence_random_terminee = False
	fautes_globales_random = 0
	temps_global_random = 0.0
	element_random_comptabilise = False
	session_active = True
	son_fin_joue = False

	while session_active and application_active:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				application_active = False
				session_active = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					application_active = False
					session_active = False
				elif moteur.est_termine and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
					session_active = False
			elif event.type == pygame.TEXTINPUT and not moteur.est_termine:
				attendu_avant = moteur.caractere_attendu
				entree = event.text
				if MODE in ("random_words", "random_letters"):
					entree = event.text.lower()

				moteur.traiter_entree(entree)
				derniere_entree = time.monotonic()

				if attendu_avant is not None:
					if entree == attendu_avant:
						if lettre_aide_active is not None:
							aide.reset_erreur(lettre_aide_active)
							lettre_aide_active = None
					else:
						if son_erreur is not None:
							son_erreur.play()
						if lettre_aide_active is not None and lettre_aide_active != attendu_avant:
							aide.reset_erreur(lettre_aide_active)
						if aide.erreur(attendu_avant):
							lettre_aide_active = attendu_avant
						else:
							lettre_aide_active = None

		if not moteur.est_termine and (time.monotonic() - derniere_entree) > 5:
			attendu = moteur.caractere_attendu
			if attendu is not None and lettre_aide_active != attendu:
				if lettre_aide_active is not None:
					aide.reset_erreur(lettre_aide_active)
				if aide.erreur(attendu):
					lettre_aide_active = attendu
				else:
					lettre_aide_active = None

		if MODE in ("random_words", "random_letters") and moteur.est_termine and not sequence_random_terminee:
			if not element_random_comptabilise:
				fautes_globales_random += moteur.fautes
				temps_global_random += moteur.temps_ecoule
				element_random_comptabilise = True

			if lettre_aide_active is not None:
				aide.reset_erreur(lettre_aide_active)
				lettre_aide_active = None
			try:
				moteur = MoteurExercice(generer_texte_pour_mode(MODE))
				derniere_entree = time.monotonic()
				element_random_comptabilise = False
			except StopIteration:
				sequence_random_terminee = True
				moteur_final = MoteurExercice("")
				moteur_final.fautes = fautes_globales_random
				moteur_final.start_time = 0.0
				moteur_final.end_time = temps_global_random
				moteur = moteur_final

		screen.fill((245, 243, 236))
		pygame.draw.rect(screen, (245, 243, 236), keyboard_zone)
		screen_text.draw(moteur, display_mode=affichage_actif(MODE))
		screen_keyboard.draw()

		if moteur.est_termine and not son_fin_joue:
			if son_fin is not None:
				son_fin.play()
			son_fin_joue = True

		if moteur.est_termine:
			font_fin = pygame.font.Font(FONT_REGULAR, 22)
			msg_fin = font_fin.render("Entree ou Espace: retour au hub", True, (60, 60, 60))
			screen.blit(msg_fin, msg_fin.get_rect(center=(screen_width // 2, int(screen_height * 0.46))))

		pygame.display.flip()

pygame.quit()
sys.exit()
