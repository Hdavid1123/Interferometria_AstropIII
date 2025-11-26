import numpy as np
import pandas as pd

def centering_voltage(df):
    
    df2 = df.copy()
    displacementV = float(df2["voltage"].mean())
    
    df2["voltage"] -= displacementV

    print(f" Valor central original {displacementV}")

    return df2, displacementV

import matplotlib.pyplot as plt

def multiplaying_df(df, col, num_mult):
    
    df2 = df.copy()
    df2[col] *= num_mult
    
    return df2

def move_voltage(df, displacement):
    
    df2 = df.copy()
    df2["voltage"] -= displacement
    
    return df2

def sustraction_noise_pos_neg(df, num_neg, num_pos):
    df2 = df.copy()

    # Restar ruido dependiendo del signo original
    corrected = np.where(df2["voltage"] > 0,
                         df2["voltage"] - num_pos,
                         df2["voltage"] - num_neg)

    # Aplicar saturación a cero
    df2["voltage"] = np.where(
        (df2["voltage"] > 0) & (corrected < 0), 0,
        np.where((df2["voltage"] < 0) & (corrected > 0), 0, corrected)
    )

    return df2

def mean_pos_neg(df, col, df_name=None):
    """
    Calcula los promedios de los valores positivos y negativos de una columna de un DataFrame.
    Luego grafica la señal original y dos líneas horizontales con los promedios.
    
    Parámetros:
        df  : DataFrame
        col : nombre de la columna a analizar
    Returns:
        mean_pos, mean_neg
    """
    if col not in df.columns:
        raise ValueError(f"La columna '{col}' no existe en el DataFrame.")
    
    pos = df[df[col] > 0][col]
    neg = df[df[col] < 0][col]
    
    mean_pos = pos.mean() if len(pos) > 0 else None
    mean_neg = neg.mean() if len(neg) > 0 else None

    plt.figure(figsize=(8,4))
    plt.plot(df["time"], df[col])

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