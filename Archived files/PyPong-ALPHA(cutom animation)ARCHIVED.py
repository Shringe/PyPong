#vscode imports
# from email.utils import parsedate
# from socket import SO_BROADCAST
# from cv2 import AGAST_FEATURE_DETECTOR_AGAST_7_12D, detail_ExposureCompensator
# from traitlets import ForwardDeclaredInstance
# from yaml import safe_dump_all
#personal imports
import pygame as pg
import os
import random
import time
import threading
import re
pg.init()


#creating window
WIDTH, HEIGHT = 900, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('PyPong-ALPHA')
#assigining colors
GREY = (20, 20, 20)
WHITE = (236, 236, 236)
CRIMSON = (153, 0, 0)
GREEN = (20, 200, 50)
fade = WHITE[0]

#assigning variables
VEL = 4#paddle speed
PADDLE_WIDTH = 30
PADDLE_HIEGHT = 116

BALL_VEL = 4#ball speed
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
def Import(file, type, x=None, y=None, alpha=255, size=32):
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

#importing ball
BALL = Import('PyPong ball', 'image', BALL_RAD, BALL_RAD)

#importing paddles
LPADDLE = Import('PyPong paddle', 'image', PADDLE_WIDTH, PADDLE_HIEGHT)
RPADDLE = Import('PyPong paddle', 'image', PADDLE_WIDTH, PADDLE_HIEGHT)

#importing logoq
LOGO = Import('Python logo', 'image', 40, 40)

#importing font
#retro font
FONT = Import('Retro Font', 'font')
FONT20 = Import('Retro Font', 'font', size=20)
#other
REG_FONT = pg.font.Font(None, 30)

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
TOGGLE_ON = Import('On_button-transformed', 'image', 45, 45)
TOGGLE_OFF = Import('Off_button', 'image', 50, 50)
#buttons
clicked_button = False
clicked_play = False
clicked_options = False
clicked_quit = False

#options menu variables
#buttons
#toggle
AdvancedPaddle_Toggle = True
placeholder1_toggle = False
placeholder2_toggle = False
placeholder3_toggle = False

#regular
clicked_back = False

#text box
paddle_tbox_focus = False
paddle_tbox_text = str(VEL)

ball_tbox_focus = False
ball_tbox_text = str(BALL_VEL)

#gamemode select variables
#Assets
CLASSIC1 = Import('ClassicFinal', 'image', 300, 160)
CLASSIC2 = Import('ClassicFinalON', 'image', 300, 160)
#buttons
clicked_2pdefault = False
clicked_1pdefault = False
#animation point
#Classic 2p
killanimate2pdefault = False
keep_killed = False
animate2pdefault_active = False
twodefault_aframe = 0
twodefault_frame1 = Import('1', 'image', 450, 240)
twodefault_frame2 = Import('2', 'image', 450, 240)
twodefault_frame3 = Import('3', 'image', 450, 240)
twodefault_frame4 = Import('4', 'image', 450, 240)
twodefault_frame5 = Import('5', 'image', 450, 240)

# twodefault_frames = [CLASSIC1, twodefault_frame1, twodefault_frame2, twodefault_frame3, twodefault_frame4, twodefault_frame5]
twodefault_frames = []
frames = []
Classic2pframenum = 0

while True:
	did_find = False
	for file in os.scandir(os.path.join('Assets', 'Classic2P animation')):
		cframe = re.findall(rf'frame{Classic2pframenum}.png', file.name)#checking if frame matches num
		if len(cframe) != 0:
			Classic2pframenum += 1
			print(cframe)
			frames.append(cframe)
			did_find = True
			break
	if not did_find:
		break
			



# sframes = sorted(frames)
# print(frames)

	#twodefault_frames.append(frame)
for frame in frames:
	print(frame, 'here')
	frame = pg.image.load(os.path.join('Assets', 'Classic2P animation', 'Classic2p ' + frame[0]))
	frame = pg.transform.scale(frame, (300, 160))

	twodefault_frames.append(frame)

	

twodefault_frames_rect = []
for frame in twodefault_frames:
	frame = frame.get_rect(center=(170, 88))
	twodefault_frames_rect.append(frame)
# for fram in twodefault_frames:
# 	WIN.blit(fram, (300, 400))
# 	pg.display.update()
# 	time.sleep(0.2)


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


