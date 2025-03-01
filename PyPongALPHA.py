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
pg.display.set_caption('PyPongALPHA')
#assigining colors
GREY = (20, 20, 20)
WHITE = (236, 236, 236)
CRIMSON = (153, 0, 0)
GREEN = (20, 200, 50)
go_fade_num = WHITE[0] - 20

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

#handle go message
go_message = None
go_location = None
start_go = False
start_go_delay = False
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

#importing logo
LOGO = Import('Python logo', 'image', 40, 40)

#importing font
#retro font
FONT = Import('Retro Font', 'font')
FONT20 = Import('Retro Font', 'font', size=20)
FONT24 = Import('Retro Font', 'font', size=24)

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
BUTTON_SELECT_AUDIO = Import('button select sound', 'sound')

#main menu variables
#Assets
TOGGLE_ON = Import('On_button', 'image', 45, 45)
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
music_toggle = False
sound_toggle = True
RAdvancedPaddle_toggle = True

#regular
clicked_back = False

#text box
paddle_tbox_focus = False
paddle_tbox_text = str(VEL)

ball_tbox_focus = False
ball_tbox_text = str(BALL_VEL)

RAdvancedPaddle_tbox_foces = False
RAdvancedPaddle_tbox_text = 10

#gamemode select variables
#buttons
clicked_2pdefault = False
clicked_1pdefault = False


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

#backgroundtimer
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
countdown = bgtimer(3, True)
go_delay = bgtimer(150, True, True)#go fade delay
go_fade = bgtimer(50, True, True)
fix_go_frame = False

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
music_toggle_button = Toggle_Button(TOGGLE_ON, TOGGLE_OFF, 40, 212, music_toggle)
sound_toggle_button = Toggle_Button(TOGGLE_ON, TOGGLE_OFF, 40, 283, sound_toggle)
RAdvancedPaddle_toggle_button = Toggle_Button(TOGGLE_ON, TOGGLE_OFF, 40, 141, RAdvancedPaddle_toggle)

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

	def update(self, text, after_text=''):
		self.text = self.font.render(str(text) + after_text, True, WHITE)
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
RAdvancedPaddle_tbox = Tbox(85, 131, 70, 45, RAdvancedPaddle_tbox_text, 2, 25, FONT24)

#button animation
class GameButton(pg.sprite.Sprite):
	def __init__(self, host_dir, frames_dir, posx, posy, length, width, center=False):
		super().__init__()
		self.frames_dir = frames_dir
		self.host_dir = host_dir

		#getting frame names from file pre sorted
		num = 0
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
		self.frame_count = 0
	
	def animate(self, speed, delay,loop=True):
		position = pg.mouse.get_pos()
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.frame_count += 1
			if self.frame_count >= delay and not self.kill_animation:
				self.current_sprite += speed
			# print('ONN DETECTED')
		else:
			self.frame_count = 0
			self.current_sprite = 0
			self.kill_animation = False
			# print('OFF DETECTED')
		
		if loop:
			self.kill_animation = False

		#looping animation
		if self.current_sprite >= len(self.sprites):
			self.current_sprite = 0
			if not loop:
				self.kill_animation = True

		self.image = self.sprites[int(self.current_sprite)]

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			global clicked_button
			clicked_button = True
			self.clicked_bool = True
			return self.clicked_bool
gbutton_spritegroup = pg.sprite.Group()
#gamemode select
twodefault_gbutton = GameButton('Assets', 'Classic2P animation', 170, 88, 300, 160, True)
gbutton_spritegroup.add(twodefault_gbutton)

