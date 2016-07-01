#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pygame.transform
import sys
import random

from pygame.locals import *

def main():

	pygame.init()

	Reloj= pygame.time.Clock()

	Ventana = pygame.display.set_mode((1400, 720))

	pygame.display.set_caption("juego")
	Fondo = pygame.image.load("fondo.jpg")
	Imagen = pygame.image.load("player_mage_sheet.png")

	transparente = Imagen.get_at((0, 0))
	Imagen.set_colorkey(transparente)

	MiMonigotillo = Monigotillo((300, 200), Imagen)

	Monedas = []

	Puntuacion = 0

# Array de monedas
	for i in range (5):
		coor_random = (random.randint(50,1350),random.randint(50,670))
		Monedas.append(Moneda(coor_random))
# Array de monstruos

	Slimes = []

	for i in range(5):
		coor_random = (random.randint(50,1350),random.randint(50,670))
		Slimes.append(Slime(coor_random))

# Array para ataques
	Attacks = []

	coordX = 300
	coordY = 200
	Coordenadas = (coordX, coordY)

	incrementoX = 0
	incrementoY = 0

	movimiento = False
	direccion = 'Abajo'


	
	start_ticks=pygame.time.get_ticks()

	while True:

		MiMonigotillo.update(Coordenadas,direccion,movimiento)

		for moneda in Monedas:
			moneda.update()

		for attack in Attacks:
			attack.update(movimiento)
			if attack.x > 1400 or attack.x < 0 or attack.y > 720 or attack.x < 0:
				Attacks.remove(attack)

		for slime in Slimes:
			slime.update(movimiento)

		Ventana.blit(pygame.transform.scale(Fondo,(1400,720)),(0,0))
		Ventana.blit(MiMonigotillo.image, MiMonigotillo.rect)

		for moneda in Monedas:
			Ventana.blit(moneda.image,moneda.rect)

		for slime in Slimes:
			Ventana.blit(slime.image,slime.rect)

		for attack in Attacks:
			Ventana.blit(attack.image,attack.rect)

		pygame.display.flip()


		for moneda in Monedas:
			if (pygame.sprite.collide_rect(moneda,MiMonigotillo)):
				Monedas.remove(moneda)
				Puntuacion = Puntuacion + 100
				if not Monedas:

					now_ticks = pygame.time.get_ticks()
					sec_passed = (now_ticks-start_ticks)/1000

					Puntuacion = Puntuacion + sec_passed*100

					Fuente= pygame.font.Font(None, 100)
					Texto = Fuente.render("Congratulations!", True, (204,204,0))
					Ventana.blit(Texto, (375, 200))
					Texto_puntuacion = Fuente.render( "Score:"+str(Puntuacion), True, (204,204,0))
					Ventana.blit(Texto_puntuacion, (500, 300))
					Texto2 = Fuente.render("Space bar to play again", True, (204,204,0))
					Ventana.blit(Texto2, (320, 370))
					pygame.display.flip()
				
					win()

		for slime in Slimes:
			for attack in Attacks:
				if (pygame.sprite.collide_rect(slime,attack)):
					Attacks.remove(attack)
					slime.vidas -= 1
					if slime.vidas == 0:
						Slimes.remove(slime)

			if (pygame.sprite.collide_rect(slime,MiMonigotillo)):
				Fuente= pygame.font.Font(None, 100)
				Texto = Fuente.render("Game Over", True, (153,0,0))
				Texto_puntuacion = Fuente.render( "Score:"+str(Puntuacion), True, (153,0,0))
				Ventana.blit(Texto, (430, 200))
				Ventana.blit(Texto_puntuacion, (430, 300))
				Texto2 = Fuente.render("Space bar to retry", True, (153,0,0))
				Ventana.blit(Texto2, (330, 400))
				pygame.display.flip()
				# Si pulsamos barra espaciadora reiniciamos el blucle
				gameover()


		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sys.exit()
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE :
					sys.exit()

				elif evento.key == pygame.K_RIGHT:
					incrementoX += 3
					movimiento = True
					direccion = 'Derecha'

				elif evento.key == pygame.K_DOWN:
					incrementoY += 3
					movimiento = True
					direccion = 'Abajo'

				elif evento.key == pygame.K_LEFT:
					incrementoX -= 3
					movimiento = True
					direccion = 'Izquierda'

				elif evento.key == pygame.K_UP:
					incrementoY -= 3
					movimiento = True
					direccion = 'Arriba'

				elif evento.key == pygame.K_SPACE:
					if MiMonigotillo.CanAttack > 1:
						MiMonigotillo.CanAttack = 0
						Attacks.append(ranged_attack((coordX,coordY),direccion))


			if evento.type == pygame.KEYUP:

				if evento.key == pygame.K_RIGHT:
					incrementoX -= 3

				elif evento.key == pygame.K_DOWN:
					incrementoY -= 3

				elif evento.key == pygame.K_LEFT:
					incrementoX += 3	

				elif evento.key == pygame.K_UP:
					incrementoY += 3

				if incrementoX == 0 and incrementoY == 0:
					movimiento = False


		if not(coordX >= 1368 and incrementoX > 0) and not(coordX <= 32 and incrementoX < 0) :
			coordX = coordX + incrementoX

		if not(coordY >= 678 and incrementoY > 0) and not(coordY <= 32 and incrementoY < 0) :
			coordY = coordY + incrementoY

		Coordenadas = (coordX, coordY)

		Reloj.tick(50)
		# now_ticks = pygame.time.get_ticks()
		# sec_passed = 24 - (now_ticks-start_ticks)/1000
		# dec_sec_passed = 1000 - (now_ticks-start_ticks)%1000


		# Fuente = pygame.font.Font(None,30)
		# Texto = Fuente.render(str(sec_passed) +':'+ str(dec_sec_passed)[:2], True, (255,255,255))
		# Ventana.blit(Texto, (0, 0))
		# Texto2 = Fuente.render("SCORE: "+str(Puntuacion),True,(255,255,255))
		# Ventana.blit(Texto2,(1230,10))
		# pygame.display.flip()

		# if (24.8 - (now_ticks-start_ticks)/1000.0) < 0.0:


		# 	Fuente= pygame.font.Font(None, 100)
		# 	Texto = Fuente.render("Congratulations!", True, (204,204,0))
		# 	Ventana.blit(Texto, (375, 200))
		# 	Texto_puntuacion = Fuente.render( "Score:"+str(Puntuacion), True, (204,204,0))
		# 	Ventana.blit(Texto_puntuacion, (500, 300))
		# 	Texto2 = Fuente.render("Space bar to play again", True, (204,204,0))
		# 	Ventana.blit(Texto2, (320, 370))
		# 	pygame.display.flip()
		
		# 	win()

