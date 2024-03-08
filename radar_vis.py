import os
import pathlib

import pygame

from datascience import *

from draw_utils import ProgressBar
from radar_chart import RadarChart

import pygbase

aa_enabled = True

animation_speed = 0.15

ANIMATION_FPS = 30
ANIMATION_LENGTH_SECONDS = 10.0

CURRENT_DIR = pathlib.Path.cwd()

OVERWRITE_PREV_RENDER = False
RENDER_DEST = CURRENT_DIR / "images"

data: dict[str, Table] = {}

for dir_name, _, file_names in os.walk(CURRENT_DIR / "music"):
	for file in file_names:
		if file.endswith(".csv"):
			file_name = file[:-4]
			data[file_name] = Table.read_table(f"{dir_name}/{file}")

top_30_movies = [playlist_name for playlist_name in data.keys() if playlist_name.startswith("(")]
lotr = ["Lord of The Rings (1)", "Lord of The Rings (2)", "Lord of The Rings (3)"]
httyd = ["HTTYD (1)", "HTTYD (2)", "HTTYD (3)"]
musicals = ["Fiddler on the Roof", "Something Rotten", "Cats (Musical)", "Les Mis (Musical)", "The Greatest Showman"]


class RadarVis(pygbase.GameState, name="radar_vis"):
	def __init__(self):
		super().__init__()

		self.progress_bar = ProgressBar((20, 20), (pygbase.Common.get_value("screen_width") - 40, pygbase.Common.get_value("screen_height") / 16),
		                                (220, 220, 220), (40, 40, 40))

		# self.radar_plots = [RadarChart((400, 400), data, "My Playlist")]
		self.radar_plots = [RadarChart((400, 400), data, *top_30_movies)]
		# self.radar_plots = [RadarChart((400, 400), data, *lotr)]
		# self.radar_plots = [RadarChart((400, 400), data, *httyd)]
		# self.radar_plots = [RadarChart((400, 400), data, *musicals)]
		# self.radar_plots = [
		#     RadarChart((200, 250), data, *top_30_movies, radius=85),
		#     RadarChart((600, 250), data, *lotr, radius=85),
		#     RadarChart((200, 600), data, *httyd, radius=85),
		#     RadarChart((600, 600), data, *musicals, radius=85)
		# ]

		pygbase.EventManager.add_handler("all", pygame.KEYDOWN, self.render_start_handler)

	def render_start_handler(self, event: pygame.Event):
		if event.key == pygame.K_s and (pygbase.InputManager.check_modifiers(pygame.KMOD_LCTRL)
		                                or pygbase.InputManager.check_modifiers(pygame.KMOD_META)):
			self.start_render()

	def start_render(self):
		print(f"Rendering images to: {RENDER_DEST}")

		# Setup folder
		if not RENDER_DEST.is_dir():
			os.mkdir(RENDER_DEST)
		elif OVERWRITE_PREV_RENDER:
			os.remove(RENDER_DEST)
			os.mkdir(RENDER_DEST)

		# Reset animation to beginning
		current_amount_played = self.radar_plots[0].percentage_played
		for radar in self.radar_plots:
			radar.set_percentage_played(0.5)

		# Setup values
		total_frames = int(ANIMATION_LENGTH_SECONDS * ANIMATION_FPS)
		temp_surface = pygame.Surface(pygbase.Common.get_value("screen_size"), flags=pygame.SRCALPHA)

		# Render frames
		for index in range(total_frames):
			for radar in self.radar_plots:
				radar.set_percentage_played(index / total_frames)

			self.progress_bar.set_progress(self.radar_plots[0].percentage_played)
			self.draw(temp_surface)

			# Save frame
			pygame.image.save(temp_surface, RENDER_DEST / f"{index}.png", namehint=".png")

		# Reset animation to prev value
		for radar in self.radar_plots:
			radar.set_percentage_played(current_amount_played)

		print("Finished render")

	def update(self, delta: float):
		speed_factor = 3 if pygbase.InputManager.check_modifiers(pygame.KMOD_SHIFT) else 1

		if pygbase.InputManager.get_key_pressed(pygame.K_RIGHT):
			for radar in self.radar_plots:
				radar.animate(animation_speed / speed_factor * delta)
		if pygbase.InputManager.get_key_pressed(pygame.K_LEFT):
			for radar in self.radar_plots:
				radar.animate(-animation_speed / speed_factor * delta)

		self.progress_bar.set_progress(self.radar_plots[0].percentage_played)

	def draw(self, surface: pygame.Surface):
		surface.fill((10, 10, 10))

		for radar in self.radar_plots:
			radar.draw(surface, aa_enabled=aa_enabled)

		self.progress_bar.draw(surface)


pygbase.init((800, 800))

pygbase.EventManager.add_handler("all", pygame.KEYDOWN, lambda e: pygbase.EventManager.post_event(pygame.QUIT) if e.key == pygame.K_ESCAPE else None)

pygbase.App(RadarVis, flags=pygame.SCALED).run()

pygbase.quit()