def quit_game():
	#randomizing the funny tip
	random_msg = random.randint(1, 100)
	if 1 <= random_msg <= 5:
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
def draw_options_menu(options_back_button, AdvancedPaddle_Toggle_button, music_toggle_button, sound_toggle_button, RAdvancedPaddle_toggle_button, paddle_tbox_text):
	WIN.blit(MAIN_MENU_BACKGROUND, (0, 0))
	#draw_text('Work In Progress')
	#opions buttons
	options_back_button.update()
	options_back_button.changeColor(pg.mouse.get_pos())

	draw_text('Advanced Paddle Collision (BETA)', (12, 40), font=FONT20, center='y')
	AdvancedPaddle_Toggle_button.update()

	draw_text('Music', (12, 182), font=FONT20, center='y')
	music_toggle_button.update()

	draw_text('sound toggle', (12, 253), font=FONT20, center='y')
	sound_toggle_button.update()

	draw_text('Randomize Advanced Paddle Collision', (12, 111), font=FONT20, center='y')
	RAdvancedPaddle_toggle_button.update()
	if RAdvancedPaddle_toggle:
		RAdvancedPaddle_tbox.update(RAdvancedPaddle_tbox_text, '%')

	draw_text('Paddle Speed', (12, 324), font=FONT20, center='y')
	paddle_tbox.update(paddle_tbox_text)

	draw_text('Ball Speed', (12, 395), font=FONT20, center='y')
	ball_tbox.update(ball_tbox_text)
	
	pg.display.update()
#getting button states
def get_reg_state(options_back_button, clicked_back):
	clicked_back = options_back_button.checkForInput(pg.mouse.get_pos())
	return clicked_back
def get_toggle_state(AdvancedPaddle_Toggle_button, AdvancedPaddle_Toggle, music_toggle_button, music_toggle, sound_toggle_button, sound_toggle, RAdvancedPaddle_toggle_button, RAdvancedPaddle_toggle):
	AdvancedPaddle_Toggle = AdvancedPaddle_Toggle_button.checkForInput(pg.mouse.get_pos())
	music_toggle = music_toggle_button.checkForInput(pg.mouse.get_pos())
	sound_toggle = sound_toggle_button.checkForInput(pg.mouse.get_pos())
	RAdvancedPaddle_toggle = RAdvancedPaddle_toggle_button.checkForInput(pg.mouse.get_pos())
	return AdvancedPaddle_Toggle, music_toggle, sound_toggle, RAdvancedPaddle_toggle

def options_menu():
	global clicked_back, clicked_button, tball_vel, AdvancedPaddle_Toggle, music_toggle, sound_toggle,RAdvancedPaddle_toggle, paddle_tbox_focus, paddle_tbox_text, VEL, ball_tbox_focus, ball_tbox_text, BALL_VEL, RAdvancedPaddle_tbox_focus, RAdvancedPaddle_tbox_text
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
				AdvancedPaddle_Toggle, music_toggle, sound_toggle, RAdvancedPaddle_toggle = get_toggle_state(AdvancedPaddle_Toggle_button, AdvancedPaddle_Toggle, music_toggle_button, music_toggle, sound_toggle_button, sound_toggle, RAdvancedPaddle_toggle_button, RAdvancedPaddle_toggle)
				if music_toggle:
					pg.mixer.music.set_volume(1)
				elif not music_toggle:
					pg.mixer.music.set_volume(0)

				if clicked_button:
					if sound_toggle:
						BUTTON_SELECT_AUDIO.play()
					clicked_button = False
				if clicked_back:
					run_options_menu = False
					VEL = paddle_tbox_text
					BALL_VEL = ball_tbox_text

				#text box
				paddle_tbox_focus, paddle_tbox_text = paddle_tbox.checkForInput(pg.mouse.get_pos())
				ball_tbox_focus, ball_tbox_text = ball_tbox.checkForInput(pg.mouse.get_pos())
				if RAdvancedPaddle_toggle:
					RAdvancedPaddle_tbox_focus, RAdvancedPaddle_tbox_text = RAdvancedPaddle_tbox.checkForInput(pg.mouse.get_pos())
			paddle_tbox_text = paddle_tbox.logic(event)
			ball_tbox_text = ball_tbox.logic(event)
			if RAdvancedPaddle_toggle:
				RAdvancedPaddle_tbox_text = RAdvancedPaddle_tbox.logic(event)
		#print(RAdvancedPaddle_tbox_focus)
		draw_options_menu(options_back_button, AdvancedPaddle_Toggle_button, music_toggle_button, sound_toggle_button, RAdvancedPaddle_toggle_button, paddle_tbox_text)

