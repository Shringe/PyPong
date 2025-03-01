import pygame as pg
import os
import random
import time
import threading
pg.init()


#creating window
WIDTH, HEIGHT = 900, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('PyPong-APLHA-v1.4')
#assigining colors
GREY = (20, 20, 20)
WHITE = (236, 236, 236)
fade_val = WHITE[0]
fade = False
fade_start = False

#assigning variables
VEL = 4#paddle speed
PADDLE_WIDTH = 30
PADDLE_HIEGHT = 116

BALL_VEL = 2#ball speed
BALL_RAD = 24#ball radius

FPS_CAP = pg.time.Clock()
FPS = 60

lscore = 0
rscore = 0
score_val = {'l':lscore, 'r':rscore}

pause = False
countdown_val = 3
countdown = None

#setting xy ball velocity
tball_vel = []#true ball velocity
xball_vel = BALL_VEL
yball_vel = BALL_VEL
tball_vel.append(xball_vel)
tball_vel.append(yball_vel)

#importing ball
BALL_IMAGE = pg.image.load(os.path.join('Assets', 'PyPong ball.png'))
BALL = pg.transform.scale(BALL_IMAGE, (BALL_RAD, BALL_RAD))

#importing paddles
PADDLE_IMAGE = pg.image.load(os.path.join('Assets', 'PyPong paddle.png'))
LPADDLE = pg.transform.scale(PADDLE_IMAGE, (PADDLE_WIDTH, PADDLE_HIEGHT))
RPADDLE = pg.transform.scale(PADDLE_IMAGE, (PADDLE_WIDTH, PADDLE_HIEGHT))

#importing logo
LOGO_IMAGE = pg.image.load(os.path.join('Assets', 'Python logo.png'))
LOGO = pg.transform.scale(LOGO_IMAGE, (40, 40))

#importing font
FONT = pg.font.Font(os.path.join('Assets', 'Retro Font.ttf'), 32)

#importing sound
PADDLE_COLLSION_AUDIO = pg.mixer.Sound(os.path.join('Assets', 'Paddle hit2.wav'))
MAIN_MENU_AUDIO = pg.mixer.music.load(os.path.join('Assets', 'music2.wav'))

#randomizing the direction of ball
def random_ball(tball_vel, random):
	random = random.randint(1, 4)
	if random == 1:#top left
		tball_vel[0] *= -1
		tball_vel[1] *= -1
	elif random == 2:#top right
		tball_vel[0] *= 1
		tball_vel[1] *= -1
	elif random == 3:#bottom left
		tball_vel[0] *= -1
		tball_vel[1] *= 1
	elif random == 4:#bottom right
		tball_vel[0] *= 1
		tball_vel[1] *= 1
	return tball_vel


def fade_timer():
	global fade
	time.sleep(3)
	fade = True
	return fade


def go_timer():
	global fade_start
	time.sleep(1)
	fade_start = True
	return fade_start

def fade_go(fade_val, fade_start, go_message, go_location):
	start_go = True
	if fade_val > 0:
		fade_val -= 1
		go_message = FONT.render('GO!', True, (fade_val, fade_val, fade_val))
		go_location = go_message.get_rect()
		go_location.center = (450, 300)
		go_location.y += 50
	else:
		fade = False
	return fade_val, go_message, go_location


def countdown(countdown_val):
	global fade_val
	while countdown_val > 0:
		print(countdown_val)
		time.sleep(1)
		countdown_val -= 1
	fade_val = WHITE[0]
	go_message = FONT.render('GO!', True, (WHITE))
	go_location = go_message.get_rect()
	go_location.center = (450, 300)
	go_location.y += 50
	threetimer = threading.Thread(target = fade_timer)
	threetimer.start()


def draw(lpaddle, rpaddle, ball, logo, lscore, rscore, fade_val, go_message=False, go_location=False):
	WIN.fill(GREY)
	if fade and go_message is not False and go_location is not False:
		onetimer = threading.Thread(target = go_timer())
		onetimer.start()
		if fade_start:
			fade_val, go_message, go_location = fade_go(fade_val, fade_start, go_message, go_location)
			WIN.blit(go_message, (go_location))
			print('yes')
	WIN.blit(LPADDLE, (lpaddle.x, lpaddle.y))
	WIN.blit(RPADDLE, (rpaddle.x, rpaddle.y))
	WIN.blit(BALL, (ball.x, ball.y))
	WIN.blit(lscore, (414, 30))
	WIN.blit(rscore, (454, 30))
	WIN.blit(LOGO, (logo.x, logo.y))
	pg.display.update()
	#pausing for score
	return fade_val, go_message, go_location


