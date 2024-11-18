import math  # Biblioteca para operaciones matemáticas (usada aquí para cálculos exponenciales).
from solution import Solution  # Importa la clase Solution (definida previamente).
import random  # Biblioteca para generación de números aleatorios.

# Diccionario que almacena capacidades predefinidas para diferentes tipos de datos.
CAPACITIES = {
    "capa": [8000, 10000, 12000, 14000],  # Capacidades para el tipo "capa".
    "capb": [5000, 6000, 7000, 8000],     # Capacidades para el tipo "capb".
    "capc": [5000, 5750, 6500, 7250],     # Capacidades para el tipo "capc".
}

def parse_large_file(file_path, capacity_index):
    """
    Procesa un archivo grande que contiene datos de instalaciones y clientes, 
    reemplazando marcadores de "capacidad" por valores concretos.
    
    Args:
        file_path (str): Ruta al archivo de datos.
        capacity_index (int): Índice para seleccionar el valor de capacidad en CAPACITIES.
    
    Returns:
        tuple: Una lista de instalaciones y una lista de clientes.
    """
    facilities = []  # Lista para almacenar datos de instalaciones.
    customers = []   # Lista para almacenar datos de clientes.

    # Obtener el nombre base del archivo (sin ruta ni extensión).
    base_name = file_path.split('/')[-1].split('.')[0]

    # Verificar si el nombre base del archivo está en CAPACITIES.
    if base_name not in CAPACITIES:
        raise ValueError(f"Unknown file base name '{base_name}' for large file parsing.")

    # Obtener el valor de capacidad correspondiente al índice.
    capacity_value = CAPACITIES[base_name][capacity_index]

    # Abrir y leer el archivo.
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Leer todas las líneas del archivo.
        m, n = map(int, lines[0].split())  # Primera línea: número de instalaciones y clientes.
        facility_lines = lines[1:1 + m]    # Líneas correspondientes a las instalaciones.
        customer_lines = lines[1 + m:]     # Líneas correspondientes a los clientes.

        # Procesar datos de instalaciones.
        for line in facility_lines:
            parts = line.split()
            facilities.append({
                'capacity': capacity_value,  # Asignar capacidad desde el valor predefinido.
                'fixed_cost': float(parts[1])  # Costo fijo de la instalación.
            })

        # Procesar datos de clientes.
        for line in customer_lines:
            parts = line.split()
            customers.append({
                'demand': float(parts[0]),  # Demanda del cliente.
                'costs': [float(c) for c in parts[1:]]  # Lista de costos de asignación.
            })

    return facilities, customers  # Retorna las listas procesadas de instalaciones y clientes.


# Clase principal que implementa el problema de localización de instalaciones.
class CFLP:
    def __init__(self, file_path, capacity_index=0):
        """
        Inicializa una instancia del problema CFLP.
        
        Args:
            file_path (str): Ruta al archivo de datos de entrada.
            capacity_index (int): Índice para seleccionar capacidad en CAPACITIES.
        """
        self.file_path = file_path  # Ruta del archivo de entrada.
        self.facilities = []       # Lista de instalaciones.
        self.customers = []        # Lista de clientes.
        self.read_instance()       # Leer y procesar los datos del archivo.

    def read_instance(self):
        """
        Lee el archivo de datos y construye las listas de instalaciones y clientes.
        """
        with open(self.file_path, 'r') as f:
            # Leer el número de instalaciones y clientes desde la primera línea.
            m, n = map(int, f.readline().split())
            
            # Leer datos de instalaciones.
            for _ in range(m):
                capacity, fixed_cost = map(float, f.readline().split())
                self.facilities.append({
                    'capacity': capacity,      # Capacidad de la instalación.
                    'fixed_cost': fixed_cost   # Costo fijo de abrir la instalación.
                })

            # Leer datos de clientes.
            for _ in range(n):
                line = f.readline().split()
                demand = float(line[0])          # Demanda del cliente.
                costs = list(map(float, line[1:]))  # Costos de asignación a cada instalación.
                self.customers.append({
                    'demand': demand,
                    'costs': costs
                })

    def simulated_annealing(self):
        """
        Implementa el algoritmo de recocido simulado para optimizar el problema CFLP.
        
        Returns:
            Solution: La mejor solución encontrada.
        """
        # Crear una solución inicial basada en los datos.
        current_solution = Solution(self.facilities, self.customers)
        best_solution = current_solution  # Inicialmente, la mejor solución es la actual.

        t = 10000  # Temperatura inicial para el algoritmo.
        cooling_rate = 0.99  # Tasa de enfriamiento (reduce la temperatura en cada iteración).
        accept_temperature = 0.00001  # Temperatura mínima para detener el algoritmo.

        # Continuar el proceso mientras la temperatura sea mayor que la mínima aceptable.
        while t > accept_temperature:
            for _ in range(10):  # Número de iteraciones por cada temperatura.
                # Generar una solución vecina.
                new_solution = current_solution.generate_neighbor()

                # Evaluar si la solución vecina es aceptable.
                if (
                    # Aceptar si el costo de la nueva solución es menor.
                    new_solution.total_cost < current_solution.total_cost
                    or 
                    # Aceptar con una probabilidad basada en la temperatura (exploración).
                    random.random() < math.exp(
                        -(new_solution.total_cost - current_solution.total_cost) / t
                    )
                ):
                    # Actualizar la solución actual con la vecina aceptada.
                    current_solution = new_solution
                    # Si la nueva solución es mejor que la mejor conocida, actualizar.
                    if new_solution.total_cost < best_solution.total_cost:
                        best_solution = new_solution

            # Reducir la temperatura aplicando la tasa de enfriamiento.
            t *= cooling_rate

        return best_solution  # Retorna la mejor solución encontrada.
