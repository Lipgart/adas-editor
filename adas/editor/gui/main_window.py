from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar
from PySide6.QtCore import Qt, QSize

from adas.editor.gui import MainWidget
from adas.editor.gui import palette


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ADAS Editor')

        # self.setStyleSheet("border: 1px solid red")

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

    def sizeHint(self):
        return QSize(1280, 850)
