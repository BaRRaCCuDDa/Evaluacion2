import urllib.parse
import requests

route_url = "https://graphhopper.com/api/1/route?"
geocode_url = "https://graphhopper.com/api/1/geocode?"
key = "045dfb5c-534d-4d49-866f-25948023ff36"  

def geocodificar(ubicacion, key):
    while ubicacion == "":
        ubicacion = input("La ubicación no puede estar vacía. Ingrese nuevamente: ").strip()
    
    parametros = urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": key})
    url = geocode_url + parametros
    
    respuesta = requests.get(url)
    datos_json = respuesta.json()
    estado = respuesta.status_code

    if estado == 200 and len(datos_json["hits"]) != 0:
        lat = datos_json["hits"][0]["point"]["lat"]
        lng = datos_json["hits"][0]["point"]["lng"]
        nombre = datos_json["hits"][0]["name"]
        valor = datos_json["hits"][0]["osm_value"]

        pais = datos_json["hits"][0].get("country", "")
        estado_reg = datos_json["hits"][0].get("state", "")

        if len(estado_reg) != 0 and len(pais) != 0:
            nueva_ubicacion = f"{nombre}, {estado_reg}, {pais}"
        elif len(pais) != 0:
            nueva_ubicacion = f"{nombre}, {pais}"
        else:
            nueva_ubicacion = nombre

        print(f"URL de Geocodificación para {nueva_ubicacion} (Tipo: {valor}):\n{url}")
    else:
        lat = "null"
        lng = "null"
        nueva_ubicacion = ubicacion
        if estado != 200:
            print(f"Estado de la API de Geocodificación: {estado}\nMensaje de error: {datos_json.get('message', 'Error desconocido')}")
            
    return estado, lat, lng, nueva_ubicacion

print("=================================================")
print("  SISTEMA DE GEOLOCALIZACIÓN Y RUTAS - API LTDA. ")
print("=================================================")

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("auto, bicicleta, a pie")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    
    perfiles = {"auto": "car", "bicicleta": "bike", "a pie": "foot"}
    vehiculo_input = input("Ingrese un perfil de vehículo de la lista (o 's' / 'salir' para terminar): ").strip().lower()
    
    if vehiculo_input in ["s", "salir"]:
        print("Saliendo del programa. ¡Hasta luego!")
        break
    elif vehiculo_input in perfiles:
        vehiculo = perfiles[vehiculo_input]
    else:
        vehiculo = "car"
        print("No se ingresó un perfil válido. Se utilizará el perfil 'auto' por defecto.")

    loc1 = input("Ingrese la ubicación de inicio (o 's' / 'salir' para terminar): ").strip()
    if loc1.lower() in ["s", "salir"]:
        print("Saliendo del programa. ¡Hasta luego!")
        break
    orig = geocodificar(loc1, key)

    loc2 = input("Ingrese la ubicación de destino (o 's' / 'salir' para terminar): ").strip()
    if loc2.lower() in ["s", "salir"]:
        print("Saliendo del programa. ¡Hasta luego!")
        break
    dest = geocodificar(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        # Se incluye locale="es" para que la narrativa venga en español
        parametros_ruta = urllib.parse.urlencode({"key": key, "vehicle": vehiculo, "locale": "es"})
        url_caminos = route_url + parametros_ruta + op + dp
        
        estado_caminos = requests.get(url_caminos).status_code
        datos_caminos = requests.get(url_caminos).json()
        
        print(f"Estado de la API de Rutas: {estado_caminos}\nURL de la API de Rutas:\n{url_caminos}")
        print("=================================================")
        print(f"Instrucciones de viaje desde {orig[3]} hasta {dest[3]} en {vehiculo_input}")
        print("=================================================")
        
        if estado_caminos == 200:
            millas = (datos_caminos["paths"][0]["distance"]) / 1000 / 1.60934
            km = (datos_caminos["paths"][0]["distance"]) / 1000
            minutos = (datos_caminos["paths"][0]["time"]) / 1000 / 60
            horas = minutos / 60

            # Salidas formateadas a 2 decimales según requerimiento
            print(f"Distancia recorrida: {km:.2f} km / {millas:.2f} millas")
            print(f"Duración estimada del viaje: {minutos:.2f} minutos ({horas:.2f} horas)")
            print("=================================================")
            print("Narrativa del viaje (Instrucciones paso a paso):")
            
            for instruccion in datos_caminos["paths"][0]["instructions"]:
                camino = instruccion["text"]
                distancia_paso = instruccion["distance"] / 1000
                millas_paso = distancia_paso / 1.60934
                print(f" - {camino} ({distancia_paso:.2f} km / {millas_paso:.2f} millas)")
            print("=================================================")
        else:
            print(f"Mensaje de error: {datos_caminos.get('message', 'No se pudo calcular la ruta')}")
            print("*************************************************")