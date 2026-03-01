# %%
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

# %%
# Información general del dataset 

# Importamos el archivo csv
dataset = pd.read_csv("states.csv") 

# Información de las columnas
print("-"*20 + " INFORMACIÓN GENERAL DEL DATASET " + "-"*20)
print(dataset.info()) 
print("\n")

# %%
# Limpieza de los datos y manipulación

# Cambiamos los porcentajes por decimales usables
dataset["Uninsured Rate (2010)"] = dataset["Uninsured Rate (2010)"].str.replace("%", "").astype(float) / 100
dataset["Uninsured Rate (2015)"] = dataset["Uninsured Rate (2015)"].str.replace("%", "").astype(float) / 100
dataset["Uninsured Rate Change (2010-2015)"] = dataset["Uninsured Rate Change (2010-2015)"].str.replace("%", "").astype(float) / 100

# Cambiamos las cantidades de dolares a enteros usables
dataset["Average Monthly Tax Credit (2016)"] = dataset["Average Monthly Tax Credit (2016)"].str.replace("$", "").astype(int)

# Rellenar los valores nulos con la media de sus respectivas columnas
dataset['Medicaid Enrollment (2013)'] = dataset['Medicaid Enrollment (2013)'].fillna(dataset['Medicaid Enrollment (2013)'].mean())
dataset['Medicaid Enrollment Change (2013-2016)'] = dataset['Medicaid Enrollment Change (2013-2016)'].fillna(dataset['Medicaid Enrollment Change (2013-2016)'].mean())

# Cambios en el dataset
print("-"*20 + " INFORMACIÓN DEL DATASET DESPUÉS DE LOS CAMBIOS " + "-"*20)
print(dataset.info()) 
print("\n")

# %%
# Variables derivadas 

# 
