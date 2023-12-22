from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QTextEdit, QLineEdit, \
    QMessageBox, QStyle
from PySide6.QtCore import Qt, QSize

from adas.config import Checker
from adas.editor.gui import MessageBox


class ConnectionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.host = None

        self.setWindowTitle('Соединение')

        self.setFixedSize(QSize(400, 120))

        layout = QVBoxLayout()
        label = QLabel()
        label.setText("Введите IP адрес / хост:")
        self.host_edit = QLineEdit()
        self.host_edit.setText("localhost")
        self.host_edit.setPlaceholderText("0.0.0.0")

        button_layout = QHBoxLayout()
        accept_button = QPushButton()
        accept_button.setText("ОК")
        accept_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogApplyButton')))
        accept_button.clicked.connect(self.__connection_create)
        reject_button = QPushButton()
        reject_button.setText("Отмена")
        reject_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogCancelButton')))
        reject_button.clicked.connect(self.reject)

        button_layout.addWidget(accept_button)
        button_layout.addWidget(reject_button)
        buttons_widget = QWidget()
        buttons_widget.setLayout(button_layout)

        layout.addWidget(label)
        layout.addWidget(self.host_edit)
        layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def __connection_create(self) -> None:
        try:
            checker = Checker(self.host_edit.text())
            if checker.check():
                self.host = self.host_edit.text()
                self.accept()
            else:
                MessageBox('Ошибка', 'Соединение не установлено', QMessageBox.StandardButton.Close, QMessageBox.Icon.Critical).exec()
                self.reject()
        except Exception as e:
            MessageBox('Ошибка', 'Соединение не установлено', QMessageBox.StandardButton.Close, QMessageBox.Icon.Critical).exec()
            self.reject()

    def get_host(self):
        assert self.host is not None
        return self.host