#gamemode select functiona
def draw_gamemode_select():
	WIN.blit(MAIN_MENU_BACKGROUND, (0, 0))
	gamemode_back_button.changeColor(pg.mouse.get_pos())
	gamemode_back_button.update()

	onedefault_button.changeColor(pg.mouse.get_pos())
	onedefault_button.update()

	twodefault_gbutton.animate(0.1, 60, False)
	gbutton_spritegroup.draw(WIN)
	
	gbutton_spritegroup.update()
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
				clicked_2pdefault = twodefault_gbutton.checkForInput(pg.mouse.get_pos())
				if clicked_back:
					run_gamemode_select = False
				elif clicked_2pdefault:
					run_gamemode_select = False

				if clicked_button:
					if sound_toggle:
						BUTTON_SELECT_AUDIO.play()
					clicked_button = False

		draw_gamemode_select()
	killanimate2pdefault = True
	
#setting music
if music_toggle:
	pg.mixer.music.play(-1)
	pg.mixer.music.set_volume(1)
else:
	pg.mixer.music.play(-1)
	pg.mixer.music.set_volume(0)


run_main = True
first = True
while run_main:
	#main menu
	if clicked_back or first:
		main_menu()
		first = False

	#options menu
	if clicked_options:
		if sound_toggle:
			BUTTON_SELECT_AUDIO.play()
		clicked_options = False
		options_menu()

	#gamemode select menu
	if clicked_play:
		if sound_toggle:
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


def draw(lpaddle, rpaddle, ball, logo, pause, count_num, go_fade_num):
	WIN.fill(GREY)
	WIN.blit(LPADDLE, (lpaddle.x, lpaddle.y))
	WIN.blit(RPADDLE, (rpaddle.x, rpaddle.y))
	WIN.blit(BALL, (ball.x, ball.y))
	draw_text(str(score_val['l']), (430, 40))
	draw_text(str(score_val['r']), (470, 40))
	WIN.blit(LOGO, (logo.x, logo.y))

	if countdown.check_status()[2]:
		draw_text(str(count_num), (450, 350))

	if go_fade.check_status()[2] and not pause and not fix_go:
		draw_text('GO!', (450, 350), (go_fade_num, go_fade_num, go_fade_num))
	
	global fix_go_frame
	if go_delay.check_status()[2] and not pause or fix_go_frame:
		draw_text('GO!', (450, 350), WHITE)
		fix_go_frame = False
			
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
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	elif ball.x + BALL_RAD + tball_vel[0] >= rpaddle.x and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT and ball.x <= rpaddle.x + 2:#right
		tball_vel[0] *= -1
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	#upper paddle collision
	if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= lpaddle.y and ball.y + tball_vel[1] <= lpaddle.y + 5:#left
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_w]:
			ball.y = lpaddle.y - abs(tball_vel[1] - 2) - BALL_RAD
			tball_vel[1] += VEL
		tball_vel[1] *= -1
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + 5:#right
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_UP]:
			ball.y = rpaddle.y - abs(tball_vel[1] - 2) - BALL_RAD
			tball_vel[1] += VEL
		tball_vel[1] *= -1
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	#lower paddle collision
	if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= lpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= lpaddle.y + PADDLE_HIEGHT:#left
		keys_pressed = pg.key.get_pressed()
		tball_vel[1] *= -1
		if keys_pressed[pg.K_s]:
			ball.y = lpaddle.y + PADDLE_HIEGHT + abs(tball_vel[1]) + 2#moving ball out of paddle
			tball_vel[1] += VEL
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= rpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT:#right
		keys_pressed = pg.key.get_pressed()
		tball_vel[1] *= -1
		if keys_pressed[pg.K_DOWN]:
			ball.y = rpaddle.y + PADDLE_HIEGHT + abs(tball_vel[1]) + 2#moving ball out of paddle
			tball_vel[1] += VEL
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()


