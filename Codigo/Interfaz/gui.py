import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Importaciones de los módulos del proyecto
from Procesos.pcb import PCB
from Algoritmos.fcfs import FCFS
from Algoritmos.sjf import SJF
from Algoritmos.round_robin import RoundRobin
from Algoritmos.prioridades import Prioridades
from IPC.Productor_Consumidor import ejecutar_demostracion_ipc

class SimuladorGUI:
    def __init__(self, root, planificador, gestor_recursos):
        self.root = root
        self.root.title("Simulador de Sistemas Operativos Multiprocesador - UAT")
        self.root.geometry("1000x850")
        
        self.planificador = planificador
        self.recursos = gestor_recursos
        self.procesos_historial = [] 
        
        self._construir_interfaz()
        self.actualizar_recursos()

    def _construir_interfaz(self):
        # --- 1. Panel de Control de Procesos ---
        panel_creacion = tk.LabelFrame(self.root, text="1. Operaciones sobre Procesos", padx=10, pady=10)
        panel_creacion.pack(fill="x", padx=10, pady=5)
        
        tk.Label(panel_creacion, text="Nombre:").grid(row=0, column=0)
        self.ent_nom = tk.Entry(panel_creacion, width=12); self.ent_nom.grid(row=0, column=1, padx=5)
        
        tk.Label(panel_creacion, text="Prio:").grid(row=0, column=2)
        self.ent_pri = tk.Entry(panel_creacion, width=5); self.ent_pri.grid(row=0, column=3, padx=5)
        
        tk.Label(panel_creacion, text="CPU (ms):").grid(row=0, column=4)
        self.ent_raf = tk.Entry(panel_creacion, width=8); self.ent_raf.grid(row=0, column=5, padx=5)
        
        tk.Label(panel_creacion, text="RAM (MB):").grid(row=0, column=6)
        self.ent_ram = tk.Entry(panel_creacion, width=8); self.ent_ram.grid(row=0, column=7, padx=5)
        
        btn_crear = tk.Button(panel_creacion, text="Crear Proceso", command=self.crear_proceso, bg="lightblue")
        btn_crear.grid(row=0, column=8, padx=10)

        # --- 2. Monitor y Configuración de Hardware Dinámico ---
        panel_medio = tk.Frame(self.root)
        panel_medio.pack(fill="x", padx=10, pady=5)
        
        panel_hw = tk.LabelFrame(panel_medio, text="2. Configuración de Hardware", padx=10, pady=10)
        panel_hw.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        f_config = tk.Frame(panel_hw); f_config.pack(fill="x")
        
        # Ajuste de CPU
        tk.Label(f_config, text="Núcleos CPU:").pack(side="left")
        self.ent_hw_cpu = tk.Entry(f_config, width=5)
        self.ent_hw_cpu.insert(0, str(self.recursos.total_cpus))
        self.ent_hw_cpu.pack(side="left", padx=5)
        
        # Ajuste de RAM
        tk.Label(f_config, text="Total RAM (MB):").pack(side="left", padx=(10, 0))
        self.ent_hw_ram = tk.Entry(f_config, width=8)
        self.ent_hw_ram.insert(0, str(self.recursos.total_ram_mb))
        self.ent_hw_ram.pack(side="left", padx=5)
        
        tk.Button(f_config, text="Aplicar Hardware", command=self.aplicar_hardware, bg="silver").pack(side="left", padx=10)

        self.lbl_estado_hw = tk.Label(panel_hw, text="Estado: --", font=("Arial", 10, "bold"), fg="darkgreen")
        self.lbl_estado_hw.pack(anchor="w", pady=(5, 0))

        # --- 3. Panel de Algoritmos ---
        panel_algo = tk.LabelFrame(panel_medio, text="3. Algoritmo de Planificación", padx=10, pady=10)
        panel_algo.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.combo_algo = ttk.Combobox(panel_algo, values=["FCFS", "SJF", "Round Robin", "Prioridades"], state="readonly")
        self.combo_algo.current(0); self.combo_algo.pack(side="left", padx=5)
        tk.Button(panel_algo, text="Cambiar", command=self.cambiar_algo).pack(side="left")

        # --- 4. Tabla de Procesos ---
        self.tree = ttk.Treeview(self.root, columns=("PID", "Nombre", "Estado", "Prio", "Ráfaga", "RAM"), show="headings", height=8)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # --- 5. Consola de Logs Estilo Terminal ---
        panel_logs = tk.LabelFrame(self.root, text="Consola de Eventos del Sistema", padx=10, pady=10)
        panel_logs.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt_logs = tk.Text(panel_logs, height=10, state="disabled", bg="black", fg="lightgreen", font=("Consolas", 10))
        self.txt_logs.pack(side="left", fill="both", expand=True)
        scroll = tk.Scrollbar(panel_logs, command=self.txt_logs.yview)
        scroll.pack(side="right", fill="y")
        self.txt_logs.configure(yscrollcommand=scroll.set)

        # --- 6. Botones de Acción ---
        panel_btns = tk.Frame(self.root); panel_btns.pack(fill="x", padx=10, pady=10)
        tk.Button(panel_btns, text="▶ Despachar Siguiente", command=self.despachar, bg="lightgreen", font=("Arial", 10, "bold")).pack(side="left")
        tk.Button(panel_btns, text="Ejecutar Demo IPC", command=self.demo, bg="salmon").pack(side="right")

    def escribir_log(self, mensaje):
        """Añade un mensaje a la consola negra de la interfaz."""
        self.txt_logs.config(state="normal")
        self.txt_logs.insert("end", f"> {mensaje}\n")
        self.txt_logs.see("end")
        self.txt_logs.config(state="disabled")

    def aplicar_hardware(self):
        """Actualiza los recursos del sistema desde la interfaz."""
        try:
            nuevos_cpus = int(self.ent_hw_cpu.get())
            nueva_ram = int(self.ent_hw_ram.get())
            
            if nuevos_cpus <= 0 or nueva_ram <= 0:
                raise ValueError
            
            # Usamos la nueva función del gestor para actualizar núcleos y memoria
            self.recursos.ajustar_cpus(nuevos_cpus)
            self.recursos.total_ram_mb = nueva_ram
            self.recursos.ram_disponible_mb = nueva_ram # Reinicio de RAM para la prueba
            
            self.escribir_log(f"Hardware actualizado: {nuevos_cpus} CPUs y {nueva_ram} MB RAM.")
            self.actualizar_recursos()
        except ValueError:
            messagebox.showerror("Error de Configuración", "Ingresa valores numéricos positivos.")

    def actualizar_recursos(self):
        """Refresca las etiquetas de estado del hardware."""
        texto = f"CPUs Libres: {self.recursos.cpus_disponibles}/{self.recursos.total_cpus} | "
        texto += f"RAM: {self.recursos.ram_disponible_mb}/{self.recursos.total_ram_mb} MB"
        self.lbl_estado_hw.config(text=texto)

    def actualizar_tabla(self):
        """Refresca la lista de procesos en el Treeview."""
        self.tree.delete(*self.tree.get_children())
        for p in self.procesos_historial:
            self.tree.insert("", "end", values=(p.pid, p.nombre, p.estado.value, p.prioridad, f"{p.rafaga_cpu}ms", f"{p.memoria_requerida}MB"))

    def crear_proceso(self):
        """Toma los datos de los entries y crea un nuevo PCB."""
        try:
            nombre = self.ent_nom.get()
            prio = int(self.ent_pri.get())
            rafaga = int(self.ent_raf.get())
            ram = int(self.ent_ram.get())
            
            p = PCB(nombre, prio, rafaga, ram)
            if self.recursos.solicitar_recursos(p):
                self.planificador.agregar_proceso(p)
                self.procesos_historial.append(p)
                self.escribir_log(f"Proceso '{nombre}' (PID {p.pid}) admitido en el sistema.")
                self.actualizar_recursos()
                self.actualizar_tabla()
            else:
                self.escribir_log(f"ERROR: No hay recursos suficientes para el proceso '{nombre}'.")
        except ValueError:
            messagebox.showwarning("Datos Inválidos", "Por favor, llena todos los campos con números válidos.")

    def cambiar_algo(self):
        """Cambia el algoritmo de planificación activo."""
        seleccion = self.combo_algo.get()
        if seleccion == "FCFS": algo = FCFS()
        elif seleccion == "SJF": algo = SJF()
        elif seleccion == "Round Robin": algo = RoundRobin(quantum=4)
        else: algo = Prioridades()
        
        self.planificador.cambiar_algoritmo(algo)
        self.escribir_log(f"Algoritmo de planificación cambiado a: {seleccion}")

    def despachar(self):
        """Ejecuta el siguiente proceso en la cola."""
        p = self.planificador.despachar_siguiente()
        if p:
            self.escribir_log(f"Asignando CPU al proceso: {p.nombre} (PID {p.pid})")
            self.actualizar_tabla()
            # Simulamos el tiempo de ejecución con un retardo
            self.root.after(1200, lambda: self.finalizar_proceso(p))
        else:
            self.escribir_log("Aviso: No hay procesos listos en la cola.")

    def finalizar_proceso(self, p):
        """Libera los recursos y actualiza el estado al terminar un proceso."""
        p.ejecutar(p.rafaga_cpu)
        self.recursos.liberar_recursos(p)
        self.escribir_log(f"Proceso {p.nombre} finalizado exitosamente. Recursos liberados.")
        self.actualizar_recursos()
        self.actualizar_tabla()

    def demo(self):
        """Lanza la demostración de Productor-Consumidor en un hilo separado."""
        threading.Thread(target=ejecutar_demostracion_ipc, args=(self.escribir_log,), daemon=True).start()