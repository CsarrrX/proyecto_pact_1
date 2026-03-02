# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as patches
from matplotlib.ticker import PercentFormatter

# Carga de datos y preparación
dataset = pd.read_csv("states_processed.csv")
dataset['State'] = dataset['State'].str.strip()

# Diccionario para mapear los nombres de los estados a sus abreviaturas de 2 letras
us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}
dataset['State_Abbrev'] = dataset['State'].map(us_state_to_abbrev)

# %%
# ----------------- VISUALIZACIÓN 1: TASA DE NO ASEGURADOS (BARRAS) ----------------- #
dataset_sorted = dataset.sort_values('Uninsured Rate (2015)', ascending=False)
plt.figure(figsize=(15, 6))

media_uninsured = dataset['Uninsured Rate (2015)'].mean()
colores1 = ['red' if x > media_uninsured else '#1f77b4' for x in dataset_sorted['Uninsured Rate (2015)']]

plt.bar(dataset_sorted['State'], dataset_sorted['Uninsured Rate (2015)'], color=colores1, alpha=0.8)
plt.axhline(y=media_uninsured, color='red', linestyle='--', linewidth=2, label=f'Media Nacional ({media_uninsured:.1%})')

plt.title('Tasa de Personas sin Seguro en 2015 por Estado (Rojo = Sobre la Media)', fontsize=16)
plt.ylabel('Tasa de Personas sin Seguro (%)', fontsize=12)
plt.xticks(rotation=90, fontsize=8)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.legend()
plt.tight_layout()

