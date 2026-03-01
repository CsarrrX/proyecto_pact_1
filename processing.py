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

# Cambiamos las <<objetos>> de la expansión por booleanos
dataset["State Medicaid Expansion (2016)"] = dataset["State Medicaid Expansion (2016)"].astype(str)
dataset["State Medicaid Expansion (2016)"] = dataset["State Medicaid Expansion (2016)"].map({"True" : True, "False" : False}) 

print(dataset.info())



