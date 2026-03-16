import pygame
import sys
from clavier import ModeleClavier
from screenText import ScreenText
from screenKeyboard import ScreenKeyboard
from moteur import MoteurExercice
from modes import charger_texte_fichier, generer_texte_aleatoire


pygame.init()

info_screen = pygame.display.Info()

screen_width = info_screen.current_w

screen_height = info_screen.current_h

pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Doigts rapide - test saisie")

text_height = int(screen_height * 0.4)
keyboard_height = screen_height - text_height

text_zone = pygame.Rect(0, 0, screen_width, text_height)
keyboard_zone = pygame.Rect(0, text_height, screen_width, keyboard_height)

screen_text = ScreenText(surface=screen, zone_rect=text_zone)
modele = ModeleClavier("clavier.json")
screen_keyboard = ScreenKeyboard(surface=screen, modele_clavier=modele)

clock = pygame.time.Clock()
running = True

MODE = "file"
TEXT_FILE = "texte.txt"
RANDOM_LEN = 200

if MODE == "file":
	texte = charger_texte_fichier(TEXT_FILE)
else:
	texte = generer_texte_aleatoire(RANDOM_LEN)

moteur = MoteurExercice(texte)

while running:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.TEXTINPUT:
			moteur.traiter_entree(event.text)

	screen_text.draw(moteur)
	screen_keyboard.draw()
	pygame.display.flip()

pygame.quit()
sys.exit()
