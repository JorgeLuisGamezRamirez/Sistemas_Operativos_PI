from collections import deque
from Algoritmos.base import AlgoritmoPlanificacion
from Procesos.pcb import PCB

class RoundRobin(AlgoritmoPlanificacion):
    """
    Algoritmo Round Robin.
    Atiende en orden de llegada (FCFS), pero el simulador lo interrumpirá 
    cuando se acabe su 'quantum' de tiempo.
    """
    def __init__(self, quantum: int = 4):
        self.quantum = quantum

    def obtener_siguiente_proceso(self, cola_listos: deque) -> PCB:
        if not cola_listos:
            return None
            
        # Saca al primero de la fila
        return cola_listos.popleft()