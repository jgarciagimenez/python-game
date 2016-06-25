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
	Imagen = pygame.image.load("monigotillo.png")

	transparente = Imagen.get_at((0, 0))
	Imagen.set_colorkey(transparente)

	MiMonigotillo = Monigotillo((300, 200), Imagen)

	Monedas = []

# Array de monedas
	for i in range (4):
		coor_random = (random.randint(50,1350),random.randint(50,670))
		Monedas.append(Moneda(coor_random))
# Array de monstruos

	Slimes = []

	for i in range(4):
		coor_random = (random.randint(50,1350),random.randint(50,670))
		Slimes.append(Slime(coor_random))

	coordX = 300
	coordY = 200
	Coordenadas = (coordX, coordY)

	incrementoX = 0
	incrementoY = 0

	movimiento = False
	direccion = 'Abajo'


	while True:

		MiMonigotillo.update(Coordenadas,direccion,movimiento)

		for moneda in Monedas:
			moneda.update()

		for slime in Slimes:
			slime.update(movimiento)

		Ventana.blit(pygame.transform.scale(Fondo,(1400,720)),(0,0))
		Ventana.blit(MiMonigotillo.image, MiMonigotillo.rect)

		for moneda in Monedas:
			Ventana.blit(moneda.image,moneda.rect)

		for slime in Slimes:
			Ventana.blit(slime.image,slime.rect)

		pygame.display.flip()


		for moneda in Monedas:
			if(pygame.sprite.collide_rect(moneda,MiMonigotillo)):
				Monedas.remove(moneda)


		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sys.exit()
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE :
					sys.exit()

				elif evento.key == pygame.K_RIGHT:
					incrementoX = 3
					movimiento = True
					direccion = 'Derecha'

				elif evento.key == pygame.K_DOWN:
					incrementoY = 3
					movimiento = True
					direccion = 'Abajo'

				elif evento.key == pygame.K_LEFT:
					incrementoX = -3
					movimiento = True
					direccion = 'Izquierda'

				elif evento.key == pygame.K_UP:
					incrementoY = -3
					movimiento = True
					direccion = 'Arriba'

			if evento.type == pygame.KEYUP:
				incrementoX = 0
				incrementoY = 0
				movimiento = False

		coordX = coordX + incrementoX
		coordY = coordY + incrementoY

		Coordenadas = (coordX, coordY)

		Reloj.tick(30)


class Monigotillo(pygame.sprite.Sprite):

	def __init__(self, coordenadas, imagen):
		pygame.sprite.Sprite.__init__(self)

		self.ImgCompleta = imagen

		a=0
		arrayAnimDerecha = []
		arrayAnimAbajo = []
		arrayAnimArriba = []

		self.arrayAnim=[]
		self.arrayAnim_abajo = []
		self.arrayAnim_izquierda = []
		self.arrayAnim_derecha = []
		self.arrayAnim_arriba = []


		while a < 6:
			arrayAnimDerecha.append(self.ImgCompleta.subsurface((a*32,160,32,64)))
			arrayAnimAbajo.append(self.ImgCompleta.subsurface((a*32,100,32,64)))
			arrayAnimArriba.append(self.ImgCompleta.subsurface((a*32,32,32,64)))
			a= a + 1

		orden = [3,2,1,3,4,5]
		for i in orden:
			self.arrayAnim_abajo.append(arrayAnimAbajo[i])
			self.arrayAnim_arriba.append(arrayAnimArriba[i])
			self.arrayAnim_derecha.append(arrayAnimDerecha[i])
			self.arrayAnim_izquierda.append(pygame.transform.flip(arrayAnimDerecha[i],True,False))


		self.anim= 0

		self.actualizado = pygame.time.get_ticks()
		self.image = self.arrayAnim_abajo[self.anim]
		self.rect = self.image.get_rect()
		self.rect.center = coordenadas


	def update(self, nuevas_coordenadas,direccion,movimiento):
		self.rect.center = nuevas_coordenadas
		if self.actualizado + 100 < pygame.time.get_ticks() and movimiento:
			self.anim= self.anim + 1
			if self.anim > 5:
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

		self.x = coordenadas[0]
		self.y = coordenadas[1]
		self.mismadirec = 0
		self.incrementoX = 0
		self.incrementoY = 0

		self.arrayAnim = []
		imagen = pygame.image.load("slime.png")
		
		self.arrayAnim.append(imagen.subsurface((0,32,32,32)))
		self.arrayAnim.append(imagen.subsurface((32,32,32,32)))
		
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



main()