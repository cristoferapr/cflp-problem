import os
import time
import matplotlib.pyplot as plt
from cflp import CFLP

# Valores óptimos para las instancias
OPTIMOS = {
    "cap41": 1040444.375,
    "cap42": 1098000.450,
    "cap43": 1153000.450,
    "cap44": 1235500.450,
    "cap51": 1025208.225,
    "cap61": 932615.750,
    "cap62": 977799.400,
    "cap63": 1014062.050,
    "cap64": 1045650.250,
    "cap71": 932615.750,
    "cap72": 977799.400,
    "cap73": 1010641.450,
    "cap74": 1034976.975,
    "cap81": 838499.288,
    "cap82": 910889.563,
    "cap83": 975889.563,
    "cap84": 1069369.525,
    "cap91": 796648.438,
    "cap92": 855733.500,
    "cap93": 896617.538,
    "cap94": 946051.325,
    "cap101": 796648.437,
    "cap102": 854704.200,
    "cap103": 893782.112,
    "cap104": 928941.750,
    "cap111": 826124.713,
    "cap112": 901377.213,
    "cap113": 970567.750,
    "cap114": 1063356.488,
    "cap121": 793439.563,
    "cap122": 852524.625,
    "cap123": 895302.325,
    "cap124": 946051.325,
    "cap131": 793439.562,
    "cap132": 851495.325,
    "cap133": 893076.712,
    "cap134": 928941.750,
}

# Capacidades predefinidas para archivos especiales.
CAPACITIES = {
    "capa": [8000, 10000, 12000, 14000],
    "capb": [5000, 6000, 7000, 8000],
    "capc": [5000, 5750, 6500, 7250],
}

def listar_instancias(carpeta, excluir=[]):
    """
    Lista los archivos en la carpeta, excluyendo los especificados.
    """
    return [f for f in os.listdir(carpeta) if f.endswith('.txt') and f not in excluir]

def guardar_resultado(archivo, solucion, tiempo):
    """
    Guarda el resultado de una solución en un archivo de texto.
    """
    with open("resultados_solucciones.txt", "a") as f:
        f.write(f"Archivo: {archivo}\n")
        f.write(f"Tiempo: {tiempo:.2f} segundos\n")
        f.write(f"Solución válida: {solucion.check_solution()}\n")
        f.write(f"Costo total: {solucion.total_cost}\n")
        f.write("-" * 40 + "\n")
    print(f"Resultado guardado en 'resultados_solucciones.txt'.")