# Guardar figura
nombre_fig1 = '01_Tasa_No_Asegurados_2015_Riesgo.png'
plt.savefig(nombre_fig1, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - FIGURA 1:")
print("La gráfica muestra la penetración de mercado y el riesgo de anti-selección potencial.")
print("Los estados en rojo (ej. Texas, Alaska) mantienen altas tasas de población sin seguro,")
print("lo que sugiere un 'pool' de riesgo comercial más pequeño y una alta carga para la red")
print("de salud pública por atenciones no compensadas (uncompensated care).")
print("="*80 + "\n")


# %%
# ----------------- VISUALIZACIÓN 2: DEPENDENCIA DE SUBSIDIOS (DISPERSIÓN) ----------------- #
plt.figure(figsize=(15, 6))
Q1 = dataset['Subsidy Dependence Ratio'].quantile(0.25)
Q3 = dataset['Subsidy Dependence Ratio'].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR

colores2 = ['#d62728' if x < limite_inferior else '#2ca02c' for x in dataset['Subsidy Dependence Ratio']]

plt.scatter(dataset['State'], dataset['Subsidy Dependence Ratio'], c=colores2, s=100, alpha=0.8)
plt.axhline(y=limite_inferior, color='#d62728', linestyle='--', label=f'Límite Inferior ({limite_inferior:.2f})')

plt.title('Ratio de Dependencia de Subsidios en el Mercado Privado (Outliers en Rojo)', fontsize=16)
plt.ylabel('Proporción de Personas c/ Subsidio', fontsize=12)
plt.xticks(rotation=90, fontsize=8)
plt.legend()
plt.tight_layout()

# Guardar figura
nombre_fig2 = '02_Dependencia_Subsidios_MercadoPrivado.png'
plt.savefig(nombre_fig2, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - FIGURA 2:")
print("Evaluación de la sensibilidad tarifaria de la cartera. La mayoría de los estados")
print("tienen entre un 80% y 90% de sus asegurados dependiendo de subsidios federales.")
print("Desde la perspectiva de fijación de primas (pricing), esto significa que el mercado")
print("es altamente elástico: un recorte en los créditos fiscales gubernamentales provocaría")
print("una espiral de muerte (death spiral) inmediata, donde solo los riesgos más enfermos")
print("se quedarían pagando la póliza completa. Los outliers en rojo tienen un riesgo menor de este fenómeno.")
print("="*80 + "\n")


# %%
# ----------------- VISUALIZACIÓN 3: MAPA DE REDUCCIÓN DE NO ASEGURADOS ----------------- #
state_coords = {
    'AK': (0, 7),                                                                                             'ME': (11, 7),
    'WA': (1, 6), 'ID': (2, 6), 'MT': (3, 6), 'ND': (4, 6), 'MN': (5, 6), 'IL': (6, 6), 'WI': (7, 6), 'MI': (8, 6), 'NY': (9, 6), 'VT': (10, 6), 'NH': (11, 6),
    'OR': (1, 5), 'NV': (2, 5), 'WY': (3, 5), 'SD': (4, 5), 'IA': (5, 5), 'IN': (6, 5), 'OH': (7, 5), 'PA': (8, 5), 'NJ': (9, 5), 'CT': (10, 5), 'MA': (11, 5),
    'CA': (1, 4), 'UT': (2, 4), 'CO': (3, 4), 'NE': (4, 4), 'MO': (5, 4), 'KY': (6, 4), 'WV': (7, 4), 'MD': (8, 4), 'DE': (9, 4), 'RI': (10, 4),
    'AZ': (2, 3), 'NM': (3, 3), 'KS': (4, 3), 'AR': (5, 3), 'TN': (6, 3), 'VA': (7, 3), 'NC': (8, 3),
    'OK': (4, 2), 'LA': (5, 2), 'MS': (6, 2), 'AL': (7, 2), 'SC': (8, 2), 'DC': (9, 2),
    'HI': (0, 1), 'TX': (4, 1), 'GA': (7, 1),
    'FL': (8, 0)
}

fig, ax = plt.subplots(figsize=(14, 8))
cmap = plt.cm.RdYlGn 

norm = mcolors.Normalize(vmin=dataset['Uninsured Rate Change (2010-2015)'].min(), 
                         vmax=dataset['Uninsured Rate Change (2010-2015)'].max())

for index, row in dataset.iterrows():
    abbrev = row['State_Abbrev']
    if abbrev in state_coords:
        x, y = state_coords[abbrev]
        val = row['Uninsured Rate Change (2010-2015)']
        color = cmap(1 - norm(val)) 
        
        rect = patches.Rectangle((x-0.4, y-0.4), 0.8, 0.8, linewidth=1, edgecolor='white', facecolor=color)
        ax.add_patch(rect)
        
        text_color = 'white' if (1 - norm(val)) > 0.7 or (1 - norm(val)) < 0.3 else 'black'
        ax.text(x, y, f"{abbrev}\n{val:.1%}", ha='center', va='center', color=text_color, fontsize=9, fontweight='bold')

ax.set_xlim(-1, 12)
ax.set_ylim(-1, 8)
ax.axis('off')
plt.title('Mapa Actuarial: Reducción en la Tasa de No Asegurados (2010-2015)\n(Verde Oscuro = Mayor Reducción de Riesgo Social)', fontsize=16)

sm = plt.cm.ScalarMappable(cmap=cmap.reversed(), norm=norm)
cbar = fig.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.03, pad=0.04)
cbar.set_label('Cambio en % de Personas sin Seguro')
cbar.ax.xaxis.set_major_formatter(PercentFormatter(1))

plt.tight_layout()

# Guardar figura
nombre_fig3 = '03_Mapa_Reduccion_No_Asegurados_2010_2015.png'
plt.savefig(nombre_fig3, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - FIGURA 3:")
print("Mapa de calor del desempeño en la estabilización de los 'pools' de riesgo estatal.")
print("Los estados en verde oscuro lograron diluir el riesgo atrayendo a personas más sanas")
print("al sistema (Ley de Grandes Números). Los estados en rojo tuvieron el menor impacto,")
print("manteniendo una concentración de morbilidad posiblemente más alta. Este efecto suele")
print("estar directamente correlacionado con la decisión gubernamental de expandir Medicaid.")
print("="*80 + "\n")

# %%
# ----------------- VISUALIZACIÓN 4: DISTRIBUCIÓN DEL RIESGO PÚBLICO VS PRIVADO (BOXPLOT) -----------------
# Separamos los estados en dos grupos: los que expandieron Medicaid y los que no
expansion_true = dataset[dataset['State Medicaid Expansion (2016)'] == True]['Public vs Private Risk Index'].dropna()
expansion_false = dataset[dataset['State Medicaid Expansion (2016)'] == False]['Public vs Private Risk Index'].dropna()

plt.figure(figsize=(10, 6))

# Creamos el Boxplot
caja = plt.boxplot([expansion_true, expansion_false], tick_labels=['Sí (Expandió)', 'No (No Expandió)'], 
                   patch_artist=True, widths=0.4)

# Colores y estilo
for box in caja['boxes']:
    box.set_facecolor('#1f77b4')
    box.set_alpha(0.7)
plt.setp(caja['medians'], color='red', linewidth=2)

# Añadimos los puntos individuales (jitter/scatter) para que se vean todos los estados
for i, d in enumerate([expansion_true, expansion_false]):
    y = d
    x = np.random.normal(i + 1, 0.04, size=len(y))
    plt.plot(x, y, 'ro', alpha=0.6, markersize=5, label='Estados individuales' if i==0 else "")

plt.title('Distribución del Índice de Riesgo (Público vs Privado)\nSegún Expansión de Medicaid', fontsize=15)
plt.ylabel('Índice (Asegurados Públicos / Asegurados Privados)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Evitar duplicados en la leyenda
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

plt.tight_layout()

# Guardar figura
nombre_fig4 = '04_Distribucion_Riesgo_Medicaid.png'
plt.savefig(nombre_fig4, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - FIGURA 4:")
print("Analiza cómo la política estatal altera la composición de la cartera de riesgo.")
print("Un índice de 1 significa que hay 1 asegurado público por cada asegurado privado.")
print("Los estados que expandieron Medicaid (izquierda) tienen cajas estadísticamente más altas")
print("y dispersas, asumiendo una mayor carga de riesgo gubernamental. Los que no expandieron")
print("mantienen el peso del riesgo principalmente en el sector comercial (primas de empleadores).")
print("="*80 + "\n")


# %%
# ----------------- VISUALIZACIÓN 5: RIESGO FINANCIERO FEDERAL (BARRAS HORIZONTALES) -----------------
# Tomamos el Top 15 de los estados que más dinero en subsidios consumen
top_15_gasto = dataset.sort_values('Annual Tax Credit Expenditure', ascending=False).head(15)

plt.figure(figsize=(12, 7))

# Gráfico de barras horizontales (se invierten [::-1] para que el mayor quede arriba)
barras = plt.barh(top_15_gasto['State'][::-1], top_15_gasto['Annual Tax Credit Expenditure'][::-1] / 1e9, 
                  color='#ff7f0e', edgecolor='black', alpha=0.85)

plt.title('Top 15 Estados con Mayor Gasto Anual en Subsidios (Riesgo Financiero)', fontsize=15)
plt.xlabel('Gasto Anual Estimado (En Miles de Millones / Billions de USD)', fontsize=12)
plt.ylabel('Estado', fontsize=12)

# Formato del eje X en Billones de dólares
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Añadir el número exacto al final de cada barra
for bar in barras:
    width = bar.get_width()
    plt.text(width + 0.05, bar.get_y() + bar.get_height()/2, f"${width:.1f}B", 
             va='center', ha='left', fontsize=10, fontweight='bold')

plt.xlim(0, max(top_15_gasto['Annual Tax Credit Expenditure']/1e9) * 1.15)
plt.tight_layout()

# Guardar figura
nombre_fig5 = '05_Gasto_Subsidios_Top15.png'
plt.savefig(nombre_fig5, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - FIGURA 5:")
print("Mide la exposición de riesgo del erario público. Vemos cómo estados altamente")
print("poblados como Florida y California concentran miles de millones de dólares en")
print("créditos fiscales anuales. Desde el punto de vista del reaseguro o de las aseguradoras")
print("locales, estos mercados son inmensamente rentables pero están sujetos a un alto")
print("'riesgo regulatorio': si el gobierno federal recorta fondos, estos mercados podrían colapsar.")
print("="*80 + "\n")


# %%
# ----------------- VISUALIZACIÓN 6: COMPOSICIÓN DE MERCADO (BARRAS 100% APILADAS) -----------------
# Elegimos los 10 estados más poblados/asegurados para ver de qué está compuesto su mercado
top_10_states = dataset.sort_values('Total Insured Approx', ascending=False).head(10)

# Las 4 columnas que sumaremos para el 100%
cols = ['Employer Health Insurance Coverage (2015)', 'Marketplace Health Insurance Coverage (2016)', 
        'Medicare Enrollment (2016)', 'Medicaid Enrollment (2016)']

labels = ['Sector Privado (Empleador)', 'Sector Privado (Marketplace)', 'Sector Público (Medicare - Edad)', 'Sector Público (Medicaid - Ingreso)']
colors = ['#2ca02c', '#d62728', '#1f77b4', '#9467bd']

fig, ax = plt.subplots(figsize=(12, 7))

# Variable para ir apilando las barras
bottom = np.zeros(len(top_10_states))
states = top_10_states['State'].tolist()

for i, col in enumerate(cols):
    # Porcentaje que representa esa columna respecto al total asegurado del estado
    percentages = top_10_states[col] / top_10_states['Total Insured Approx']
    ax.bar(states, percentages, bottom=bottom, label=labels[i], color=colors[i], edgecolor='white', alpha=0.9)
    bottom += percentages

ax.set_title('Composición de la Cartera (Market Share) - Top 10 Estados Más Poblados', fontsize=15)
ax.set_ylabel('Porcentaje de la Población Asegurada (100%)', fontsize=12)

# Mover la leyenda afuera de la gráfica para no tapar los datos
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

# Línea del 50% como referencia
ax.axhline(0.5, color='black', linestyle='--', linewidth=2, alpha=0.8)
ax.text(9.5, 0.51, 'Marca del 50%', fontweight='bold', ha='right')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Guardar figura
nombre_fig6 = '06_Composicion_Mercado_Apiladas.png'
plt.savefig(nombre_fig6, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - FIGURA 6:")
print("Analiza la diversificación de fuentes de cobertura para estimar estabilidad de primas.")
print("El color verde (Empleador) es el riesgo más estable y rentable, que domina más del 50%")
print("del mercado en todos los estados. El bloque púrpura (Medicaid) varía enormemente;")
print("en estados como Nueva York o California ocupa una enorme porción de su cartera, mientras")
print("que en Texas es significativamente más bajo, lo que indica distintas prioridades de tarificación.")
print("="*80 + "\n")

# %%
# ----------------- VISUALIZACIÓN 7: GRÁFICO DE PASTEL (PIE CHART) -----------------
# Calculamos el total nacional sumando la población de todos los estados en cada rubro
cols_pie = [
    'Employer Health Insurance Coverage (2015)',
    'Medicaid Enrollment (2016)',
    'Medicare Enrollment (2016)',
    'Marketplace Health Insurance Coverage (2016)'
]
totales_nacionales = dataset[cols_pie].sum()

labels_pie = ['Sector Privado\n(Empleador)', 'Sector Público\n(Medicaid)', 'Sector Público\n(Medicare)', 'Sector Privado\n(Marketplace)']
colores_pie = ['#2ca02c', '#9467bd', '#1f77b4', '#d62728']

# "Explode" separa una rebanada para destacarla (en este caso el Marketplace)
explode = (0.05, 0.05, 0.05, 0.15)  

plt.figure(figsize=(9, 9))
plt.pie(totales_nacionales, labels=labels_pie, colors=colores_pie, autopct='%1.1f%%', 
        startangle=140, explode=explode, shadow=True, textprops={'fontsize': 12, 'fontweight': 'bold'})

plt.title('Distribución de Asegurados a Nivel Nacional (Mercado Total)', fontsize=16)
plt.tight_layout()

nombre_fig7 = '07_Pastel_Mercado_Nacional.png'
plt.savefig(nombre_fig7, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - GRÁFICO DE PASTEL:")
print("Este gráfico resume el 'Market Share' agregado de los Estados Unidos. A nivel macro,")
print("el sistema se sostiene gracias a las pólizas corporativas (Empleadores, >50%), que inyectan")
print("dinero privado al sistema. Destacamos la rebanada roja (Marketplace), ya que, aunque")
print("es la porción más pequeña del mercado, es la más volátil, la que consume más")
print("subsidios directos y la que genera los mayores retos de tarificación individual.")
print("="*80 + "\n")


# %%
# ----------------- VISUALIZACIÓN 8: HISTOGRAMA -----------------
# Vemos cómo se distribuyen los 52 estados según su tasa de no asegurados
plt.figure(figsize=(10, 6))

# Creamos el histograma con 12 "canastas" (bins)
counts, bins, patches = plt.hist(dataset['Uninsured Rate (2015)'], bins=12, 
                                 color='#17becf', edgecolor='black', alpha=0.8)

media_nacional = dataset['Uninsured Rate (2015)'].mean()
plt.axvline(media_nacional, color='red', linestyle='dashed', linewidth=2, 
            label=f'Media de Estados ({media_nacional:.1%})')

plt.title('Histograma: Distribución de la Tasa de No Asegurados (2015)', fontsize=15)
plt.xlabel('Tasa de Personas sin Seguro (%)', fontsize=12)
plt.ylabel('Frecuencia (Cantidad de Estados)', fontsize=12)

# Formatear el eje X a porcentaje
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
nombre_fig8 = '08_Histograma_No_Asegurados.png'
plt.savefig(nombre_fig8, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - HISTOGRAMA:")
print("El histograma revela la 'Forma de la Distribución' del riesgo país. Vemos una clara")
print("asimetría hacia la izquierda (sesgo positivo). La mayoría de los estados (la campana más alta)")
print("han logrado concentrar sus tasas de no asegurados entre el 5% y el 10%. Sin embargo, la")
print("larga 'cola' hacia la derecha nos advierte de estados atípicos con problemas sistémicos")
print("graves, superando el 15% de desprotección. Esta es una distribución no normal típica en siniestralidad.")
print("="*80 + "\n")


# %%
# ----------------- VISUALIZACIÓN 9: GRÁFICO DE LÍNEAS -----------------
# Seleccionamos el Top 5 de estados con mayor volumen para ver su evolución temporal
top_5 = dataset.sort_values('Total Insured Approx', ascending=False).head(5)

plt.figure(figsize=(10, 6))

años = ['2010', '2015']
marcadores = ['o', 's', '^', 'D', 'v']

for i, (_, row) in enumerate(top_5.iterrows()):
    valores = [row['Uninsured Rate (2010)'], row['Uninsured Rate (2015)']]
    plt.plot(años, valores, marker=marcadores[i], markersize=8, linewidth=2.5, label=row['State'])

plt.title('Evolución (Tendencia) de la Tasa de No Asegurados (2010 vs 2015)\nTop 5 Estados de Mayor Volumen', fontsize=15)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Tasa de Personas sin Seguro (%)', fontsize=12)

plt.legend(title='Estado', title_fontsize='12', fontsize='11', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
nombre_fig9 = '09_Lineas_Evolucion_Top5.png'
plt.savefig(nombre_fig9, dpi=300)
plt.show()

print("\n" + "="*80)
print("INTERPRETACIÓN ACTUARIAL - GRÁFICO DE LÍNEAS:")
print("Evaluamos la 'Tendencia Histórica' (Trend). Todas las líneas tienen una pendiente negativa,")
print("confirmando que las reformas de salud (como el ACA) lograron su objetivo primordial")
print("en los macro-mercados. Actuarialmente, una caída tan drástica en 5 años (como la de California)")
print("implica un ingreso masivo de vidas nuevas al 'pool'. Estas vidas nuevas suelen traer")
print("morbilidad desconocida o 'demanda reprimida' de servicios, lo que encarece las pólizas")
print("en el corto plazo antes de estabilizarse.")
print("="*80 + "\n")
