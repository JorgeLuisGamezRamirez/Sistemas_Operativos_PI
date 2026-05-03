from abc import ABC, abstractmethod
from collections import deque
from Procesos.pcb import PCB

class AlgoritmoPlanificacion(ABC):
    """
    Clase base abstracta (Plantilla) para los algoritmos de planificación.
    Aplica el Patrón de Diseño Strategy.
    """
    
    @abstractmethod
    def obtener_siguiente_proceso(self, cola_listos: deque) -> PCB:
        """
        Método que todos los algoritmos deben implementar obligatoriamente.
        Recibe la cola de procesos listos y decide cuál es el siguiente a ejecutar.
        """
        pass