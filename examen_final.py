#%%
import kagglehub

# Download latest version
path = kagglehub.dataset_download("uciml/adult-census-income")

print("Path to dataset files:", path)
# %%
import pandas as pd
import os

# Suponiendo que 'path' es el directorio que contiene 'adult.csv'
file_path = os.path.join(path, 'adult.csv')
adult_df = pd.read_csv(file_path)
adult_df.head()

# %%
adult_df.shape
# %%
adult_df.info()
# %%
adult_df.isnull().sum()
# %%
import numpy as np
adult_clean = adult_df.replace('?', np.nan).dropna()

# %%
adult_clean.isnull().sum()

# %%
columnas_eliminar = ['education', 'fnlwgt', 'capital-gain', 'capital-loss']
adult_clean = adult_clean.drop(columns=columnas_eliminar)

#%%
# Variables numéricas (selección manual)
numeric_cols = [
    'age',  #anonimizacion
    'fnlwgt',
    'education.num',
    'capital.gain',
    'capital.loss',
    'hours.per.week'
]

# Variables categóricas (selección manual)
categorical_cols = [
    'workclass',
    'education',
    'marital.status',
    'occupation',
    'relationship',
    'race',
    'sex',
    'native.country',
    'income'   # variable objetivo
]

numeric_cols, categorical_cols

#%%
