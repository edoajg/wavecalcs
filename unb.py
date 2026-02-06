import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo CSV con el delimitador correcto
df = pd.read_csv("waves.csv", delimiter=";")

# Convertir la columna de tiempo a numérico (si no lo es ya)
df["tiempo"] = pd.to_numeric(df["tiempo"])


# Graficar las formas de onda de las tres fases
plt.figure(figsize=(10, 5))
plt.plot(df["tiempo"], df["Voltage_L1"], label="VA", color="r")
plt.plot(df["tiempo"], df["Voltage_L2"], label="VB", color="g")
plt.plot(df["tiempo"], df["Voltage_L3"], label="VC", color="b")

plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Formas de Onda de las Tres Fases")
plt.legend()
plt.grid()
plt.show()


# Cargar el archivo CSV (ajusta el nombre si es diferente)
unb = pd.read_csv("unb.csv", delimiter=";")
unb.set_index('Start', inplace=True)
# Extraer columnas relevantes
V1 = unb["V1avg"]
V2 = unb["V2avg"]
V3 = unb["V3avg"]

# Calcular promedio, máximo y mínimo
V_promedio = (V1 + V2 + V3) / 3
V_max = pd.concat([V1, V2, V3], axis=1).max(axis=1)
V_min = pd.concat([V1, V2, V3], axis=1).min(axis=1)

# Calcular desbalance NEMA
unb["Desbalance_NEMA (%)"] = (V_max - V_min) / V_promedio * 100

# Filtro para identificar eventos con desbalance superior a 1%
unb["Desbalance_Alto"] = unb["Desbalance_NEMA (%)"] > 1

# Mostrar solo las filas con desbalance alto
desbalance_alto_df = unb[unb["Desbalance_Alto"]]

print("Filas con desbalance > 1%:")
print(desbalance_alto_df[["V1avg", "V2avg", "V3avg", "Desbalance_NEMA (%)"]])

# (Opcional) Guardar todo el DataFrame con marca en nuevo CSV
unb.to_csv("desbalance_nema_con_marca.csv", index=False)
print("Archivo guardado como 'desbalance_nema_con_marca.csv'")

# Crear figura
plt.figure(figsize=(12, 6))

# Graficar el desbalance
plt.plot(unb["Desbalance_NEMA (%)"], label="Desbalance NEMA (%)", color="blue")

# Resaltar los puntos que superan el umbral (1%)
plt.scatter(unb.index[unb["Desbalance_Alto"]],
            unb.loc[unb["Desbalance_Alto"], "Desbalance_NEMA (%)"],
            color="red", label="Desbalance > 1%", zorder=5)

# Opcional: agregar línea horizontal como referencia del 1%
plt.axhline(1, color="gray", linestyle="--", label="Límite 1% NEMA")

# Estética del gráfico
plt.title("Desbalance de Tensión según NEMA")
plt.xlabel("Índice de muestra")
plt.ylabel("Desbalance (%)")
indices = unb.index[::len(unb) // 4]  # Tomar 4 índices distribuidos
plt.xticks(indices)  # Establecer etiquetas del eje x
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.tight_layout()
plt.show()


# Calcula la corriente promedio
unb['I_prom'] = (unb['I1avg'] + unb['I2avg'] + unb['I3avg']) / 3

# Encuentra las corrientes máxima y mínima
unb['I_max'] = unb[['I1avg', 'I2avg', 'I3avg']].max(axis=1)
unb['I_min'] = unb[['I1avg', 'I2avg', 'I3avg']].min(axis=1)

# Calcula el desbalance de corriente como porcentaje
unb['Desbalance_Corriente_%'] = (unb['I_max'] - unb['I_min']) / unb['I_prom'] * 100

# Muestra el DataFrame con el nuevo cálculo
print(unb[['I1avg', 'I2avg', 'I3avg', 'Desbalance_Corriente_%']])


# Graficar el desbalance de corriente
plt.figure(figsize=(10, 6))
plt.bar(unb.index, unb['Desbalance_Corriente_%'], color='b', alpha=0.7)
plt.title('Desbalance de Corriente (%) por Medición')
plt.xlabel('Índice de Medición')
plt.ylabel('Desbalance de Corriente (%)')
indices = unb.index[::len(unb) // 4]  # Tomar 4 índices distribuidos
plt.xticks(indices)  # Establecer etiquetas del eje x
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.axhline(y=5, color='r', linestyle='--', label='Límite Máximo (5%)')  # Línea de límite
plt.axhline(y=10, color='orange', linestyle='--', label='Límite Crítico (10%)')  # Línea de límite
plt.legend()
plt.tight_layout()
plt.show()




##########################secuencias
# Definir el operador de fase a = e^(j120°)
a = np.exp(2j * np.pi / 3)

# Calcular las secuencias
df["Secuencia Cero"] = (df["Voltage_L1"] + df["Voltage_L2"] + df["Voltage_L3"]) / 3
df["Secuencia Positiva"] = (df["Voltage_L1"] + a * df["Voltage_L2"] + a**2 * df["Voltage_L3"]) / 3
df["Secuencia Negativa"] = (df["Voltage_L1"] + a**2 * df["Voltage_L2"] + a * df["Voltage_L3"]) / 3



# Graficar la magnitud de las secuencias
plt.figure(figsize=(10, 5))
plt.plot(df["tiempo"], np.abs(df["Secuencia Cero"]), label="Secuencia Cero", linestyle="dashed", color="k")
plt.plot(df["tiempo"], np.abs(df["Secuencia Positiva"]), label="Secuencia Positiva", color="g")
plt.plot(df["tiempo"], np.abs(df["Secuencia Negativa"]), label="Secuencia Negativa", color="r")

plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Magnitud de las Secuencias de Voltaje")
plt.legend()
plt.grid()
plt.show()

df.to_csv("secuencias_voltaje.csv", index=False)
print("Archivo guardado como secuencias_voltaje.csv")

############secuencias corriente

# Calcular las secuencias
df["Secuencia Cero"] = (df["Current_L1"] + df["Current_L2"] + df["Current_L3"]) / 3
df["Secuencia Positiva"] = (df["Current_L1"] + a * df["Current_L2"] + a**2 * df["Current_L3"]) / 3
df["Secuencia Negativa"] = (df["Current_L1"] + a**2 * df["Current_L2"] + a * df["Current_L3"]) / 3


# Graficar la magnitud de las secuencias
plt.figure(figsize=(10, 5))
plt.plot(df["tiempo"], np.abs(df["Secuencia Cero"]), label="Secuencia Cero", linestyle="dashed", color="k")
plt.plot(df["tiempo"], np.abs(df["Secuencia Positiva"]), label="Secuencia Positiva", color="g")
plt.plot(df["tiempo"], np.abs(df["Secuencia Negativa"]), label="Secuencia Negativa", color="r")

plt.xlabel("Tiempo (s)")
plt.ylabel("Corriente (A)")
plt.title("Magnitud de las Secuencias de Corriente")
plt.legend()
plt.grid()
plt.show()

df.to_csv("secuencias_corriente.csv", index=False)
print("Archivo guardado como secuencias_corriente.csv")