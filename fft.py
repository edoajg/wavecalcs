import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

archivo = 'waves.csv'
datos = pd.read_csv(archivo, sep=';')


# Suponiendo que 'datos' es tu DataFrame con las columnas necesarias
# Definimos las columnas para las tres fases
columnas_fases = [1, 2, 3]  # Columnas para las fases
n_armonicos = 50  # Número de armónicos a analizar
f_fundamental = 50  # Frecuencia fundamental en Hz

# Crear una figura para los gráficos
plt.figure(figsize=(12, 6))

# Iterar sobre cada fase
for i, col in enumerate(columnas_fases):
    tiempo = datos.iloc[:, 0].values  # Primera columna: tiempo (s)
    señal = datos.iloc[:, col].values   # Señal de la fase actual

    # Calcular la frecuencia de muestreo
    dt = np.mean(np.diff(tiempo))  # Paso de tiempo medio
    fs = 1 / dt  # Frecuencia de muestreo

    # Aplicar FFT
    N = len(señal)  # Número de muestras
    fft_resultado = np.fft.fft(señal)  # Transformada de Fourier
    frecuencias = np.fft.fftfreq(N, d=dt)  # Escala de frecuencia

    # Tomar solo la mitad del espectro (frecuencias positivas)
    mitad = N // 2
    frecuencias = frecuencias[:mitad]
    magnitud_fft = np.abs(fft_resultado[:mitad]) / N  # Normalización

    # Calcular porcentajes de armónicos
    porcentajes = []
    for f in [f_fundamental * (n + 1) for n in range(n_armonicos)]:
        idx = np.argmin(np.abs(frecuencias - f))
        magnitud = magnitud_fft[idx]
        porcentaje = 100 * magnitud / magnitud_fft[np.argmin(np.abs(frecuencias - f_fundamental))]
        porcentajes.append(porcentaje)

    # Calcular THD
    armonicos_sq = [magnitud_fft[np.argmin(np.abs(frecuencias - f))] ** 2 for f in [f_fundamental * (n + 1) for n in range(1, n_armonicos)]]
    thd = (np.sqrt(np.sum(armonicos_sq)) / magnitud_fft[np.argmin(np.abs(frecuencias - f_fundamental))]) * 100  # THD como porcentaje

    # Graficar los porcentajes de armónicos
    bar_width = 0.25  # Ancho de las barras
    x_positions = np.arange(n_armonicos) + (i * bar_width)  # Posiciones ajustadas para cada fase
    bars = plt.bar(x_positions, porcentajes, width=bar_width, label=f'Fase {i + 1}')  # Usar posiciones ajustadas

    # Etiquetas sobre algunas barras
    for bar, valor in zip(bars, porcentajes):
        altura = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, altura + 0.3, f"{valor:.1f}%", 
                 ha='center', va='bottom', fontsize=7, rotation=45)

    # Agregar barra de THD
    plt.bar(-0.5 + (i * 0.1), thd, width=bar_width, color='orange', edgecolor='black', label=f'THD Fase {i + 1}: {thd:.2f}')
  #  plt.text(-0.5 + (i * 0.1), thd + 0.5, f"THD: {thd:.2f}%", ha='center', va='bottom', fontsize=10)

# Configurar el gráfico
plt.xlabel("Orden del armónico")
plt.xticks(np.arange(n_armonicos), list(range(1, n_armonicos + 1)))  # Ajustar ticks del eje x
plt.ylabel("Magnitud (% respecto a la fundamental)")
plt.title("Análisis armónico - 50 primeros armónicos y THD")
plt.grid(axis='y')

# Ajustar límites
plt.ylim(0, max(max(porcentajes), thd) * 1.3)

# Leyenda
plt.legend()
plt.tight_layout()
plt.show()


n_armonico = []
valores_rms = []
porcentajes = []

for n in range(n_armonicos):
    frec = f_fundamental * (n + 1)  # Calcular la frecuencia del armónico
    idx = np.argmin(np.abs(frecuencias - frec))  # Obtener el índice más cercano
    magnitud = magnitud_fft[idx]  # Magnitud de FFT
    
    # Calcular RMS (asumiendo que magnitud_fft ya es el valor RMS)
    rms_value = magnitud  # Aquí se puede modificar si necesitas un cálculo diferente
    rms_percentage = 100 * rms_value / magnitud_fft[np.argmin(np.abs(frecuencias - f_fundamental))]  # % respecto a la fundamental
    
    # Guardar resultados
    n_armonico.append(frec / f_fundamental)  # n_armónico
    valores_rms.append(rms_value)          # valor RMS
    porcentajes.append(rms_percentage)      # % fundamental

# --- Crear DataFrame ---
df = pd.DataFrame({
    'n_armónico': n_armonico,
    'Valor RMS': valores_rms,
    '% Fundamental': porcentajes
})

# --- Guardar en CSV ---
df.to_csv('armonicos_rms.csv', index=False)

print("Archivo CSV guardado como 'armonicos_rms.csv'")