from collections import deque
from Algoritmos.base import AlgoritmoPlanificacion
from Procesos.pcb import PCB

class SJF(AlgoritmoPlanificacion):
    """
    Algoritmo Shortest Job First.
    Despacha el proceso que tenga la ráfaga de CPU más corta.
    """
    def obtener_siguiente_proceso(self, cola_listos: deque) -> PCB:
        if not cola_listos:
            return None
            
        # Encontramos el proceso con la menor rafaga_cpu
        proceso_mas_corto = min(cola_listos, key=lambda pcb: pcb.rafaga_cpu)
        
        # Lo sacamos de la cola y lo retornamos
        cola_listos.remove(proceso_mas_corto)
        return proceso_mas_corto