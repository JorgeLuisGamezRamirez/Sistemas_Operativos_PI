import sys
import os
import tkinter as tk

# --- ESTO SOLUCIONA EL ERROR DE MÓDULOS ---
# Le dice a Python que mire una carpeta hacia atrás para encontrar IPC, Recursos, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ahora sí, las importaciones funcionarán sin problemas
from Recursos.gestor_recursos import GestorRecursos
from Algoritmos.fcfs import FCFS
from Algoritmos.planificador import Planificador
from Interfaz.gui import SimuladorGUI

def main():
    print("Iniciando Simulador de Gestor de Procesos...")
    
    # Inicializar hardware simulado
    recursos_sistema = GestorRecursos(total_cpus=2, total_ram_mb=4096)
    
    # Inicializar planificador
    algoritmo_inicial = FCFS()
    planificador_sistema = Planificador(algoritmo=algoritmo_inicial)
    
    # Levantar la ventana
    root = tk.Tk()
    app = SimuladorGUI(root, planificador_sistema, recursos_sistema)
    
    root.mainloop()

if __name__ == "__main__":
    main()