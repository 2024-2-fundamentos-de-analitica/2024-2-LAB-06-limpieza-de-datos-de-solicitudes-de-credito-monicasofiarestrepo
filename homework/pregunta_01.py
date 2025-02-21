"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import os
import pandas as pd

def load_data(input_path):
    """Carga los datos desde el archivo CSV"""
    return pd.read_csv(input_path, sep=';', index_col=0)

def clean_text(text_series):
    """Limpia series de texto: lowercase, strip y reemplazo de caracteres"""
    clean = text_series.str.lower().str.replace("_", " ").str.replace("-", " ").str.strip()
    return clean

def clean_amount(amount_series):
    """Limpia y convierte la columna de monto"""
    return (amount_series.str.strip()
            .str.replace("$","")
            .str.replace(",","")
            .str.replace(".00","")
            .astype(int))

def process_dates(date_series):
    """Procesa y homologa las fechas"""
    dates = pd.to_datetime(date_series, dayfirst=True, errors='coerce')
    mask = dates.isnull()
    dates[mask] = pd.to_datetime(
        date_series[mask], 
        format="%Y/%m/%d", 
        errors='coerce'
    )
    return dates

def clean_dataframe(df):
    """Aplica todas las transformaciones al dataframe"""
    # Eliminar nulos y duplicados
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    
    
    df['sexo'] = df['sexo'].str.lower()
    # Limpiar columnas de texto simple
    df['tipo_de_emprendimiento'] = df['tipo_de_emprendimiento'].str.lower().str.strip()
    df['barrio'] = df['barrio'].str.lower().str.replace("_", " ").str.replace("-", " ")

    
    # Limpiar columnas de texto con reemplazo de caracteres
    text_replace_columns = ['idea_negocio', 'línea_credito']
    for col in text_replace_columns:
        df[col] = clean_text(df[col])
    
    # Procesar monto
    df['monto_del_credito'] = clean_amount(df['monto_del_credito'])
    
    # Procesar fechas
    df['fecha_de_beneficio'] = process_dates(df['fecha_de_beneficio'])
    
    # df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    return df

def save_data(df, output_path):
    """Guarda los datos procesados"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep=';')


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    INPUT_PATH = 'files/input/solicitudes_de_credito.csv'
    OUTPUT_PATH = 'files/output/solicitudes_de_credito.csv'
    
    # Proceso completo
    df = load_data(INPUT_PATH)
    df = clean_dataframe(df)
    save_data(df, OUTPUT_PATH)
