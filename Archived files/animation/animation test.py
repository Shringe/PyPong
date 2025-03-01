from argparse import ONE_OR_MORE
import pygame as pg
import os
import time
import threading
pg.init()


#creating window
WIDTH, HEIGHT = 900, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Animation')
GREY = (20, 20, 20)

FPS_CAP = pg.time.Clock()
FPS = 60

ONE = pg.image.load(os.path.join('animation', '1.png'))
TWO = pg.image.load(os.path.join('animation', '2.png'))
THREE = pg.image.load(os.path.join('animation', '3.png'))
FOUR = pg.image.load(os.path.join('animation', '4.png'))
FIVE = pg.image.load(os.path.join('animation', '5.png'))
frames = [ONE, TWO, THREE, FOUR, FIVE]

aframe = 0
def draw(frames, aframe):
	WIN.fill(GREY)
	WIN.blit(frames[aframe], (0, 0))

	pg.display.update()

def animate():
	global aframe
	while True:
		time.sleep(0.25)
		if aframe >= 4:
			aframe = 0
			break
		else :
			aframe += 1


thread = threading.Thread(target = animate)
thread.daemon = True
thread.start()
while True:
	FPS_CAP.tick(FPS)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			exit()
	draw(frames, aframe)