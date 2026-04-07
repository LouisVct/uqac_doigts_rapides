
import pygame

# Variables globales pour les paramètres par défaut
_default_surface = None
_default_font = None
_default_color = "black"
_default_background = "#FAF9F6"
_default_pos = (20, 30)

def init_render(surface=None, font=None, color=None, background=None, pos=None):
	global _default_surface, _default_font, _default_color, _default_background, _default_pos
	if surface is not None:
		_default_surface = surface
	if font is not None:
		_default_font = font
	if color is not None:
		_default_color = color
	if background is not None:
		_default_background = background
	if pos is not None:
		_default_pos = pos

def render_text(text, surface=None, font=None, color=None, background=None, pos=None):
	s = surface if surface is not None else _default_surface
	f = font if font is not None else _default_font
	c = color if color is not None else _default_color
	b = background if background is not None else _default_background
	p = pos if pos is not None else _default_pos
	if s is None or f is None:
		raise ValueError("Surface et font doivent être définis soit via init_render soit à l'appel.")
	txt_surf = f.render(text, True, c, b)
	s.blit(txt_surf, p)
