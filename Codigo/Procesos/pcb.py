import time
from enum import Enum

class EstadoProceso(Enum):
    """Enumerador para manejar los estados del proceso de forma segura."""
    NUEVO = "Nuevo"
    LISTO = "Listo"
    EJECUTANDO = "Ejecutando"
    ESPERANDO = "Esperando"
    TERMINADO = "Terminado"

class PCB:
    """
    Bloque de Control de Proceso (Process Control Block).
    Almacena toda la información vital de un proceso en ejecución.
    """
    _siguiente_pid = 1  # Variable de clase para generar PID automático y único

    def __init__(self, nombre: str, prioridad: int, rafaga_cpu: int, memoria_requerida: int):
        # Identificación
        self.pid = PCB._siguiente_pid
        PCB._siguiente_pid += 1
        self.nombre = nombre
        
        # Estados y métricas de tiempo
        self.estado = EstadoProceso.NUEVO
        self.fecha_creacion = time.time()
        
        # Atributos de planificación
        self.prioridad = prioridad
        self.rafaga_cpu = rafaga_cpu               # Tiempo total que necesita en CPU (ms)
        self.tiempo_ejecutado = 0                  # Tiempo que ya ha pasado en la CPU
        
        # Recursos
        self.memoria_requerida = memoria_requerida # MB de RAM que necesita
        self.cpu_asignada = 1                      # Por defecto requiere 1 núcleo

    def cambiar_estado(self, nuevo_estado: EstadoProceso):
        """Actualiza el estado actual del proceso."""
        self.estado = nuevo_estado

    def esta_terminado(self) -> bool:
        """Verifica si el proceso ya cumplió su tiempo de ráfaga."""
        return self.tiempo_ejecutado >= self.rafaga_cpu

    def ejecutar(self, tiempo: int):
        """Simula la ejecución sumando tiempo al contador."""
        self.tiempo_ejecutado += tiempo
        if self.esta_terminado():
            self.cambiar_estado(EstadoProceso.TERMINADO)

    def __str__(self):
        """Formato de texto para cuando necesitemos imprimir el proceso en consola (Logs)."""
        return f"[PID {self.pid}] {self.nombre} | {self.estado.value} | Prio: {self.prioridad} | CPU: {self.tiempo_ejecutado}/{self.rafaga_cpu}ms | RAM: {self.memoria_requerida}MB"