#advanced paddle collision functions
def calculate_projectory(paddle, ball, BALL_RAD):
	global tball_vel
	vel_before = tball_vel[0]
	#projectory calc
	paddle_mid = paddle.y + PADDLE_HIEGHT / 2
	distance = ball.y + BALL_RAD / 2 - paddle_mid
	tball_vel[1] = distance / 5
	x = abs(PADDLE_HIEGHT / 2 - (abs(distance)/ 1)) / 30
	#print(x)
	tball_vel[0] *= x
	#forcing it to change dir
	if vel_before < 0:
		tball_vel[0] = abs(tball_vel[0])
	elif vel_before > 0:
		tball_vel[0] = -abs(tball_vel[0])

	#capping max speed
	for vel in range(len(tball_vel)):
		if tball_vel[vel] >  BALL_VEL * 1.65:
			tball_vel[vel] = BALL_VEL * 1.65
		elif tball_vel[vel] < BALL_VEL * 1.65 * -1:
			tball_vel[vel] = BALL_VEL * 1.65 * -1
	#print(tball_vel[0])
	#tball_vel[1] = BALL_VEL
def randomize_projectory(tball_vel):
	num = random.randint(100 - RAdvancedPaddle_tbox_text, 100 + RAdvancedPaddle_tbox_text) / 100
	tball_vel[1] *= num
	print(f'randomized: {int(num*10)}%, raw: {num}')
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
		
		#calculating projectory
		calculate_projectory(lpaddle, ball, BALL_RAD)
		tball_vel = randomize_projectory(tball_vel)
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	elif ball.x + BALL_RAD + tball_vel[0] >= rpaddle.x and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT and ball.x <= rpaddle.x + 2:#right
		
		#calculating projectory
		calculate_projectory(rpaddle, ball, BALL_RAD)
		tball_vel = randomize_projectory(tball_vel)
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()

	#upper paddle collision
	if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= lpaddle.y and ball.y + tball_vel[1] <= lpaddle.y + 5:#left
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_w]:
			ball.y = lpaddle.y - abs(tball_vel[1] - 2) - BALL_RAD
			tball_vel[1] += VEL
		tball_vel[1] *= -1
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] + BALL_RAD >= rpaddle.y and ball.y + tball_vel[1] <= rpaddle.y + 5:#right
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_UP]:
			ball.y = rpaddle.y - abs(tball_vel[1] - 2) - BALL_RAD
			tball_vel[1] += VEL
		tball_vel[1] *= -1
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	#lower paddle collision
	if ball.x + tball_vel[0] + BALL_RAD >= lpaddle.x and ball.x + tball_vel[0] <= lpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= lpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= lpaddle.y + PADDLE_HIEGHT:#left
		keys_pressed = pg.key.get_pressed()
		tball_vel[1] *= -1
		if keys_pressed[pg.K_s]:
			ball.y = lpaddle.y + PADDLE_HIEGHT + abs(tball_vel[1]) + 2#moving ball out of paddle
			tball_vel[1] += VEL
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()
	elif ball.x + tball_vel[0] + BALL_RAD >= rpaddle.x and ball.x + tball_vel[0] <= rpaddle.x + PADDLE_WIDTH and ball.y + tball_vel[1] >= rpaddle.y + PADDLE_WIDTH - 5 and ball.y + tball_vel[1] <= rpaddle.y + PADDLE_HIEGHT:#right
		keys_pressed = pg.key.get_pressed()
		tball_vel[1] *= -1
		if keys_pressed[pg.K_DOWN]:
			ball.y = rpaddle.y + PADDLE_HIEGHT + abs(tball_vel[1]) + 2#moving ball out of paddle
			tball_vel[1] += VEL
		if sound_toggle:
			PADDLE_COLLSION_AUDIO.play()

	#resetting speed if bug accurs
	for vel in range(len(tball_vel)):
		if -1 <= tball_vel[vel] <= 1:
			tball_vel[vel] = BALL_VEL

