import matplotlib.pyplot as plt
import time

# Configurar estilo gráfico
plt.style.use('seaborn-v0_8-dark-palette')

# Parámetros del motor
kv = 100  # Constante de motor (rpm/V)

# Listas para guardar los datos
voltajes = []
velocidades = []

# Mensaje de bienvenida
print("\n🚗 Simulación de Motor Eléctrico - Voltaje a Velocidad (rpm)")
print("-------------------------------------------------------------")

# Crear la figura
plt.ion()  # Activar modo interactivo
fig, ax = plt.subplots(figsize=(8,5))

# Bucle principal
while True:
    try:
        # Input de voltaje
        voltaje = float(input("🔌 Ingrese el voltaje aplicado al motor (V) (o -1 para salir): "))

        # Salir
        if voltaje == -1:
            print("\n🛑 Simulación terminada. ¡Hasta luego!")
            break

        # Calcular velocidad
        velocidad = kv * voltaje

        # Guardar valores
        voltajes.append(voltaje)
        velocidades.append(velocidad)

        # Mostrar resultado
        print(f"⚡ Para {voltaje:.2f} V => Velocidad = {velocidad:.2f} rpm.\n")

        # Limpiar y actualizar gráfica
        ax.clear()
        ax.plot(voltajes, velocidades, marker='o', linestyle='-', color='cyan')
        ax.set_title('Relación Voltaje vs Velocidad del Motor', fontsize=16)
        ax.set_xlabel('Voltaje (V)', fontsize=12)
        ax.set_ylabel('Velocidad (rpm)', fontsize=12)
        ax.grid(True)
        ax.set_xlim(left=0)  # No permitir valores negativos
        ax.set_ylim(bottom=0)
        for i in range(len(voltajes)):
            ax.text(voltajes[i], velocidades[i]+20, f"{velocidades[i]:.0f} rpm", ha='center', fontsize=8, color='black')
        plt.draw()
        plt.pause(0.5)  # Pequeña pausa para animar

    except ValueError:
        print("⚠️ Error: Ingresa un número válido.\n")

# Dejar la última gráfica fija
plt.ioff()
plt.show()
