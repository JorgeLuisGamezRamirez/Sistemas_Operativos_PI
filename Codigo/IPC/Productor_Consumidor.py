import threading
import time
import random

class BufferCompartido:
    def __init__(self, capacidad: int = 5, callback_log=None):
        self.capacidad = capacidad
        self.buffer = []
        self.mutex = threading.Lock()
        self.espacios_vacios = threading.Semaphore(capacidad)
        self.elementos_llenos = threading.Semaphore(0)
        self.callback_log = callback_log # Función de la GUI para escribir

    def producir(self, id_productor: int, item: str):
        self.espacios_vacios.acquire()
        self.mutex.acquire()
        
        self.buffer.append(item)
        msg = f"🟢 [Productor {id_productor}] produjo: '{item}'. Buffer: {len(self.buffer)}/{self.capacidad}"
        
        if self.callback_log:
            self.callback_log(msg)
        else:
            print(msg)
            
        self.mutex.release()
        self.elementos_llenos.release()
        time.sleep(random.uniform(0.1, 0.4))

    def consumir(self, id_consumidor: int) -> str:
        self.elementos_llenos.acquire()
        self.mutex.acquire()
        
        item = self.buffer.pop(0)
        msg = f"🔴 [Consumidor {id_consumidor}] consumió: '{item}'. Buffer: {len(self.buffer)}/{self.capacidad}"
        
        if self.callback_log:
            self.callback_log(msg)
        else:
            print(msg)
            
        self.mutex.release()
        self.espacios_vacios.release()
        time.sleep(random.uniform(0.1, 0.4))
        return item

def ejecutar_demostracion_ipc(callback_log=None):
    """Ejecuta la demo enviando los resultados al callback de la GUI."""
    if callback_log:
        callback_log("=== INICIANDO DEMOSTRACIÓN IPC (PRODUCTOR-CONSUMIDOR) ===")
    
    buffer = BufferCompartido(capacidad=5, callback_log=callback_log)
    
    def tarea_productor(id_prod):
        for i in range(5):
            buffer.producir(id_prod, f"Dato_{id_prod}_{i+1}")
            
    def tarea_consumidor(id_cons):
        for _ in range(5):
            buffer.consumir(id_cons)

    productores = [threading.Thread(target=tarea_productor, args=(i,)) for i in range(1, 3)]
    consumidores = [threading.Thread(target=tarea_consumidor, args=(i,)) for i in range(1, 3)]
    
    for t in productores + consumidores: t.start()
    for t in productores + consumidores: t.join()
    
    if callback_log:
        callback_log("=== FIN DE LA DEMOSTRACIÓN IPC ===")