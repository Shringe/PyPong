import pygame as pg
import re
import os
pg.init()

#Creating window
WIDTH, HEIGHT = 900, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Animation')
GREY = (20, 20, 20)

#fps
FPS_CAP = pg.time.Clock()
FPS = 60


class animate(pg.sprite.Sprite):
	def __init__(self, host_dir, frames_dir, posx, posy, length, width, center=False):
		super().__init__()
		self.frames_dir = frames_dir
		self.host_dir = host_dir

		#getting frame names from file pre sorted
		num = 1
		frames = []
		while True:
			found_frame = False
			for file in os.scandir(os.path.join(self.host_dir, self.frames_dir)):
				frame = re.findall(rf'.*frame{num}.png', file.name)#checking if frame matches num
				if len(frame) != 0:
					num += 1
					frames.append(frame[0])
					found_frame = True
					break

			if not found_frame:
				break

		#importing frames
		self.sprites = []
		for frame in frames:
			frame = pg.image.load(os.path.join(self.host_dir, self.frames_dir, frame))
			frame = pg.transform.scale(frame, (length, width))
			self.sprites.append(frame)
		

		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		if center:
			self.rect.center = (posx, posy)
		else:
			self.rect = (posx, posy)
		self.kill_animation = False
	
	def animate(self, speed, kill_animation, loop=True):
		if not kill_animation and not self.kill_animation:
			self.current_sprite += speed
		else:
			self.current_sprite = 0
		
		if loop:
			self.kill_animation = False

		#looping animation
		if self.current_sprite >= len(self.sprites):
			self.current_sprite = 0
			if not loop:
				self.kill_animation = True


		self.image = self.sprites[int(self.current_sprite)]


animation = animate('Assets', 'Classic2P animation', 450, 300, 300, 180, True)
countup = animate('animation', 'frames', 600, 500, 200, 100)
sprite_group = pg.sprite.Group()
sprite_group.add(animation, countup)



def draw():
	WIN.fill(GREY)

	animation.animate(0.065, False, True)
	countup.animate(0.19, True)
	
	sprite_group.draw(WIN)
	sprite_group.update()
	
	pg.display.update()

while True:
	FPS_CAP.tick(FPS)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			quit()
	draw()

	