#BaralTech's button class
class Button():
	def __init__(self, image, x_pos, y_pos, text_input, col=GREEN, font=FONT):
		self.image = image
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.color = col
		self.font = font
		self.clicked_bool = False
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
			self.clicked_bool = True
			return self.clicked_bool

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, (self.color))
		else:
			self.text = self.font.render(self.text_input, True, WHITE)
#options menu
options_back_button = Button(BUTTON2, 795, 545, 'Back', font=FONT20)
#main menu
play_button = Button(BUTTON1, 450, 150, 'Play')
options_button = Button(BUTTON1, 450, 300, 'Options')
quit_button = Button(BUTTON1, 450, 450, 'Quit')
#gamemode select
gamemode_back_button = Button(BUTTON2, 795, 545, 'Back', font=FONT20)
class GameButton():
	def __init__(self, image, image2,  x_pos, y_pos, text_input, col=GREEN, font=FONT):
		self.Timage = image
		self.image1 = image
		self.image2 = image2
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.color = col
		self.font = font
		self.clicked_bool = False
		self.rect = image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, WHITE)
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def animate(self, position, killthread, keep_killed):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom) and not animate2pdefault_active and not keep_killed:
			
			animate2pdefault_thread = threading.Thread(target = animate2pdefault)
			animate2pdefault_thread.daemon = True
			animate2pdefault_thread.start()			
			print('starting')
		elif not position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom) and animate2pdefault_active:
			#if animate2pdefault_active:
			print('stopping')
			killthread = True
			keep_killed = False
			return killthread, keep_killed
		# else:
		# 	return False


	def update(self):
		WIN.blit(self.Timage, self.rect)
		#WIN.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			global clicked_button
			clicked_button = True
			self.clicked_bool = True
			return self.clicked_bool


	def changeImage(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.Timage = self.image2
			#print('true')
		else:
			self.Timage = self.image1
			#print('false')
twodefault_button = GameButton(CLASSIC1, CLASSIC2, 170, 88, '')
onedefault_button = Button(BUTTON1, 190, 250, '1 Player Classic', CRIMSON)

#My button class
class Toggle_Button():
	def __init__(self, on_image, off_image, x_pos, y_pos, toggle):
		self.off_image = on_image
		self.on_image = off_image
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.toggle = toggle
		self.rect = self.on_image.get_rect(center=(self.x_pos, self.y_pos))

	def update(self):
		if self.toggle:
			WIN.blit(self.off_image, self.rect)
		else:
			WIN.blit(self.on_image, self.rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			global clicked_button
			clicked_button = True
			if self.toggle:
				self.toggle = False
			else:
				self.toggle = True
		return self.toggle
#options menu
AdvancedPaddle_Toggle_button = Toggle_Button(TOGGLE_ON, TOGGLE_OFF, 40, 70, AdvancedPaddle_Toggle)
placeholder1_toggle_button = Toggle_Button(TOGGLE_ON, TOGGLE_OFF, 40, 141, placeholder1_toggle)
placeholder2_toggle_button = Toggle_Button(TOGGLE_ON, TOGGLE_OFF, 40, 212, placeholder2_toggle)
placeholder3_toggle_button = Toggle_Button(TOGGLE_ON, TOGGLE_OFF, 40, 283, placeholder3_toggle)

#My text box class
class Tbox():
	def __init__(self, x_pos, y_pos, width, height, text_value, minimum=0, max=10, font=FONT20):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.width = width
		self.height = height
		self.font = font
		self.minimum = minimum
		self.max = int(max)
		self.clicked_bool = False
		self.text_value = int(text_value)

	def update(self, text):
		self.text = self.font.render(str(text), True, WHITE)
		self.text_rect = self.text.get_rect(center=(self.x_pos + self.width / 2, self.y_pos + self.height / 2))
		pg.draw.rect(WIN, WHITE, (self.x_pos, self.y_pos, self.width, self.height), True)

		WIN.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		self.clicked_bool = False
		try:
			if int(self.text_value) > self.max:
				self.text_value = self.max
			elif int(self.text_value) < self.minimum:
				self.text_value = self.minimum
		except:
			self.text_value = self.minimum
		if position[0] in range(self.x_pos, self.x_pos + self.width) and position[1] in range(self.y_pos, self.y_pos + self.height):
			self.clicked_bool = True
		return self.clicked_bool, self.text_value
	
	def logic(self, event):
		if event.type == pg.KEYDOWN and self.clicked_bool:
			if event.key == pg.K_BACKSPACE:
				self.text_value = str(self.text_value)
				self.text_value = self.text_value[:-1]
			elif event.key == pg.K_RETURN:
				self.clicked_bool = False
				try:
					if int(self.text_value) > self.max:
						self.text_value = self.max
					elif int(self.text_value) < self.minimum:
						self.text_value = self.minimum
				except:
					self.text_value = self.minimum

			else:
				try:
					self.text_value = str(self.text_value)
					self.text_value += event.unicode
					self.text_value = int(float(self.text_value))

					if len(str(self.text_value)) > 2:
						#purposely breaking code to move to except block
						self.text_value + 'string'

				except:
					self.text_value = str(self.text_value)
					self.text_value = self.text_value[:-1]
		return self.text_value
#options menu
paddle_tbox = Tbox(16, 342, 40, 30, paddle_tbox_text, 2, 10)
ball_tbox = Tbox(16, 413, 40, 30, ball_tbox_text, 2, 10)


def quit_game():
	#randomizing the funny tip
	random_msg = random.randint(1, 100)
	if 1 <= random_msg <= 10:
		print('Is that a Jojo reference!?')
	elif 11 <= random_msg <= 20:
		print('''
         (
          )
     __..---..__
 ,-='  /  |  \  `=-.
:--..___________..--;
 \.,_____________,./
		''')
		print('This post was brought to you by the FCA(FAT CAT ASSOCIATION)')
	elif 21 <= random_msg <= 30:
		print('(Insert gigachad image here)')
	elif 31 <= random_msg <= 40:
		print('No, i dont think i will.')
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
	WIN.blit(MAIN_MENU_BACKGROUND, (0, 0))
	#updating buttons
	play_button.update()
	play_button.changeColor(pg.mouse.get_pos())
	options_button.update()
	options_button.changeColor(pg.mouse.get_pos())
	quit_button.update()
	quit_button.changeColor(pg.mouse.get_pos())

	pg.display.update()
def main_menu():
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

#defining options menu functions
def draw_options_menu(options_back_button, AdvancedPaddle_Toggle_button, placeholder1_toggle_button, placeholder2_toggle_button, placeholder3_toggle_button, paddle_tbox_text):
	WIN.blit(MAIN_MENU_BACKGROUND, (0, 0))
	draw_text('Work In Progress')
	#opions buttons
	options_back_button.update()
	options_back_button.changeColor(pg.mouse.get_pos())

	draw_text('Advanced Paddle Collision (UNSTABLE)', (12, 40), font=FONT20, center='y')
	AdvancedPaddle_Toggle_button.update()

	draw_text('placeholer1', (12, 111), font=FONT20, center='y')
	placeholder1_toggle_button.update()

	draw_text('placeholder2', (12, 182), font=FONT20, center='y')
	placeholder2_toggle_button.update()

	draw_text('placeholder3', (12, 253), font=FONT20, center='y')
	placeholder3_toggle_button.update()

	draw_text('Paddle Speed', (12, 324), font=FONT20, center='y')
	paddle_tbox.update(paddle_tbox_text)

	draw_text('Ball Speed', (12, 395), font=FONT20, center='y')
	ball_tbox.update(ball_tbox_text)
	
	pg.display.update()
#getting button states
def get_reg_state(options_back_button, clicked_back):
	clicked_back = options_back_button.checkForInput(pg.mouse.get_pos())
	return clicked_back
def get_toggle_state(AdvancedPaddle_Toggle_button, AdvancedPaddle_Toggle, placeholder1_toggle_button, placeholder1_toggle, placeholder2_toggle_button, placeholder2_toggle, placeholder3_toggle_button, placeholder3_toggle):
	AdvancedPaddle_Toggle = AdvancedPaddle_Toggle_button.checkForInput(pg.mouse.get_pos())
	placeholder1_toggle = placeholder1_toggle_button.checkForInput(pg.mouse.get_pos())
	placeholder2_toggle = placeholder2_toggle_button.checkForInput(pg.mouse.get_pos())
	placeholder3_toggle = placeholder3_toggle_button.checkForInput(pg.mouse.get_pos())
	return AdvancedPaddle_Toggle, placeholder1_toggle, placeholder2_toggle, placeholder3_toggle

def options_menu():
	global clicked_back, clicked_button, tball_vel, AdvancedPaddle_Toggle, placeholder1_toggle, placeholder2_toggle,placeholder3_toggle, paddle_tbox_focus, paddle_tbox_text, VEL, ball_tbox_focus, ball_tbox_text, BALL_VEL
	run_options_menu = True
	while run_options_menu:
		FPS_CAP.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quit_game()

			if event.type == pg.MOUSEBUTTONDOWN:
				#reg button
				clicked_back = get_reg_state(options_back_button, clicked_back)

				#toggles
				AdvancedPaddle_Toggle, placeholder1_toggle, placeholder2_toggle, placeholder3_toggle = get_toggle_state(AdvancedPaddle_Toggle_button, AdvancedPaddle_Toggle, placeholder1_toggle_button, placeholder1_toggle, placeholder2_toggle_button, placeholder2_toggle, placeholder3_toggle_button, placeholder3_toggle)

				if clicked_button:
					BUTTON_SELECT_AUDIO.play()
					clicked_button = False
				if clicked_back:
					run_options_menu = False
					VEL = paddle_tbox_text
					BALL_VEL = ball_tbox_text

				#text box
				paddle_tbox_focus, paddle_tbox_text = paddle_tbox.checkForInput(pg.mouse.get_pos())
				ball_tbox_focus, ball_tbox_text = ball_tbox.checkForInput(pg.mouse.get_pos())
			paddle_tbox_text = paddle_tbox.logic(event)
			ball_tbox_text = ball_tbox.logic(event)	

		draw_options_menu(options_back_button, AdvancedPaddle_Toggle_button, placeholder1_toggle_button, placeholder2_toggle_button, placeholder3_toggle_button, paddle_tbox_text)

#gamemode select functions
def animate2pdefault():
	global twodefault_aframe, killanimate2pdefault, animate2pdefault_active, keep_killed
	animate2pdefault_active = True
	double_break = False
	time.sleep(0.48)
	if not killanimate2pdefault:
		#cycling the animation frames
		while True:
			for i in range(5):
				time.sleep(0.05)
				if killanimate2pdefault:
					#killanimate2pdefault = False
					twodefault_aframe = 0
					animate2pdefault_active = False
					double_break = True
	
					break
			if double_break:
				break

			if twodefault_aframe >= 22:
				twodefault_aframe = 0
				keep_killed = True
				killanimate2pdefault = True
			else:
				twodefault_aframe += 1
			


def draw_gamemode_select():
	WIN.blit(MAIN_MENU_BACKGROUND, (0, 0))
	gamemode_back_button.changeColor(pg.mouse.get_pos())
	gamemode_back_button.update()

	twodefault_button.changeImage(pg.mouse.get_pos())
	#twodefault_button.update()
	WIN.blit(twodefault_frames[twodefault_aframe], (twodefault_frames_rect[twodefault_aframe]))
	#print(twodefault_aframe)

	onedefault_button.changeColor(pg.mouse.get_pos())
	onedefault_button.update()

	pg.display.update()

def gamemode_select():
	global clicked_button, clicked_back, clicked_2pdefault, killanimate2pdefault, keep_killed
	run_gamemode_select = True

	while run_gamemode_select:
		FPS_CAP.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quit_game()
			if event.type == pg.MOUSEBUTTONDOWN:
				clicked_back = gamemode_back_button.checkForInput(pg.mouse.get_pos())
				clicked_2pdefault = twodefault_button.checkForInput(pg.mouse.get_pos())
				if clicked_back:
					run_gamemode_select = False
				elif clicked_2pdefault:
					run_gamemode_select = False

				if clicked_button:
					BUTTON_SELECT_AUDIO.play()
					clicked_button = False

		killanimate2pdefault = twodefault_button.animate(pg.mouse.get_pos(), killanimate2pdefault, keep_killed)
		print(keep_killed, 'me')

		draw_gamemode_select()
	killanimate2pdefault = True
	


run_main = True
first = True
while run_main:
	#main menu
	if clicked_back or first:
		main_menu()
		first = False

	#options menu
	if clicked_options:
		BUTTON_SELECT_AUDIO.play()
		clicked_options = False
		options_menu()

	#gamemode select menu
	if clicked_play:
		BUTTON_SELECT_AUDIO.play()
		gamemode_select()
	
	#breaking
	if clicked_2pdefault or clicked_1pdefault:
		run_main = False


#defining main game loop functions
def random_ball(tball_vel):
	num = random.randint(1, 4)
	if num == 1:#top left
		tball_vel[0] *= -1
		tball_vel[1] *= -1
	elif num == 2:#top right
		tball_vel[0] *= 1
		tball_vel[1] *= -1
	elif num == 3:#bottom left
		tball_vel[0] *= -1
		tball_vel[1] *= 1
	elif num == 4:#bottom right
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


def draw(lpaddle, rpaddle, ball, logo, lscore, rscore, pause):
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


def handle_ball(tball_vel, ball, lpaddle, rpaddle, PADDLE_WIDTH, PADDLE_HIEGHT, BALL_VEL, BALL_RAD, VEL):
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
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_w]:
			ball.y = lpaddle.y - abs(tball_vel[1] - 2) - BALL_RAD
			tball_vel[1] += VEL
		tball_vel[1] *= -1
		PADDLE_COLLSION_AUDIO.play()
	elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + 5:#right
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_UP]:
			ball.y = rpaddle.y - abs(tball_vel[1] - 2) - BALL_RAD
			tball_vel[1] += VEL
		tball_vel[1] *= -1
		PADDLE_COLLSION_AUDIO.play()
	#lower paddle collision
	if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= lpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= lpaddle.y + PADDLE_HIEGHT:#left
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_s]:
			ball.y = lpaddle.y + abs(tball_vel[1] + 2)
			tball_vel[1] += VEL
		tball_vel[1] *= -1
		PADDLE_COLLSION_AUDIO.play()
	elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= rpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT:#right
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_DOWN]:
			ball.y = rpaddle.y + abs(tball_vel[1] + 2)
			tball_vel[1] += VEL
		tball_vel[1] *= -1
		PADDLE_COLLSION_AUDIO.play()


