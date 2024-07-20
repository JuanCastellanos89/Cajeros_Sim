import numpy as np
import random
import matplotlib.pyplot as plt

# Definir constantes
NUM_CAJAS = 3
HORAS_OPERACION = 8
MINUTOS_OPERACION = HORAS_OPERACION * 60
DIAS_SIMULACION = 10

# Probabilidades y tiempos
prob_retiro = 0.70
prob_pago = 0.30

# Tipos de usuarios y sus probabilidades
usuarios_retiro = ['rápido', 'normal', 'lento', 'muy lento']
prob_usuarios_retiro = [0.23, 0.40, 0.17, 0.20]
tiempos_servicio_retiro = [1, 2, 3, 4]

usuarios_pago = ['rápido', 'normal', 'lento', 'muy lento']
prob_usuarios_pago = [0.10, 0.20, 0.30, 0.40]
tiempos_servicio_pago = [3, 3, 5, 7]

# Función para generar el próximo evento
def generar_proximo_evento():
    if random.random() < prob_retiro:
        tipo_usuario = np.random.choice(usuarios_retiro, p=prob_usuarios_retiro)
        tiempo_servicio = np.random.exponential(tiempos_servicio_retiro[usuarios_retiro.index(tipo_usuario)])
        return 'retiro', tipo_usuario, tiempo_servicio
    else:
        tipo_usuario = np.random.choice(usuarios_pago, p=prob_usuarios_pago)
        tiempo_servicio = np.random.exponential(tiempos_servicio_pago[usuarios_pago.index(tipo_usuario)])
        return 'pago', tipo_usuario, tiempo_servicio

# Función para simular un día
def simular_dia():
    tiempos_atencion_cajeros = [[] for _ in range(NUM_CAJAS)]
    cantidad_usuarios = {'retiro': {'rápido': 0, 'normal': 0, 'lento': 0, 'muy lento': 0},
                         'pago': {'rápido': 0, 'normal': 0, 'lento': 0, 'muy lento': 0}}
    total_usuarios_cajeros = [{'retiro': 0, 'pago': 0} for _ in range(NUM_CAJAS)]
    
    tiempo_actual = 0

    while tiempo_actual < MINUTOS_OPERACION:
        # Generar el próximo evento (nuevo cliente llegando)
        tipo_accion, tipo_usuario, tiempo_servicio = generar_proximo_evento()
        
        # Encontrar el próximo cajero disponible
        cajero_disponible = np.argmin([sum(cola) for cola in tiempos_atencion_cajeros])
        
        # Asignar el cliente al cajero disponible
        tiempos_atencion_cajeros[cajero_disponible].append(tiempo_servicio)
        cantidad_usuarios[tipo_accion][tipo_usuario] += 1
        total_usuarios_cajeros[cajero_disponible][tipo_accion] += 1
        
        # Avanzar el tiempo
        tiempo_actual += np.random.exponential(1)

    # Calcular tiempo promedio de atención por cajero
    tiempo_promedio_cajeros = [np.mean(tiempos) for tiempos in tiempos_atencion_cajeros]
    
    return tiempos_atencion_cajeros, cantidad_usuarios, tiempo_promedio_cajeros, total_usuarios_cajeros

# Ejecutar múltiples corridas
resultados_por_dia = []
for _ in range(DIAS_SIMULACION):
    resultados_por_dia.append(simular_dia())

# Variables para acumular los totales de usuarios por tipo
total_usuarios = {
    'retiro': {'rápido': 0, 'normal': 0, 'lento': 0, 'muy lento': 0},
    'pago': {'rápido': 0, 'normal': 0, 'lento': 0, 'muy lento': 0}
}

total_usuarios_retiro = 0
total_usuarios_pago = 0

# Analizar los resultados por día
estadisticas_por_dia = []
tiempos_promedio_cajero_menor = []
tiempos_promedio_cajero_mayor = []
total_usuarios_retiro_dias = []
total_usuarios_pago_dias = []

