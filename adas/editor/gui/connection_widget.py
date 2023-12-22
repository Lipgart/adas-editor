from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QSize


class ConnectionWidget(QWidget):
    def __init__(self, connect_callback):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel()
        label.setText("Нет соединения.")
        button = QPushButton()
        button.setText("Соединение")
        button.clicked.connect(connect_callback)

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button)

        main_widget = QWidget()
        main_widget.setFixedSize(QSize(300, 100))
        main_widget.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(main_widget, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(main_layout)
