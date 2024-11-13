import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QTabWidget, QHBoxLayout
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)


class GraphTab(QWidget):
    def __init__(self, parent=None, func="sin"):
        super().__init__(parent)
        self.func = func
        self.init_ui()
        self.x_data = np.linspace(0, 10, 100)
        self.y_data = np.zeros_like(self.x_data)
        self.line, = self.canvas.ax.plot([], [], label=f"{func}(x)")
        self.ani = None  # Для хранения анимации

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Создаем холст для графика
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

        # Добавляем кнопку для начала/остановки анимации
        self.start_button = QPushButton("Начать анимацию")
        self.start_button.clicked.connect(self.start_animation)
        layout.addWidget(self.start_button)

        # Добавляем кнопку для остановки анимации
        self.stop_button = QPushButton("Остановить анимацию")
        self.stop_button.clicked.connect(self.stop_animation)
        layout.addWidget(self.stop_button)

    def start_animation(self):
        # Запускаем анимацию
        self.ani = FuncAnimation(
            self.canvas.fig, self.update_graph,
            frames=np.linspace(0, 2 * np.pi, 128),
            blit=False, interval=50
        )
        self.canvas.draw()

    def stop_animation(self):
        # Останавливаем анимацию
        if self.ani:
            self.ani.event_source.stop()
            self.ani = None

    def update_graph(self, frame):
        # Обновляем данные графика
        if self.func == "sin":
            self.y_data = np.sin(self.x_data + frame)
            self.line.set_color("blue")
        elif self.func == "cos":
            self.y_data = np.cos(self.x_data + frame)
            self.line.set_color("red")

        # Обновляем данные линии
        self.line.set_data(self.x_data, self.y_data)

        # Настройки осей
        self.canvas.ax.set_xlim(0, 10)
        self.canvas.ax.set_ylim(-1.5, 1.5)
        self.canvas.ax.set_title(f"Анимация {self.func}(x)")
        self.canvas.ax.set_xlabel("X")
        self.canvas.ax.set_ylabel("Y")
        self.canvas.ax.legend()

        # Перерисовываем холст
        self.canvas.draw()


class GraphApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SCADA")
        self.setGeometry(100, 100, 800, 600)

        # Создаем центральный виджет и компоновку
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Создаем QTabWidget для вкладок
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Добавляем вкладки с анимацией
        self.add_graph_tab("sin(x)", "sin")
        self.add_graph_tab("cos(x)", "cos")

    def add_graph_tab(self, title, func):
        tab = GraphTab(self.tabs, func)
        self.tabs.addTab(tab, title)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphApp()
    window.show()
    sys.exit(app.exec_())
