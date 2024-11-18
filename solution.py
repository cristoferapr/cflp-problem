import random  # Biblioteca para generar números aleatorios.
import time  # Biblioteca para trabajar con el tiempo.

# Configurar la semilla del generador de números aleatorios basada en el tiempo actual.
random.seed(time.time())

# Clase que representa el costo de asignar un cliente a una instalación específica.
class CustomerCost:
    def __init__(self, value, id_):
        self.value = value  # El costo de asignar este cliente a una instalación.
        self.id = id_       # El identificador del cliente.

# Clase que representa a un cliente en el problema.
class Customer:
    def __init__(self, demand, costs=None):
        self.demand = demand  # Cantidad de recursos que requiere el cliente.
        self.costs = costs or []  # Lista de costos asociados con cada instalación.

# Clase que representa una instalación.
class Facility:
    def __init__(self, capacity, cost):
        self.capacity = capacity  # Capacidad máxima de la instalación.
        self.cost = cost          # Costo fijo de mantener la instalación abierta.

# Método para realizar búsqueda local dentro de la clase `Solution`.
def local_search(self):
    """
    Mejora la solución actual mediante búsqueda local.
    Reasigna clientes a instalaciones para reducir el costo total, respetando restricciones.
    """
    for customer_id, current_facility in enumerate(self.customer_result):
        # Inicialmente, se considera que la instalación actual es la mejor.
        best_facility = current_facility
        best_cost = (self.facilities[current_facility]['fixed_cost'] + 
                     self.customers[customer_id]['costs'][current_facility])

        # Explorar todas las instalaciones para encontrar una asignación mejor.
        for facility_id in range(len(self.facilities)):
            # Comprobar si la instalación es diferente y tiene capacidad suficiente.
            if (facility_id != current_facility and 
                self.customers[customer_id]['demand'] <= self.spare_capacity[facility_id]):
                # Calcular el nuevo costo al reasignar a esta instalación.
                new_cost = (self.facilities[facility_id]['fixed_cost'] + 
                            self.customers[customer_id]['costs'][facility_id])
                # Si el costo es mejor, actualizar la mejor opción encontrada.
                if new_cost < best_cost:
                    best_facility = facility_id
                    best_cost = new_cost

        # Si se encuentra una mejor instalación, realizar la reasignación.
        if best_facility != current_facility:
            # Actualizar las capacidades disponibles de las instalaciones.
            self.spare_capacity[current_facility] += self.customers[customer_id]['demand']
            self.spare_capacity[best_facility] -= self.customers[customer_id]['demand']

            # Actualizar los resultados de clientes e instalaciones.
            self.customer_result[customer_id] = best_facility
            self.facility_result[current_facility] = any(
                c == current_facility for c in self.customer_result
            )
            self.facility_result[best_facility] = 1  # Marcar la nueva instalación como abierta.

    # Recalcular el costo total de la solución después de los cambios.
    self.calculate_total_cost()

