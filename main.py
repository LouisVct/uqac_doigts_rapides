
import pygame
import sys
from render import render_text, init_render


pygame.init()

police = "fonts/OpenDyslexic-Regular.otf"
W, H = 1080, 720
backgroundColor = "#FAF9F6"
fontColor = "black"
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Doigts rapide - test saisie")
font = pygame.font.Font(police, 35)

# Initialisation des paramètres par défaut pour render_text
init_render(surface=screen, font=font, color=fontColor, background=backgroundColor, pos=(20, 30))

input_text = ""
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(backgroundColor)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.TEXTINPUT:
            input_text += event.text
            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
                
    render_text(input_text)
    pygame.display.flip()

pygame.quit()
sys.exit()