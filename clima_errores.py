import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def manejar_respuesta(respuesta):
    status_code = respuesta.status_code

    if status_code in (200, 201):
        print(f"\n[ÉXITO] Código HTTP {status_code}: Solicitud procesada correctamente.")
        try:
            data = respuesta.json()
            if "main" in data:
                nombre = data.get("name", "Desconocida")
                pais = data.get("sys", {}).get("country", "")
                temp = data["main"]["temp"]
                descripcion = data["weather"][0]["description"].capitalize()
                print(f"--- Clima en {nombre}, {pais} ---")
                print(f"Temperatura actual: {temp}°C")
                print(f"Descripción: {descripcion}")
            else:
                print(f"Datos recibidos: {data}")
        except Exception:
            print(f"Respuesta del servidor: {respuesta.text[:150]}")

    elif status_code == 400:
        print("\n[ERROR 400]: Solicitud incorrecta. Revisa los parámetros enviados a la API.")

    elif status_code == 401:
        print("\n[ERROR 401]: No autorizado. Tu API Key es inválida o no ha sido activada.")

    elif status_code == 404:
        print("\n[ERROR 404]: Recurso no encontrado. La ciudad o endpoint especificado no existe.")

    elif status_code == 429:
        retry_after = respuesta.headers.get("Retry-After", "10")
        print(f"\n[ERROR 429]: Demasiadas peticiones. Has superado el límite de tasa de la API. Esperar {retry_after} segundos.")

    elif status_code == 500:
        print("\n[ERROR 500]: Error interno del servidor. El servidor remoto encontró una condición inesperada.")

    else:
        print(f"\n[CÓDIGO HTTP {status_code}]: Respuesta no categorizada del servidor.")

def realizar_peticion(url, params=None):
    try:
        print(f"\nEnviando petición a: {url}")
        respuesta = requests.get(url, params=params, timeout=5)
        manejar_respuesta(respuesta)

    except requests.exceptions.ConnectionError:
        print("\n[ERROR DE CONEXIÓN]: No se pudo conectar al servidor. Revisa tu conexión a internet o el dominio.")

    except requests.exceptions.Timeout:
        print("\n[ERROR DE TIEMPO DE ESPERA]: La petición excedió el tiempo límite permitido (Timeout).")

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR DE RED DE PETICIÓN]: Ocurrió un error inesperado: {e}")

def probar_diferentes_codigos():
    print("==================================================")
    print(" LABORATORIO 3.3 - MANEJO DE ERRORES HTTP (API) ")
    print("==================================================")
    print("1. Probar Éxito (200 OK - Ciudad válida)")
    print("2. Probar Error 401 (No autorizado - API Key falsa)")
    print("3. Probar Error 404 (Recurso/Ciudad no existente)")
    print("4. Probar Error 400 (Solicitud incorrecta)")
    print("5. Probar Error 429 (Demasiadas peticiones)")
    print("6. Probar Error 500 (Error interno del servidor)")
    print("7. Probar Excepción ConnectionError (Dominio inexistente)")
    print("8. Probar Excepción Timeout (Simulación de retardo de red)")
    print("==================================================")

    opcion = input("Selecciona una opción a probar (1-8): ").strip()

    if opcion == "1":
        ciudad = input("Ingrese la ciudad (ej. Aguascalientes): ").strip() or "Aguascalientes"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
        realizar_peticion(url)

    elif opcion == "2":
        url = "https://api.openweathermap.org/data/2.5/weather?q=Aguascalientes&appid=KEY_FALSA_12345&units=metric"
        realizar_peticion(url)

    elif opcion == "3":
        url = f"https://api.openweathermap.org/data/2.5/weather?q=ciudad_inexistente_xyz999&appid={API_KEY}&units=metric"
        realizar_peticion(url)

    elif opcion == "4":
        url = "https://httpbin.org/status/400"
        realizar_peticion(url)

    elif opcion == "5":
        url = "https://httpbin.org/status/429"
        realizar_peticion(url)

    elif opcion == "6":
        url = "https://httpbin.org/status/500"
        realizar_peticion(url)

    elif opcion == "7":
        url = "https://dominio-totalmente-falso-123456.com/api"
        realizar_peticion(url)

    elif opcion == "8":
        url = "https://httpbin.org/delay/10"
        realizar_peticion(url)

    else:
        print("Opción inválida.")

if __name__ == "__main__":
    probar_diferentes_codigos()