#advanced paddle collision functions
def calculate_projectory(paddle, ball, BALL_RAD):
	global tball_vel
	vel_before = tball_vel[1]
	#projectory calc
	paddle_mid = paddle.y + PADDLE_HIEGHT / 2
	distance = ball.y + BALL_RAD / 2 - paddle_mid
	print(distance)
	if distance < 0: #and tball_vel[1] < 0:
		#tball_vel[1] *= distance / 100
		tball_vel[1] = -abs(tball_vel[1])
	elif distance > 0: #and tball_vel[1] > 0:
		#tball_vel[1] *= distance / 100
		tball_vel[1] = abs(tball_vel[1])
	# 	print('before')
	# 	tball_vel[1] = -abs(tball_vel[1])
	# 	print('after', tball_vel[1])
	# 	print('force up', tball_vel[1])
	# elif distance > 0:

	# 	print('before', tball_vel[1])
	# 	tball_vel[1] = abs(tball_vel[1])
	# 	print('after', tball_vel[1])
	# 	print('force down')


	# paddle_mid = paddle.y + PADDLE_HIEGHT / 2
	# distance = paddle_mid - (ball.y + BALL_RAD) / 2
	# reduction = PADDLE_HIEGHT / 2 / 3
	# y_vel = distance / reduction

	#cushioning impact if ball has to reverse dir
	# if tball_vel[1] >= 0 and not distance >= 0:
	# 	tball_vel[1] *= distance / 100000000000
	# 	tball_vel[1] = -abs(tball_vel[1])
	# 	print('upper paddle hit')
		# tball_vel[1] = y_vel * -1 / 2
	# 	# print('change detected, cushioning blow')
	# elif tball_vel[1] < 0 and not distance < 0:
	# 	tball_vel[1] *= distance / 100000000000
	# 	tball_vel[1] = abs(tball_vel[1])
	# 	print('lower paddle hit')
		# tball_vel[1] = y_vel * -1 / 2
		# print('change detected, cushioning blow')

	# tball_vel[0] += y_vel * -1 / 6
	#setting max and minimum speeds
	for vel in range(len(tball_vel)):
		if tball_vel[vel] >  BALL_VEL * 1.65:
			tball_vel[vel] = BALL_VEL * 1.65
		elif tball_vel[vel] < BALL_VEL * 1.65 * -1:
			tball_vel[vel] = BALL_VEL * 1.65 * -1


