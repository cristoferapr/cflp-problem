import math  # Biblioteca para operaciones matemáticas.
from solution import Solution  # Clase Solution para manejar las soluciones del problema.
import random  # Biblioteca para generación de números aleatorios.
import os  # Para manejar rutas de archivos.

# Capacidades predefinidas para archivos especiales.
CAPACITIES = {
    "capa": [8000, 10000, 12000, 14000],
    "capb": [5000, 6000, 7000, 8000],
    "capc": [5000, 5750, 6500, 7250],
}

def parse_large_file(file_path, capacity_index):
    """
    Procesa un archivo grande reemplazando 'capacity' con un valor específico.
    
    Args:
        file_path (str): Ruta al archivo.
        capacity_index (int): Índice para seleccionar el valor de capacidad.
    
    Returns:
        tuple: Una lista de instalaciones y una lista de clientes.
    """
    facilities = []
    customers = []

    # Determinar el tipo de archivo según su nombre.
    base_name = os.path.basename(file_path).split('.')[0]
    if base_name not in CAPACITIES:
        raise ValueError(f"Archivo {base_name} no es un tipo especial reconocido (capa, capb, capc).")

    # Obtener el valor de capacidad correspondiente.
    capacity_value = CAPACITIES[base_name][capacity_index]

    with open(file_path, 'r') as file:
        lines = file.readlines()
        m, n = map(int, lines[0].split())  # Número de instalaciones y clientes.
        facility_lines = lines[1:1 + m]
        customer_lines = lines[1 + m:]

        # Procesar instalaciones.
        for line in facility_lines:
            parts = line.split()
            facilities.append({
                'capacity': capacity_value,  # Reemplaza 'capacity' por el valor específico.
                'fixed_cost': float(parts[1])
            })

        # Procesar clientes.
        for line in customer_lines:
            parts = line.split()
            customers.append({
                'demand': float(parts[0]),
                'costs': [float(c) for c in parts[1:]]
            })

    return facilities, customers


class CFLP:
    def __init__(self, file_path, capacity_index=0):
        """
        Inicializa una instancia del problema CFLP.
        
        Args:
            file_path (str): Ruta al archivo de datos.
            capacity_index (int): Índice para seleccionar capacidad en CAPACITIES (para archivos especiales).
        """
        self.file_path = file_path
        self.capacity_index = capacity_index
        self.facilities = []
        self.customers = []
        self.read_instance()

    def read_instance(self):
        """
        Lee el archivo de datos y construye las listas de instalaciones y clientes.
        """
        # Determinar si el archivo es especial (capa, capb, capc) o regular.
        base_name = os.path.basename(self.file_path).split('.')[0]
        if base_name in CAPACITIES:
            # Usar parse_large_file para archivos especiales.
            print(f"Procesando archivo especial: {base_name}")
            self.facilities, self.customers = parse_large_file(self.file_path, self.capacity_index)
        else:
            # Leer archivo regular.
            with open(self.file_path, 'r') as f:
                m, n = map(int, f.readline().split())
                for _ in range(m):
                    capacity, fixed_cost = map(float, f.readline().split())
                    self.facilities.append({
                        'capacity': capacity,
                        'fixed_cost': fixed_cost
                    })
                for _ in range(n):
                    line = f.readline().split()
                    demand = float(line[0])
                    costs = list(map(float, line[1:]))
                    self.customers.append({
                        'demand': demand,
                        'costs': costs
                    })

    def simulated_annealing(self, temperature=1000, cooling_rate=0.9995, iterations=10, accept_temperature=0.01):
        """
        Implementa el algoritmo de recocido simulado para optimizar el problema CFLP.
        
        Args:
            temperature (float): Temperatura inicial para el algoritmo.
            cooling_rate (float): Tasa de enfriamiento para reducir la temperatura.
            iterations (int): Número de iteraciones por cada temperatura.
            accept_temperature (float): Temperatura mínima para detener el algoritmo.
        
        Returns:
            Solution: La mejor solución encontrada.
        """
        current_solution = Solution(self.facilities, self.customers)
        best_solution = current_solution
        print(f"Costo inicial: {current_solution.total_cost}")

        t = temperature

        while t > accept_temperature:
            for _ in range(iterations):
                new_solution = current_solution.generate_neighbor()
                new_solution.local_search(max_customers=100)

                if (
                    new_solution.total_cost < current_solution.total_cost
                    or random.random() < math.exp(
                        -(new_solution.total_cost - current_solution.total_cost) / t
                    )
                ):
                    current_solution = new_solution
                    if new_solution.total_cost < best_solution.total_cost:
                        best_solution = new_solution

            t *= cooling_rate

        return best_solution

