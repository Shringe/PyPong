import pygame as pg
import time
import os
pg.init()

WIDTH, HEIGHT = 900, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('BG TIMER TEST')
GREY = (20, 20, 20)
WHITE = (236, 236, 236)
FONT = pg.font.Font(os.path.join('Assets', 'Retro Font.ttf'), 60)


FPS_CAP = pg.time.Clock()
FPS = 60

def draw_text(text, location=(450, 300), color=WHITE, font=FONT, center='both'):
	if center == 'both':
		text_surface = font.render(text, True, color)
		text_location = text_surface.get_rect()
		text_location.center = location
	elif center == 'x':
		text_surface = font.render(text, True, color)
		text_location = text_surface.get_rect()
		text_location.centerx = location[0]
		text_location[1] = location[1]
	elif center == 'y':
		text_surface = font.render(text, True, color)
		text_location = text_surface.get_rect()
		text_location.centery = location[1]
		text_location[0] = location[0]
	WIN.blit(text_surface, text_location)

class bgtimer:
	def __init__(self, time, kill, cframe=False, fps=60):
		self.time = time
		self.fps = fps
		self.fcount = 0
		self.scount = 0
		self.kill = kill
		self.cframe = cframe#count frames instead of seconds

	def count(self):
		if not self.kill:
			self.fcount += 1
			#scaling frame to second
			if self.fcount == self.fps:
				self.scount += 1
				if not self.cframe:
					self.fcount = 0
			#finishing timer
			if self.cframe:
				if self.fcount == self.time:
					self.kill = True
			else:	
				if self.scount == self.time:
					self.kill = True

	def check_status(self):
		#time left
		if self.cframe:
			time_left = self.time - self.fcount
		else:
			time_left = self.time - self.scount
		
		status = not self.kill
		if self.cframe:
			return self.fcount, time_left, status
		else:
			return self.scount, time_left, status

	def restart(self):
		self.fcount = 0
		self.scount = 0
		self.kill = False

	def force_finish(self):
		if self.cframe:
			self.fcount = self.time
		else:
			self.scount = self.time
		self.kill = True
timer3 = bgtimer(3, False)
kcooldown = bgtimer(30, True, True)

def draw():
	WIN.fill(GREY)
	draw_text('time ellapsed: ' + str(data[0]), (20, 230), center='y')
	draw_text('time left: ' + str(data[1]), (20, 300), center='y')
	draw_text('status: ' + str(data[2]), (20, 370), center='y')
	#print(data)
	pg.display.update()

num = 0
jnum = 0
while True:
	FPS_CAP.tick(FPS)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			quit()
	
	#detecting keypress
	keys = pg.key.get_pressed()
	if keys[pg.K_k]:
		if not kcooldown.check_status()[2]:
			print('K Detected', num)
			num += 1
			timer3.restart()
			kcooldown.restart()
	if keys[pg.K_j]:
		print('J Detected', jnum)
		jnum += 1
		timer3.force_finish()
	
	timer3.count()
	kcooldown.count()
	#print(kcooldown.check_status())
	data = timer3.check_status()
	draw()