import pandas as pd

'''
Antes de cargar el archivo, tuve que instalar 'openpyxl' (pip install openpyxl)
para poder cargar el archivo .xlsx
'''

# 1) Carga del archivo Excel original
df = pd.read_excel('datos/ventas_raw.xlsx')

# 2) Revisar información general
print('\nVista general del archivo')
print(df.info())
print(df.head())

# 3) Asegurarse de que la fecha esté en formato datetime
df['Fecha de Venta'] = pd.to_datetime(df['Fecha de Venta'], errors='coerce')
# errors='coerce' reemplaza con NaT (Not a Time) si encuentra un valor que no se puede convertir a fecha

# ** Esto siguiente sirve para hacer limpieza de valores nulos (aunque en esta tabla no los hay)
filas_originales = len(df)
print(f'\nTotal de filas originales {filas_originales}')
print('\nValores nulos por columna:')
print(df[['Fecha de Venta', 'Unidades', 'Precio Unitario']].isnull().sum())

# 4) Eliminar filas con fechas inválidas o valores nulos
df = df.dropna(subset=['Fecha de Venta', 'Unidades', 'Precio Unitario'])
# df.dropna() es una función de pandas que elimina filas que tienen valores nulos (NaN o NaT).
# subset= es para especificar en qué columnas eliminar estos valores nulos

filas_despues_nulos = len(df)
eliminadas_por_nulos = filas_originales - filas_despues_nulos
print(f'\nFilas eliminadas por valores nulos: {eliminadas_por_nulos}')  # **

# 5) Eliminar posibles duplicados
df = df.drop_duplicates()
'''
df.drop_duplicates():
Es una función que elimina filas duplicadas (iguales en todas las columnas)
No necesita argumentos para funcionar, pero se puede usar subset=['col1', 'col2']
si se quisiera eliminar duplicados solo basados en ciertas columnas.
'''

filas_finales = len(df)
eliminadas_por_duplicados = filas_despues_nulos - filas_finales
print(f"\nFilas eliminadas por duplicados: {eliminadas_por_duplicados}")
print(f"\nTotal de filas finales: {filas_finales}")

# 6) Recalcular el total (por seguridad)
df['Total'] = (df['Unidades'] * df['Precio Unitario']).round(2)  # Redondea a 2 decimales

# 7. Guardar archivo limpio
df.to_excel('datos/ventas_limpias.xlsx', index=False)
'''
index=False:
Cuando se guarda un DataFrame en Excel, pandas por defecto incluye la columna del índice
(esa columna que numera las filas: 0, 1, 2, 3, …).
- Si NO se pone index=False, el archivo Excel incluirá una columna extra con esos números como si fuera una columna más.
- Si SÍ se pone index=False, esa columna del índice no se guarda y el Excel se ve solo con las columnas reales.
'''

print("\n✅ Archivo limpio guardado como 'ventas_limpias.xlsx'")
