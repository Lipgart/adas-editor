from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout


class LabeledEdit(QWidget):
    def __init__(self, text: str, value: str = None, tip: str = None, label_width: int = None, edit_width: int = None):
        super().__init__()

        label = QLabel(text)

        if label_width is not None:
            label.setFixedWidth(label_width)

        self.edit = QLineEdit()

        if value is not None:
            self.edit.setText(value)

        if tip is not None:
            self.edit.setPlaceholderText(tip)

        if edit_width is not None:
            self.edit.setFixedWidth(edit_width)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.edit, Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def set(self, text):
        self.edit.setText(str(text))

    def get(self):
        return self.edit.text()
