import requests
import urllib.parse

headers = {'User-Agent': 'DEVASC_Lab_Application/1.0'}

def get_coords(location_name):
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(location_name)}&format=json&limit=1"
    try:
        res = requests.get(url, headers=headers).json()
        if res:
            return float(res[0]["lat"]), float(res[0]["lon"]), res[0]["display_name"]
    except Exception:
        pass
    return None, None, None

while True:
    print("\n" + "="*60)
    orig = input("Ubicación de origen (o 'q'/'quit' para salir): ").strip()
    if orig.lower() in ["q", "quit"]:
        print("¡Programa finalizado!")
        break

    dest = input("Ubicación de destino (o 'q'/'quit' para salir): ").strip()
    if dest.lower() in ["q", "quit"]:
        print("¡Programa finalizado!")
        break

    print("\nObteniendo coordenadas y calculando ruta...")
    lat1, lon1, name1 = get_coords(orig)
    lat2, lon2, name2 = get_coords(dest)

    if not lat1 or not lat2:
        print("\n[ERROR] No se pudo geolocalizar una o ambas ubicaciones. Intente nuevamente.")
        continue

    route_url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false&steps=true"
    
    try:
        res = requests.get(route_url, headers=headers).json()
        if res.get("code") == "Ok":
            route = res["routes"][0]
            distance_meters = route["distance"]
            duration_seconds = route["duration"]

            distance_km = distance_meters / 1000.0
            distance_miles = distance_km / 1.60934

            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            seconds = int(duration_seconds % 60)
            formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            fuel_liters = (distance_km / 100.0) * 8.5
            fuel_gal = fuel_liters / 3.78541

            print("\n" + "-"*60)
            print(f"RUTA: {orig.upper()} ===> {dest.upper()}")
            print("-"*60)
            print(f"Distancia:    {distance_miles:.2f} millas ({distance_km:.2f} km)")
            print(f"Tiempo:       {formatted_time}")
            print(f"Combustible:  {fuel_gal:.2f} galones ({fuel_liters:.2f} litros)")
            print(f"Origen Coor:  Lat {lat1:.5f}, Lng {lon1:.5f}")
            print(f"Destino Coor: Lat {lat2:.5f}, Lng {lon2:.5f}")

            print("\nIndicaciones detalladas del viaje:")
            print("-" * 40)
            steps = route["legs"][0]["steps"]
            for step in steps:
                name = step.get("name", "")
                if not name:
                    name = "Continúe por la vía principal"
                step_dist_km = step["distance"] / 1000.0
                if step_dist_km > 0:
                    print(f"• {name} ({step_dist_km:.2f} km)")
        else:
            print("\n[ERROR] No se pudo calcular la ruta entre las ubicaciones.")
    except Exception as e:
        print(f"\n[ERROR DE CONEXIÓN]: {e}")
