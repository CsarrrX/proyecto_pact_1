# %%
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

# %%
# Información general del dataset 
dataset = pd.read_csv("states.csv") # Importamos el archivo csv
print("-"*20 + " INFORMACIÓN GENERAL DEL DATASET " + "-"*20)
print(dataset.info()) # Información de las columnas
print("\n")

# %%
# Limpieza de los datos y manipulación
dataset["Uninsured Rate (2010)"] = dataset["Uninsured Rate (2010)"].str.replace("%", "").astype(float) / 100
dataset["Uninsured Rate (2015)"] = dataset["Uninsured Rate (2015)"].str.replace("%", "").astype(float) / 100



