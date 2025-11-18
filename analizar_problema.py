import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar dataset
df = pd.read_csv('df_finanzas.csv', sep=';', low_memory=False)

# Aplicar transformaciones básicas
valores_validos = ["S", "N"]
df = df[df["ACUMULA_DEC_CUARTO"].isin(valores_validos)].copy()
df = df[df["ACUMULA_DEC_TERCERO"].isin(valores_validos)].copy()

valores_a_eliminar = [
    "ESTADO ESTADOS UNIDOS", "ESTADO COLOMBIA", "ESTADO ESPAÑA",
    "ESTADO CANADA", "ESTADO ITALIA", "ESTADO ARGENTINA",
    "ESTADO CHINA", "ESTADO PERU", "ESTADO CHILE", "REGIONAL"
]
df = df[~df['NOMBRE_PROVINCIA'].isin(valores_a_eliminar)].copy()
df['GENERO'] = df['GENERO'].replace({'MUJER': 'FEMENINO', 'HOMBRE': 'MASCULINO'})
df['RMU_PUESTO'] = df['RMU_PUESTO'].astype(str).str.replace(',', '.').astype(float)

# Crear categorías
cuartiles = df['RMU_PUESTO'].quantile([0.25, 0.5, 0.75]).values

def clasificar_sueldo(rmu):
    if rmu <= cuartiles[0]:
        return 'Bajo'
    elif rmu <= cuartiles[1]:
        return 'Medio-Bajo'
    elif rmu <= cuartiles[2]:
        return 'Medio-Alto'
    else:
        return 'Alto'

df['CATEGORIA_SUELDO'] = df['RMU_PUESTO'].apply(clasificar_sueldo)

print('='*70)
print('ANÁLISIS DEL PROBLEMA DE BAJO ACCURACY')
print('='*70)

print('\n1. DISTRIBUCIÓN DE SUELDOS POR CUARTILES:')
print(f'Q1 (Bajo ≤):        ${cuartiles[0]:.2f}')
print(f'Q2 (Medio-Bajo ≤):  ${cuartiles[1]:.2f}')
print(f'Q3 (Medio-Alto ≤):  ${cuartiles[2]:.2f}')
print(f'Max (Alto):         ${df["RMU_PUESTO"].max():.2f}')

print('\n2. SOLAPAMIENTO ENTRE CATEGORÍAS:')
print('¿Las categorías están bien separadas?')
for cat in ['Bajo', 'Medio-Bajo', 'Medio-Alto', 'Alto']:
    subset = df[df['CATEGORIA_SUELDO'] == cat]['RMU_PUESTO']
    print(f'\n{cat}:')
    print(f'  Min: ${subset.min():.2f}, Max: ${subset.max():.2f}')
    print(f'  Media: ${subset.mean():.2f}, Std: ${subset.std():.2f}')

print('\n3. ANALIZAR SI CANTON APORTA INFORMACIÓN:')
# Ver si hay diferencias de sueldo por cantón
canton_stats = df.groupby('NOMBRE_CANTON')['RMU_PUESTO'].agg(['mean', 'std', 'count'])
canton_stats = canton_stats.sort_values('mean', ascending=False)
print(f'\nCantones con mayor sueldo promedio (top 10):')
print(canton_stats.head(10))
print(f'\nCantones con menor sueldo promedio (bottom 10):')
print(canton_stats.tail(10))
print(f'\nVariación de sueldo entre cantones:')
print(f'  Sueldo más alto: ${canton_stats["mean"].max():.2f}')
print(f'  Sueldo más bajo: ${canton_stats["mean"].min():.2f}')
print(f'  Diferencia: ${canton_stats["mean"].max() - canton_stats["mean"].min():.2f}')
print(f'  → CANTON SÍ APORTA INFORMACIÓN!')

print('\n4. ANALIZAR SI PROVINCIA APORTA:')
provincia_stats = df.groupby('NOMBRE_PROVINCIA')['RMU_PUESTO'].agg(['mean', 'std', 'count'])
provincia_stats = provincia_stats.sort_values('mean', ascending=False)
print(f'\nProvincias con mayor sueldo promedio:')
print(provincia_stats.head())
print(f'\nVariación: ${provincia_stats["mean"].max() - provincia_stats["mean"].min():.2f}')

print('\n5. CORRELACIÓN DE FEATURES CON EL SUELDO:')
# Preparar datos numéricos
df_temp = df.copy()
df_temp = df_temp.dropna(subset=['GENERO'])
df_temp['GENERO_NUM'] = (df_temp['GENERO'] == 'MASCULINO').astype(int)

# Convertir fechas
df_temp['FECHA_NACIMIENTO'] = pd.to_datetime(df_temp['FECHA_NACIMIENTO'], format='%d/%m/%y', errors='coerce')
df_temp['FECHA_NACIMIENTO'] = df_temp['FECHA_NACIMIENTO'].apply(
    lambda x: x - pd.DateOffset(years=100) if pd.notna(x) and x.year > 2016 else x
)
df_temp['EDAD'] = (pd.Timestamp('2016-01-01') - df_temp['FECHA_NACIMIENTO']).dt.days // 365

correlaciones = df_temp[['RMU_PUESTO', 'GENERO_NUM', 'EDAD']].corr()['RMU_PUESTO'].sort_values(ascending=False)
print(correlaciones)

print('\n6. ANÁLISIS DE FEATURES CATEGÓRICAS IMPORTANTES:')
for col in ['SECTOR_DESC', 'NOMBRE_REGIMEN_LABORAL', 'NOMBRE_NIVEL_OCUPACIONAL']:
    if col in df.columns:
        stats = df.groupby(col)['RMU_PUESTO'].mean().sort_values(ascending=False)
        print(f'\n{col} - Variación de sueldo:')
        print(f'  Max: ${stats.max():.2f}')
        print(f'  Min: ${stats.min():.2f}')
        print(f'  Diferencia: ${stats.max() - stats.min():.2f}')

print('\n' + '='*70)
print('CONCLUSIONES:')
print('='*70)
print('✅ CANTON debe MANTENERSE - Aporta información geográfica valiosa')
print('✅ Las clases Medio-Alto y Medio-Bajo están muy cerca → CONFUSIÓN')
print('⚠️  Posible solución: Reducir a 3 clases o mejorar arquitectura')
