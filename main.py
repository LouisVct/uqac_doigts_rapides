import pygame
import sys


pygame.init()


police = "fonts/OpenDyslexic-Regular.otf"

W, H = 1080, 720
backgroundColor = "#FAF9F6"
fontColor = "black"
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Doigts rapide - test saisie")


font = pygame.font.Font(police, 35)

input_text = ""
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(backgroundColor)
    clock.tick(60) # écran 60 fps max, donc pas besoin plus

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.TEXTINPUT:
            input_text += event.text
            
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

    
    

    txt_surf = font.render(input_text, True, fontColor)
    screen.blit(txt_surf, (20, 30))

    pygame.display.flip()

pygame.quit()
sys.exit()