import pandas as pd

def procesar_owon(df_noise1):
    """
    Procesa un DataFrame OWON en formato exportado por la app del osciloscopio.
    
    Toma:  
        df_noise1 → DataFrame con columnas Unnamed: 0, Unnamed: 1, CH1
                    incluyendo metadatos y datos crudos.
    
    Devuelve:
        metadata → diccionario con metadatos limpios
        data_df → DataFrame con columnas index, time, voltage + metadatos  
                   y con index como índice real.
    """

    # -----------------------------
    # 1. Extraer metadatos (primeras 5 filas)
    # -----------------------------
    meta_df = df_noise1.iloc[:5][["Unnamed: 0", "CH1"]]

    # Convertir a diccionario
    metadata = (
        meta_df
        .set_index("Unnamed: 0")["CH1"]
        .to_dict()
    )

    # Agregar el nombre del canal (valor fijo que estaba en la cabecera)
    metadata["Channel"] = "CH1"

    # Limpiar las claves (quitar ":")
    metadata = {k.replace(":", "").strip(): v for k, v in metadata.items()}

    # -----------------------------
    # 2. Extraer datos numéricos (desde fila 5)
    # -----------------------------
    data_df = df_noise1.iloc[5:].copy()

    # Renombrar columnas
    data_df.columns = ["index", "time", "voltage"]

    # -----------------------------
    # 3. Limpiar columnas numéricas
    # -----------------------------
    # índice
    data_df["index"] = data_df["index"].astype(int)

    # tiempo: quitar 'us' y convertir coma → punto
    data_df["time"] = (
        data_df["time"]
        .astype(str)
        .str.replace("us", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # voltaje: coma → punto
    data_df["voltage"] = (
        data_df["voltage"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    data_df.set_index("index", inplace=True)

    return metadata, data_df
