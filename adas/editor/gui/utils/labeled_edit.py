from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QSizePolicy


class LabeledEdit(QWidget):
    def __init__(self, text: str, value: str = None, tip: str = None, label_width: int = None, edit_width: int = None):
        super().__init__()

        label = QLabel(text)
        label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))

        if label_width is not None:
            label.setFixedWidth(label_width)

        self.edit = QLineEdit()
        self.edit.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.edit.setAlignment(Qt.AlignmentFlag.AlignRight)

        if value is not None:
            self.edit.setText(value)

        if tip is not None:
            self.edit.setPlaceholderText(tip)

        if edit_width is not None:
            self.edit.setFixedWidth(edit_width)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.edit, Qt.AlignmentFlag.AlignLeft)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))

        self.setLayout(layout)

    def set(self, text):
        self.edit.setText(str(text))

    def get(self):
        return self.edit.text()
