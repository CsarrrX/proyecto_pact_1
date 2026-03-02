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

print("-"*20 + " PRIMERAS 5 COLUMNAS DEL DATASET " + "-"*20)
print(dataset.head()) 
print("\n")

print("-"*20 + " DESCRIPCIÓN GENERAL DEL DATASET " + "-"*20)
print(dataset.describe()) 
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

# Para la columna booleana rellenar con la moda 
dataset['State Medicaid Expansion (2016)'] = dataset['State Medicaid Expansion (2016)'].fillna(dataset['State Medicaid Expansion (2016)'].mode()[0])

# Identificamos los outliers de manera visual
plt.figure(figsize=(15, 6))

Q1 = dataset['Medicaid Enrollment (2016)'].quantile(0.25)
Q3 = dataset['Medicaid Enrollment (2016)'].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR

colores = ['red' if x > limite_superior else 'blue' for x in dataset['Medicaid Enrollment (2016)']]

plt.scatter(dataset['State'], dataset['Medicaid Enrollment (2016)'], c=colores, s=100, alpha=0.7)
plt.axhline(y=limite_superior, color='r', linestyle='--', label=f'Límite de Outliers ({limite_superior:,.0f})')

plt.title('Inscripciones en Medicaid por Estado (Outliers en Rojo)', fontsize=14)
plt.ylabel('Número de Personas Inscritas', fontsize=12)
plt.xticks(rotation=90, fontsize=8)
plt.legend()
plt.tight_layout()
plt.show()

# Cambios en el dataset
print("-"*20 + " INFORMACIÓN DEL DATASET DESPUÉS DE LOS CAMBIOS " + "-"*20)
print(dataset.info()) 
print("\n")

# %%
# Variables derivadas 

# 1. Aproximación de población total asegurada por estado
dataset['Total Insured Approx'] = (
    dataset['Employer Health Insurance Coverage (2015)'] + 
    dataset['Marketplace Health Insurance Coverage (2016)'] + 
    dataset['Medicaid Enrollment (2016)'] + 
    dataset['Medicare Enrollment (2016)']
)

# 2. Índice de Riesgo Público vs Privado
dataset['Public vs Private Risk Index'] = (
    (dataset['Medicaid Enrollment (2016)'] + dataset['Medicare Enrollment (2016)']) / 
    (dataset['Employer Health Insurance Coverage (2015)'] + dataset['Marketplace Health Insurance Coverage (2016)'])
)

# 3. Gasto Anual Estimado en Subsidios
dataset['Annual Tax Credit Expenditure'] = (
    dataset['Marketplace Tax Credits (2016)'] * dataset['Average Monthly Tax Credit (2016)'] * 12
)

# 4. Ratio de Dependencia de Subsidios en el Mercado Privado
dataset['Subsidy Dependence Ratio'] = (
    dataset['Marketplace Tax Credits (2016)'] / 
    dataset['Marketplace Health Insurance Coverage (2016)']
)

dataset.to_csv("states_processed.csv", index=False)