class Monigotillo(pygame.sprite.Sprite):

	def __init__(self, coordenadas, imagen):
		pygame.sprite.Sprite.__init__(self)

		self.ImgCompleta = imagen
		self.CanAttack = 0

		a=0
		arrayAnimDerecha = []
		arrayAnimAbajo = []
		arrayAnimArriba = []

		self.arrayAnim=[]
		self.arrayAnim_abajo = []
		self.arrayAnim_izquierda = []
		self.arrayAnim_derecha = []
		self.arrayAnim_arriba = []


		for a in range(10):
			self.arrayAnim_derecha.append(self.ImgCompleta.subsurface((a*32,515,32,64)))
			self.arrayAnim_abajo.append(self.ImgCompleta.subsurface((a*32,365,32,64)))
			self.arrayAnim_arriba.append(self.ImgCompleta.subsurface((a*32,290,32,64)))
			self.arrayAnim_izquierda.append(self.ImgCompleta.subsurface((a*32,440,32,64)))


		self.anim= 0
		self.actualizado = pygame.time.get_ticks()
		self.image = self.arrayAnim_abajo[self.anim]
		self.rect = self.image.get_rect()
		self.rect.center = coordenadas


	def update(self, nuevas_coordenadas,direccion,movimiento):
		self.rect.center = nuevas_coordenadas

		if self.actualizado + 100 < pygame.time.get_ticks() and movimiento:
			self.anim= self.anim + 1
			if self.anim > 9:
				self.anim= 0

			if direccion == 'Abajo':
				self.image = self.arrayAnim_abajo[self.anim]

			if direccion == 'Arriba':
				self.image = self.arrayAnim_arriba[self.anim]

			if direccion == 'Derecha':
				self.image = self.arrayAnim_derecha[self.anim]

			if direccion == 'Izquierda':
				self.image = self.arrayAnim_izquierda[self.anim]

			self.actualizado= pygame.time.get_ticks()
			if movimiento:
				self.CanAttack += 1