def randomize_projectory(tball_vel):
	#randomizing balls projectory by about 10%
	neg_num = random.randint(-110, -100)
	neg_num /= 100
	num = random.randint(100, 110)
	num /= 100
	decider = random.randint(0, 1)
	if decider == 0:
		tball_vel[1] *= neg_num
	else:
		tball_vel[1] *= num
	return tball_vel


def handle_advanced_collision(ball, tball_vel, lpaddle, rpaddle, PADDLE_WIDTH, PADDLE_HIEGHT, BALL_RAD):
	ball.x += tball_vel[0]
	ball.y += tball_vel[1]

	if ball.y + tball_vel[1] >= 576:#floor collision
		tball_vel[1] *= -1
		ball.y = 576 - tball_vel[1] - 2
	elif ball.y + tball_vel[1] <= 0:#ceiling collision
		tball_vel[1] *= -1


	#side paddle collision
	if ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= lpaddle.y and ball.y + tball_vel[1] <= lpaddle.y + PADDLE_HIEGHT and ball.x >= lpaddle.x + PADDLE_WIDTH - 2:#left
		tball_vel[0] *= -1
		#calculating projectory
		calculate_projectory(lpaddle, ball, BALL_RAD)
		#tball_vel = randomize_projectory(tball_vel)
		PADDLE_COLLSION_AUDIO.play()
	elif ball.x + BALL_RAD + tball_vel[0] >= rpaddle.x and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT and ball.x <= rpaddle.x + 2:#right
		tball_vel[0] *= -1
		#calculating projectory
		calculate_projectory(rpaddle, ball, BALL_RAD)
		#tball_vel = randomize_projectory(tball_vel)
		PADDLE_COLLSION_AUDIO.play()

	# #upper paddle collision
	# if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= lpaddle.y and ball.y + tball_vel[1] <= lpaddle.y + 5:#left
	# 	tball_vel[1] *= -1
	# 	PADDLE_COLLSION_AUDIO.play()
	# elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + 5:#right
	# 	tball_vel[1] *= -1
	# 	PADDLE_COLLSION_AUDIO.play()
	# #lower paddle collision
	# if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= lpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= lpaddle.y + PADDLE_HIEGHT:#left
	# 	tball_vel[1] *= -1
	# 	PADDLE_COLLSION_AUDIO.play()
	# elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= rpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT:#right
	# 	tball_vel[1] *= -1
	# 	PADDLE_COLLSION_AUDIO.play()

	#resetting speed if bug accurs
	for vel in range(len(tball_vel)):
		if -3 <= tball_vel[vel] <= 3:
			tball_vel[vel] = BALL_VEL

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
	for vel in range(len(tball_vel)):
		tball_vel[vel] = BALL_VEL
	#randomizing ball
	random_ball(tball_vel)
	#counting down
	global start_count, pause
	start_count = True
	pause = True
	#setting delay
	global start_go
	start_go = True



