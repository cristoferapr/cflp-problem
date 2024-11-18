import time  # Biblioteca para medir el tiempo de ejecución.
from cflp import CFLP  # Importa la clase CFLP, que implementa el problema de localización de instalaciones.

def main():
    """
    Función principal que ejecuta el problema CFLP para una instancia específica,
    utilizando el algoritmo de recocido simulado para encontrar la mejor solución.
    """

    # Nombre del archivo que contiene los datos de la instancia.
    file_name = f"./instances/cap92.txt"
    print(f"Processing {file_name}")  # Mensaje para indicar que se está procesando el archivo.

    # Crear una instancia del problema CFLP utilizando el archivo especificado.
    cflp = CFLP(file_name)

    # Medir el tiempo de inicio del algoritmo.
    start_time = time.time()

    # Ejecutar el algoritmo de recocido simulado para encontrar la mejor solución.
    best_solution = cflp.simulated_annealing()

    # Medir el tiempo de finalización del algoritmo.
    end_time = time.time()

    # Calcular la duración total de la ejecución.
    duration = end_time - start_time

    # Imprimir el tiempo de ejecución y validar la solución obtenida.
    print(f"Finished {file_name} in {duration:.2f}s")  # Tiempo total en segundos.
    print(f"Solution valid: {best_solution.check_solution()}")  # Verificar si la solución cumple restricciones.
    
    # Imprimir los detalles de la mejor solución encontrada.
    best_solution.print_solution()

# Verificar si este archivo se está ejecutando como programa principal.
if __name__ == "__main__":
    main()
