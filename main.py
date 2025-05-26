import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from statistics import mean


class ProcesoThread(QThread):
    proceso_agregado = pyqtSignal(list)

    def __init__(self, proceso):
        super().__init__()
        self.proceso = proceso

    def run(self):
        # Simulación de operaciones intensivas
        self.proceso_agregado.emit(self.proceso)

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Planificador de Procesos")
        self.setGeometry(100, 100, 1000, 600)

        # Definir nombres de columnas y anchos predeterminados
        self.encabezados_procesos = ["Proceso", "Tiempo de\nLlegada", "Inicio", "Fin", "Tiempo de\nEjecución", "Tiempo en\nEspera", "Paro", "Porcentaje"]
        self.anchos_columnas = [100, 100, 100, 100, 100, 100, 100, 200]

        self.iniciarInterfaz()

    def iniciarInterfaz(self):
        # Botones
        hbox_botones = QHBoxLayout()
        self.nombres_botones = ["Agregar", "Terminar", "Pausar", "Continuar"]
        for nombre in self.nombres_botones:
            boton = QPushButton(nombre)
            hbox_botones.addWidget(boton)
            boton.clicked.connect(self.on_boton_clickeado)

        # Botón FCFS
        self.btn_fcfs = QPushButton("FCFS")
        self.btn_fcfs.clicked.connect(self.iniciar_FCFS)

        # Etiqueta para el ciclo
        self.etiqueta_ciclo = QLabel("Ciclo: ---")
        self.hbox_fcfs_ciclo = QHBoxLayout()
        self.hbox_fcfs_ciclo.addWidget(self.btn_fcfs)
        self.hbox_fcfs_ciclo.addWidget(self.etiqueta_ciclo)

        # Tabla de procesos
        self.tabla_procesos = QTableWidget()
        self.tabla_procesos.setColumnCount(len(self.encabezados_procesos))
        self.tabla_procesos.setHorizontalHeaderLabels(self.encabezados_procesos)

        # Establecer anchos de columnas
        for index, ancho in enumerate(self.anchos_columnas):
            self.tabla_procesos.setColumnWidth(index, ancho)

        # Tabla de promedios
        self.tabla_promedios = QTableWidget()
        self.tabla_promedios.setColumnCount(len(self.encabezados_procesos))
        self.tabla_promedios.setHorizontalHeaderLabels(self.encabezados_procesos)
        self.tabla_promedios.setRowCount(1)  # Una fila para el promedio
        self.tabla_promedios.setItem(0, 0, QTableWidgetItem("Promedio"))
        for i in range(1, len(self.encabezados_procesos)):
            self.tabla_promedios.setItem(0, i, QTableWidgetItem("---"))
        progreso = QProgressBar()
        progreso.setValue(0)
        self.tabla_promedios.setCellWidget(0, 7, progreso)

        # Establecer el tamaño de la tabla de promedios
        altura_total = self.tabla_promedios.verticalHeader().defaultSectionSize() + self.tabla_promedios.rowHeight(0) * 2
        self.tabla_promedios.setFixedHeight(altura_total)

        # Establecer modo de ajuste de tamaño de las secciones de la cabecera
        self.tabla_procesos.horizontalHeader().setStretchLastSection(True)
        self.tabla_procesos.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tabla_promedios.horizontalHeader().setStretchLastSection(True)
        self.tabla_promedios.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Diseño de la ventana
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_botones)
        vbox.addWidget(self.tabla_procesos)
        vbox.addLayout(self.hbox_fcfs_ciclo)
        vbox.addWidget(self.tabla_promedios)

        self.setLayout(vbox)

        self.proceso_actual = 0  # Variable para rastrear el índice del último proceso agregado
        self.ciclo_actual = 0
        self.procesos = []

    def on_boton_clickeado(self):
        sender = self.sender()
        self.pausa = 0
        self.terminar = 0
        if sender.text() == "Agregar":
            proceso_nombre = chr(ord('A') + self.proceso_actual)  # Convertir el índice actual a una letra mayúscula
            tiempo_llegada = str(random.randint(self.ciclo_actual, self.ciclo_actual + 5))  # Generar un tiempo de llegada aleatorio entre 0 y 20
            tiempo_ejecucion = str(random.randint(10, 15))  # Generar un tiempo de ejecución aleatorio entre 10 y 15
            proceso = [proceso_nombre, tiempo_llegada, "0", "0", tiempo_ejecucion, "0", "0", "0"]  # Ejemplo de proceso
            self.agregar_proceso(proceso)
            self.proceso_actual = (self.proceso_actual + 1) % 26  # Incrementar el índice y volver a "A" si alcanza "Z"
        if sender.text() == "Terminar":
            self.terminar = 1
        if sender.text() == "Pausar":
            self.pausa = 1
        if sender.text() == "Continuar":
            self.pausa = 0

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)
        self.agregar_proceso_tabla(proceso)  # Agregar el proceso a la tabla de procesos inmediatamente

    def actualizar_tabla(self, proceso):
        row_count = self.tabla_procesos.rowCount()
        self.tabla_procesos.setRowCount(row_count + 1)
        for col, valor in enumerate(proceso):
            item = QTableWidgetItem(valor)
            self.tabla_procesos.setItem(row_count, col, item)
        # Agregar barra de carga en la columna "Porcentaje"
        progreso = QProgressBar()
        progreso.setValue(0)
        self.tabla_procesos.setCellWidget(row_count, 7, progreso)
        self.tabla_procesos.sortItems(1)  # Ordenar por la columna 1 (tiempo de llegada)
        self.calcular_promedio()

    def inicializar_procesos(self):
        if self.ciclo_actual == 0:
            # Establecer todos los procesos en la tabla de procesos a "0":
            # en las columnas "Inicio", "Fin", "Espera", "Paro" y "Porcentaje"
            for i in range(self.tabla_procesos.rowCount()):
                for j in range(2, 7):  # Columnas desde "Inicio" hasta "Porcentaje"
                    if j != 4:  # Excluir la columna "Tiempo"
                        item = QTableWidgetItem("0")
                        self.tabla_procesos.setItem(i, j, item)
                self.tabla_procesos.cellWidget(i, 7).setValue(int(0))

    def eliminar_fila_seleccionada(self):
        selected_items = self.tabla_procesos.selectedItems()  # Obtener los elementos seleccionados
        if selected_items:  # Verificar si se ha seleccionado algún elemento
            row_index = selected_items[0].row()  # Obtener el índice de la fila seleccionada
            self.tabla_procesos.removeRow(row_index)  # Eliminar la fila seleccionada

    def logica_FCFS(self):
        # Ordenar la tabla "tabla_procesos" por la columna de tiempo de llegada
        # Lógica específica del algoritmo FCFS
        self.calcular_promedio()
        for i in range(self.tabla_procesos.rowCount()):
            proceso = [self.tabla_procesos.item(i, j).text() for j in range(self.tabla_procesos.columnCount())]
            if self.pausa == 1:
                proceso[5] = str(int(proceso[5]) + 1)
                self.tabla_procesos.setItem(i, 5, QTableWidgetItem(str(int(proceso[5]))))
                proceso[6] = str(self.ciclo_actual)
                self.tabla_procesos.setItem(i, 6, QTableWidgetItem(str(int(proceso[6]))))
                break
            elif self.terminar == 1:
                self.eliminar_fila_seleccionada()
                self.terminar = 0
                break
            elif proceso[7] != proceso[4] and int(proceso[1]) <= self.ciclo_actual:  # Si el proceso no ha completado su tiempo
                if proceso[7] == "0":
                    self.tabla_procesos.setItem(i, 2, QTableWidgetItem(str(self.ciclo_actual)))
                self.actualizar_progreso(proceso, i)
                if proceso[7] == proceso[4]:
                    self.tabla_procesos.setItem(i, 3, QTableWidgetItem(str(self.ciclo_actual + 1)))
                break
            # Conectar la señal itemSelectionChanged a la función eliminar_fila_seleccionada
            # self.tabla_procesos.itemSelectionChanged.connect(self.eliminar_fila_seleccionada)

    def actualizar_progreso(self, proceso, i):
        proceso[7] = str(int(proceso[7]) + 1)
        porcentaje = (int(proceso[7]) / int(proceso[4])) * 100
        self.tabla_procesos.cellWidget(i, 7).setValue(int(porcentaje))
        self.tabla_procesos.setItem(i, 7, QTableWidgetItem(str(int(proceso[7]))))

    def calcular_promedio(self):
        proceso_numeros = []
        for i in range(self.tabla_procesos.rowCount()):
            proceso = [self.tabla_procesos.item(i, j).text() for j in range(1, 8)]
            proceso_numeros.append([int(elemento) for elemento in proceso])
        # Transponer la lista para obtener las columnas
        columnas = zip(*proceso_numeros)
        # Calcular el promedio para cada columna
        promedios = [sum(columna) / len(columna) for columna in columnas]
        promedios_formateados = [format(promedio, ".2f") for promedio in promedios]
        for i in range(1, len(self.encabezados_procesos)):
            if i == len(self.encabezados_procesos) - 1:
                porcentaje_total = (float(promedios[6])/float(promedios[3])) * 100
                self.tabla_promedios.cellWidget(0, 7).setValue(int(porcentaje_total))
                porcentaje_total = format(porcentaje_total, ".2f")
                self.tabla_promedios.setItem(0, i, QTableWidgetItem(str(porcentaje_total)))

            else:
                self.tabla_promedios.setItem(0, i, QTableWidgetItem(str(promedios_formateados[i-1])))

    def iniciar_FCFS(self):
        self.inicializar_procesos()
        #self.tabla_procesos.sortItems(1)  # Ordenar por la columna 1 (tiempo de llegada)
        self.ciclo_actual = 0
        timer = QTimer(self)
        timer.timeout.connect(self.avanzar_ciclo)
        timer.start(1000)  # Establecer el intervalo del temporizador en 1 segundo

    def avanzar_ciclo(self):
        self.etiqueta_ciclo.setText("Ciclo: {}".format(self.ciclo_actual))
        self.logica_FCFS()
        self.ciclo_actual += 1

    def agregar_proceso_tabla(self, proceso):
        self.proceso_thread = ProcesoThread(proceso)
        self.proceso_thread.proceso_agregado.connect(self.actualizar_tabla)
        self.proceso_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventanaPrincipal = VentanaPrincipal()
    ventanaPrincipal.show()
    sys.exit(app.exec_())