def handle_key_press(keys_pressed, lpaddle, rpaddle):
#left paddle
	if keys_pressed[pg.K_w] and lpaddle.y - VEL >= 0: #up
		lpaddle.y -= VEL
	if keys_pressed[pg.K_s] and lpaddle.y + VEL <= 482: #down
		lpaddle.y += VEL
#right paddle
	if keys_pressed[pg.K_UP] and rpaddle.y - VEL >= 0: #up
		rpaddle.y -= VEL
	if keys_pressed[pg.K_DOWN] and rpaddle.y + VEL <= 482: #down
		rpaddle.y += VEL


def handle_ball(tball_vel, ball, lpaddle, rpaddle, PADDLE_WIDTH, PADDLE_HIEGHT, BALL_VEL, BALL_RAD):
	ball.x += tball_vel[0]
	ball.y += tball_vel[1]
	if ball.y + BALL_VEL >= 576:#floor collision
		tball_vel[1] *= -1
	elif ball.y + BALL_VEL <= 0:#ceiling collision
		tball_vel[1] *= -1
	#side paddle collision
	if ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= lpaddle.y and ball.y + tball_vel[1] <= lpaddle.y + PADDLE_HIEGHT and ball.x >= lpaddle.x + PADDLE_WIDTH - 2:#left
		tball_vel[0] *= -1
		PADDLE_COLLSION_AUDIO.play()
	elif ball.x + BALL_RAD + tball_vel[0] >= rpaddle.x and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT and ball.x <= rpaddle.x + 2:#right
		tball_vel[0] *= -1
		PADDLE_COLLSION_AUDIO.play()
	#upper paddle collision
	if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= lpaddle.y and ball.y + tball_vel[1] <= lpaddle.y + 5:#left
		tball_vel[1] *= -1
		PADDLE_COLLSION_AUDIO.play()
	elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + 5:#rigght
		tball_vel[1] *= -1
		PADDLE_COLLSION_AUDIO.play()
	#lower paddle collision
	if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= lpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= lpaddle.y + PADDLE_HIEGHT:#left
		tball_vel[1] *= -1
		PADDLE_COLLSION_AUDIO.play()
	elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= rpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT:#right
		tball_vel[1] *= -1
		PADDLE_COLLSION_AUDIO.play()


def handle_score(ball, BALL_RAD, score_val, lpaddle, rpaddle):
	#detecting score
	if ball.x + BALL_RAD + 20 < 0:
		score_val['r'] += 1
		reset_main(ball, lpaddle, rpaddle)
	elif ball.x - 20 > 900:
		score_val['l'] += 1
		reset_main(ball, lpaddle, rpaddle)
	#rendering font
	lscore = FONT.render(str(score_val['l']), True, WHITE)
	rscore = FONT.render(str(score_val['r']), True, WHITE)
	return lscore, rscore, score_val


def reset_main(ball, lpaddle, rpaddle):
	#resseting sprite position
	ball.x, ball.y = 426, 280
	lpaddle.x, lpaddle.y = 18, 242
	rpaddle.x, rpaddle.y = 852, 242
	#randomizing ball
	random_ball(tball_vel, random)
	#counting down
	countdown(countdown_val)


def main(lscore, rscore, score_val, pause, fade_val):
	#loading assets
	lpaddle = pg.Rect(18, 242, PADDLE_WIDTH, PADDLE_HIEGHT)
	rpaddle = pg.Rect(852, 242, PADDLE_WIDTH, PADDLE_HIEGHT)
	ball = pg.Rect(426, 280, BALL_RAD, BALL_RAD)
	logo = pg.Rect(20, 540, 40, 40)
	random_ball(tball_vel, random)
	run = True
	while run:
		FPS_CAP.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False
				print('===========================')
				print('>>>>>>Exit Successful<<<<<<')
				print('===========================')
		keys_pressed = pg.key.get_pressed()
		handle_key_press(keys_pressed, lpaddle, rpaddle)
		handle_ball(tball_vel, ball, lpaddle, rpaddle, PADDLE_WIDTH, PADDLE_HIEGHT, BALL_VEL, BALL_RAD)
		lscore, rscore, score_val = handle_score(ball, BALL_RAD, score_val, lpaddle, rpaddle)
		try:
			fade_val, go_message, go_location = draw(lpaddle, rpaddle, ball, logo, lscore, rscore, fade_val, go_message, go_location)
		except:
			fade_val, go_message, go_location  =  draw(lpaddle, rpaddle, ball, logo, lscore, rscore, fade_val)
	pg.quit()
	quit()


if __name__ == "__main__":
	main(lscore, rscore, score_val, pause, fade_val)
