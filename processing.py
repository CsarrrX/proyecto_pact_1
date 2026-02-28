# %%
import pandas as pd 
import numpy as np 
import matplotlib as plt 

# %% [markdown]
#
#    # Análisis de Seguros de Salud y Planes Dentales (Marketplace US)
#
#    El presente proyecto se fundamenta en los datos abiertos del Health Insurance Marketplace de Estados Unidos. Aunque el dataset original proveía una base de datos procesada en SQL, se tomó la determinación de trabajar directamente con los archivos fuente en formato CSV. Esta decisión permite demostrar un ciclo completo de ciencia de datos, desde la ingesta de datos crudos hasta la limpieza y el modelado actuarial.
#
#    ## Estructura del Dataset Original
#
#    El ecosistema de datos se compone de seis archivos principales que detallan la oferta de planes individuales y para pequeñas empresas:
#
#    1. BenefitsCostSharing.csv: Detalle de copagos, coseguros y límites de beneficios.
#    2. PlanAttributes.csv: Características técnicas del diseño del plan y valores actuariales.
#    3. Rate.csv: Tablas de primas y costos mensuales por edad y ubicación.
#    4. BusinessRules.csv: Reglas operativas y de elegibilidad.
#    5. Network.csv: Identificadores de las redes de proveedores médicos.
#    6. ServiceArea.csv: Definiciones geográficas de cobertura a nivel condado.
#
#    ---
#
#    ## Criterios de Selección y Reducción de Dimensionalidad
#
#    Para optimizar el análisis y garantizar la relevancia estadística de los resultados, se aplicó una estrategia de filtrado sobre las fuentes de información:
#
#    ### Exclusión de Tablas Transaccionales y Administrativas
#
#    Se decidió no integrar los archivos *BusinessRules.csv*, *Network.csv* y *ServiceArea.csv* debido a que su contenido es primordialmente descriptivo o administrativo. En un contexto de análisis de riesgo y tarificación, estas tablas presentan una baja varianza explicativa:
#
#    * Las reglas de negocio suelen ser constantes legales que no impactan directamente en la modelación de la siniestralidad.
#    * La información geográfica detallada ya se encuentra capturada de forma agregada en la variable *StateCode* de las tablas principales.
#    * Los nombres de las redes operativas funcionan como etiquetas de mercadeo sin un peso numérico directo en la estructura de costos.
#
#    ### Consolidación de Variables en Tablas Principales
#
#    En las tablas seleccionadas (*BenefitsCostSharing*, *PlanAttributes* y *Rate*), se realizó una limpieza profunda para eliminar la redundancia:
#
#    * Selección de Variables de Exposición: Se priorizaron las variables de *Total Essential Health Benefit (TEHB)* sobre los desgloses individuales para evitar la colinealidad.
#    * Enfoque Individual: Se descartaron las métricas de grupos familiares para estandarizar la comparación de primas y deducibles sobre una unidad de riesgo uniforme: *el individuo*.
#    * Calidad de la Información: Se eliminaron columnas con una tasa de valores nulos superior al 80%, asegurando que cada variable incluida aporte información robusta al análisis final.

# %%
# Definimos columnas de interés
CostShare_cols = ["PlanId", "BusinessYear", "StateCode", "BenefitName", "CopayInnTier1", "CoinsInnTier1", "IsCovered"]
Rate_cols = ["PlanId", "BusinessYear", "StateCode", "RatingAreaId", "Age", "Tobacco", "IndividualRate"] 
Plan_cols = ["PlanId", "BusinessYear", "StateCode", "MetalLevel", "PlanType", "IssuerActuarialValue", "TEHBDedInnTier1Individual", "TEHBInnTier1IndividualMOOP"]

# Limpieza de datos utilizables
CostShare_df = pd.read_csv("dataset/BenefitsCostSharing.csv", usecols=CostShare_cols) 
Rate_df = pd.read_csv("dataset/Rate.csv", usecols=Rate_cols) 
Plan_Attributes_df = pd.read_csv("dataset/PlanAttributes.csv", usecols=Plan_cols) 

