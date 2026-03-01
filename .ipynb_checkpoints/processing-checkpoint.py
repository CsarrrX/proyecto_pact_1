import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %% 1. CONFIGURACIÓN DE ESTILO ESTÉTICO
plt.rcParams['figure.facecolor'] = '#FDFDFD'
plt.rcParams['axes.facecolor'] = '#FDFDFD'
plt.rcParams['axes.edgecolor'] = '#D1D1D1'
plt.rcParams['axes.labelcolor'] = '#4F4F4F'
plt.rcParams['xtick.color'] = '#4F4F4F'
plt.rcParams['ytick.color'] = '#4F4F4F'
pastel_palette = ["#FFB7B2", "#FFDAC1", "#E2F0CB", "#B5EAD7", "#C7CEEA", "#F3B0C3"]

# %% 2. CARGA Y LIMPIEZA
CostShare_df = pd.read_csv("dataset/BenefitsCostSharing.csv")
Rate_df = pd.read_csv("dataset/Rate.csv")
Plan_Attributes_df = pd.read_csv("dataset/PlanAttributes.csv")

# Limpieza de montos y porcentajes
def clean_num(col):
    return pd.to_numeric(col.astype(str).str.replace(r'[\$,%]', '', regex=True).replace('No Charge', '0'), errors='coerce').fillna(0)

Plan_Attributes_df["TEHBDedInnTier1Individual"] = clean_num(Plan_Attributes_df["TEHBDedInnTier1Individual"])
Rate_df["IndividualRate"] = clean_num(Rate_df["IndividualRate"])

# Estandarización de Edad
def clean_age(a):
    a = str(a).lower()
    if '0-14' in a: return 14
    if '64' in a or 'over' in a: return 65
    try: return int(a)
    except: return np.nan

Rate_df['Age_Num'] = Rate_df['Age'].apply(clean_age)
Rate_df = Rate_df.dropna(subset=['Age_Num'])

# Consolidación Actuarial
df = pd.merge(Plan_Attributes_df, Rate_df, on=["PlanId", "BusinessYear", "StateCode"])

# Filtrado de Outliers (IQR)
Q1, Q3 = df['IndividualRate'].quantile([0.25, 0.75])
IQR = Q3 - Q1
df = df[(df['IndividualRate'] >= Q1 - 1.5*IQR) & (df['IndividualRate'] <= Q3 + 1.5*IQR)]

# Variable Derivada: Segmentos de edad
df['Age_Group'] = pd.cut(df['Age_Num'], bins=[0, 25, 45, 65], labels=['Joven', 'Adulto', 'Senior'])
# --- VARIABLE DERIVADA 2: Índice de Eficiencia del Plan (Numérica Continua) ---
# Calculamos cuánto paga el usuario por cada punto porcentual de Cobertura Actuarial (AV)
# Un índice más bajo significa que el plan es más "barato" por el beneficio que ofrece.
df['Cost_Efficiency_Index'] = df['IndividualRate'] / (df['IssuerActuarialValue'] * 100)

# %% 3. VISUALIZACIONES (ESTILO PASTEL CON BORDES LIMPÍOS)

fig, axs = plt.subplots(3, 2, figsize=(16, 20))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# 1. Pastel - Distribución de Mercado
labels = df['MetalLevel'].value_counts().index
axs[0, 0].pie(df['MetalLevel'].value_counts(), labels=labels, autopct='%1.1f%%', 
              colors=pastel_palette, startangle=140, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axs[0, 0].set_title('Concentración de Riesgo por Nivel de Plan', fontweight='bold')

# 2. Barras - Prima por Edad
sns.barplot(x='Age_Group', y='IndividualRate', data=df, ax=axs[0, 1], palette=pastel_palette, 
            edgecolor='#4F4F4F', linewidth=0.5, capsize=.1)
axs[0, 1].set_title('Costo Mensual Promedio según Etapa de Vida', fontweight='bold')

# 3. Histograma - Deducibles
sns.histplot(df['TEHBDedInnTier1Individual'], bins=15, ax=axs[1, 0], color="#B5EAD7", 
             kde=True, edgecolor='white', line_kws={'linewidth': 3})
axs[1, 0].set_title('Distribución de Deducibles (Barreras de Entrada)', fontweight='bold')

# 4. Boxplot - Fumadores (Bordes redondeados estilizados)
sns.boxplot(x='Tobacco', y='IndividualRate', data=df, ax=axs[1, 1], palette=[pastel_palette[0], pastel_palette[4]], 
            width=0.5, fliersize=2)
axs[1, 1].set_title('Impacto del Tabaquismo en la Tarifa', fontweight='bold')

# 5. Líneas - Tendencia Temporal
yearly_avg = df.groupby('BusinessYear')['IndividualRate'].mean()
axs[2, 0].plot(yearly_avg.index, yearly_avg.values, marker='o', markersize=10, 
               linewidth=4, color=pastel_palette[5], markerfacecolor='white')
axs[2, 0].set_title('Evolución de Primas en el Tiempo', fontweight='bold')
axs[2, 0].set_xticks(yearly_avg.index)

# 6. Scatter - Deducible vs Prima
hb = axs[2, 1].hexbin(df['TEHBDedInnTier1Individual'], df['IndividualRate'], gridsize=20, cmap='Pastel1', mincnt=1)
axs[2, 1].set_title('Densidad: Relación Deducible vs Prima', fontweight='bold')
fig.colorbar(hb, ax=axs[2, 1], label='Frecuencia de Planes')

# Estética general: Quitar bordes superiores y derechos (despine)
for ax in axs.flat:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.show()
