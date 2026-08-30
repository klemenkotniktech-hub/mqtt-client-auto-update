import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": SQL_USER,
    "password": SQL_PASSWORD,
    "database": "mqtt_project",
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def save_sensor_data(
    device_id,
    measurement_timestamp,
    received_timestamp,
    temperature,
    humidity,
    pressure,
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO sensor_data (
        device_id,
        measurement_timestamp,
        received_timestamp,
        temperature,
        humidity,
        pressure
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            device_id,
            measurement_timestamp,
            received_timestamp,
            temperature,
            humidity,
            pressure,
        )
    )

    connection.commit()

    cursor.close()
    connection.close()



if __name__ == "__main__":
    connection = get_connection()
    print("Connected to MySQL!")

    connection.close()