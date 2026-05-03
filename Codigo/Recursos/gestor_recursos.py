class GestorRecursos:
    def __init__(self, total_cpus=4, total_ram_mb=16384):
        self.total_cpus = total_cpus
        self.cpus_disponibles = total_cpus
        self.total_ram_mb = total_ram_mb
        self.ram_disponible_mb = total_ram_mb

    def ajustar_cpus(self, nuevo_total):
        # Calculamos la diferencia para no perder la cuenta de CPUs ocupados
        usados = self.total_cpus - self.cpus_disponibles
        self.total_cpus = nuevo_total
        self.cpus_disponibles = nuevo_total - usados

    def solicitar_recursos(self, pcb):
        if self.ram_disponible_mb >= pcb.memoria_requerida and self.cpus_disponibles > 0:
            self.ram_disponible_mb -= pcb.memoria_requerida
            self.cpus_disponibles -= 1
            return True
        return False

    def liberar_recursos(self, pcb):
        self.ram_disponible_mb += pcb.memoria_requerida
        self.cpus_disponibles += 1
        if self.cpus_disponibles > self.total_cpus:
            self.cpus_disponibles = self.total_cpus