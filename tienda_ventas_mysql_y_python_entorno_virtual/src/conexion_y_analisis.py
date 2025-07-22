'''
Importar las librerías después de haberlas instalado:
- pip install sqlalchemy --> Para conectar con las bases de datos usando SQLAlchemy
- pip install mysql-connector-python --> Driver MySQL para SQLAlchemy
- pip install pandas --> Para la manipulación de los datos
- pip install seaborn --> seaborn es una biblioteca basada en matplotlib que genera gráficos más elegantes.
- pip install matplotlib --> Para generar gráficos
- pip install python-dotenv --> Para cargar variables de entorno desde un archivo .env
'''

# Librerías
from sqlalchemy import create_engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv  # Para cargar variables de entorno
import os  # Para acceder a variables de entorno


def conectar_bd():
    '''
    Intenta crear un motor de conexión con SQLAlchemy y devuelve el motor si tiene éxito.
    Si falla, imprime el error y devuelve None.
    Usa variables de entorno para configurar la conexión.
    '''
    load_dotenv()  # Cargar variables de entorno desde el archivo .env
    try:
        engine = create_engine(
            f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        )
        print('Conexión exitosa a la base de datos')
        return engine
    except Exception as e:
        print(f'Error al conectar: {e}')
        return None


def ejecutar_consulta(engine, query):
    '''
    Ejecuta una consulta SQL y devuelve los resultados como un DataFrame de pandas.
    Si ocurre un error, imprime el mensaje y devuelve None.
    '''
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f'Error al ejecutar la consulta: {e}')
        return None


def validar_datos(df):
    '''
    Valida que el DataFrame no esté vacío y contenga las columnas necesarias ('cantidad', 'precio_unitario').
    Devuelve True si los datos son válidos, False si no lo son.
    '''
    if df.empty:
        print("Error: El DataFrame está vacío.")
        return False
    if 'cantidad' not in df.columns or 'precio_unitario' not in df.columns:
        print("Error: Faltan columnas necesarias ('cantidad', 'precio_unitario').")
        return False
    return True


def calcular_totales(df):
    '''
    Calcula el precio total por producto y el total gastado por cliente.
    Devuelve un DataFrame con el total gastado por cliente.
    Si ocurre un error, imprime el mensaje y devuelve None.
    '''
    try:
        # Validar los datos antes de calcular
        if not validar_datos(df):
            return None

        # Calcular el precio total multiplicando cantidad por precio unitario
        df['precio_total'] = df['cantidad'] * df['precio_unitario']
        # Calcular el total gastado por cliente
        total_por_cliente = df.groupby('cliente')['precio_total'].sum().reset_index()
        # Mostrar resultados
        return total_por_cliente
    except KeyError as e:
        print(f'Error en los datos: falta la columna {e}')
        return None


def generar_grafico(total_por_cliente):
    '''
    Genera un gráfico de barras del total gastado por cliente usando Seaborn.
    '''
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x='cliente',
            y='precio_total',
            data=total_por_cliente,
            palette='Blues_d',
            hue='cliente',  # Asignar 'cliente' a hue. Indica que las categorías (clientes) deben ser representadas por diferentes colores.
            legend=False  # Desactivar la leyenda. Evita que aparezca una leyenda redundante, ya que todos los valores de x son únicos.
        )
        plt.title('Total gastado por el cliente', fontsize=16)
        plt.xlabel('Cliente', fontsize=12)
        plt.ylabel('Total gastado (€)', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f'Error al generar gráfico: {e}')


'''
El bloque if __name__ == "__main__": actúa como una condición que verifica si el archivo
está siendo ejecutado directamente o importado como módulo.
'''
if __name__ == '__main__':
    # Conectar a la base de datos
    engine = conectar_bd()

    if engine:
        try:
            # Consulta de prueba: ver pedidos
            query = 'SELECT * FROM pedidos;'
            df_pedidos = ejecutar_consulta(engine, query)
            if df_pedidos is not None:
                print('\nPedidos:')
                print(df_pedidos)

            # Consulta avanzada: unir tablas
            query = """
            SELECT
                p.id_pedido,
                c.nombre AS cliente,
                pr.nombre AS producto,
                dp.cantidad,
                pr.precio_unitario
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            JOIN detalles_pedido dp ON p.id_pedido = dp.id_pedido
            JOIN productos pr ON dp.id_producto = pr.id_producto;
            """
            df = ejecutar_consulta(engine, query)
            if df is not None:
                print('\nDatos combinados:')
                print(df)

                # Calcular totales
                total_por_cliente = calcular_totales(df)
                if total_por_cliente is not None:
                    print('\nTotal gastado por cliente:')
                    print(total_por_cliente)

                    # Crear la carpeta resultados si no existe
                    os.makedirs("resultados", exist_ok=True)
                    # Guardar resultados en un archivo CSV
                    total_por_cliente.to_csv('resultados/total_por_cliente.csv', index=False)
                    print("\nResultados guardados en: 'resultados/total_por_cliente.csv.'")

                    # Generar gráfico
                    generar_grafico(total_por_cliente)
        finally:
            # Cerrar el motor de conexión
            engine.dispose()
            print("\nMotor de conexión cerrado.")
