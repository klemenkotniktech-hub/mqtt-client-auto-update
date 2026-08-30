CREATE DATABASE mqtt_project;

USE mqtt_project;

CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    measurement_timestamp DATETIME NOT NULL,
    received_timestamp DATETIME NOT NULL,
    stored_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT
);