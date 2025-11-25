import numpy as np
import pandas as pd

def centering_voltage(df):
    
    df2 = df.copy()
    displacementV = float(df2["voltage"].mean())
    
    df2["voltage"] -= displacementV

    print(f" Valor central original {displacementV}")

    return df2

import matplotlib.pyplot as plt

def mean_pos_neg(df, col, df_name=None):
    """
    Calcula los promedios de los valores positivos y negativos 
    de una columna de un DataFrame. Luego grafica la señal original
    y dos líneas horizontales con los promedios.
    
    Parámetros:
        df  : DataFrame
        col : nombre de la columna a analizar
    
    Returns:
        mean_pos, mean_neg
    """

    if col not in df.columns:
        raise ValueError(f"La columna '{col}' no existe en el DataFrame.")
    
    # Valores positivos y negativos
    pos = df[df[col] > 0][col]
    neg = df[df[col] < 0][col]
    
    # Promedios
    mean_pos = pos.mean() if len(pos) > 0 else None
    mean_neg = neg.mean() if len(neg) > 0 else None

    # --- Gráfico ---
    plt.figure(figsize=(8,4))
    plt.plot(df["time"], df[col])

    # Líneas horizontales
    if mean_pos is not None:
        plt.axhline(mean_pos, linestyle='--', color="black", label=f"Promedio + ({mean_pos:.3f})")
    if mean_neg is not None:
        plt.axhline(mean_neg, linestyle='--', color="black", label=f"Promedio - ({mean_neg:.3f})")

    plt.title(f"{df_name}: señal y promedios positivos/negativos de '{col}'")
    plt.xlabel("Tiempo [uS]")
    plt.ylabel(col)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return mean_neg, mean_pos

    