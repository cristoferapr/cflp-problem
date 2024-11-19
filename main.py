import os
import time
from cflp import CFLP

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
