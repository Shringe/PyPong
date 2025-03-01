import pygame as pg
import os
import random
import time
import threading
import sys
pg.init()

#creating window
WIDTH, HEIGHT = 900, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('PyPong-APLHA-v1.8')
#assigining colors
GREY = (20, 20, 20)
WHITE = (236, 236, 236)
fade = WHITE[0]

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

#handleing countdown
countdown_val_input = 3
countdown_val = countdown_val_input
countdown = None

#handle go message
go_message = None
go_location = None
start_go = False
start_fade = False
start_timer = True
blit_go = False

#handle timers
delay_done = False
start_count = False

start_timer1 = True
blit_countdown = False

#setting xy ball velocity
tball_vel = []#true ball velocity
xball_vel = BALL_VEL
yball_vel = BALL_VEL
tball_vel.append(xball_vel)
tball_vel.append(yball_vel)
#creating import function
operating_system = sys.platform
file_dir = os.path.dirname(os.path.realpath(__file__))
Assets_dir = file_dir + '/Assets'
def Import_LINUX(file, type, x, y, alpha, size):
	if type == 'image':
		object_surface = pg.image.load(os.path.join('Assets', file + '.png'))
		if x is not None and y is not None:
			object = pg.transform.scale(object_surface, (x, y))
		try:
			object.set_alpha(alpha)
		except:
			object = object_surface
			object.set_alpha(alpha)
		return object
	elif type == 'sound':
		object = pg.mixer.Sound(os.path.join('Assets', file + '.wav'))
		return object
	elif type == 'music':
		object = pg.mixer.music.load(os.path.join('Assets', file + '.wav'))
		return object
	elif type == 'font':
		object = pg.font.Font(os.path.join('Assets', file + '.ttf'), size)
		return object
	else:
		print('file type:', '"' + type + '"', 'unreconized')
		quit()

def Import_WINDOWS(file, type, x, y, alpha, size):
	if type == 'image':
		object_surface = pg.image.load(os.path.join('Assets', file + '.png'))
		if x is not None and y is not None:
			object = pg.transform.scale(object_surface, (x, y))
		try:
			object.set_alpha(alpha)
		except:
			object = object_surface
			object.set_alpha(alpha)
		return object
	elif type == 'sound':
		object = pg.mixer.Sound(os.path.join('Assets', file + '.wav'))
		return object
	elif type == 'music':
		object = pg.mixer.music.load(os.path.join('Assets', file + '.wav'))
		return object
	elif type == 'font':
		object = pg.font.Font(os.path.join('Assets', file + '.ttf'), size)
		return object
	else:
		print('file type:', '"' + type + '"', 'unreconized')
		quit()

def Import(file, type, x=None, y=None, alpha=255, size=32):
	if operating_system == 'linux':
		Import_WINDOWS(file, type, x, y, alpha, size)
	elif operating_system == 'linux':
		Import_LINUX(file, type, x, y, alpha, size)
	else:
		print('operating system not supported')
		quit()

#importing ball
BALL = Import('PyPong ball', 'image', BALL_RAD, BALL_RAD)

#importing paddles
LPADDLE = Import('PyPong paddle', 'image', PADDLE_WIDTH, PADDLE_HIEGHT)
RPADDLE = Import('PyPong paddle', 'image', PADDLE_WIDTH, PADDLE_HIEGHT)

#importing logoq
LOGO = Import('Python logo', 'image', 40, 40)

#importing font
FONT = Import('Retro Font', 'font')
FONT20 = Import('Retro Font', 'font', size=20)

#importing sound
PADDLE_COLLSION_AUDIO = Import('paddle hit', 'sound')

#importing main menu textures
BUTTON1 = Import('button1', 'image', 340, 140, 145)
BUTTON2 = Import('button1', 'image', 170, 70, 145)

MAIN_MENU_BACKGROUND = Import('main menu background', 'image')
#importing sounds
MAIN_MENU_AUDIO = Import('music', 'music')
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(1)
BUTTON_SELECT_AUDIO = Import('button select sound', 'sound')

#main menu variables
#Assets
#buttons
clicked_button = False
clicked_play = False
clicked_options = False
clicked_quit = False

#options menu variables
#buttons
clicked_back = False
def draw_text(text, location=(450, 300), color=WHITE, font=FONT):
	text_surface = font.render(text, True, color)
	text_location = text_surface.get_rect()
	text_location.center = location
	WIN.blit(text_surface, text_location)


