import tkinter as tk
from tkinter import ttk, messagebox
import threading
from Procesos.pcb import PCB
from Algoritmos.fcfs import FCFS
from Algoritmos.sjf import SJF
from Algoritmos.round_robin import RoundRobin
from Algoritmos.prioridades import Prioridades
from IPC.productor_consumidor import ejecutar_demostracion_ipc

class SimuladorGUI:
    def __init__(self, root, planificador, gestor_recursos):
        self.root = root
        self.root.title("Simulador de Gestor de Procesos - SO")
        self.root.geometry("950x750") # Un poco más alta para los logs
        
        self.planificador = planificador
        self.recursos = gestor_recursos
        self.procesos_historial = [] 
        
        self._construir_interfaz()
        self.actualizar_recursos()
        self.escribir_log("Sistemas iniciado. Listo para crear procesos...")

    def _construir_interfaz(self):
        # --- Panel Superior: Creación ---
        panel_creacion = tk.LabelFrame(self.root, text="1. Operaciones sobre Procesos", padx=10, pady=10)
        panel_creacion.pack(fill="x", padx=10, pady=5)
        
        tk.Label(panel_creacion, text="Nombre:").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(panel_creacion, width=12)
        self.entry_nombre.grid(row=0, column=1, padx=5)
        
        tk.Label(panel_creacion, text="Prio:").grid(row=0, column=2)
        self.entry_prio = tk.Entry(panel_creacion, width=5)
        self.entry_prio.grid(row=0, column=3, padx=5)
        
        tk.Label(panel_creacion, text="CPU (ms):").grid(row=0, column=4)
        self.entry_rafaga = tk.Entry(panel_creacion, width=8)
        self.entry_rafaga.grid(row=0, column=5, padx=5)
        
        tk.Label(panel_creacion, text="RAM (MB):").grid(row=0, column=6)
        self.entry_ram = tk.Entry(panel_creacion, width=8)
        self.entry_ram.grid(row=0, column=7, padx=5)
        
        btn_crear = tk.Button(panel_creacion, text="Crear Proceso", command=self.crear_proceso, bg="lightblue")
        btn_crear.grid(row=0, column=8, padx=10)

        # --- Panel Medio: Recursos y Algoritmos ---
        panel_medio = tk.Frame(self.root)
        panel_medio.pack(fill="x", padx=10, pady=5)
        
        panel_recursos = tk.LabelFrame(panel_medio, text="2. Estado de Recursos", padx=10, pady=10)
        panel_recursos.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.lbl_cpu = tk.Label(panel_recursos, text="CPU: --", font=("Arial", 10, "bold"))
        self.lbl_cpu.pack(anchor="w")
        self.lbl_ram = tk.Label(panel_recursos, text="RAM: --", font=("Arial", 10, "bold"))
        self.lbl_ram.pack(anchor="w")
        
        panel_algo = tk.LabelFrame(panel_medio, text="3. Algoritmo de Planificación", padx=10, pady=10)
        panel_algo.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self.combo_algo = ttk.Combobox(panel_algo, values=["FCFS", "SJF", "Round Robin", "Prioridades"], state="readonly")
        self.combo_algo.current(0)
        self.combo_algo.pack(side="left", padx=5)
        tk.Button(panel_algo, text="Cambiar", command=self.cambiar_algoritmo).pack(side="left")

        # --- Panel Central: Tabla ---
        panel_tabla = tk.LabelFrame(self.root, text="Cola de Procesos", padx=10, pady=10)
        panel_tabla.pack(fill="both", expand=True, padx=10, pady=5)
        
        columnas = ("PID", "Nombre", "Estado", "Prioridad", "Ráfaga", "RAM")
        self.tree = ttk.Treeview(panel_tabla, columns=columnas, show="headings", height=6)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # --- Panel Inferior: Consola de Logs ---
        panel_logs = tk.LabelFrame(self.root, text="Logs del Sistema / IPC", padx=10, pady=10)
        panel_logs.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt_logs = tk.Text(panel_logs, height=10, state="disabled", bg="black", fg="lightgreen", font=("Consolas", 10))
        scroll = tk.Scrollbar(panel_logs, command=self.txt_logs.yview)
        self.txt_logs.configure(yscrollcommand=scroll.set)
        self.txt_logs.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # --- Botones de Acción ---
        panel_btns = tk.Frame(self.root)
        panel_btns.pack(fill="x", padx=10, pady=10)
        
        tk.Button(panel_btns, text="▶ Despachar Siguiente", command=self.despachar_proceso, bg="lightgreen", font=("Arial", 10, "bold")).pack(side="left")
        tk.Button(panel_btns, text="Ejecutar Demo IPC", command=self.lanzar_demo_ipc, bg="salmon").pack(side="right")

    def escribir_log(self, mensaje):
        self.txt_logs.config(state="normal")
        self.txt_logs.insert("end", f"> {mensaje}\n")
        self.txt_logs.see("end")
        self.txt_logs.config(state="disabled")

    def actualizar_recursos(self):
        self.lbl_cpu.config(text=f"CPU Disponible: {self.recursos.cpus_disponibles} / {self.recursos.total_cpus}")
        self.lbl_ram.config(text=f"RAM Disponible: {self.recursos.ram_disponible_mb} / {self.recursos.total_ram_mb} MB")

    def actualizar_tabla(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for p in self.procesos_historial:
            self.tree.insert("", "end", values=(p.pid, p.nombre, p.estado.value, p.prioridad, f"{p.rafaga_cpu}ms", f"{p.memoria_requerida}MB"))

    def crear_proceso(self):
        try:
            nombre = self.entry_nombre.get()
            prio = int(self.entry_prio.get())
            rafaga = int(self.entry_rafaga.get())
            ram = int(self.entry_ram.get())
            
            p = PCB(nombre, prio, rafaga, ram)
            if self.recursos.solicitar_recursos(p):
                self.planificador.agregar_proceso(p)
                self.procesos_historial.append(p)
                self.escribir_log(f"Proceso '{nombre}' (PID {p.pid}) creado y recursos asignados.")
                self.actualizar_recursos()
                self.actualizar_tabla()
            else:
                self.escribir_log(f"FALLO: No hay recursos suficientes para '{nombre}'.")
        except:
            messagebox.showwarning("Error", "Datos inválidos.")

    def cambiar_algoritmo(self):
        s = self.combo_algo.get()
        if s == "FCFS": algo = FCFS()
        elif s == "SJF": algo = SJF()
        elif s == "Round Robin": algo = RoundRobin(quantum=4)
        else: algo = Prioridades()
        
        self.planificador.cambiar_algoritmo(algo)
        self.escribir_log(f"Planificador cambiado a algoritmo: {s}")

    def despachar_proceso(self):
        p = self.planificador.despachar_siguiente()
        if p:
            self.escribir_log(f"Ejecutando PID {p.pid} ({p.nombre})...")
            self.actualizar_tabla()
            
            # Simulación: termina después de un pequeño delay
            def finalizar():
                p.ejecutar(p.rafaga_cpu)
                self.recursos.liberar_recursos(p)
                self.escribir_log(f"PID {p.pid} finalizado. Recursos liberados.")
                self.actualizar_recursos()
                self.actualizar_tabla()
            
            self.root.after(1000, finalizar)
        else:
            self.escribir_log("Planificador: No hay procesos listos.")

    def lanzar_demo_ipc(self):
        threading.Thread(target=ejecutar_demostracion_ipc, args=(self.escribir_log,)).start()