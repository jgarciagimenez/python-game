#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pygame.transform
import sys
import random
import math
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MySQLdb as db

from pygame.locals import *

Vidas = 3
Puntuacion = 0
Name = None

def nivel1(MyName):
	global Name
	Name = MyName
	pygame.init()

	Reloj= pygame.time.Clock()

	Ventana = pygame.display.set_mode((1400, 720))

	pygame.display.set_caption("juego")
	Fondo = pygame.image.load("Fondo.jpg")
	Imagen = pygame.image.load("player_mage_sheet.png")
	Corazon = pygame.image.load("heart.png")


	transparente = Imagen.get_at((0, 0))
	Imagen.set_colorkey(transparente)

	MiMonigotillo = Monigotillo((100, 360), Imagen)

	global Puntuacion
	global Vidas
	Vidas = 3


	Slimes = []

	for i in range(4):
		coor_random = (random.randint(700,1350),random.randint(50,670))
		Slimes.append(Slime(coor_random))

	# Array para ataques
	Attacks = []

	# Array para ataques de boss
	
	slime_Attacks = []

	coordX = 100
	coordY = 360
	Coordenadas = (coordX, coordY)

	incrementoX = 0
	incrementoY = 0

	movimiento = False
	direccion = 'Abajo'


	
	start_ticks=pygame.time.get_ticks()

	while True:

		now_ticks = pygame.time.get_ticks()
		MiMonigotillo.update(Coordenadas,direccion,movimiento)

		for attack in Attacks:
			attack.update(movimiento)
			if attack.x > 1400 or attack.x < 0 or attack.y > 720 or attack.x < 0:
				Attacks.remove(attack)

		for slime in Slimes:
			slime.update(movimiento)
			if slime.CanAttack > 100:
				slime.CanAttack = 0
				slime_Attacks.append( slime_attack((slime.x,slime.y),(Coordenadas)))

		for attack in slime_Attacks:			
			attack.update(movimiento)
			if attack.x > 1400 or attack.x < 0 or attack.y > 720 or attack.x < 0:
				slime_Attacks.remove(attack)


		Ventana.blit(pygame.transform.scale(Fondo,(1400,720)),(0,0))
		Ventana.blit(MiMonigotillo.image, MiMonigotillo.rect)
		Ventana.blit(Corazon,(1280,15))

		for slime in Slimes:
			Ventana.blit(slime.image,slime.rect)

		for attack in Attacks:
			Ventana.blit(attack.image,attack.rect)

		for attack in slime_Attacks:
			Ventana.blit(attack.image,attack.rect)
			if (pygame.sprite.collide_rect(attack,MiMonigotillo)):
				Vidas -= 1
				slime_Attacks.remove(attack)

				if  Vidas == 0:
					Fuente= pygame.font.Font(None, 100)
					Texto = Fuente.render("Game Over", True, (153,0,0))
					Texto2 = Fuente.render("Space bar to retry", True, (153,0,0))
					Ventana.blit(Texto2, (330, 400))
					pygame.display.flip()
					# Si pulsamos barra espaciadora reiniciamos el blucle
					gameover()


		pygame.display.flip()


		# for moneda in Monedas:
		# 	if (pygame.sprite.collide_rect(moneda,MiMonigotillo)):
		# 		Monedas.remove(moneda)
		# 		Puntuacion = Puntuacion + 100
		# 		if not Monedas:

		# 			now_ticks = pygame.time.get_ticks()
		# 			sec_passed = (now_ticks-start_ticks)/1000

		# 			Puntuacion = Puntuacion + sec_passed*100

		# 			Fuente= pygame.font.Font(None, 100)
		# 			Texto = Fuente.render("Congratulations!", True, (204,204,0))
		# 			Ventana.blit(Texto, (375, 200))
		# 			Texto_puntuacion = Fuente.render( "Score:"+str(Puntuacion), True, (204,204,0))
		# 			Ventana.blit(Texto_puntuacion, (500, 300))
		# 			Texto2 = Fuente.render("Space bar to play again", True, (204,204,0))
		# 			Ventana.blit(Texto2, (320, 370))
		# 			pygame.display.flip()
				
		# 			win()

		for slime in Slimes:
			for attack in Attacks:
				if (pygame.sprite.collide_rect(slime,attack)):
					Attacks.remove(attack)
					slime.vidas -= 1
					if slime.vidas == 0:
						Slimes.remove(slime)
						if not Slimes:
							Fuente= pygame.font.Font(None, 100)
							Texto = Fuente.render("Congratulations!", True, (204,204,0))
		 					Ventana.blit(Texto, (375, 200))
		 					pygame.display.flip()
		 					Texto2 = Fuente.render("Return to next level", True, (204,204,0))
		 			  		Ventana.blit(Texto2, (320, 370))
		 			  		pygame.display.flip()

		 					now_ticks = pygame.time.get_ticks()
							sec_passed = (now_ticks-start_ticks)/1000
		 					Puntuacion += Puntuacion + (50-sec_passed)*100

		 			  		lvl1to2()


			if (pygame.sprite.collide_rect(slime,MiMonigotillo)):

				Vidas -= 1
				if Vidas == 0:
					Fuente= pygame.font.Font(None, 100)
					Texto = Fuente.render("Game Over", True, (153,0,0))
					Texto2 = Fuente.render("Return bar to retry", True, (153,0,0))
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
		now_ticks = pygame.time.get_ticks()
		sec_passed = (now_ticks-start_ticks)/1000
		dec_sec_passed = now_ticks-start_ticks%1000


		Fuente = pygame.font.Font(None,40)
		Texto = Fuente.render(str(sec_passed) +':'+ str(dec_sec_passed)[:2], True, (255,255,255))
		Ventana.blit(Texto, (30, 10))
		Texto2 = Fuente.render(": "+str(Vidas),True,(255,255,255))
		Ventana.blit(Texto2,(1330,25))
		pygame.display.flip()
		