#BaralTech's button class
class Button():
	def __init__(self, image, x_pos, y_pos, text_input, clicked_bool, font=FONT):
		self.image = image
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.font = font
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, WHITE)
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self):
		WIN.blit(self.image, self.rect)
		WIN.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			global clicked_button
			clicked_button = True
			clicked_bool = True
			return clicked_bool

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, (20, 200, 50))
		else:
			self.text = self.font.render(self.text_input, True, WHITE)


def quit_game():
	#randomizing the funny tip
	random_msg = random.randint(1, 10)
	if random_msg == 1:
		print('Is that a Jojo reference!?')
	elif random_msg == 2:
		print('''
         (
          )
     __..---..__
 ,-='  /  |  \  `=-.
:--..___________..--;
 \.,_____________,./
		''')
		print('This post was brought to you by the FCA(FAT CAT ASSOCIATION)')
	elif random_msg == 3:
		print('(Insert gigachad image here)')
	elif random_msg == 4:
		print('No, i dont thinnk i will.')
	else:
		print('Thanks for playing!')

	#finishing process
	print('===========================')
	print('>>>>>>Exit Successful<<<<<<')
	print('===========================')
	pg.quit()
	quit()

#main menu functins
def draw_main_menu(MAIN_MENU_BACKGROUND, play_button, options_button, quit_button):
	WIN.fill(GREY)
	WIN.blit(MAIN_MENU_BACKGROUND, (0, 0))
	#updating buttons
	play_button.update()
	play_button.changeColor(pg.mouse.get_pos())
	options_button.update()
	options_button.changeColor(pg.mouse.get_pos())
	quit_button.update()
	quit_button.changeColor(pg.mouse.get_pos())

	pg.display.update()

#defining options menu functions
def draw_options_menu(options_back_button):
	WIN.fill(GREY)
	WIN.blit(MAIN_MENU_BACKGROUND, (0, 0))
	#opions buttons
	options_back_button.update()
	options_back_button.changeColor(pg.mouse.get_pos())
	draw_text('Work In Progress')
	pg.display.update()

run_main = True
first = True
while run_main:
	#main menu
	def main_menu():
		play_button = Button(BUTTON1, 450, 150, 'Play', False)
		options_button = Button(BUTTON1, 450, 300, 'Options', False)
		quit_button = Button(BUTTON1, 450, 450, 'Quit', False)
		run_main_menu = True
		while run_main_menu:
			FPS_CAP.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit_game()

				if event.type == pg.MOUSEBUTTONDOWN:
					#checking if buttons are clicked
					global clicked_play, clicked_options, clicked_quit, clicked_button
					clicked_play = play_button.checkForInput(pg.mouse.get_pos())
					clicked_options = options_button.checkForInput(pg.mouse.get_pos())
					clicked_quit = quit_button.checkForInput(pg.mouse.get_pos())
					if clicked_quit:
						quit_game()
					elif clicked_button:
						run_main_menu = False
						clicked_button = False
			draw_main_menu(MAIN_MENU_BACKGROUND, play_button, options_button, quit_button)
	if clicked_back or first:
		clicked = False
		main_menu()
		first = False

	#options menu
	def options_menu():
		options_back_button = Button(BUTTON2, 795, 545, 'Back', False, FONT20)
		run_options_menu = True
		while run_options_menu:
			FPS_CAP.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit_game()

				if event.type == pg.MOUSEBUTTONDOWN:
					global clicked_back, clicked_button
					clicked_back = options_back_button.checkForInput(pg.mouse.get_pos())
					if clicked_button:
						BUTTON_SELECT_AUDIO.play()
						clicked_button = False
					if clicked_back:
						run_options_menu = False
			draw_options_menu(options_back_button)
	if clicked_options:
		BUTTON_SELECT_AUDIO.play()
		clicked_options = False
		options_menu()
	if clicked_play:
		run_main = False



#defining main game loop functions
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


def timer1_sec():
	global start_timer1, countdown_val, countdown_val_surface, countdown_val_location, blit_countdown
	start_timer1 = False
	blit_countdown = True
	while countdown_val > 0:
		countdown_val_surface = FONT.render(str(countdown_val), True, (WHITE))
		countdown_val_location = countdown_val_surface.get_rect()
		countdown_val_location.center = (440, 300)
		countdown_val_location.y += 50
		time.sleep(1)
		countdown_val -=1
	blit_countdown = False
	global delay_done
	delay_done = True
	start_timer1 = True