for dia, resultado in enumerate(resultados_por_dia):
    tiempos_atencion_cajeros, cantidad_usuarios, tiempo_promedio_cajeros, total_usuarios_cajeros = resultado
    
    cajero_menor_tiempo = np.argmin(tiempo_promedio_cajeros) + 1  # Ajustar la numeración del cajero
    cajero_mayor_tiempo = np.argmax(tiempo_promedio_cajeros) + 1  # Ajustar la numeración del cajero
    
    # Acumular los totales de usuarios por tipo
    for tipo in usuarios_retiro:
        total_usuarios['retiro'][tipo] += cantidad_usuarios['retiro'][tipo]
    for tipo in usuarios_pago:
        total_usuarios['pago'][tipo] += cantidad_usuarios['pago'][tipo]
    
    total_usuarios_retiro_dia = sum(cantidad_usuarios['retiro'].values())
    total_usuarios_pago_dia = sum(cantidad_usuarios['pago'].values())
    
    total_usuarios_retiro += total_usuarios_retiro_dia
    total_usuarios_pago += total_usuarios_pago_dia
    
    promedio_diario_retiro = total_usuarios_retiro_dia / NUM_CAJAS
    promedio_diario_pago = total_usuarios_pago_dia / NUM_CAJAS
    
    estadisticas_por_dia.append({
        'Día': dia + 1,
        'Tiempo promedio cajero menor': tiempo_promedio_cajeros[cajero_menor_tiempo - 1],
        'Tiempo promedio cajero mayor': tiempo_promedio_cajeros[cajero_mayor_tiempo - 1],
        'Cajero menor tiempo': cajero_menor_tiempo,
        'Cajero mayor tiempo': cajero_mayor_tiempo,
        'Total usuarios retiro': cantidad_usuarios['retiro'],
        'Total usuarios pago': cantidad_usuarios['pago'],
        'Total usuarios día': total_usuarios_retiro_dia + total_usuarios_pago_dia,
        'Promedio diario retiro': promedio_diario_retiro,
        'Promedio diario pago': promedio_diario_pago,
        'Total usuarios cajeros': total_usuarios_cajeros,
        'Total usuarios retiro día': total_usuarios_retiro_dia,
        'Total usuarios pago día': total_usuarios_pago_dia
    })

    tiempos_promedio_cajero_menor.append(tiempo_promedio_cajeros[cajero_menor_tiempo - 1])
    tiempos_promedio_cajero_mayor.append(tiempo_promedio_cajeros[cajero_mayor_tiempo - 1])
    total_usuarios_retiro_dias.append(total_usuarios_retiro_dia)
    total_usuarios_pago_dias.append(total_usuarios_pago_dia)

# Calcular promedios de usuarios por tipo
promedio_usuarios_retiro = {tipo: total / DIAS_SIMULACION for tipo, total in total_usuarios['retiro'].items()}
promedio_usuarios_pago = {tipo: total / DIAS_SIMULACION for tipo, total in total_usuarios['pago'].items()}

# Calcular el promedio total de usuarios de retiro y pago para la totalidad de los días
promedio_total_usuarios_retiro = total_usuarios_retiro / DIAS_SIMULACION
promedio_total_usuarios_pago = total_usuarios_pago / DIAS_SIMULACION

# Mostrar resultados
for estadisticas in estadisticas_por_dia:
    print(f"Día {estadisticas['Día']}:")
    print(f"  Tiempo promedio del cajero con menor tiempo de atención: {estadisticas['Tiempo promedio cajero menor']:.2f} minutos")
    print(f"  Tiempo promedio del cajero con mayor tiempo de atención: {estadisticas['Tiempo promedio cajero mayor']:.2f} minutos")
    print(f"  Cajero con menor tiempo de atención: {estadisticas['Cajero menor tiempo']}")
    print(f"  Cajero con mayor tiempo de atención: {estadisticas['Cajero mayor tiempo']}")
    print(f"  Total de usuarios de retiro en el día: {estadisticas['Total usuarios retiro día']}")
    print(f"  Total de usuarios de pago en el día: {estadisticas['Total usuarios pago día']}")
    print(f"  Promedio diario de usuarios (retiro): {estadisticas['Promedio diario retiro']:.2f}")
    print(f"  Promedio diario de usuarios (pago): {estadisticas['Promedio diario pago']:.2f}")
    print("  Total de usuarios por tipo (retiro):")
    for tipo, cantidad in estadisticas['Total usuarios retiro'].items():
        print(f"    {tipo}: {cantidad}")
    print("  Total de usuarios por tipo (pago):")
    for tipo, cantidad in estadisticas['Total usuarios pago'].items():
        print(f"    {tipo}: {cantidad}")
    print("  Total de usuarios atendidos por cada cajero en el día:")
    for i, total in enumerate(estadisticas['Total usuarios cajeros']):
        print(f"    Cajero {i + 1} - Retiros: {total['retiro']}, Pagos: {total['pago']}")       
    print(f"  Total de usuarios en el día: {estadisticas['Total usuarios día']}")
    print()
    print()
    



