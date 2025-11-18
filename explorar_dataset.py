import pandas as pd
import numpy as np

# Cargar y limpiar dataset
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

print('='*70)
print('ANÁLISIS DE COLUMNAS PROBLEMÁTICAS')
print('='*70)

print('\n1. GÉNERO:')
print(df['GENERO'].value_counts(dropna=False))
print(f'   Nulls: {df["GENERO"].isna().sum()} ({df["GENERO"].isna().sum()/len(df)*100:.2f}%)')

print('\n2. FECHA_NACIMIENTO:')
print(f'   Valores únicos: {df["FECHA_NACIMIENTO"].nunique()}')
print(f'   Nulls: {df["FECHA_NACIMIENTO"].isna().sum()}')
print(f'   Sample: {df["FECHA_NACIMIENTO"].head(5).tolist()}')

print('\n3. FECHA_INICIO:')
print(f'   Valores únicos: {df["FECHA_INICIO"].nunique()}')
print(f'   Nulls: {df["FECHA_INICIO"].isna().sum()}')
print(f'   Sample: {df["FECHA_INICIO"].head(5).tolist()}')

print('\n4. NUMERO_DOCUMENTO:')
print(f'   Valores únicos: {df["NUMERO_DOCUMENTO"].nunique()}')
print(f'   Total registros: {len(df)}')
print(f'   Proporción única: {df["NUMERO_DOCUMENTO"].nunique()/len(df)*100:.2f}%')
print(f'   Nulls: {df["NUMERO_DOCUMENTO"].isna().sum()}')

print('\n5. ANÁLISIS GENERAL DE NULLS:')
print('='*70)
nulls = df.isnull().sum()
nulls_pct = (nulls / len(df) * 100).round(2)
nulls_df = pd.DataFrame({
    'Columna': nulls.index,
    'Nulls': nulls.values,
    'Porcentaje': nulls_pct.values
})
nulls_df = nulls_df[nulls_df['Nulls'] > 0].sort_values('Nulls', ascending=False)
print(nulls_df.to_string(index=False))

print('\n6. CALCULAR EDAD Y ANTIGÜEDAD:')
# Detectar formato de fecha (d/m/y)
df['FECHA_NACIMIENTO'] = pd.to_datetime(df['FECHA_NACIMIENTO'], format='%d/%m/%y', errors='coerce')
df['FECHA_INICIO'] = pd.to_datetime(df['FECHA_INICIO'], format='%d/%m/%y', errors='coerce')

# Si la fecha de nacimiento es futura, restar 100 años (problema del año 2000)
df['FECHA_NACIMIENTO'] = df['FECHA_NACIMIENTO'].apply(
    lambda x: x - pd.DateOffset(years=100) if pd.notna(x) and x.year > 2016 else x
)

df['EDAD'] = (pd.Timestamp('2016-01-01') - df['FECHA_NACIMIENTO']).dt.days // 365
df['ANTIGUEDAD_DIAS'] = (pd.Timestamp('2016-01-01') - df['FECHA_INICIO']).dt.days

print(f'\nEDAD - Stats:')
print(df['EDAD'].describe())
print(f'\nANTIGÜEDAD (días) - Stats:')
print(df['ANTIGUEDAD_DIAS'].describe())

print('\n' + '='*70)
print('RESUMEN DE CAMBIOS RECOMENDADOS:')
print('='*70)
print('✅ 1. NUMERO_DOCUMENTO → ELIMINAR (casi único, no aporta)')
print('✅ 2. FECHA_NACIMIENTO → Convertir a EDAD (numérico)')
print('✅ 3. FECHA_INICIO → Convertir a ANTIGUEDAD_DIAS (numérico)')
print('✅ 4. GENERO → Dropna antes de entrenar (son pocos nulls)')
print(f'\nRegistros con GENERO null: {df["GENERO"].isna().sum()} ({df["GENERO"].isna().sum()/len(df)*100:.2f}%)')
