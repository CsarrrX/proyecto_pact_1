# %% [markdown]
# # PROYECTO: ANÁLISIS ACTUARIAL DE MERCADO DE SALUD (US)
# Integrantes: [Nombres aquí]

# %%
import pandas as pd
import matplotlib.pyplot as plt

# %% --- CONFIGURACIÓN DE ESTILO ---
# Colores pastel seleccionados para que se vea premium
C_ROSA, C_AMAR, C_VERD, C_AZUL, C_LILA = "#FFB7B2", "#FFDAC1", "#E2F0CB", "#B5EAD7", "#C7CEEA"
PASTEL_MAP = [C_AZUL, C_ROSA, C_LILA, C_VERD, C_AMAR]

# %% --- CARGA Y LIMPIEZA PROFUNDA ---
# Cargo solo lo que sirve para no matar la memoria
df_plans = pd.read_csv("dataset/PlanAttributes.csv", low_memory=False)
df_rates = pd.read_csv("dataset/Rate.csv", low_memory=False)

# Limpieza de strings a números (Deducibles y Primas)
def to_num(s):
    return pd.to_numeric(str(s).replace('$', '').replace(',', '').replace('%', ''), errors='coerce')

df_plans['Ded'] = to_num(df_plans['TEHBDedInnTier1Individual'])
df_rates['Rate'] = to_num(df_rates['IndividualRate'])

# Estandarizo Edad: Quito "Family Option" y convierto rangos a enteros
df_rates['Age_Int'] = df_rates['Age'].replace({'0-14': 14, '64 and over': 65}).apply(pd.to_numeric, errors='coerce')
df_rates = df_rates.dropna(subset=['Age_Int', 'Rate'])

# Merge clave: Unimos por Plan, Año y Estado
df = pd.merge(df_plans[['PlanId', 'BusinessYear', 'StateCode', 'MetalLevel', 'IssuerActuarialValue', 'Ded']], 
              df_rates[['PlanId', 'BusinessYear', 'StateCode', 'Age_Int', 'Tobacco', 'Rate']], 
              on=['PlanId', 'BusinessYear', 'StateCode'])

# Filtro actuarial: Quito outliers (Primas > $2000 o $0 no tienen sentido aquí)
df = df[(df['Rate'] > 0) & (df['Rate'] < df['Rate'].quantile(0.98))].dropna()

# %% --- VARIABLES DERIVADAS (Lo que le da el toque pro) ---

# 1. Grupo Etario (Categórica)
df['Grupo_Edad'] = pd.cut(df['Age_Int'], bins=[0, 30, 55, 100], labels=['Joven', 'Adulto', 'Senior'])

# 2. Costo por Cobertura (Numérica Continua)
# Cuánto cuesta cada 1% de valor actuarial que el plan cubre
df['Costo_por_AV'] = df['Rate'] / (df['IssuerActuarialValue'] * 100)

# 3. Dummy de Riesgo Elevado (Binaria)
# Si el plan tiene deducible bajo y es fumador, es un perfil de alto riesgo
df['High_Risk_Profile'] = ((df['Ded'] < 1000) & (df['Tobacco'] == 'Tobacco User')).astype(int)

# %% --- VISUALIZACIONES (Matplotlib Puro) ---

fig, axs = plt.subplots(3, 2, figsize=(15, 18), facecolor='white')
fig.suptitle('Dashboard de Análisis Actuarial - Marketplace Salud', fontsize=20, fontweight='bold', color='#333')

def set_border_radius(ax):
    """Limpia los bordes para un look moderno"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_facecolor('#F9F9F9')

# 1. PIE: Distribución de Planes
data_pie = df['MetalLevel'].value_counts()
axs[0, 0].pie(data_pie, labels=data_pie.index, autopct='%1.1f%%', colors=PASTEL_MAP, 
              wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axs[0, 0].set_title('Planes por Nivel de Metal', pad=20)

# 2. BARRAS: Prima Promedio por Edad
age_means = df.groupby('Grupo_Edad')['Rate'].mean()
axs[0, 1].bar(age_means.index, age_means.values, color=C_VERD, edgecolor='#777', linewidth=0.8)
axs[0, 1].set_title('Tarifa Mensual vs Ciclo de Vida')
axs[0, 1].set_ylabel('USD ($)')

# 3. HISTOGRAMA: Deducibles
axs[1, 0].hist(df['Ded'], bins=30, color=C_AZUL, edgecolor='white')
axs[1, 0].set_title('Frecuencia de Deducibles (Retención de Riesgo)')
axs[1, 0].set_xlabel('Monto Deducible')

# 4. BOXPLOT: Tabaco (Hecho a mano con Matplotlib)
tobacco_data = [df[df['Tobacco'] == 'No Tobacco Use']['Rate'], df[df['Tobacco'] == 'Tobacco User']['Rate']]
bp = axs[1, 1].boxplot(tobacco_data, patch_artist=True, labels=['No Fumador', 'Fumador'])
for patch, color in zip(bp['boxes'], [C_LILA, C_ROSA]):
    patch.set_facecolor(color)
axs[1, 1].set_title('Impacto del Tabaquismo en la Prima')

# 5. LÍNEAS: Inflación Médica (Tendencia Anual)
trend = df.groupby('BusinessYear')['Rate'].mean()
axs[2, 0].plot(trend.index, trend.values, marker='o', color=C_ROSA, linewidth=3, markersize=8)
axs[2, 0].set_title('Evolución Temporal de la Tarifa')
axs[2, 0].set_xticks(trend.index)

# 6. SCATTER: Deducible vs Prima (Relación Técnica)
# Uso alpha para ver densidad de puntos
axs[2, 1].scatter(df['Ded'], df['Rate'], alpha=0.1, color=C_LILA, s=10)
axs[2, 1].set_title('Correlación: Deducible vs Tarifa')
axs[2, 1].set_xlabel('Deducible')
axs[2, 1].set_ylabel('Prima')

for ax in axs.flat: set_border_radius(ax)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# %% [markdown]
# ### CONCLUSIONES RÁPIDAS (Para el video)
# 1. El mercado está concentrado en niveles Silver (70% de AV), buscando el subsidio fiscal.
# 2. La edad es un factor multiplicador: el riesgo Senior se tarifa 3 veces más caro que el Joven.
# 3. Existe una correlación negativa clara entre deducible y prima: a mayor retención propia, menor costo mensual.
