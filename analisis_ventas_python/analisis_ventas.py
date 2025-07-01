import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sales_data_sample.csv', encoding='latin1')
# Visualizar las primeras 5 filas
print(df.head())
# Información general de la base de datos
print(df.info())
# Estadísticas
print(df.describe())

# Convertir la columna ORDERDATE a formato de fecha (datetime)
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
print(df['ORDERDATE'])

# Extraer año y mes (aunque ya existen YEAR_ID y MONTH_ID)
df['AÑO'] = df['ORDERDATE'].dt.year
df['MES'] = df['ORDERDATE'].dt.month
df['DIA'] = df['ORDERDATE'].dt.day
'''
    - .dt significa: "quiero acceder a partes de una fecha".
    - Funciona solo si la columna es de tipo fecha (datetime64).
    - Es muy útil para crear nuevas columnas y agrupar por mes, año, día, etc.
'''

print(df[['ORDERDATE', 'AÑO', 'MES', 'DIA']].head())

# Agrupar y sumar ventas por año
ventas_por_anio = df.groupby('AÑO')['SALES'].sum()
print(ventas_por_anio)
# Visualizar las ventas por AÑO con gráfico de barras
ventas_por_anio.plot(kind='bar', title='Ventas totales por Año', color='skyblue')
plt.ylabel('Total Ventas (€)')
plt.xlabel('AÑO')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Agrupar y sumar ventas por mes
ventas_por_mes = df.groupby('MES')['SALES'].sum()
print(ventas_por_mes)
# Visualizar las ventas por MES con gráfico de barras
ventas_por_mes.plot(kind='bar', title='Ventas Totales por Mes', color='orange')
plt.ylabel('Total Ventas (€)')
plt.xlabel('MES')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Análisis por líneas de producto (PRODUCTLINE)
ventas_por_producto = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False)
print(ventas_por_producto)
# Gráfico tipo barra
ventas_por_producto.plot(kind='bar', title='Ventas por Línea de Productos', color='mediumseagreen')
plt.ylabel('Total Ventas (€)')
plt.xlabel('LÍNEA DE PRODUCTO')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Ventas por país (COUNTRY)
ventas_por_pais = df.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=False)
print(ventas_por_pais)
# Gráfico tipo barra
ventas_por_pais.head(10).plot(kind='bar', title='Top 10 países por ventas', color='cornflowerblue')
plt.ylabel('Total Ventas (€)')
plt.xlabel('PAÍS')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Análisis de ventas por tamaño de cliente (DEALSIZE)
ventas_por_tamanio = df.groupby('DEALSIZE')['SALES'].sum().sort_values(ascending=False)
print(ventas_por_tamanio)
# Gráfico tipo barra
ventas_por_tamanio.plot(kind='bar', title='Ventas por Tamaño de Cliente', color='tomato')
plt.ylabel('Total Ventas (€)')
plt.xlabel('TAMAÑO DE CLIENTE')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
