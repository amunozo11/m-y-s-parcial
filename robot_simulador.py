import pygame
import sys
import math
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
from tkinter import simpledialog

# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRID_SIZE = 20
GRID_SPACING = 1.0

# Colores
WHITE = (1.0, 1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0, 1.0)
GREEN = (0.0, 1.0, 0.0, 1.0)
BLUE = (0.0, 0.0, 1.0, 1.0)
YELLOW = (1.0, 1.0, 0.0, 1.0)
GRAY = (0.5, 0.5, 0.5, 1.0)
BLACK = (0.0, 0.0, 0.0, 1.0)

class DifferentialRobot:
    def __init__(self):
        # Parámetros físicos del robot
        self.wheel_radius = 0.1  # metros
        self.wheel_distance = 0.4  # metros
        self.max_wheel_velocity = 6.0  # rad/s
        
        # Estado del robot
        self.x = 0.0  # posición x
        self.y = 0.0  # posición y
        self.theta = 0.0  # orientación en radianes
        
        # Velocidades
        self.v_left = 0.0  # velocidad rueda izquierda (rad/s)
        self.v_right = 0.0  # velocidad rueda derecha (rad/s)
        self.linear_velocity = 0.0  # velocidad lineal (m/s)
        self.angular_velocity = 0.0  # velocidad angular (rad/s)
        
        # Trayectoria
        self.trail = []
        self.max_trail_length = 1000
        
        # Modo de control
        self.control_mode = "MANUAL"  # "MANUAL", "AUTO_POSITION", "AUTO_PATH"
        
        # Objetivos
        self.target_position = None  # (x, y, theta)
        self.path = []  # lista de posiciones (x, y, theta)
        self.current_path_index = 0
        
        # Parámetros de control
        self.position_tolerance = 0.1  # metros
        self.angle_tolerance = 0.05  # radianes
        
        # Voltajes (simulación)
        self.left_voltage = 0.0  # voltios
        self.right_voltage = 0.0  # voltios
        self.max_voltage = 12.0  # voltios
        
        # Constantes del motor (simuladas)
        self.motor_constant = 0.6  # rad/s por voltio
        
        # Tiempo
        self.last_update_time = pygame.time.get_ticks() / 1000.0
    
    def update(self, dt):
        # Actualizar velocidades de las ruedas basadas en voltajes
        self.v_left = self.motor_constant * self.left_voltage
        self.v_right = self.motor_constant * self.right_voltage
        
        # Limitar velocidades
        self.v_left = max(min(self.v_left, self.max_wheel_velocity), -self.max_wheel_velocity)
        self.v_right = max(min(self.v_right, self.max_wheel_velocity), -self.max_wheel_velocity)
        
        # Calcular velocidades del robot
        self.linear_velocity = (self.v_right + self.v_left) * self.wheel_radius / 2
        self.angular_velocity = (self.v_right - self.v_left) * self.wheel_radius / self.wheel_distance
        
        # Actualizar posición y orientación
        self.x += self.linear_velocity * math.cos(self.theta) * dt
        self.y += self.linear_velocity * math.sin(self.theta) * dt
        self.theta += self.angular_velocity * dt
        
        # Normalizar ángulo
        self.theta = self.theta % (2 * math.pi)
        
        # Guardar posición en la trayectoria
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Actualizar control automático
        if self.control_mode == "AUTO_POSITION" and self.target_position:
            self.move_to_target()
        elif self.control_mode == "AUTO_PATH" and self.path:
            if self.current_path_index < len(self.path):
                self.target_position = self.path[self.current_path_index]
                reached = self.move_to_target()
                if reached:
                    self.current_path_index += 1
                    if self.current_path_index >= len(self.path):
                        self.control_mode = "MANUAL"
                        self.left_voltage = 0.0
                        self.right_voltage = 0.0
            else:
                self.control_mode = "MANUAL"
                self.left_voltage = 0.0
                self.right_voltage = 0.0
    
    def move_to_target(self):
        """Control para mover el robot a una posición objetivo (x, y, theta)"""
        target_x, target_y, target_theta = self.target_position
        
        # Calcular distancia y ángulo al objetivo
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Si estamos cerca de la posición objetivo, ajustar la orientación
        if distance < self.position_tolerance:
            # Calcular diferencia de ángulo
            angle_diff = (target_theta - self.theta) % (2 * math.pi)
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
                
            # Si el ángulo es correcto, hemos llegado
            if abs(angle_diff) < self.angle_tolerance:
                self.left_voltage = 0.0
                self.right_voltage = 0.0
                return True
            
            # Ajustar orientación
            if angle_diff > 0:
                self.left_voltage = -2.0
                self.right_voltage = 2.0
            else:
                self.left_voltage = 2.0
                self.right_voltage = -2.0
                
            # Reducir voltaje para movimientos pequeños
            factor = min(1.0, abs(angle_diff) / 0.5)
            self.left_voltage *= factor
            self.right_voltage *= factor
            
            return False
        
        # Calcular ángulo hacia el objetivo
        target_angle = math.atan2(dy, dx)
        angle_diff = (target_angle - self.theta) % (2 * math.pi)
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        
        # Ajustar orientación primero
        if abs(angle_diff) > 0.1:
            if angle_diff > 0:
                self.left_voltage = -3.0
                self.right_voltage = 3.0
            else:
                self.left_voltage = 3.0
                self.right_voltage = -3.0
                
            # Reducir voltaje para movimientos pequeños
            factor = min(1.0, abs(angle_diff) / 0.5)
            self.left_voltage *= factor
            self.right_voltage *= factor
        else:
            # Moverse hacia adelante
            base_voltage = 10.0
            self.left_voltage = base_voltage
            self.right_voltage = base_voltage
            
            # Ajuste proporcional para mantener la dirección
            steering = angle_diff * 2.0
            self.left_voltage -= steering
            self.right_voltage += steering
            
            # Reducir velocidad al acercarse al objetivo
            if distance < 1.0:
                factor = max(0.3, distance)
                self.left_voltage *= factor
                self.right_voltage *= factor
        
        return False
    
    def set_target_position(self, x, y, theta=None):
        """Establece una posición objetivo y activa el modo automático"""
        if theta is None:
            # Si no se especifica theta, calcular ángulo hacia el objetivo
            dx = x - self.x
            dy = y - self.y
            theta = math.atan2(dy, dx)
        
        self.target_position = (x, y, theta)
        self.control_mode = "AUTO_POSITION"
    
    def set_path(self, path):
        """Establece una ruta a seguir"""
        self.path = path
        self.current_path_index = 0
        self.control_mode = "AUTO_PATH"
    
    def draw(self):
        """Dibuja el robot en OpenGL"""
        # Dibujar trayectoria
        glBegin(GL_LINE_STRIP)
        glColor4f(*GRAY)
        for x, y in self.trail:
            glVertex3f(x, y, 0.01)
        glEnd()
        
        # Guardar matriz actual
        glPushMatrix()
        
        # Trasladar y rotar
        glTranslatef(self.x, self.y, 0.1)
        glRotatef(self.theta * 180 / math.pi, 0, 0, 1)
        
        # Dibujar cuerpo del robot
        glColor4f(*BLUE)
        self._draw_robot_body()
        
        # Dibujar ruedas
        glColor4f(*BLACK)
        self._draw_wheel(-self.wheel_distance/2, 0)
        self._draw_wheel(self.wheel_distance/2, 0)
        
        # Dibujar flecha de dirección
        glBegin(GL_LINES)
        glColor4f(*RED)
        glVertex3f(0, 0, 0.2)
        glVertex3f(0.3, 0, 0.2)
        glEnd()
        
        # Dibujar punta de flecha
        glBegin(GL_TRIANGLES)
        glVertex3f(0.3, 0, 0.2)
        glVertex3f(0.25, 0.05, 0.2)
        glVertex3f(0.25, -0.05, 0.2)
        glEnd()
        
        # Restaurar matriz
        glPopMatrix()
        
        # Dibujar objetivo si existe
        if self.target_position:
            tx, ty, ttheta = self.target_position
            glPushMatrix()
            glTranslatef(tx, ty, 0.05)
            
            # Círculo objetivo
            glColor4f(*GREEN)
            self._draw_circle(0.2)
            
            # Línea de orientación objetivo
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0.05)
            glVertex3f(0.3 * math.cos(ttheta), 0.3 * math.sin(ttheta), 0.05)
            glEnd()
            
            glPopMatrix()
        
        # Dibujar ruta si existe
        if self.path and len(self.path) > 0:
            glBegin(GL_LINE_STRIP)
            glColor4f(*YELLOW)
            for x, y, _ in self.path:
                glVertex3f(x, y, 0.02)
            glEnd()
            
            # Dibujar puntos de la ruta
            glPointSize(5.0)
            glBegin(GL_POINTS)
            for i, (x, y, _) in enumerate(self.path):
                if i == self.current_path_index:
                    glColor4f(*GREEN)
                else:
                    glColor4f(*YELLOW)
                glVertex3f(x, y, 0.02)
            glEnd()
    
    def _draw_robot_body(self):
        """Dibuja el cuerpo del robot"""
        # Base del robot
        glBegin(GL_QUADS)
        w, l = self.wheel_distance * 0.8, self.wheel_distance * 1.2
        glVertex3f(-l/2, -w/2, 0)
        glVertex3f(l/2, -w/2, 0)
        glVertex3f(l/2, w/2, 0)
        glVertex3f(-l/2, w/2, 0)
        glEnd()
        
        # Círculo central
        glPushMatrix()
        glTranslatef(0, 0, 0.05)
        glColor4f(*WHITE)
        self._draw_circle(self.wheel_distance * 0.3)
        glPopMatrix()
    
    def _draw_wheel(self, x, y):
        """Dibuja una rueda en la posición relativa (x,y)"""
        glPushMatrix()
        glTranslatef(x, y, 0)
        
        # Rueda (cilindro)
        radius = self.wheel_radius
        width = 0.05
        
        # Lado 1
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)
        for i in range(21):
            angle = i * 2 * math.pi / 20
            glVertex3f(radius * math.cos(angle), radius * math.sin(angle), 0)
        glEnd()
        
        # Lado 2
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, width)
        for i in range(21):
            angle = i * 2 * math.pi / 20
            glVertex3f(radius * math.cos(angle), radius * math.sin(angle), width)
        glEnd()
        
        # Superficie lateral
        glBegin(GL_QUAD_STRIP)
        for i in range(21):
            angle = i * 2 * math.pi / 20
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, 0)
            glVertex3f(x, y, width)
        glEnd()
        
        glPopMatrix()
    
    def _draw_circle(self, radius, segments=20):
        """Dibuja un círculo en el plano XY"""
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)
        for i in range(segments + 1):
            angle = i * 2 * math.pi / segments
            glVertex3f(radius * math.cos(angle), radius * math.sin(angle), 0)
        glEnd()