def main(lscore, rscore, score_val, AdvancedPaddle_Toggle):
	#loading assets
	lpaddle = pg.Rect(18, 242, PADDLE_WIDTH, PADDLE_HIEGHT)
	rpaddle = pg.Rect(852, 242, PADDLE_WIDTH, PADDLE_HIEGHT)
	ball = pg.Rect(426, 280, BALL_RAD, BALL_RAD)
	logo = pg.Rect(20, 540, 40, 40)
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
			if AdvancedPaddle_Toggle:
				handle_advanced_collision(ball, tball_vel, lpaddle, rpaddle, PADDLE_WIDTH, PADDLE_HIEGHT, BALL_RAD)
			else:
				handle_ball(tball_vel, ball, lpaddle, rpaddle, PADDLE_WIDTH, PADDLE_HIEGHT, BALL_VEL, BALL_RAD, VEL)
		lscore, rscore, score_val = handle_score(ball, BALL_RAD, score_val, lpaddle, rpaddle)
		pause = draw(lpaddle, rpaddle, ball, logo, lscore, rscore, pause)
	quit_game()


def fade_main_menu_music():
	music_vol = pg.mixer.music.get_volume()
	while music_vol > 0.0001:
		FPS_CAP.tick(FPS)
		music_vol -= 0.002
		try:
			pg.mixer.music.set_volume(music_vol)
		except:
			pass

#checking button presses
if placeholder1_toggle:
	pass
if placeholder2_toggle:
	pass
if placeholder3_toggle:
	pass

if clicked_2pdefault:
	fade_music = threading.Thread(target = fade_main_menu_music)
	fade_music.daemon = True
	fade_music.start()
	main(lscore, rscore, score_val, AdvancedPaddle_Toggle)

