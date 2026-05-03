import sys
import os
import tkinter as tk

# --- SOLUCIÓN DE RUTAS ---
directorio_actual = os.path.dirname(os.path.abspath(__file__))
if directorio_actual not in sys.path:
    sys.path.insert(0, directorio_actual)

from Recursos.gestor_recursos import GestorRecursos
from Algoritmos.fcfs import FCFS
from Algoritmos.planificador import Planificador
from Interfaz.gui import SimuladorGUI

def main():
    print("Iniciando Simulador Multiprocesador - UAT")
    recursos_sistema = GestorRecursos()
    
    algoritmo_inicial = FCFS()
    planificador_sistema = Planificador(algoritmo=algoritmo_inicial)
    
    root = tk.Tk()
    app = SimuladorGUI(root, planificador_sistema, recursos_sistema)
    root.mainloop()

if __name__ == "__main__":
    main()