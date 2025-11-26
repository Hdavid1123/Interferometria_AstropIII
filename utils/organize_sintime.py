def preparar_df_owon(df, col_time, sp_mult):
    """
    df        : dataframe original leído desde OWON
    col_time  : nombre de la columna que contiene los índices de tiempo
    sp_mult   : factor para convertir el índice en tiempo real (por ejemplo SP en µs)
    """

    # 1. Copia desde la fila 5 en adelante (los datos reales)
    df2 = df.iloc[5:].copy()

    # 2. Multiplica la columna de tiempo por el factor SP
    df2[col_time] = df2[col_time] * sp_mult

    # 3. Renombra columnas a "time" y "voltage"
    df2.columns = ["time", "voltage"]

    return df2

import pandas as pd
import numpy as np

def procesar_owon_sin(df):
    """
    Procesa un archivo OWON que contiene 5 filas de metadatos
    con posibles NaN en las columnas.

    Devuelve:
        metadata → diccionario limpio
        data_df → DataFrame con columnas time (float, en us) y voltage (float)
    """

    # -----------------------------
    # 1. Extraer metadatos
    # -----------------------------
    meta_df = df.iloc[:5][["Unnamed: 0", "CH1"]]

    metadata = {}
    for idx, row in meta_df.iterrows():
        key = row["Unnamed: 0"]
        value = row["CH1"]

        # Saltar filas donde key es NaN
        if pd.isna(key):
            continue

        # Convertir claves a texto seguro
        key = str(key).replace(":", "").strip()

        # Si el valor es NaN, poner None
        if pd.isna(value):
            value = None
        else:
            value = str(value).strip()

        metadata[key] = value

    metadata["Channel"] = "CH1"

    # -----------------------------
    # 2. Extraer datos desde fila 5
    # -----------------------------
    data_df = df.iloc[5:].copy()

    # Renombrar columnas
    data_df.columns = ["index", "time", "voltage"]

    # Quitar índice OWON y dejar index verdadero
    data_df["index"] = pd.to_numeric(data_df["index"], errors="coerce").astype("Int64")

    # -----------------------------
    # 3. Limpiar columna time
    # -----------------------------
    data_df["time"] = (
        data_df["time"]
        .astype(str)
        .str.replace("us", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    data_df["time"] = pd.to_numeric(data_df["time"], errors="coerce")

    # -----------------------------
    # 4. Limpiar columna voltage
    # -----------------------------
    data_df["voltage"] = (
        data_df["voltage"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )
    data_df["voltage"] = pd.to_numeric(data_df["voltage"], errors="coerce")

    # Establecer índice real
    data_df.set_index("index", inplace=True)

    return metadata, data_df