def handle_score(ball, BALL_RAD, score_val, lpaddle, rpaddle, go_fade_num):
	#detecting score
	if ball.x + BALL_RAD + 20 < 0:
		score_val['r'] += 1
		reset_main(ball, lpaddle, rpaddle)
	elif ball.x - 20 > 900:
		score_val['l'] += 1
		reset_main(ball, lpaddle, rpaddle)
	
	#starting the countdown
	if start_count:
		countdown.count()
		count_num = countdown.check_status()[1]
		global remote_pause
		if not countdown.check_status()[2]:
			remote_pause = False
		else:
			remote_pause = True
		#print(countdown.check_status())

	#handleing GO! fadeing
	global start_go
	if not countdown.check_status()[2] and start_go:
		global remote_restart_go_fade
		if remote_restart_go_fade:
			remote_restart_go_fade = False
			go_fade.restart()
		go_fade.count()
		go_fade_num = int(go_fade.check_status()[1] * 3 * 1.45 + 20)#scaling 1-50 timer to 20-236 scale
		global fix_go
		fix_go = False
		if not go_fade.check_status()[2]:
			start_go = False

	#handleing GO! fade delay
	global start_go_delay
	if not countdown.check_status()[2] and start_go_delay:
		global remote_restart_go_delay
		if remote_restart_go_delay:
			remote_restart_go_delay = False
			go_delay.restart()
		go_delay.count()
		if not go_delay.check_status()[2]:
			go_delay.force_finish()
			start_go_delay = False
			start_go = True
			global fix_go_frame#go doesnt show for 1 frame before fading
			fix_go_frame = True
			#print('test')
	#print(go_fade.check_status())

	return score_val, count_num, go_fade_num


def reset_main(ball, lpaddle, rpaddle):
	#resseting sprite position
	ball.x, ball.y = 435, 280
	lpaddle.x, lpaddle.y = 18, 242
	rpaddle.x, rpaddle.y = 852, 242
	global tball_vel
	for vel in range(len(tball_vel)):
		tball_vel[vel] = BALL_VEL
	#randomizing ball
	tball_vel = random_ball(tball_vel)
	#counting down
	global start_count, pause
	start_count = True
	countdown.restart()
	go_fade.force_finish()
	# pause = True
	#setting delay
	global start_go_delay
	start_go_delay = True
	global remote_restart_go_fade
	remote_restart_go_fade = True
	global remote_restart_go_delay
	remote_restart_go_delay = True



def main(lscore, rscore, score_val, AdvancedPaddle_Toggle, go_fade_num):
	#loading assets
	lpaddle = pg.Rect(18, 242, PADDLE_WIDTH, PADDLE_HIEGHT)
	rpaddle = pg.Rect(852, 242, PADDLE_WIDTH, PADDLE_HIEGHT)
	ball = pg.Rect(438, 280, BALL_RAD, BALL_RAD)
	logo = pg.Rect(20, 540, 40, 40)
	reset_main(ball, lpaddle, rpaddle)
	global pause, fix_go
	pause = True
	fix_go = True#GO message glitch makes it pre blit once at the start
	run_main = True
	while run_main:
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
		score_val, count_num, go_fade_num = handle_score(ball, BALL_RAD, score_val, lpaddle, rpaddle, go_fade_num)
		pause = draw(lpaddle, rpaddle, ball, logo, pause, count_num, go_fade_num)
		if remote_pause:
			pause = True
		else:
			pause = False
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


	pass

#starting
if clicked_2pdefault:
	fade_music = threading.Thread(target = fade_main_menu_music)
	fade_music.daemon = True
	fade_music.start()
	if __name__ == '__main__':
		main(lscore, rscore, score_val, AdvancedPaddle_Toggle, go_fade_num)