#!/usr/bin/python3

import pygame
import objects
from objects import Vector
import time
from colour import Colour

# Global Declare
g_displayWidth = 800
g_displayHeight = 800
g_display = Vector(g_displayWidth,g_displayHeight)

# Create Pygame Window
g_displayWindow = pygame.display.set_mode(g_display.t())
g_gameClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("PyStick")

def gameLoop(gameDisplay):
	gameExit = False
	gamePaused = True
	Sprites = objects.Sprite.All
	Mouse = Vector()
		
	# Load Player
	P1 = objects.Character('assets\\survivor',Vector(120,120),Vector(120,120))
	P1.name = 'player'

	# Set Stating position
	startPos = (g_display / 2) - (P1.box / 2)
	P1.position = startPos

	keyLEFT = keyRIGHT = keyUP = keyDOWN = 0

	# GameLoop
	while not gameExit:

		# Read Events
		for event in pygame.event.get():
			# Exit if window quits
			if event.type == pygame.QUIT:
				gameExit = True

			if event.type == pygame.MOUSEMOTION:
				Mouse = Vector(event.pos[0],event.pos[1])

			if event.type == pygame.MOUSEBUTTONDOWN:
				if P1.state == 'idle' or P1.state == 'move':
					if event.button == 1:
						P1.changeAnimation(P1.holding,'shoot')
					elif event.button == 3:
						P1.changeAnimation(P1.holding,'meleeattack')
 
			# Read key Values
			if event.type == pygame.KEYDOWN:
				key = event.unicode.lower()
				if key == 'a':
					keyLEFT = 1
				elif key == 'd':
					keyRIGHT = 1
				elif key == 'w':
					keyUP = 1
				elif key == 's':
					keyDOWN = 1
				elif key == ' ':
					gamePaused = not gamePaused
				elif key == 'r':
					if P1.state == 'idle' or P1.state == 'move':
						P1.changeAnimation(P1.holding,'reload')
			if event.type == pygame.KEYUP:
				key = chr(event.key).lower()
				if key == 'a':
					keyLEFT = 0
				elif key == 'd':
					keyRIGHT = 0
				elif key == 'w':
					keyUP = 0
				elif key == 's':
					keyDOWN = 0
				elif event.key == pygame.K_ESCAPE:
					gameExit = True

		gameDisplay.fill(Colour.DavyGrey)

		# Run Simulation
		if not gamePaused:
			P1.move(Vector(keyRIGHT - keyLEFT,keyDOWN - keyUP) * P1.movespeed)

			if P1.changed['moving']:
				if P1.moving and P1.state == 'idle':
					P1.changeAnimation(P1.holding,'move')
				elif not P1.moving and P1.state == 'move':
					P1.changeAnimation(P1.holding,'idle')

			P1.setang(P1.direction(Mouse))

			#DRAW TO FRAME
			Sprites.draw(gameDisplay)

		#UPDATE DISPLAY
		pygame.display.update()
		g_gameClock.tick(60)

# START GAME LOOP
gameLoop(g_displayWindow)
pygame.quit()
quit()
