#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pygame.transform
import sys
import random
import math

from pygame.locals import *


class target_atack (pygame.sprite.Sprite):
	
	def __init__(self, coordenadas,target):
		pygame.sprite.Sprite.__init__(self)

		self.x = coordenadas[0]
		self.y = coordenadas[1]
		self.target_x = target[0]
		self.target_y = target[1]
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
	
					self.x += self.target_x
					self.y += self.target_y



def boss_attack_1(coordenadas,target):

	Attacks = []

	## Calculamos el movimiento de cada ataque. Primero el ataque central
	modulo = dist(coordenadas,target)
	central = (((coordenadas[0] - target[0])/modulo),((coordenadas[1] - target[1])/modulo))
	Attacks.append(target_atack(coordenadas,central))


	for i in [-3,-2,-1,1,2,3]:
		Attacks.append(target_atack(coordenadas,(central[0]+i,central[0]-i)))
		
	return Attacks


def dist (a,b):

	suma = (a[0]-b[0])*(a[0]-b[0])
	suma += (a[1]-b[1])*(a[1]-b[1])
	return math.sqrt(float(suma))


Attacks = boss_attack_1((0,0),(1,1))
for attac in Attacks:
	print attac.target_x
	