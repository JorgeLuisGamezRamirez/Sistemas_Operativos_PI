from collections import deque
from Procesos.pcb import PCB, EstadoProceso
from Algoritmos.base import AlgoritmoPlanificacion

class Planificador:
    """
    Administra la cola de listos y delega la decisión de despacho 
    al algoritmo de planificación (Estrategia) seleccionado.
    """
    def __init__(self, algoritmo: AlgoritmoPlanificacion):
        self.algoritmo_actual = algoritmo
        self.cola_listos = deque()

    def cambiar_algoritmo(self, nuevo_algoritmo: AlgoritmoPlanificacion):
        """Permite cambiar la estrategia en tiempo de ejecución desde la interfaz."""
        self.algoritmo_actual = nuevo_algoritmo
        print(f"🔄 [Planificador] Algoritmo cambiado a: {nuevo_algoritmo.__class__.__name__}")

    def agregar_proceso(self, pcb: PCB):
        """Prepara el proceso y lo forma en la fila."""
        pcb.cambiar_estado(EstadoProceso.LISTO)
        self.cola_listos.append(pcb)
        print(f"📥 [Planificador] PID {pcb.pid} ({pcb.nombre}) entró a la cola de listos.")

    def despachar_siguiente(self) -> PCB:
        """
        Delega la decisión al algoritmo actual.
        """
        if not self.cola_listos:
            return None
        
        # Le pasamos la cola al algoritmo para que tome la decisión
        siguiente = self.algoritmo_actual.obtener_siguiente_proceso(self.cola_listos)
        
        if siguiente:
            siguiente.cambiar_estado(EstadoProceso.EJECUTANDO)
            print(f"🚀 [Planificador] Despachando a CPU: PID {siguiente.pid} ({siguiente.nombre}).")
            
        return siguiente