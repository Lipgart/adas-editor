from enum import Enum

from PySide6.QtWidgets import QWidget, QStackedLayout, QDialog, QTabWidget
from PySide6.QtCore import Qt, QTimer

from adas.editor.gui import ConnectionWidget, ConnectionDialog, VideoServerWidget, View360Widget


class State(Enum):
    Disconnected = 0
    Connected = 1


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.state = State.Disconnected

        self.layout = QStackedLayout()
        connection_widget = ConnectionWidget(self.connect)
        self.tab_widget = QTabWidget()

        self.layout.addWidget(connection_widget)
        self.layout.addWidget(self.tab_widget)

        self.setLayout(self.layout)

        QTimer.singleShot(0, self.connect)

    def connect(self):
        connect_dialog = ConnectionDialog()
        if connect_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        host = connect_dialog.get_host()
        video_server_config = VideoServerWidget(host)
        view360_config = View360Widget(host)

        self.tab_widget.clear()
        self.tab_widget.addTab(view360_config, 'Конфигурация кругового обзора')
        self.tab_widget.addTab(video_server_config, 'Конфигурация видео-сервера')
        self.layout.setCurrentIndex(State.Connected.value)