def nivel2():

	global Vidas
	global Puntuacion

	pygame.init()

	Reloj= pygame.time.Clock()

	Ventana = pygame.display.set_mode((1400, 720))

	pygame.display.set_caption("juego")
	Fondo = pygame.image.load("Fondo.jpg")
	Imagen = pygame.image.load("player_mage_sheet.png")
	Corazon = pygame.image.load("heart.png")

	transparente = Imagen.get_at((0, 0))
	Imagen.set_colorkey(transparente)

	MiMonigotillo = Monigotillo((700, 600), Imagen)
	MiBoss = Boss((700,120))

	# Array para ataques
	Attacks = []

	# Array para ataques de boss
	
	Boss_Attacks = []

	coordX = 700
	coordY = 600
	Coordenadas = (coordX, coordY)

	incrementoX = 0
	incrementoY = 0

	movimiento = False
	direccion = 'Abajo'


	
	start_ticks=pygame.time.get_ticks()

	while True:

		now_ticks = pygame.time.get_ticks()
		MiMonigotillo.update(Coordenadas,direccion,movimiento)
		MiBoss.update(movimiento)

		if MiBoss.CanAttack > 70:
		 	MiBoss.CanAttack = 0
		 	Boss_Attacks.append( boss_attack_1((MiBoss.x,MiBoss.y),Coordenadas))


		for attack in Attacks:
			attack.update(movimiento)

			if (pygame.sprite.collide_rect(MiBoss,attack)):
				Attacks.remove(attack)
				MiBoss.vidas -= 1

				if MiBoss.vidas ==0:
					now_ticks = pygame.time.get_ticks()
					sec_passed = (now_ticks-start_ticks)/1000
					Puntuacion += Puntuacion + (100-sec_passed)*100

					Fuente= pygame.font.Font(None, 100)
					Texto = Fuente.render("Congratulations!", True, (204,204,0))
					Ventana.blit(Texto, (375, 200))
					pygame.display.flip()
					Texto_puntuacion = Fuente.render( "Score:"+str(Puntuacion), True, (204,204,0))
					Ventana.blit(Texto_puntuacion, (500, 300))
					Texto2 = Fuente.render("Return to play again", True, (204,204,0))
					Ventana.blit(Texto2, (320, 370))
					pygame.display.flip()

					win()


		 	if attack.x > 1400 or attack.x < 0 or attack.y > 720 or attack.x < 0:
		 		Attacks.remove(attack)


		for attack in Boss_Attacks:
			for ball in attack:
				ball.update(movimiento)

				if (pygame.sprite.collide_rect(MiMonigotillo,ball)):
					attack.remove(ball)
					Vidas -= 1

					if  Vidas == 0:
						Fuente= pygame.font.Font(None, 100)
						Texto = Fuente.render("Game Over", True, (153,0,0))
						Texto2 = Fuente.render("Return to retry", True, (153,0,0))
						Ventana.blit(Texto2, (330, 400))
						pygame.display.flip()
						# Si pulsamos barra espaciadora reiniciamos el blucle
						gameover()


				if ball.x > 1400 or ball.x < 0 or ball.y > 720 or ball.x < 0:
					attack.remove(ball)
			if not attack:
				Boss_Attacks.remove(attack)


		Ventana.blit(pygame.transform.scale(Fondo,(1400,720)),(0,0))
		Ventana.blit(MiMonigotillo.image, MiMonigotillo.rect)
		Ventana.blit(MiBoss.image,MiBoss.rect)
		Ventana.blit(Corazon,(1280,15))


		for attack in Attacks:
			Ventana.blit(attack.image,attack.rect)

		for attack in Boss_Attacks:
			for ball in attack:
				Ventana.blit(ball.image,ball.rect)

		pygame.display.flip()


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

		now_ticks = pygame.time.get_ticks()
		sec_passed = (now_ticks-start_ticks)/1000
		dec_sec_passed = now_ticks-start_ticks%1000

		Fuente = pygame.font.Font(None,40)
		Texto = Fuente.render(str(sec_passed) +':'+ str(dec_sec_passed)[:2], True, (255,255,255))
		Ventana.blit(Texto, (30, 10))
		Texto2 = Fuente.render(": "+str(Vidas),True,(255,255,255))
		Ventana.blit(Texto2,(1330,25))
		pygame.display.flip()


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