def countdown(countdown_val_input):
	global start_go, delay_done, countdown_val, start_count, start_timer1, countdown_val_surface, countdown_val_location, blit_countdown
	if countdown_val > 0:
		if start_timer1:
			#countding down
			timer1 = threading.Thread(target = timer1_sec)
			timer1.daemon = True
			timer1.start()
	else:
		blit_countdown = False
		start_count = False
		countdown_val = countdown_val_input
		start_go = True


def timer6_sec():
	time.sleep(5.5)
	global start_fade, start_timer
	start_fade = True
	start_timer = True


def timer3_sec():
	time.sleep(3)
	global blit_go
	blit_go = True


def fade_go():
	global go_message, go_location, start_go, start_fade, start_timer, fade, blit_go
	#setting timer
	if start_fade is False and start_timer:
		start_timer = False
		timer6 = threading.Thread(target = timer6_sec)
		timer6.daemon = True
		timer6.start()
		timer3 = threading.Thread(target = timer3_sec)
		timer3.daemon = True
		timer3.start()
	#checking fade is reconized
	if fade is None:
		fade = WHITE[0]
	#fading go
	if start_fade:
		fade -= 3
	else:
		fade = WHITE[0]
	#deleting go
	if fade < 20:
		start_go = False
		start_fade = False
		fade = WHITE[0]
		blit_go = False
	#rendering go
	go_message = FONT.render('GO!', True, (fade, fade, fade))
	go_location = go_message.get_rect()
	go_location.center = (450, 300)
	go_location.y += 50
	return fade


def draw(lpaddle, rpaddle, ball, logo, lscore, rscore, pause, fade):
	WIN.fill(GREY)
	if start_go:
		fade_go()
		if start_go and blit_go:
			WIN.blit(go_message, (go_location))
			pause = False
	if blit_countdown:
		WIN.blit(countdown_val_surface, (countdown_val_location))
	WIN.blit(LPADDLE, (lpaddle.x, lpaddle.y))
	WIN.blit(RPADDLE, (rpaddle.x, rpaddle.y))
	WIN.blit(BALL, (ball.x, ball.y))
	WIN.blit(lscore, (414, 30))
	WIN.blit(rscore, (454, 30))
	WIN.blit(LOGO, (logo.x, logo.y))
	pg.display.update()
	return pause


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
	#starting the countdown
	if start_count:
		global pause
		pause = True
		countdown(countdown_val_input)
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
	global start_count
	start_count = True
	#setting delay
	global start_go
	start_go = True



def main(lscore, rscore, score_val, fade):
	#loading assets
	lpaddle = pg.Rect(18, 242, PADDLE_WIDTH, PADDLE_HIEGHT)
	rpaddle = pg.Rect(852, 242, PADDLE_WIDTH, PADDLE_HIEGHT)
	ball = pg.Rect(426, 280, BALL_RAD, BALL_RAD)
	logo = pg.Rect(20, 540, 40, 40)
	random_ball(tball_vel, random)
	reset_main(ball, lpaddle, rpaddle)
	run_main = True
	while run_main:
		global pause
		FPS_CAP.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				run_main = False
		if pause is False:
			keys_pressed = pg.key.get_pressed()
			handle_key_press(keys_pressed, lpaddle, rpaddle)
			handle_ball(tball_vel, ball, lpaddle, rpaddle, PADDLE_WIDTH, PADDLE_HIEGHT, BALL_VEL, BALL_RAD)
		lscore, rscore, score_val = handle_score(ball, BALL_RAD, score_val, lpaddle, rpaddle)
		pause = draw(lpaddle, rpaddle, ball, logo, lscore, rscore, pause, fade)
	quit_game()


def fade_main_menu_music():
	music_vol = pg.mixer.music.get_volume()
	while music_vol > 0.0001:
		FPS_CAP.tick(FPS)
		music_vol -= 0.002
		pg.mixer.music.set_volume(music_vol)

#checking main menu button presses
if clicked_play:
	fade_music = threading.Thread(target = fade_main_menu_music)
	fade_music.daemon = True
	fade_music.start()
	BUTTON_SELECT_AUDIO.play()
	main(lscore, rscore, score_val, fade)
