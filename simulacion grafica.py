import pygame
import math

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
width, height = 1000, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulación PRO - Robot Diferencial 🚗")

# Colores
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Robot
robot_pos = [width // 2, height // 2]
robot_angle = 0  # grados
robot_length = 40
robot_width = 20
speed = 2
rotation_speed = 3  # grados/frame

# Rastro
trail = []

# Fuente
font = pygame.font.SysFont('Arial', 18)

# Control
automatic_mode = False
target_pos = None

# Reloj
clock = pygame.time.Clock()

# Función para dibujar el robot como un carrito
def draw_robot(x, y, angle):
    rect = pygame.Rect(0, 0, robot_length, robot_width)
    rect.center = (x, y)
    rotated_rect = pygame.transform.rotate(pygame.Surface((robot_length, robot_width)), -angle)
    rotated_rect.fill(BLUE)
    rotated_center = rotated_rect.get_rect(center=(x, y))
    screen.blit(rotated_rect, rotated_center)

    # Dirección (flecha roja)
    arrow_length = 30
    end_x = x + arrow_length * math.cos(math.radians(angle))
    end_y = y - arrow_length * math.sin(math.radians(angle))
    pygame.draw.line(screen, RED, (x, y), (end_x, end_y), 3)

# Función para mover hacia el objetivo
def move_to_target():
    global robot_pos, robot_angle

    dx = target_pos[0] - robot_pos[0]
    dy = target_pos[1] - robot_pos[1]
    distance = math.hypot(dx, dy)

    if distance > 5:
        target_angle = math.degrees(math.atan2(-dy, dx))
        angle_diff = (target_angle - robot_angle + 360) % 360
        if angle_diff > 180:
            angle_diff -= 360

        # Rotar hacia el objetivo
        if abs(angle_diff) > 5:
            if angle_diff > 0:
                robot_angle += rotation_speed
            else:
                robot_angle -= rotation_speed
        else:
            # Avanzar si ya está orientado
            robot_pos[0] += speed * math.cos(math.radians(robot_angle))
            robot_pos[1] -= speed * math.sin(math.radians(robot_angle))
    else:
        return True  # Llegó al objetivo
    return False

# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Clic para seleccionar objetivo
        if event.type == pygame.MOUSEBUTTONDOWN:
            target_pos = pygame.mouse.get_pos()
            automatic_mode = True

    keys = pygame.key.get_pressed()

    # Modo manual
    if not automatic_mode:
        if keys[pygame.K_UP]:
            robot_pos[0] += speed * math.cos(math.radians(robot_angle))
            robot_pos[1] -= speed * math.sin(math.radians(robot_angle))
        if keys[pygame.K_LEFT]:
            robot_angle += rotation_speed
        if keys[pygame.K_RIGHT]:
            robot_angle -= rotation_speed

    # Modo automático
    if automatic_mode and target_pos:
        arrived = move_to_target()
        if arrived:
            automatic_mode = False
            target_pos = None

    # Guardar rastro
    trail.append((int(robot_pos[0]), int(robot_pos[1])))

    # Dibujar rastro
    for point in trail:
        pygame.draw.circle(screen, GRAY, point, 2)

    # Dibujar robot
    draw_robot(robot_pos[0], robot_pos[1], robot_angle)

    # Dibujar objetivo
    if target_pos:
        pygame.draw.circle(screen, GREEN, target_pos, 8)

    # Mostrar información
    info_text = f"Pos: ({int(robot_pos[0])}, {int(robot_pos[1])}) | Ángulo: {int(robot_angle)%360}° | Modo: {'AUTO' if automatic_mode else 'MANUAL'}"
    text_surface = font.render(info_text, True, BLACK)
    screen.blit(text_surface, (20, 20))

    # Actualizar
    pygame.display.flip()
    clock.tick(60)

# Salir
pygame.quit()
