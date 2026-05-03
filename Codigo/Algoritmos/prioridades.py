from collections import deque
from Algoritmos.base import AlgoritmoPlanificacion
from Procesos.pcb import PCB

class Prioridades(AlgoritmoPlanificacion):
    """
    Algoritmo por Prioridades.
    Despacha el proceso con el valor de prioridad más bajo (0 = Máxima Prioridad).
    """
    def obtener_siguiente_proceso(self, cola_listos: deque) -> PCB:
        if not cola_listos:
            return None
            
        # Encontramos el proceso con el número de prioridad más cercano a 0
        proceso_prioritario = min(cola_listos, key=lambda pcb: pcb.prioridad)
        
        # Lo sacamos de la cola y lo retornamos
        cola_listos.remove(proceso_prioritario)
        return proceso_prioritario