class Simulator:
    def __init__(self):
        # Inicializar pygame y OpenGL
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Simulador 3D de Robot Diferencial")
        
        # Configurar OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Configurar vista
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 50.0)
        
        # Inicializar robot
        self.robot = DifferentialRobot()
        
        # Configurar cámara
        self.camera_distance = 10.0
        self.camera_height = 8.0
        self.camera_angle = 0.0
        self.camera_mode = "FIXED"  # "FIXED", "FOLLOW"
        
        # Reloj para control de tiempo
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks() / 1000.0
        
        # Fuente para texto
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 18)
        
        # Interfaz
        self.show_help = False
        self.show_info = True
        
        # Inicializar Tkinter para diálogos
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana principal
    
    def update_camera(self):
        """Actualiza la posición y orientación de la cámara"""
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        if self.camera_mode == "FOLLOW":
            # Cámara sigue al robot
            eye_x = self.robot.x - self.camera_distance * math.cos(self.robot.theta)
            eye_y = self.robot.y - self.camera_distance * math.sin(self.robot.theta)
            eye_z = self.camera_height
            
            target_x = self.robot.x
            target_y = self.robot.y
            target_z = 0
            
            up_x, up_y, up_z = 0, 0, 1
            
            gluLookAt(eye_x, eye_y, eye_z, target_x, target_y, target_z, up_x, up_y, up_z)
        else:
            # Cámara fija con rotación
            eye_x = self.camera_distance * math.cos(self.camera_angle)
            eye_y = self.camera_distance * math.sin(self.camera_angle)
            eye_z = self.camera_height
            
            target_x = 0
            target_y = 0
            target_z = 0
            
            up_x, up_y, up_z = 0, 0, 1
            
            gluLookAt(eye_x, eye_y, eye_z, target_x, target_y, target_z, up_x, up_y, up_z)
    
    def draw_grid(self):
        """Dibuja una cuadrícula en el plano XY"""
        glBegin(GL_LINES)
        glColor4f(0.5, 0.5, 0.5, 0.5)
        
        # Líneas horizontales
        for i in range(-GRID_SIZE, GRID_SIZE + 1):
            glVertex3f(-GRID_SIZE * GRID_SPACING, i * GRID_SPACING, 0)
            glVertex3f(GRID_SIZE * GRID_SPACING, i * GRID_SPACING, 0)
        
        # Líneas verticales
        for i in range(-GRID_SIZE, GRID_SIZE + 1):
            glVertex3f(i * GRID_SPACING, -GRID_SIZE * GRID_SPACING, 0)
            glVertex3f(i * GRID_SPACING, GRID_SIZE * GRID_SPACING, 0)
        
        glEnd()
        
        # Ejes principales
        glBegin(GL_LINES)
        # Eje X (rojo)
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glVertex3f(0, 0, 0.01)
        glVertex3f(GRID_SIZE * GRID_SPACING, 0, 0.01)
        
        # Eje Y (verde)
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glVertex3f(0, 0, 0.01)
        glVertex3f(0, GRID_SIZE * GRID_SPACING, 0.01)
        
        # Eje Z (azul)
        glColor4f(0.0, 0.0, 1.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()
    
    def render_text(self, text, position, color=(255, 255, 255)):
        """Renderiza texto en la pantalla"""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)
    
    def draw_info(self):
        """Dibuja información del robot y controles en la pantalla"""
        if not self.show_info:
            return
            
        # Guardar estado OpenGL
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        
        # Dibujar fondo semitransparente para el panel de información
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.7)
        
        glBegin(GL_QUADS)
        glVertex2f(10, 10)
        glVertex2f(350, 10)
        glVertex2f(350, 180)
        glVertex2f(10, 180)
        glEnd()
        
        # Restaurar estado OpenGL para renderizar texto
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
        glEnable(GL_DEPTH_TEST)
        
        # Renderizar información del robot
        info_lines = [
            f"Posición: ({self.robot.x:.2f}, {self.robot.y:.2f})",
            f"Orientación: {math.degrees(self.robot.theta):.1f}°",
            f"Velocidad lineal: {self.robot.linear_velocity:.2f} m/s",
            f"Velocidad angular: {math.degrees(self.robot.angular_velocity):.2f} °/s",
            f"Voltaje izquierdo: {self.robot.left_voltage:.2f} V",
            f"Voltaje derecho: {self.robot.right_voltage:.2f} V",
            f"Modo de control: {self.robot.control_mode}",
            f"Cámara: {self.camera_mode}"
        ]
        
        for i, line in enumerate(info_lines):
            self.render_text(line, (20, 20 + i * 20))
        
        # Mostrar ayuda
        if self.show_help:
            help_lines = [
                "Controles:",
                "W/S: Aumentar/disminuir voltaje de ambos motores",
                "A/D: Girar izquierda/derecha",
                "Q/E: Rotar cámara",
                "R: Reiniciar posición del robot",
                "C: Cambiar modo de cámara",
                "P: Establecer posición objetivo (X,Y,Theta)",
                "L: Programar ruta",
                "H: Mostrar/ocultar ayuda",
                "I: Mostrar/ocultar información",
                "ESC: Salir"
            ]
            
            # Dibujar fondo para ayuda
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
            
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            
            glDisable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            
            glColor4f(0.0, 0.0, 0.0, 0.7)
            glBegin(GL_QUADS)
            glVertex2f(SCREEN_WIDTH - 360, 10)
            glVertex2f(SCREEN_WIDTH - 10, 10)
            glVertex2f(SCREEN_WIDTH - 10, 10 + len(help_lines) * 20 + 10)
            glVertex2f(SCREEN_WIDTH - 360, 10 + len(help_lines) * 20 + 10)
            glEnd()
            
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
            
            glEnable(GL_DEPTH_TEST)
            
            for i, line in enumerate(help_lines):
                self.render_text(line, (SCREEN_WIDTH - 350, 20 + i * 20))
    
    def handle_input(self):
        """Maneja la entrada del usuario"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_h:
                    self.show_help = not self.show_help
                
                if event.key == pygame.K_i:
                    self.show_info = not self.show_info
                
                if event.key == pygame.K_r:
                    # Reiniciar posición del robot
                    self.robot.x = 0.0
                    self.robot.y = 0.0
                    self.robot.theta = 0.0
                    self.robot.trail = []
                
                if event.key == pygame.K_c:
                    # Cambiar modo de cámara
                    if self.camera_mode == "FIXED":
                        self.camera_mode = "FOLLOW"
                    else:
                        self.camera_mode = "FIXED"
                
                if event.key == pygame.K_p:
                    # Establecer posición objetivo
                    self.set_target_position()
                
                if event.key == pygame.K_l:
                    # Programar ruta
                    self.program_path()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo
                    # Convertir coordenadas de pantalla a coordenadas del mundo
                    world_pos = self.screen_to_world(event.pos)
                    if world_pos:
                        self.robot.set_target_position(world_pos[0], world_pos[1])
        
        # Controles continuos
        keys = pygame.key.get_pressed()
        
        # Solo procesar controles manuales si no estamos en modo automático
        if self.robot.control_mode == "MANUAL":
            # Control de motores
            if keys[pygame.K_w]:
                self.robot.left_voltage += 0.1
                self.robot.right_voltage += 0.1
            if keys[pygame.K_s]:
                self.robot.left_voltage -= 0.1
                self.robot.right_voltage -= 0.1
            if keys[pygame.K_a]:
                self.robot.left_voltage -= 0.1
                self.robot.right_voltage += 0.1
            if keys[pygame.K_d]:
                self.robot.left_voltage += 0.1
                self.robot.right_voltage -= 0.1
            
            # Limitar voltajes
            self.robot.left_voltage = max(min(self.robot.left_voltage, self.robot.max_voltage), -self.robot.max_voltage)
            self.robot.right_voltage = max(min(self.robot.right_voltage, self.robot.max_voltage), -self.robot.max_voltage)
            
            # Reducir voltajes gradualmente si no se presionan teclas
            if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
                self.robot.left_voltage *= 0.95
                self.robot.right_voltage *= 0.95
                
                # Si los voltajes son muy pequeños, establecerlos a cero
                if abs(self.robot.left_voltage) < 0.1:
                    self.robot.left_voltage = 0.0
                if abs(self.robot.right_voltage) < 0.1:
                    self.robot.right_voltage = 0.0
        
        # Control de cámara
        if keys[pygame.K_q]:
            self.camera_angle += 0.02
        if keys[pygame.K_e]:
            self.camera_angle -= 0.02
        
        return True
    
    def screen_to_world(self, screen_pos):
        """Convierte coordenadas de pantalla a coordenadas del mundo"""
        x, y = screen_pos
        
        # Obtener matrices de proyección y modelview
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        # Obtener profundidad en el punto
        winZ = glReadPixels(x, viewport[3] - y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        
        # Si el punto está demasiado lejos, no es válido
        if winZ[0][0] >= 1.0:
            return None
        
        # Desproyectar para obtener coordenadas del mundo
        world_pos = gluUnProject(x, viewport[3] - y, winZ[0][0], modelview, projection, viewport)
        
        return world_pos
    
    def set_target_position(self):
        """Abre un diálogo para establecer una posición objetivo"""
        try:
            x = simpledialog.askfloat("Posición X", "Ingrese la coordenada X:", parent=self.root)
            if x is None:
                return
                
            y = simpledialog.askfloat("Posición Y", "Ingrese la coordenada Y:", parent=self.root)
            if y is None:
                return
                
            theta = simpledialog.askfloat("Orientación", "Ingrese la orientación (grados):", parent=self.root)
            if theta is None:
                return
                
            # Convertir grados a radianes
            theta_rad = math.radians(theta)
            
            # Establecer posición objetivo
            self.robot.set_target_position(x, y, theta_rad)
            
        except Exception as e:
            print(f"Error al establecer posición: {e}")
    
    def program_path(self):
        """Abre un diálogo para programar una ruta"""
        try:
            # Preguntar cuántos puntos tendrá la ruta
            num_points = simpledialog.askinteger("Puntos de ruta", "¿Cuántos puntos tendrá la ruta?", parent=self.root, minvalue=1, maxvalue=10)
            if num_points is None:
                return
            
            path = []
            
            # Solicitar cada punto
            for i in range(num_points):
                x = simpledialog.askfloat(f"Punto {i+1}", f"Ingrese la coordenada X del punto {i+1}:", parent=self.root)
                if x is None:
                    return
                    
                y = simpledialog.askfloat(f"Punto {i+1}", f"Ingrese la coordenada Y del punto {i+1}:", parent=self.root)
                if y is None:
                    return
                    
                theta = simpledialog.askfloat(f"Punto {i+1}", f"Ingrese la orientación (grados) del punto {i+1}:", parent=self.root)
                if theta is None:
                    return
                
                # Convertir grados a radianes
                theta_rad = math.radians(theta)
                
                path.append((x, y, theta_rad))
            
            # Establecer ruta
            self.robot.set_path(path)
            
        except Exception as e:
            print(f"Error al programar ruta: {e}")
    
    def run(self):
        """Bucle principal del simulador"""
        running = True
        
        while running:
            # Manejar entrada
            running = self.handle_input()
            
            # Calcular delta de tiempo
            current_time = pygame.time.get_ticks() / 1000.0
            dt = current_time - self.last_time
            self.last_time = current_time
            
            # Actualizar robot
            self.robot.update(dt)
            
            # Limpiar pantalla
            glClearColor(0.9, 0.9, 0.9, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Actualizar cámara
            self.update_camera()
            
            # Dibujar escena
            self.draw_grid()
            self.robot.draw()
            
            # Dibujar información
            self.draw_info()
            
            # Actualizar pantalla
            pygame.display.flip()
            
            # Controlar FPS
            self.clock.tick(60)
        
        # Limpiar
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()
