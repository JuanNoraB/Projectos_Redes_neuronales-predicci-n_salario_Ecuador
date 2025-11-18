#%%
#read csv
import pandas as pd
file_path = 'df_finanzas.csv'
df = pd.read_csv(file_path,sep=';')
df.head()

cols_eliminar = [
    "ID",
    "COMISION_SERVICIO_TIPO",
    "Unnamed: 32",
    "Unnamed: 33",
    "Unnamed: 34",
    "Unnamed: 35",
    "Unnamed: 36",
    "Unnamed: 37",
    "ENLACE_GRUPO",
    "EJERCICIO_FISCAL",
    "SECTOR_DESC",
    "ENTIDAD_DESC",
    "UNIDAD_EJECUTORA",
    "UNIDAD_EJECUTORA_DESC",
    "PARTIDAD_INDIVIDUAL",
    "APELLIDOS_NOMBRES",
    "FECHA_FIN",
    "NOMBRE_MODALIDAD_LABORAL",
    "DESCRIPCION_ESCALA_OCUPACIONAL",
    "NOMBRE_ESTADO_SERVIDOR",
    "ESTRUCTURA_ORGANICA"
]

df = df.drop(columns=cols_eliminar, errors="ignore")

# %%
df.columns
# %%
#delete columns
columns_delete = ['Unnamed: 32', 'Unnamed: 33',
       'Unnamed: 34', 'Unnamed: 35', 'Unnamed: 36', 'Unnamed: 37']
df = df.drop(columns=columns_delete)
df.head()
# %%
df.isnull().sum()
# %%
# fo COMISION_SERVICIO_TIPO            
df['COMISION_SERVICIO_TIPO'].unique()
# %%
#delete COMISION_SERVICIO_TIPO
df.drop(columns=['COMISION_SERVICIO_TIPO'], inplace=True)

# %%
df.isnull().sum()  
# %%
#delete null
df = df.dropna()

# %%
df.isnull().sum()

#%%
df.info()

# %%
for i in df.columns:
    if len(df[i].unique()) < 100:
        print(i, df[i].unique())

# %%
#LIMPIAR PROVICIAS
# Lista de valores incorrectos que deben eliminarse por completo
valores_a_eliminar = [
    "ESTADO ESTADOS UNIDOS",
    "ESTADO COLOMBIA",
    "ESTADO ESPAÑA",
    "ESTADO CANADA",
    "ESTADO ITALIA",
    "ESTADO ARGENTINA",
    "ESTADO CHINA",
    "ESTADO PERU",
    "ESTADO CHILE",
    "REGIONAL"
]

# Eliminación de filas que contengan esos valores
df = df[~df['NOMBRE_PROVINCIA'].isin(valores_a_eliminar)].copy()

#LIMPIAR GENERO 
df['GENERO'] = df['GENERO'].replace({
    'MUJER': 'FEMENINO',
    'HOMBRE': 'MASCULINO'
})
#%%