# Clase principal que representa una solución al problema.
class Solution:
    def __init__(self, facilities, customers):
        self.facilities = facilities  # Lista de instalaciones disponibles.
        self.customers = customers    # Lista de clientes que necesitan ser atendidos.
        self.total_cost = 0           # Costo total de la solución.
        self.facility_result = [0] * len(facilities)  # Estado de cada instalación (0: cerrada, 1: abierta).
        self.customer_result = [-1] * len(customers)  # Asignación de cada cliente a una instalación.
        self.spare_capacity = [{"id": i, "capacity": facilities[i]['capacity']} for i in range(len(facilities))]
        self.facility_sequence = list(range(len(facilities)))  # Secuencia de instalaciones.
        self.customer_sequence = list(range(len(customers)))  # Secuencia de clientes.

        # Generar una solución inicial aleatoria.
        self.random_generate()
        # Calcular el costo total de la solución inicial.
        self.calculate_total_cost()

    def random_generate(self):
        """
        Genera una solución inicial asignando clientes a instalaciones
        de manera aleatoria, respetando restricciones de capacidad.
        """
        # Inicializar las instalaciones como cerradas y con capacidad máxima.
        for facility_id in range(len(self.facilities)):
            self.facility_result[facility_id] = 0  # Inicialmente cerradas.
            self.spare_capacity[facility_id] = self.facilities[facility_id]['capacity']

        # Ordenar clientes por demanda (opcional) y luego mezclarlos aleatoriamente.
        self.customer_sequence.sort(
            key=lambda c_id: self.customers[c_id]['demand'], reverse=True
        )
        random.shuffle(self.customer_sequence)  # Mezclar el orden.

        # Asignar cada cliente a una instalación disponible.
        for customer_id in self.customer_sequence:
            # Crear una lista priorizada de instalaciones, considerando un componente aleatorio.
            prioritized_facilities = sorted(
                self.facility_sequence,
                key=lambda f_id: self.customers[customer_id]['costs'][f_id] + random.uniform(0, 0.1)
            )

            # Intentar asignar al cliente a una instalación priorizada.
            for facility_id in prioritized_facilities:
                if self.customers[customer_id]['demand'] <= self.spare_capacity[facility_id]:
                    # Reducir la capacidad disponible de la instalación.
                    self.spare_capacity[facility_id] -= self.customers[customer_id]['demand']
                    # Registrar la asignación del cliente.
                    self.customer_result[customer_id] = facility_id
                    # Marcar la instalación como abierta.
                    self.facility_result[facility_id] = 1
                    break
            else:
                # Si no se puede asignar al cliente, lanzar un error.
                print(f"Failed to assign customer {customer_id}")
                raise ValueError(f"Cannot assign customer {customer_id}")

    def calculate_total_cost(self):
        """
        Calcula el costo total de la solución, considerando costos fijos y variables.
        """
        self.total_cost = 0  # Reiniciar el costo total.
        # Sumar costos fijos de las instalaciones abiertas.
        for facility_id, is_open in enumerate(self.facility_result):
            if is_open:
                self.total_cost += self.facilities[facility_id]['fixed_cost']

        # Sumar los costos de asignación de cada cliente.
        for customer_id, facility_id in enumerate(self.customer_result):
            self.total_cost += self.customers[customer_id]['costs'][facility_id]

    def check_solution(self):
        """
        Verifica que ninguna instalación exceda su capacidad máxima.
        """
        # Inicializar el uso de capacidad de cada instalación.
        used_capacity = [0] * len(self.facilities)
        for customer_id, facility_id in enumerate(self.customer_result):
            used_capacity[facility_id] += self.customers[customer_id]['demand']

        # Verificar que el uso de capacidad no exceda el límite en ninguna instalación.
        for i, facility in enumerate(self.facilities):
            if used_capacity[i] > facility['capacity']:
                return False
        return True

    def generate_neighbor(self):
        """
        Genera una solución vecina modificando la asignación de un cliente.
        """
        neighbor = Solution(self.facilities, self.customers)  # Crear una copia de la solución actual.
        random_customer = random.randint(0, len(self.customers) - 1)  # Seleccionar un cliente aleatorio.
        current_facility = self.customer_result[random_customer]  # Obtener la instalación actual del cliente.

        # Seleccionar una nueva instalación aleatoria para este cliente.
        new_facility = random.choice([
            f_id for f_id in range(len(self.facilities))
            if f_id != current_facility and self.customers[random_customer]['demand'] <= neighbor.spare_capacity[f_id]
        ])

        if new_facility:
            # Actualizar la asignación del cliente y ajustar capacidades.
            neighbor.spare_capacity[current_facility] += self.customers[random_customer]['demand']
            neighbor.spare_capacity[new_facility] -= self.customers[random_customer]['demand']
            neighbor.customer_result[random_customer] = new_facility
            neighbor.facility_result[current_facility] = int(any(
                c == current_facility for c in neighbor.customer_result
            ))
            neighbor.facility_result[new_facility] = 1

        # Recalcular el costo total para la nueva solución.
        neighbor.calculate_total_cost()
        return neighbor

    def __lt__(self, other):
        """
        Comparar soluciones basándose en el costo total.
        """
        return self.total_cost < other.total_cost

    def print_solution(self):
        """
        Imprime los detalles de la solución.
        """
        print(f"Total Cost: {self.total_cost}")
        print(f"Facility Open Status: {self.facility_result}")
        print(f"Customer Assignments: {self.customer_result}")
