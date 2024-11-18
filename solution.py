import random
import time 

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

    def log_spare_capacity(self, message=""):
        print(f"{message}")
        for i, spare in enumerate(self.spare_capacity):
            print(f"Instalación {i}: Capacidad libre {spare}, "
                f"Capacidad máxima {self.facilities[i]['capacity']}, "
                f"Estado abierto: {self.facility_result[i]}")
        print("-" * 50)


    def random_generate(self):
        """
        Genera una solución inicial asignando clientes a instalaciones
        de manera aleatoria pero considerando costos.
        """
        for facility_id in range(len(self.facilities)):
            self.facility_result[facility_id] = 0
            self.spare_capacity[facility_id] = self.facilities[facility_id]['capacity']

        random.shuffle(self.customer_sequence)

        for customer_id in self.customer_sequence:
            prioritized_facilities = sorted(
                self.facility_sequence,
                key=lambda f_id: self.customers[customer_id]['costs'][f_id] + random.uniform(0, 10)
            )
            for facility_id in prioritized_facilities:
                if self.customers[customer_id]['demand'] <= self.spare_capacity[facility_id]:
                    self.spare_capacity[facility_id] -= self.customers[customer_id]['demand']
                    self.customer_result[customer_id] = facility_id
                    self.facility_result[facility_id] = 1
                    break
            else:
                raise ValueError(f"No se puede asignar al cliente {customer_id}, demanda excede la capacidad disponible.")

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
        Genera una solución vecina modificando varias asignaciones de clientes y estados de instalaciones.
        """
        neighbor = Solution(self.facilities, self.customers)
        neighbor.customer_result = self.customer_result.copy()
        neighbor.spare_capacity = self.spare_capacity.copy()
        neighbor.facility_result = self.facility_result.copy()

        # Cambiar aleatoriamente 10-20 asignaciones de clientes.
        for _ in range(random.randint(10, 20)):
            random_customer = random.randint(0, len(self.customers) - 1)
            current_facility = neighbor.customer_result[random_customer]

            # Seleccionar una nueva instalación.
            new_facility = random.choice([
                f_id for f_id in range(len(self.facilities))
                if f_id != current_facility and self.customers[random_customer]['demand'] <= neighbor.spare_capacity[f_id]
            ])

            if new_facility:
                neighbor.spare_capacity[current_facility] += self.customers[random_customer]['demand']
                neighbor.spare_capacity[new_facility] -= self.customers[random_customer]['demand']
                neighbor.customer_result[random_customer] = new_facility

        # Abrir o cerrar instalaciones aleatoriamente.
        for _ in range(5):
            random_facility = random.randint(0, len(self.facilities) - 1)
            neighbor.facility_result[random_facility] ^= 1  # Alternar estado abierto/cerrado.

        neighbor.calculate_total_cost()
        return neighbor


    def local_search(self, max_customers=50):
        """
        Mejora parcial de la solución considerando un subconjunto aleatorio de clientes.
        """
        customers_to_consider = random.sample(
            range(len(self.customer_result)),
            min(max_customers, len(self.customer_result))
        )
        for customer_id in customers_to_consider:
            current_facility = self.customer_result[customer_id]
            best_facility = current_facility
            best_cost = self.customers[customer_id]['costs'][current_facility]

            for facility_id in range(len(self.facilities)):
                if (facility_id != current_facility and
                    self.customers[customer_id]['demand'] <= self.spare_capacity[facility_id]):
                    new_cost = self.customers[customer_id]['costs'][facility_id]
                    if new_cost < best_cost or random.random() < 0.2:
                        best_facility = facility_id
                        best_cost = new_cost

            if best_facility != current_facility:
                self.spare_capacity[current_facility] += self.customers[customer_id]['demand']
                self.spare_capacity[best_facility] -= self.customers[customer_id]['demand']
                self.customer_result[customer_id] = best_facility

        

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
