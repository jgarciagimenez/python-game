#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pygame.transform
import sys

from pygame.locals import *

def main():

    pygame.init()

    Reloj= pygame.time.Clock()

    Ventana = pygame.display.set_mode((1400, 720))
    pygame.display.set_caption("Monigotillo animado")

    Fondo = pygame.image.load("fondo.jpg")

    Imagen = pygame.image.load("monigotillo.png")
    transparente = Imagen.get_at((0, 0))
    Imagen.set_colorkey(transparente)

    MiMonigotillo = Monigotillo((300, 200), Imagen)

    coordX = 300
    coordY = 200
    Coordenadas = (coordX, coordY)

    incrementoX = 0
    incrementoY = 0

    movimiento = False
    direccion = 'Abajo'


    while True:

        MiMonigotillo.update(Coordenadas,direccion,movimiento)

        Ventana.blit(Fondo, (0, 0))
        Ventana.blit(MiMonigotillo.image, MiMonigotillo.rect)

        pygame.display.flip()

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


main()