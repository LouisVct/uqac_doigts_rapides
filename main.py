import pygame
import sys
from clavier import ModeleClavier
from screenText import ScreenText
from screenKeyboard import ScreenKeyboard


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
input_text = ""

while running:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		elif event.type == pygame.TEXTINPUT:
			input_text += event.text
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
			input_text = input_text[:-1]

	screen_text.draw(input_text)
	screen_keyboard.draw()
	pygame.display.flip()

pygame.quit()
sys.exit()