# Mostrar el promedio total de usuarios de retiro y pago para la totalidad de los días
print(f"\nPromedio total de usuarios de retiro para la totalidad de los días: {promedio_total_usuarios_retiro:.2f}")
print(f"Promedio total de usuarios de pago para la totalidad de los días: {promedio_total_usuarios_pago:.2f}")

# Crear gráficos de líneas para visualizar los datos

# Gráfico de líneas para tiempos promedio de atención del cajero con menor y mayor tiempo
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(range(1, DIAS_SIMULACION + 1), tiempos_promedio_cajero_menor, marker='o', linestyle='-', color='b')
plt.title('Tiempos promedio del cajero con menor tiempo de atención')
plt.xlabel('Día')
plt.ylabel('Tiempo promedio (minutos)')

plt.subplot(1, 2, 2)
plt.plot(range(1, DIAS_SIMULACION + 1), tiempos_promedio_cajero_mayor, marker='o', linestyle='-', color='r')
plt.title('Tiempos promedio del cajero con mayor tiempo de atención')
plt.xlabel('Día')
plt.ylabel('Tiempo promedio (minutos)')

plt.tight_layout()
plt.show()

# Gráfico de líneas para el promedio de usuarios de cada tipo en la totalidad de cajeros
plt.figure(figsize=(12, 6))

usuarios_tipos = ['rápido', 'normal', 'lento', 'muy lento']
promedio_retiro = [promedio_usuarios_retiro[tipo] for tipo in usuarios_tipos]
promedio_pago = [promedio_usuarios_pago[tipo] for tipo in usuarios_tipos]

x = np.arange(len(usuarios_tipos))

plt.plot(x, promedio_retiro, marker='o', linestyle='-', color='b', label='Retiros')
plt.plot(x, promedio_pago, marker='o', linestyle='-', color='r', label='Pagos')

plt.xticks(x, usuarios_tipos)
plt.ylabel('Promedio de usuarios')
plt.title('Promedio de usuarios de cada tipo en la totalidad de cajeros')
plt.legend()

plt.tight_layout()
plt.show()

# Gráfico de líneas para el total de usuarios de cada tipo en cada una de las réplicas
plt.figure(figsize=(12, 6))

# Totales de usuarios de retiro y pago por día para todas las réplicas
total_usuarios_retiro_todos = [sum(dia['Total usuarios retiro'].values()) for dia in estadisticas_por_dia]
total_usuarios_pago_todos = [sum(dia['Total usuarios pago'].values()) for dia in estadisticas_por_dia]

plt.subplot(1, 2, 1)
plt.plot(range(1, DIAS_SIMULACION + 1), total_usuarios_retiro_todos, marker='o', linestyle='-', color='b')
plt.title('Total de usuarios de retiro en cada réplica')
plt.xlabel('Réplica')
plt.ylabel('Total de usuarios')

plt.subplot(1, 2, 2)
plt.plot(range(1, DIAS_SIMULACION + 1), total_usuarios_pago_todos, marker='o', linestyle='-', color='r')
plt.title('Total de usuarios de pago en cada réplica')
plt.xlabel('Réplica')
plt.ylabel('Total de usuarios')

plt.tight_layout()
plt.show()