class ranged_attack(pygame.sprite.Sprite):
	
	def __init__(self, coordenadas,direccion):
		pygame.sprite.Sprite.__init__(self)

		self.x = coordenadas[0]
		self.y = coordenadas[1]
		self.Direccion = direccion
		self.arrayAnim = []

		self.arrayAnim = []
		imagen = pygame.image.load("ball.png")
		
		self.arrayAnim.append(imagen.subsurface((64,64,32,32)))
		self.arrayAnim.append(imagen.subsurface((64,32,32,32)))
		self.arrayAnim.append(imagen.subsurface((64,0,32,32)))	
		self.arrayAnim.append(imagen.subsurface((64,32,32,32)))	


		self.anim= 0

		self.actualizado = pygame.time.get_ticks()
		self.image = self.arrayAnim[self.anim]
		self.rect = self.image.get_rect()
		self.rect.center = coordenadas	

	def update(self,movimiento):

			self.rect.center = (self.x,self.y)
			
			if self.actualizado + 120 < pygame.time.get_ticks():
				self.anim= self.anim + 1
				if self.anim > 3:
					self.anim= 0

				self.image = self.arrayAnim[self.anim]
				self.actualizado= pygame.time.get_ticks()

			if movimiento:
			
				if self.Direccion == "Derecha":
					self.x += 10

				if self.Direccion == "Izquierda":
					self.x -= 10

				if self.Direccion == "Abajo":
					self.y += 10

				if self.Direccion == "Arriba":
					self.y -= 10


class Boss_attack_1(pygame.sprite.Sprite):
	
	def __init__(self, coordenadas,direccion):
		pygame.sprite.Sprite.__init__(self)

		self.x = coordenadas[0]
		self.y = coordenadas[1]
		self.Direccion = direccion
		self.arrayAnim = []

		self.arrayAnim = []
		imagen = pygame.image.load("ball.png")
		
		self.arrayAnim.append(imagen.subsurface((64,64,32,32)))
		self.arrayAnim.append(imagen.subsurface((64,32,32,32)))
		self.arrayAnim.append(imagen.subsurface((64,0,32,32)))	
		self.arrayAnim.append(imagen.subsurface((64,32,32,32)))	


		self.anim= 0

		self.actualizado = pygame.time.get_ticks()
		self.image = self.arrayAnim[self.anim]
		self.rect = self.image.get_rect()
		self.rect.center = coordenadas	

	def update(self,movimiento):

			self.rect.center = (self.x,self.y)
			
			if self.actualizado + 120 < pygame.time.get_ticks():
				self.anim= self.anim + 1
				if self.anim > 3:
					self.anim= 0

				self.image = self.arrayAnim[self.anim]
				self.actualizado= pygame.time.get_ticks()

			if movimiento:
			
				if self.Direccion == "Derecha":
					self.x += 10

				if self.Direccion == "Izquierda":
					self.x -= 10

				if self.Direccion == "Abajo":
					self.y += 10

				if self.Direccion == "Arriba":
					self.y -= 10

					

