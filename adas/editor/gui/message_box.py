from PySide6.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
    def __init__(self, title: str, text: str, buttons: QMessageBox.StandardButton, icon: QMessageBox.Icon):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(buttons)
        self.setIcon(icon)
