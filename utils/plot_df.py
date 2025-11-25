import matplotlib.pyplot as plt

def plot_df(df, x_col="time", y_col="voltage", xlim=None, ylim=None, title=None, xlabel=None, ylabel=None):
    """
    Grafica dos columnas de un DataFrame usando sus nombres.
    
    Parámetros:
        df     : DataFrame
        x_col  : nombre de la columna para el eje X
        y_col  : nombre de la columna para el eje Y
        title  : título opcional
        xlabel : etiqueta opcional del eje X
        ylabel : etiqueta opcional del eje Y
    """

    # Validación opcional para evitar errores comunes
    if x_col not in df.columns:
        raise ValueError(f"La columna '{x_col}' no existe en el DataFrame.")
    if y_col not in df.columns:
        raise ValueError(f"La columna '{y_col}' no existe en el DataFrame.")

    plt.figure(figsize=(8,4))
    plt.plot(df[x_col], df[y_col])
    plt.xlabel(xlabel if xlabel else x_col)
    plt.ylabel(ylabel if ylabel else y_col)
    plt.title(title if title else f"{y_col} vs {x_col}")
    if xlim is not None:
        plt.xlim(xlim[0],xlim[1])
    if ylim is not None:    
        plt.ylim(ylim[0],ylim[1])
    plt.grid(True)
    plt.tight_layout()
    plt.show()
