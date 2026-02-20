import pygame


class ScreenText:
    def __init__(
        self,
        surface,
        zone_rect,
        font_path="fonts/OpenDyslexic-Regular.otf",
        font_size=50,
        background_color="#FAF9F6",
        font_color="black",
        text_pos=(20, 30),
    ):
        self.surface = surface
        self.zone_rect = zone_rect
        self.background_color = background_color
        self.font_color = font_color
        self.font = pygame.font.Font(font_path, font_size)
        self.text_pos = text_pos

    def draw(self, text):
        pygame.draw.rect(self.surface, self.background_color, self.zone_rect)

        txt_surf = self.font.render(text, True, self.font_color, self.background_color)
        x = self.zone_rect.x + self.text_pos[0]
        y = self.zone_rect.y + self.text_pos[1]
        self.surface.blit(txt_surf, (x, y))