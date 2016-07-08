# python-game
Simple game to test pygame library

Este es un pequeño juego para experimentar con la libreria pygame e integrarlo con otros sistemas como bases de datos y interfaces graficas.

El juego consiste en derrotar a los enemigos atacando con la barra espaciadora, tiene la peculiaridad de que cuando el 
personaje no se mueve, se para el tiempo del juego aunque el cronometro sigue corriendo, la puntuacion depende del tiempo
en pasar el juego.

El juego consta de dos niveles.

Para lanzar el juego, primero hay que crear una base de datos de MySQL con las instrucciones del archivo createDatabase.
A continuacion hay que ejecutar el programa Interfaz.py que implementa las funciones definidas en juego.py con 
una interfaz grafica donde se explica un poco el juego.