def comparar_con_optimos(resultados):
    """
    Compara los resultados obtenidos con los valores óptimos y genera un gráfico.
    """
    diferencias = {res["Instancia"]: res["Costo Total"] - res["Óptimo"] for res in resultados}
    plt.figure(figsize=(10, 6))
    instancias = list(diferencias.keys())
    diferencias_valores = list(diferencias.values())
    plt.bar(instancias, diferencias_valores)
    plt.xlabel("Instancias")
    plt.ylabel("Diferencia entre obtenido y óptimo")
    plt.title("Comparación de costos obtenidos vs óptimos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("comparacion_costos.png")
    plt.show()
    print("Gráfico guardado como 'comparacion_costos.png'.")

def main():
    """
    Menú interactivo para resolver problemas CFLP.
    """
    carpeta_instancias = "./instances"
    excluir_especiales = ["capa.txt", "capb.txt", "capc.txt"]

    while True:
        print("\nMenú Principal:")
        print("1. Resolver una instancia regular")
        print("2. Resolver todas las instancias regulares")
        print("3. Resolver una instancia especial (capa, capb, capc)")
        print("4. Resolver un archivo especificado por nombre")
        print("5. Salir")
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            # Resolver una instancia regular
            instancias = listar_instancias(carpeta_instancias, excluir=excluir_especiales)
            print("\nInstancias disponibles:")
            for i, instancia in enumerate(instancias):
                print(f"{i + 1}. {instancia}")
            seleccion = int(input("Selecciona una instancia: ")) - 1
            file_name = os.path.join(carpeta_instancias, instancias[seleccion])
            
            temperatura = float(input("Temperatura inicial (default 1000): ") or 1000)
            cooling_rate = float(input("Cooling rate (default 0.9995): ") or 0.9995)
            iteraciones = int(input("Iteraciones por temperatura (default 10): ") or 10)

            print(f"Procesando {file_name}...")
            cflp = CFLP(file_name)
            start_time = time.time()
            best_solution = cflp.simulated_annealing(
                temperature=temperatura,
                cooling_rate=cooling_rate,
                iterations=iteraciones
            )
            end_time = time.time()
            
            print(f"Finalizado en {end_time - start_time:.2f}s")
            print(f"Solution valid: {best_solution.check_solution()}")
            best_solution.print_solution()

            guardar_resultado(file_name, best_solution, end_time - start_time)

        elif opcion == "2":
            # Resolver todas las instancias regulares
            instancias = listar_instancias(carpeta_instancias, excluir=excluir_especiales)
            print("\nResolviendo todas las instancias regulares...")
            resultados = []
            temperatura = float(input("Temperatura inicial (default 1000): ") or 1000)
            cooling_rate = float(input("Cooling rate (default 0.9995): ") or 0.9995)
            iteraciones = int(input("Iteraciones por temperatura (default 10): ") or 10)

            for instancia in instancias:
                file_name = os.path.join(carpeta_instancias, instancia)
                print(f"Procesando {file_name}...")
                cflp = CFLP(file_name)
                start_time = time.time()
                best_solution = cflp.simulated_annealing(
                    temperature=temperatura,
                    cooling_rate=cooling_rate,
                    iterations=iteraciones
                )
                end_time = time.time()
                
                guardar_resultado(file_name, best_solution, end_time - start_time)

                instancia_nombre = instancia.split('.')[0]
                if instancia_nombre in OPTIMOS:
                    resultados.append({
                        "Instancia": instancia_nombre,
                        "Costo Total": best_solution.total_cost,
                        "Óptimo": OPTIMOS[instancia_nombre],
                        "Tiempo (s)": end_time - start_time
                    })

            if resultados:
                comparar_con_optimos(resultados)

        elif opcion == "3":
            # Resolver una instancia especial
            print("\nInstancias especiales disponibles:")
            for i, especial in enumerate(excluir_especiales):
                print(f"{i + 1}. {especial}")
            seleccion = int(input("Selecciona una instancia especial: ")) - 1
            instancia_especial = excluir_especiales[seleccion]
            file_name = os.path.join(carpeta_instancias, instancia_especial)

            print("Capacidades disponibles:")
            for i, capacidad in enumerate(CAPACITIES[instancia_especial.split('.')[0]]):
                print(f"{i + 1}. {capacidad}")
            seleccion_capacidad = int(input("Selecciona una capacidad: ")) - 1

            temperatura = float(input("Temperatura inicial (default 1000): ") or 1000)
            cooling_rate = float(input("Cooling rate (default 0.9995): ") or 0.9995)
            iteraciones = int(input("Iteraciones por temperatura (default 10): ") or 10)

            print(f"Procesando {file_name} con capacidad {CAPACITIES[instancia_especial.split('.')[0]][seleccion_capacidad]}...")
            cflp = CFLP(file_name, capacity_index=seleccion_capacidad)
            start_time = time.time()
            best_solution = cflp.simulated_annealing(
                temperature=temperatura,
                cooling_rate=cooling_rate,
                iterations=iteraciones
            )
            end_time = time.time()
            
            print(f"Finalizado en {end_time - start_time:.2f}s")
            print(f"Solution valid: {best_solution.check_solution()}")
            best_solution.print_solution()

            guardar_resultado(file_name, best_solution, end_time - start_time)

        elif opcion == "4":
            # Resolver un archivo especificado por nombre
            archivo_nombre = input("Ingresa el nombre del archivo (debe estar en la carpeta raíz): ").strip()
            if not os.path.exists(archivo_nombre):
                print(f"El archivo {archivo_nombre} no existe en la carpeta raíz.")
                continue
            
            temperatura = float(input("Temperatura inicial (default 1000): ") or 1000)
            cooling_rate = float(input("Cooling rate (default 0.9995): ") or 0.9995)
            iteraciones = int(input("Iteraciones por temperatura (default 10): ") or 10)

            print(f"Procesando {archivo_nombre}...")
            cflp = CFLP(archivo_nombre)
            start_time = time.time()
            best_solution = cflp.simulated_annealing(
                temperature=temperatura,
                cooling_rate=cooling_rate,
                iterations=iteraciones
            )
            end_time = time.time()
            
            print(f"Finalizado en {end_time - start_time:.2f}s")
            print(f"Solution valid: {best_solution.check_solution()}")
            best_solution.print_solution()

            guardar_resultado(archivo_nombre, best_solution, end_time - start_time)

        elif opcion == "5":
            # Salir
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()