class Moneda(pygame.sprite.Sprite):

	def __init__(self, coordenadas):
		pygame.sprite.Sprite.__init__(self)

		self.arrayAnim = []

		for i in range(1,7):
			self.arrayAnim.append(pygame.image.load("Coin"+str(i)+".png"))

		self.anim= 0

		self.actualizado = pygame.time.get_ticks()
		self.image = self.arrayAnim[self.anim]
		self.rect = self.image.get_rect()
		self.rect.center = coordenadas	

	def update(self):

		if self.actualizado + 70 < pygame.time.get_ticks():
			self.anim= self.anim + 1
			if self.anim > 5:
				self.anim= 0

			self.image = self.arrayAnim[self.anim]

			self.actualizado= pygame.time.get_ticks()

class Slime(pygame.sprite.Sprite):

	def __init__(self, coordenadas):
		pygame.sprite.Sprite.__init__(self)

		self.vidas = 3

		self.x = coordenadas[0]
		self.y = coordenadas[1]
		self.mismadirec = 0
		self.incrementoX = 0
		self.incrementoY = 0

		self.arrayAnim = []
		imagen = pygame.image.load("slime.png")
	
		self.arrayAnim.append(pygame.transform.scale(imagen.subsurface((0,32,32,32)),(64,64)))
		self.arrayAnim.append(pygame.transform.scale(imagen.subsurface((32,32,32,32)),(64,64)))
		
		self.anim= 0
		self.actualizado = pygame.time.get_ticks()
		self.image = self.arrayAnim[self.anim]
		self.rect = self.image.get_rect()
		self.rect.center = coordenadas	

	def update(self, movimiento):
		self.rect.center = (self.x,self.y)
		self.mismadirec = self.mismadirec + 1

		if self.mismadirec > 10:
			self.mismadirec = 0

		if self.actualizado + 170 < pygame.time.get_ticks():
			self.anim= self.anim + 1
			if self.anim > 1:
				self.anim= 0

			self.image = self.arrayAnim[self.anim]

			self.actualizado= pygame.time.get_ticks()

		if self.mismadirec % 10 == 0:

			self.incrementoX = random.choice([-4,4,0])			
			self.incrementoY = random.choice([-4,4,0])

		if movimiento:
			
			self.x = self.x + self.incrementoX 
			self.y = self.y + self.incrementoY

			if self.x > 1400 or self.x < 0 and self.mismadirec % 3 == 0 :
				self.incrementoX = self.incrementoX * (-1)
				self.mismadirec = 0

			if self.y > 720 or self.y < 0 and self.mismadirec % 3 == 0 :
				self.incrementoY = self.incrementoY * (-1)
				self.mismadirec = 0

def gameover():

	pygame.event.clear()
	while True:
		evento = pygame.event.wait()

		if evento.type == pygame.QUIT:
			sys.exit()

		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_ESCAPE :
				sys.exit()

			if evento.key == pygame.K_SPACE :
				main()

def win():

	pygame.event.clear()

	while True:
		evento = pygame.event.wait()

		if evento.type == pygame.QUIT:
			sys.exit()

		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_ESCAPE :
				sys.exit()

			if evento.key == pygame.K_SPACE :
				main()

def name():
	pygame.init()
	screen = pygame.display.set_mode((480, 360))
	name = ""
	font = pygame.font.Font(None, 50)
	while True:
		for evt in pygame.event.get():
			if evt.type == KEYDOWN:
				if evt.unicode.isalpha():
					name += evt.unicode
				elif evt.key == K_BACKSPACE:
					name = name[:-1]
				elif evt.key == K_RETURN:
					name = ""
			elif evt.type == QUIT:
				return
		screen.fill((0, 0, 0))
		block = font.render(name, True, (255, 255, 255))
		rect = block.get_rect()
		rect.center = screen.get_rect().center
		screen.blit(block, rect)
		pygame.display.flip()


main()