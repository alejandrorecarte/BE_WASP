import pymysql
import os
import time
import logging
from controllers.exceptions import DbException
from fastapi import Depends

# Configuración del logger
logger = logging.getLogger(__name__)

def establish_connection():
    """
    Establece la conexión a la base de datos con reintentos en caso de fallo.
    """
    try:
        logger.info("Establishing DB connection...")
        connection_tries = int(os.getenv("CONNECTION_TRIES", 3))
        connection_stablished = False

        while not connection_stablished:
            if connection_tries == 0:
                raise Exception("Could not connect to db.")
            
            try:
                # Conectar a la base de datos directamente
                connection = pymysql.connect(
                    host=os.getenv("DB_HOST"),
                    port=int(os.getenv("DB_PORT", 3306)),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME")
                )
                connection_stablished = True
            except Exception as e:
                logger.warning(f"Could not connect to DB, retries remaining: {connection_tries}. Error: {str(e)}")
                connection_tries -= 1
                time.sleep(5)

        logger.info("DB connection established.")
        return connection
    except Exception as e:
        logger.error(f"Error establishing DB connection: {e}")
        raise DbException(str(e))

def close_connection(connection):
    """
    Cierra la conexión a la base de datos.
    """
    if connection:
        connection.close()
        logger.info("DB connection closed.")


def execute(query: str, params: tuple, connection):
    """
    Ejecuta una consulta SQL con los parámetros proporcionados.
    """
    try:
        # Crear un cursor
        with connection.cursor() as cursor:
            logger.info(f"Executing query: {query} with params: {params}")
            # Ejecutar la consulta
            cursor.execute(query, params)

            # Confirmar la transacción
            connection.commit()

    except pymysql.MySQLError as error:
        connection.rollback()
        logger.warning(str(error))
        raise DbException(f"Error executing query: {str(error)}")


def execute_query(query: str, params: tuple, connection):
    """
    Ejecuta una consulta SQL y devuelve los resultados.
    """
    try:
        # Crear un cursor para ejecutar la consulta
        with connection.cursor() as cursor:
            logger.info(f"Executing query: {query} with params: {params}")
            cursor.execute(query, params)

            # Obtener los resultados
            results = cursor.fetchall()
            logger.info(f"Query results: {results}")
            return results

    except pymysql.MySQLError as error:
        connection.rollback()
        logger.warning(str(error))
        raise DbException(f"Error executing query: {str(error)}")


def get_db_connection():
    """
    Dependencia para obtener la conexión a la base de datos.
    """
    connection = establish_connection()
    try:
        yield connection
    finally:
        close_connection(connection)
