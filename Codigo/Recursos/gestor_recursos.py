class GestorRecursos:
    """
    Administra los recursos del sistema (CPU y Memoria RAM).
    Permite la asignación y liberación dinámica para los procesos, simulando
    la detección de conflictos cuando no hay recursos suficientes.
    """
    
    def __init__(self, total_cpus: int, total_ram_mb: int):
        self.total_cpus = total_cpus
        self.total_ram_mb = total_ram_mb
        
        # Contadores de recursos actualmente disponibles
        self.cpus_disponibles = total_cpus
        self.ram_disponible_mb = total_ram_mb

    def solicitar_recursos(self, pcb) -> bool:
        """
        Verifica si hay recursos suficientes para el proceso.
        Si hay, los asigna y retorna True. Si hay conflicto, retorna False.
        """
        if self.cpus_disponibles >= pcb.cpu_asignada and self.ram_disponible_mb >= pcb.memoria_requerida:
            self.cpus_disponibles -= pcb.cpu_asignada
            self.ram_disponible_mb -= pcb.memoria_requerida
            print(f"✅ [Recursos] Asignados a {pcb.nombre}. Disponibles: {self.cpus_disponibles} CPUs, {self.ram_disponible_mb}MB RAM.")
            return True
        else:
            # Detección de conflicto: No hay suficientes recursos
            print(f"❌ [Recursos] Conflicto: Recursos insuficientes para {pcb.nombre}.")
            return False

    def liberar_recursos(self, pcb):
        """
        Devuelve los recursos al pool general cuando el proceso termina o se suspende.
        """
        self.cpus_disponibles += pcb.cpu_asignada
        self.ram_disponible_mb += pcb.memoria_requerida
        
        # Medida de seguridad para no exceder el total original por algún error de cálculo
        self.cpus_disponibles = min(self.cpus_disponibles, self.total_cpus)
        self.ram_disponible_mb = min(self.ram_disponible_mb, self.total_ram_mb)
        
        print(f"♻️ [Recursos] Liberados por {pcb.nombre}. Disponibles: {self.cpus_disponibles} CPUs, {self.ram_disponible_mb}MB RAM.")