import pygame.gfxdraw


def get_sign(num):
	if num != 0:
		return num / abs(num)
	else:
		return num


def draw_thick_circle(surface: pygame.Surface, pos, radius, color, width: int = 1):
	pygame.gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), radius, color)
	for i in range(0, int(width / 2)):
		pygame.gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), radius + i, color)
		pygame.gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), radius - i, color)


def draw_thick_polygon(surface: pygame.Surface, points: list, color, center, width: int = 1):
	polygon_line_points = points.copy()
	for index, point in enumerate(polygon_line_points[:]):
		offset_vector = ((point - points[index - 1]).normalize() + (point - points[(index + 1) % len(points)]).normalize()).normalize() * width
		polygon_line_points.append(point + offset_vector * get_sign((point - center).dot(point + offset_vector)))

	pygame.gfxdraw.filled_polygon(surface, polygon_line_points, color)

	# pygame.gfxdraw.aapolygon(surface, points, color)
	# for i in range(0, width):
	# 	# Expands / shrinks the outline in the direction outwards from the two adjacent points
	# 	# Uses vector addition
	# 	# When I wrote this, only me and God knew how it worked. Now, only God knows.

	# 	pygame.gfxdraw.aapolygon(surface, [
	# 	    point - ((point - points[index - 1]).normalize() + (point - points[(index + 1) % len(points)]).normalize()).normalize() *
	# 	    (i / 2) * get_sign(
	# 	        (point - center).dot((point - points[index - 1]).normalize() + (point - points[(index + 1) % len(points)]).normalize()))
	# 	    for index, point in enumerate(points)
	# 	], color)
	# 	pygame.gfxdraw.aapolygon(surface, [
	# 	    point + ((point - points[index - 1]).normalize() + (point - points[(index + 1) % len(points)]).normalize()).normalize() *
	# 	    (i / 2) * get_sign(
	# 	        (point - center).dot((point - points[index - 1]).normalize() + (point - points[(index + 1) % len(points)]).normalize()))
	# 	    for index, point in enumerate(points)
	# 	], color)

	# 	# pygame.gfxdraw.aapolygon(surface, [
	# 	#     point + (points[index - 1] + points[(index + 1) % len(points)]).normalize() * (i / 2)
	# 	#     for index, point in enumerate(points)
	# 	# ], color)


class ProgressBar:
	def __init__(self, pos: tuple, size: tuple, color, background_color, border: int = 5) -> None:
		self.pos = pygame.Vector2(pos)
		self.size = pygame.Vector2(size)

		self.color = color
		self.background_color = background_color

		self.border = border

		self.progress = 0.0

	def set_progress(self, progress):
		self.progress = pygame.math.clamp(progress, 0, 1)

	def draw(self, surface: pygame.Surface):
		pygame.draw.rect(surface, self.background_color, (self.pos, self.size))
		pygame.draw.rect(surface, self.color, (self.pos.x + self.border, self.pos.y + self.border,
		                                       (self.size.x - self.border * 2) * self.progress, self.size.y - self.border * 2))