class target_attack (pygame.sprite.Sprite):
	
	def __init__(self, coordenadas,target):
		pygame.sprite.Sprite.__init__(self)

		self.x = coordenadas[0]
		self.y = coordenadas[1]
		self.target_x = target[0]
		self.target_y = target[1]
		self.arrayAnim = []

		self.arrayAnim = []
		imagen = pygame.image.load("ball2.png")
		
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
	

				self.x += int(self.target_x)
				self.y += int(self.target_y)

def boss_attack_1(coordenadas,target):

	Attacks = []

	## Calculamos el movimiento de cada ataque. Primero el ataque central
	modulo = dist(coordenadas,target)
	unidad = (((coordenadas[0] - target[0])*-1/modulo),((coordenadas[1] - target[1])*-1/modulo))
	central = (unidad[0]*4,unidad[1]*4)
	
	Attacks.append(target_attack(coordenadas,central))


	angulo = angulo_polares(unidad)
	
	for i in [0.50,-0.50,0.20,-0.20]:
	
			Attacks.append(target_attack(coordenadas,(unidad[0]+math.cos(angulo+i)*4,4*math.sin(angulo+i)+unidad[1])))

	return Attacks

def slime_attack(coordenadas,target):

	## Calculamos el movimiento de cada ataque. Primero el ataque central
	modulo = dist(coordenadas,target)
	unidad = (((coordenadas[0] - target[0])*-1/modulo),((coordenadas[1] - target[1])*-1/modulo))
	attack = (unidad[0]*6,unidad[1]*6)

	return target_attack(coordenadas,attack)			

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
		self.CanAttack = 0

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
			
			self.CanAttack += 1
			self.x = self.x + self.incrementoX 
			self.y = self.y + self.incrementoY

			if self.x > 1350 or self.x < 0 and self.mismadirec % 3 == 0 :
				self.incrementoX = self.incrementoX * (-1)
				self.mismadirec = 0

			if self.y > 670 or self.y < 0 and self.mismadirec % 3 == 0 :
				self.incrementoY = self.incrementoY * (-1)
				self.mismadirec = 0

class Boss(pygame.sprite.Sprite):

	def __init__(self, coordenadas):
		pygame.sprite.Sprite.__init__(self)

		self.vidas = 10

		self.x = coordenadas[0]
		self.y = coordenadas[1]
		self.incrementoX = 2
		self.CanAttack = 0

		self.arrayAnim = []		

	##############################################################################	
	## Thanks to Stephen "Redshrike" Challener for the boss sprite
	## Check it out at http://opengameart.org/content/harlequin-epicycle-mod
	##############################################################################

		self.arrayAnim.append(pygame.image.load("archon-1.png"))
		self.arrayAnim.append(pygame.image.load("archon-2.png"))
		self.arrayAnim.append(pygame.image.load("archon-3.png"))

		
		self.anim= 0
		self.actualizado = pygame.time.get_ticks()
		self.image = self.arrayAnim[self.anim]
		self.rect = self.image.get_rect()
		self.rect.center = coordenadas	

	def update(self, movimiento):
		self.rect.center = (self.x,self.y)

		if self.actualizado + 170 < pygame.time.get_ticks():
			self.anim= self.anim + 1
			if self.anim > 2:
				self.anim= 0

			self.image = self.arrayAnim[self.anim]
			self.actualizado= pygame.time.get_ticks()


		if movimiento:
			self.CanAttack += 1
			
			self.x += self.incrementoX

			if self.x <= 500 :
				self.incrementoX = 2
			if self.x >= 900:
				self.incrementoX -= 2

def dist (a,b):

	suma = (a[0]-b[0])*(a[0]-b[0])
	suma += (a[1]-b[1])*(a[1]-b[1])
	return math.sqrt(float(suma))

def gameover():

	pygame.event.clear()
	global Vidas
	Vidas = 3

	while True:
		evento = pygame.event.wait()

		if evento.type == pygame.QUIT:
			sys.exit()

		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_ESCAPE :
				sys.exit()

			if evento.key == pygame.K_RETURN:
				nivel1()

def win():

	pygame.event.clear()

	while True:
		evento = pygame.event.wait()

		if evento.type == pygame.QUIT:
			sys.exit()

		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_ESCAPE :
				sys.exit()

			if evento.key == pygame.K_RETURN :
				nivel1()

def lvl1to2():

	pygame.event.clear()

	while True:
		evento = pygame.event.wait()

		if evento.type == pygame.QUIT:
			sys.exit()

		if evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_ESCAPE :
				sys.exit()

			if evento.key == pygame.K_RETURN :
				nivel2()

def angulo_polares(a):

	x = a[0]
	y = a[1]

	if x > 0 and y >= 0:
		return math.atan(y/x)

	if x == 0 and y > 0:
		return math.pi/2

	if x < 0:
		return math.atan(y/x)+math.pi

	if x == 0 and y > 0:
		return math.pi*3/2

	if x > 0 and y < 0:
		return math.atan(y/x)+2*math.pi

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

