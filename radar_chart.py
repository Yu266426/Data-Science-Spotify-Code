import pygbase

import pygame
import pygame.gfxdraw

from datascience import *

from draw_utils import draw_thick_circle


class RadarChart:
	CATEGORIES = ["danceability", "energy", "acousticness", "instrumentalness", "liveness", "valence", "mode"]
	
	SCALE_FACTORS = {
		"time_signature": 5
	}

	PLOT_COLOR_OUTER = (255, 255, 255)
	PLOT_COLOR_INNER = (220, 220, 220)
	PLOT_COLOR_RADIAL = (200, 200, 200)

	TEXT_COLOR = (255, 255, 255)

	DATA_COLOR_OUTLINE = (12, 108, 235)
	DATA_COLOR_FILL = (156, 212, 240)

	def __init__(self, pos: tuple, data: dict[str, Table], *playlist_names: str, radius: int = 280, alpha: float = -1) -> None:
		self.pos = pygame.Vector2(pos)
		self.radius = radius
		self.alpha = alpha if alpha != -1 else 1 / len(playlist_names)

		# Plot
		self.plot_surface = pygame.Surface((radius * 2.2, radius * 2.2), flags=pygame.SRCALPHA)
		self.angles: list[int] = [a for a in range(0, 360, int(360 / len(self.CATEGORIES)))][:len(self.CATEGORIES)]

		self.texts: list[pygbase.ui.text.Text] = []
		for index, category in enumerate(self.CATEGORIES):
			self.texts.append(
			    pygbase.ui.text.Text(self.pos + pygame.Vector2(0, self.radius + 60).rotate(self.angles[index]),
			         "arial",
			         20,
			         self.TEXT_COLOR,
			         text=category,
			         alignment=pygbase.ui.text.UIAlignment.CENTER,
			         use_sys=True))

		# Data vis
		self.data_vis_surface = pygame.Surface((radius * 2, radius * 2), flags=pygame.SRCALPHA)

		self.num_playlists = len(playlist_names)
		self.playlists: list[Table] = [data[playlist_name] for playlist_name in playlist_names]

		self.playlist_lengths = [playlist.num_rows for playlist in self.playlists]
		self.max_playlist_length = max(self.playlist_lengths)

		self.percentage_played = 0.0

	def set_percentage_played(self, amount: float):
		self.percentage_played = pygame.math.clamp(amount, 0, 1 - 1 / self.max_playlist_length)

	def animate(self, amount: float):
		self.percentage_played += amount

		self.percentage_played = pygame.math.clamp(self.percentage_played, 0, 1 - 1 / self.max_playlist_length)

	def _get_index(self, playlist_index: int):
		return int(self.percentage_played * self.playlist_lengths[playlist_index])

	def _get_index_float(self, playlist_index: int):
		return self.percentage_played * self.playlist_lengths[playlist_index]

	def draw(self, surface: pygame.Surface, aa_enabled: bool = True) -> None:
		# Data
		for playlist_index in range(self.num_playlists):
			# Generate points
			data_outline = []
			for index, category in enumerate(self.CATEGORIES):
				current_category = self.playlists[playlist_index].column(category)
				data_value = pygame.math.lerp(current_category.item(self._get_index(playlist_index) % self.playlist_lengths[playlist_index]),
				                              current_category.item((self._get_index(playlist_index) + 1) % self.playlist_lengths[playlist_index]),
				                              self._get_index_float(playlist_index) % 1.0)

				# Generate points with centered position, as it is drawn on an intermediate surface
				scale_factor = self.SCALE_FACTORS[category] if category in self.SCALE_FACTORS else 1
				data_outline.append(pygame.Vector2(self.radius) + pygame.Vector2(0, self.radius * (data_value / scale_factor)).rotate(self.angles[index]))
			# data_outline.append(self.pos + pygame.Vector2(0, self.radius * data_value).rotate(self.angles[index]))

			# Draw to intermediate surface
			self.data_vis_surface.fill((0, 0, 0, 0))
			# if not aa_enabled:
			pygame.draw.polygon(self.data_vis_surface, self.DATA_COLOR_FILL, data_outline)
			pygame.draw.polygon(self.data_vis_surface, self.DATA_COLOR_OUTLINE, data_outline, width=6)
			# else:
			# 	draw_thick_polygon(self.data_vis_surface, data_outline, self.DATA_COLOR_OUTLINE, self.pos, width=20)
			# 	pygame.gfxdraw.filled_polygon(self.data_vis_surface, data_outline, self.DATA_COLOR_FILL)
			# 	# pygame.gfxdraw.filled_polygon(surface, data_outline, self.DATA_COLOR_FILL)
			# 	# draw_thick_polygon(surface, data_outline, self.DATA_COLOR_OUTLINE, self.pos, width=3)

			# Draw to screen
			self.data_vis_surface.fill((int(self.alpha * 255), int(self.alpha * 255), int(self.alpha * 255), 0), special_flags=pygame.BLEND_MULT)
			surface.blit(self.data_vis_surface, self.pos - pygame.Vector2(self.radius), special_flags=pygame.BLEND_ADD)

		# Plot
		self.plot_surface.fill((0, 0, 0, 0))
		# Radial Sections
		for angle in self.angles:
			if not aa_enabled:
				pygame.draw.line(self.plot_surface, self.PLOT_COLOR_RADIAL, pygame.Vector2(self.radius * 1.1),
				                 pygame.Vector2(self.radius * 1.1) + pygame.Vector2(0, self.radius).rotate(angle))
			else:
				pygame.draw.aaline(self.plot_surface, self.PLOT_COLOR_RADIAL, pygame.Vector2(self.radius * 1.1),
				                   pygame.Vector2(self.radius * 1.1) + pygame.Vector2(0, self.radius).rotate(angle))

		# Circle Sections
		if not aa_enabled:
			pygame.draw.circle(self.plot_surface, self.PLOT_COLOR_OUTER, pygame.Vector2(self.radius * 1.1), self.radius, width=2)
			pygame.draw.circle(self.plot_surface, self.PLOT_COLOR_INNER, pygame.Vector2(self.radius * 1.1), self.radius / 2, width=1)
		else:
			# Attempt to draw thicker line
			pygame.gfxdraw.aacircle(self.plot_surface, int(self.radius * 1.1), int(self.radius * 1.1), int(self.radius / 2), self.PLOT_COLOR_INNER)

			draw_thick_circle(self.plot_surface, pygame.Vector2(self.radius * 1.1), self.radius, self.PLOT_COLOR_OUTER, width=4)

		surface.blit(self.plot_surface, self.pos - pygame.Vector2(self.radius * 1.1), special_flags=pygame.BLEND_ADD)

		# Text
		for text in self.texts:
			text.draw(surface)
