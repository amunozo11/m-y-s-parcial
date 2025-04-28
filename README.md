# 🤖 Simulador de Robot Diferencial

<div align="center">

![Robot Simulation](https://img.shields.io/badge/Simulation-Robot-blue)
![Python](https://img.shields.io/badge/Python-3.11.6-yellow)
![OpenGL](https://img.shields.io/badge/OpenGL-3D-green)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

<p align="center">
Simulación gráfica interactiva en 3D de un robot diferencial con control manual y automático, visualización de datos, trayectoria e interacción en tiempo real.
</p>

<div align="center">

[📋 Requisitos](#-requisitos) • 
[⚙️ Instalación](#️-instalación) • 
[📁 Archivos](#-archivos-principales) • 
[🎮 Controles](#-controles-de-simulación) • 
[✨ Características](#-características-principales) • 
[🚀 Inicio Rápido](#-inicio-rápido)

</div>

---

## 📋 Requisitos

- **Python:** 3.11.6 o superior
- **Sistema Operativo:** Windows, Linux, macOS
- **Entorno virtual recomendado:** `.venv`
- **Librerías:**
  - matplotlib
  - pygame
  - numpy
  - PyOpenGL
  - tkinter (incluido en Python oficial para Windows)

## ⚙️ Instalación

\`\`\`bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual (Windows)
.venv\Scripts\activate

# Activar entorno virtual (Linux/macOS)
source .venv/bin/activate

# Instalar dependencias
pip install matplotlib pygame numpy PyOpenGL
\`\`\`

## 📁 Archivos Principales

### 1. `robot_simulador.py`

<div align="center">
<img src="https://img.shields.io/badge/3D-Simulation-blue" alt="3D Simulation">
</div>

**Objetivo:** Simulación 3D interactiva de un robot diferencial usando Pygame y OpenGL.

**Características:**
- Entorno 3D interactivo con cuadrícula pulsante
- Seguimiento de trayectoria y orientación del robot
- Panel HUD con información de estado en pantalla
- Control manual mediante teclado y control automático hacia objetivos o rutas
- Modos de cámara: Fija, Seguimiento, Vista Superior

**Ejecución:**
\`\`\`bash
python robot_simulador.py
\`\`\`

### 2. `simulacion_voltaje.py`

<div align="center">
<img src="https://img.shields.io/badge/Data-Visualization-orange" alt="Data Visualization">
</div>

**Objetivo:** Simular y graficar el comportamiento del voltaje de los motores a lo largo del tiempo.

**Características:**
- Generación dinámica de gráficos de voltaje
- Observación de cambios de estado en tiempo real
- Análisis de señales de comportamiento dinámico

**Ejecución:**
\`\`\`bash
python simulacion_voltaje.py
\`\`\`

## 🎮 Controles de Simulación

| Tecla | Acción |
|-------|--------|
| **W / S** | Aumentar / Disminuir voltaje de ambos motores |
| **A / D** | Girar izquierda / derecha |
| **Q / E** | Rotar la cámara |
| **R** | Reiniciar la posición del robot |
| **C** | Cambiar modo de cámara (FIXED / FOLLOW / TOP) |
| **P** | Establecer posición objetivo (X, Y, Theta) |
| **L** | Programar ruta de múltiples puntos |
| **G** | Mostrar / Ocultar coordenadas de la cuadrícula |
| **T** | Mostrar / Ocultar el panel de posición |
| **H** | Mostrar / Ocultar ayuda |
| **I** | Mostrar / Ocultar información del robot |
| **Clic izquierdo** | Establecer un objetivo en la posición seleccionada |
| **ESC** | Salir de la simulación |

## ✨ Características Principales

### Visualización y Simulación
- ✅ Entorno 3D interactivo con cuadrícula pulsante animada
- ✅ Robot diferencial con orientación y traza de movimiento
- ✅ Panel HUD de información dinámico
- ✅ Mensajes de estado flotantes (con efecto fade out)
- ✅ Múltiples modos de cámara interactivos

### Control y Navegación
- ✅ Control manual mediante teclado (W, A, S, D)
- ✅ Control automático hacia posiciones objetivo
- ✅ Programación de rutas con múltiples puntos
- ✅ Navegación por clic en el entorno 3D

### Análisis de Datos
- ✅ Simulación de voltaje dinámica y gráfica
- ✅ Visualización de trayectoria con colores dinámicos
- ✅ Información en tiempo real de posición, orientación y velocidades

## 📊 Previsualización Esperada

- Simulación visual 3D con cuadrícula animada y ejes resaltados
- Robot diferencial animado, rotando y moviéndose de forma realista
- Panel de datos dinámico informativo (HUD)
- Mensajes flotantes de eventos
- Gráfica de voltaje dinámico y evolución temporal

## 🚀 Inicio Rápido

\`\`\`bash
# Clonar el repositorio (si aplica)
git clone https://github.com/tu-usuario/robot-diferencial-sim.git
cd robot-diferencial-sim

# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Instalar dependencias
pip install matplotlib pygame numpy PyOpenGL

# Ejecutar el simulador
python robot_simulador.py

# O ejecutar la simulación de voltaje
python simulacion_voltaje.py
\`\`\`
