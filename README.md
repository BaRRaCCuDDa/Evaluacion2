# Evaluacion2 - Software de Geolocalizacion (API Ltda.)

## Descripcion del Proyecto
Este repositorio contiene el script mejorado de geolocalizacion en Python desarrollado para la Biblioteca Nacional por encargo de API Ltda. El programa consume la API REST de Graphhopper Directions para geocodificar ubicaciones y calcular rutas optimas de viaje.

### Caracteristicas implementadas:
- Interfaz de consola e interaccion 100% en espanol.
- Resultados de distancia (km/millas) y duracion (minutos/horas) formateados a 2 decimales.
- Narrativa del viaje paso a paso en espanol (locale=es).
- Opcion de salida segura en cualquier etapa mediante los comandos 's' o 'salir'.

## Requisitos Previos
- Python 3
- Libreria requests (pip3 install requests)
- API Key activa de Graphhopper

## Instrucciones de Ejecucion
1. Clonar el repositorio: git clone https://github.com/BaRRaCCuDDa/Evaluacion2.git
2. Entrar a la carpeta: cd Evaluacion2
3. Configurar la API Key en la variable key dentro de geolocalizacion.py
4. Ejecutar el script: python3 geolocalizacion.py
