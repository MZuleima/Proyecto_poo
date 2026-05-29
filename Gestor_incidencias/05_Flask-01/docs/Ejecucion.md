# Manual de Ejecución del Sistema (Consola y Web)

El sistema soporta un doble entorno de presentación (interfaz de línea de comandos clásica y servidor API Web mediante Flask), ambos conectados al mismo motor de persistencia relacional SQLite.

## 1. Requisitos Previos e Instalación

Asegúrate de contar con Python 3.8 o superior. Antes de iniciar cualquiera de los entornos, es obligatorio instalar las dependencias del proyecto e inicializar el archivo de datos:

```bash
# 1. Instalar Flask y dependencias necesarias
pip install -r requirements.txt

# 2. Inicializar la base de datos relacional (Tablas y Catálogos Semilla)
python crear_bd.py