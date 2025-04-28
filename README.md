
🐍 Proyecto de Simulación de Robot Diferencial
Simulación gráfica en 2D/3D de un robot diferencial con visualización de datos y control dinámico.

📦 Requisitos Generales
Python: 3.11.6

Entorno virtual recomendado: .venv

bash
Copiar
Editar
python -m venv .venv
.venv\Scripts\activate
pip install matplotlib pygame numpy PyOpenGL
📁 Archivos Principales
1. simulacion voltaje.py
🔵 Objetivo:
Simular y graficar el comportamiento del voltaje de los motores a lo largo del tiempo.

🔵 Importaciones usadas:

python
Copiar
Editar
import matplotlib.pyplot as plt
import time
🔵 Características:

Crea una gráfica dinámica que muestra la evolución de los voltajes.

Permite observar cambios de estado en el robot respecto al tiempo.

Ideal para análisis de señales y comportamiento dinámico.

🔵 Ejecución:

bash
Copiar
Editar
python simulacion voltaje.py
2. robot_simulador.py
🚗 Objetivo:
Simulación 3D interactiva de un robot diferencial usando Pygame y OpenGL.

🚗 Importaciones usadas:

python
Copiar
Editar
import pygame
import sys
import math
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
from tkinter import simpledialog
🚗 Características principales:

Entorno 3D interactivo con cuadrícula pulsante.

Seguimiento de trayectoria del robot.

HUD informativo en pantalla (posición, velocidad, voltajes, modo de control).

Sistema de mensajes de estado y ayudas visuales.

Control manual y automático (posiciones y rutas programadas).

Cámara con modos dinámicos: fija, seguimiento o vista superior.

🚗 Ejecución:

bash
Copiar
Editar
python robot_simulador.py
🎮 Controles

Tecla	Acción
W / S	Aumentar / Disminuir voltaje de ambos motores
A / D	Girar izquierda / derecha
Q / E	Rotar la cámara
R	Reiniciar la posición del robot
C	Cambiar modo de cámara (FIXED / FOLLOW / TOP)
P	Establecer posición objetivo (X, Y, Theta)
L	Programar una ruta con múltiples puntos
G	Mostrar / ocultar coordenadas de la cuadrícula
T	Mostrar / ocultar el panel de posición
H	Mostrar / ocultar ayuda en pantalla
I	Mostrar / ocultar información del robot
Clic izquierdo	Seleccionar un punto como objetivo
ESC	Salir de la simulación
✨ Visuales y mejoras
Cuadrícula pulsante en 3D.

Flecha indicadora de orientación del robot.

Renderizado correcto de textos en HUD (sin problemas de OpenGL).

Multiplicador de velocidad general para ajustar la dinámica del robot.

Mensajes de estado flotantes con transparencia.

Modo automático para seguir posiciones y rutas.

🛠 Librerías necesarias
matplotlib

pygame

numpy

PyOpenGL

(tkinter viene incluido con Python oficial en Windows.)

Instalarlas todas en tu entorno virtual con:

bash
Copiar
Editar
pip install matplotlib pygame numpy PyOpenGL
📷 Previsualización (visual esperada)
✅ Cuadrícula dinámica
✅ Robot diferencial animado
✅ Traza histórica de posiciones
✅ Panel HUD informativo
✅ Mensajes flotantes
✅ Gráficas de voltaje dinámico

🚀 Cómo comenzar
bash
Copiar
Editar
# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install matplotlib pygame numpy PyOpenGL

# Ejecutar simulador 3D
python robot_simulador.py

# O ejecutar la simulación de voltaje
python simulacion voltaje.py
🤝 Autores
Proyecto desarrollado para prácticas de Modelado y Simulación.