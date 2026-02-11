import os
import math
import pygame
import asyncio

# Stage size
WIDTH = 1080
HEIGHT = 720

# Background color (RGB)
BG_COLOR = (14, 14, 14)

# Scale factor for pixel-art sprites (adjust to taste)
# Use integer values for crisp pixel scaling
SCALE = 8

# Player tuning
PLAYER_SPEED = 350  # world pixels per second (tweak this)


def load_sprite(path, scale=1):
	"""Load an image and scale it. If missing, return a placeholder surface."""
	if not os.path.exists(path):
		print(f"Warning: sprite not found: {path} — using placeholder")
		# create a placeholder (16x16) scaled up
		base = pygame.Surface((16, 16), pygame.SRCALPHA)
		base.fill((255, 0, 255))
		if scale != 1:
			return pygame.transform.scale(base, (16 * scale, 16 * scale))
		return base
	img = pygame.image.load(path).convert_alpha()
	if scale != 1:
		w, h = img.get_size()
		img = pygame.transform.scale(img, (w * scale, h * scale))
	return img

class WorldSprite:
	def __init__(self, img, world_x, world_y):
		self.img = img
		self.world_x = world_x
		self.world_y = world_y

class Player:
    def __init__(self, x=0, y=0, scale=1):
        self.world_x = x
        self.world_y = y
        self.scale = scale
        self.facing_right = False
        sprites_dir = 'sprites'
        self.frames = []
        for i in (1, 2, 3):
            path = os.path.join(sprites_dir, f'sprite.{i}.png')
            self.frames.append(load_sprite(path, scale=scale))

        self.idle_image = self.frames[0]
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_delay = 120

    def update(self, moving, dt_ms, dir_x=0):
        if moving:
            if dir_x > 0:
                self.facing_right = True
            elif dir_x < 0:
                self.facing_right = False
            self.anim_timer += dt_ms
            if self.anim_timer >= self.anim_delay:
                self.anim_timer %= self.anim_delay
                self.anim_index = (self.anim_index + 1) % len(self.frames)
        else:
            self.anim_index = 0
            self.anim_timer = 0

    def image(self):
        img = self.frames[self.anim_index]
        if self.facing_right:
            return pygame.transform.flip(img, True, False)
        return img

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bear Country")
clock = pygame.time.Clock()

async def main():
	
	# font for HUD
	font = pygame.font.Font(None, 20)

	sprites_dir = 'sprites'

	# create player centered in world coordinates (we use world coords relative to player)
	player = Player(x=0, y=0, scale=SCALE)

	# Create 10 copies of sprite.15 placed along x-axis at gradually increasing intervals
	sprite_imgs = {}
	for i in range(12, 17):
		sprite_path = os.path.join(sprites_dir, f'sprite.{i}.png')
		sprite_imgs[i] = load_sprite(sprite_path, scale=SCALE)
	world_sprites = []
	start_x = 300
	# intervals increase by 30 pixels each time
	for i in range(10):
		x = start_x + sum(150 + j * 100 for j in range(i))
		if i == 1: x = 500
		y = 0  # align vertically with player world y
		world_sprites.append(WorldSprite(sprite_imgs[15], x, y))
		
	world_sprites.append(WorldSprite(sprite_imgs[14], 500, 500))
	world_sprites.append(WorldSprite(sprite_imgs[16], -500, -500))

	running = True
	while running:
		dt = clock.tick(60)
		dt_s = dt / 1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False

		keys = pygame.key.get_pressed()
		dx = 0
		dy = 0
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			dy -= 1
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			dy += 1
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			dx -= 1
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			dx += 1

		# preserve horizontal intent before normalization for facing
		raw_dx = dx

		moving = (dx != 0 or dy != 0)
		# normalize diagonal movement
		if moving:
			length = math.hypot(dx, dy)
			dx = dx / length
			dy = dy / length
			# update player world position
			player.world_x += dx * PLAYER_SPEED * dt_s
			player.world_y += dy * PLAYER_SPEED * dt_s

		player.update(moving, dt, dir_x=raw_dx)

		# draw
		screen.fill(BG_COLOR)

		center_x = WIDTH // 2
		center_y = HEIGHT // 2

		# draw world sprites relative to player world position so player stays centered
		for ws in world_sprites:
			screen_x = center_x + int(ws.world_x - player.world_x)
			screen_y = center_y + int(ws.world_y - player.world_y)
			rect = ws.img.get_rect(center=(screen_x, screen_y))
			screen.blit(ws.img, rect)

		# draw player at center
		player_img = player.image()
		player_rect = player_img.get_rect(center=(center_x, center_y))
		screen.blit(player_img, player_rect)

		# HUD: show a copy-pastable WorldSprite(...) line with player world coords
		coords_code = f"X: {int(player.world_x)}, Y: {int(player.world_y)}"
		hud_surf = font.render(coords_code, True, (255, 255, 255))
		screen.blit(hud_surf, (8, 8))

		pygame.display.flip()
		await asyncio.sleep(0)  # allow async tasks to run

	pygame.quit()


# Ensure you call main correctly at the bottom of the file
if __name__ == "__main__":
    asyncio.run(main())
