from collections import deque
from Algoritmos.base import AlgoritmoPlanificacion
from Procesos.pcb import PCB

class FCFS(AlgoritmoPlanificacion):
    """
    Algoritmo First-Come, First-Served.
    Despacha el proceso que lleve más tiempo esperando en la cola.
    """
    def obtener_siguiente_proceso(self, cola_listos: deque) -> PCB:
        if not cola_listos:
            return None
            
        # Saca el elemento más a la izquierda (el más viejo)
        return cola_listos.popleft()