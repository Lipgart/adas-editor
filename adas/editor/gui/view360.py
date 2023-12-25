import json

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QScrollArea, QGroupBox, QPushButton, QStyle, \
    QHBoxLayout, QMessageBox, QFileDialog, QLabel, QLineEdit, QSizePolicy
from adas.config import ParseError

from adas.config.view360 import ExternalConnector, Config, pack, parse

from adas.editor.gui.utils import LabeledEdit, MessageBox


def remove_trailing_zeros(value):
    i, p = f'{value:.5f}'.split('.')
    p = p[0] + p[1:].rstrip('0')
    return '.'.join([i, p])


class SidedVectorEdit(QGroupBox):
    def __init__(self, title, values):
        super().__init__()
        self.setTitle(title)

        names = { 'left': 'Левая', 'front': 'Передняя', 'right': 'Правая', 'rear': 'Задняя' }

        LABEL_WIDTH = 100
        EDIT_WIDTH = 100

        layout = QVBoxLayout()

        self.edits = {}
        for side in ['left', 'front', 'right', 'rear']:
            vector = values.Get(side)
            vector_layout = QHBoxLayout()
            label = QLabel(names[side])
            label.setFixedWidth(LABEL_WIDTH)
            vector_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)

            self.edits[side] = []

            if isinstance(vector, list):
                for value in vector:
                    value_widget = QLineEdit()
                    value_widget.setAlignment(Qt.AlignmentFlag.AlignRight)
                    value_widget.setText(remove_trailing_zeros(value))
                    value_widget.setFixedWidth(EDIT_WIDTH)
                    vector_layout.addWidget(value_widget, alignment=Qt.AlignmentFlag.AlignRight)
                    self.edits[side].append(value_widget)
            else:
                value = vector
                value_widget = QLineEdit()
                value_widget.setAlignment(Qt.AlignmentFlag.AlignRight)
                value_widget.setText(remove_trailing_zeros(value))
                value_widget.setFixedWidth(EDIT_WIDTH)
                vector_layout.addWidget(value_widget, alignment=Qt.AlignmentFlag.AlignRight)
                self.edits[side].append(value_widget)

            vector_widget = QWidget()
            vector_widget.setLayout(vector_layout)
            layout.addWidget(vector_widget, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)


class SidedMatrixEdit(QGroupBox):
    def __init__(self, title, values):
        super().__init__()
        self.setTitle(title)

        names = { 'left': 'Левая', 'front': 'Передняя', 'right': 'Правая', 'rear': 'Задняя' }

        LABEL_WIDTH = 100
        EDIT_WIDTH = 100

        layout = QVBoxLayout()

        self.edits = {}
        for side in ['left', 'front', 'right', 'rear']:
            matrix = values.Get(side)

            side_layout = QHBoxLayout()
            label = QLabel(names[side])
            label.setFixedWidth(LABEL_WIDTH)
            side_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

            row_layout = QVBoxLayout()

            self.edits[side] = []

            for row in matrix:
                column_layout = QHBoxLayout()

                row_widgets = []

                for value in row:
                    value_widget = QLineEdit()
                    value_widget.setAlignment(Qt.AlignmentFlag.AlignRight)
                    value_widget.setText(remove_trailing_zeros(value))
                    value_widget.setFixedWidth(EDIT_WIDTH)
                    column_layout.addWidget(value_widget, alignment=Qt.AlignmentFlag.AlignRight)
                    row_widgets.append(value_widget)

                column_widget = QWidget()
                column_widget.setLayout(column_layout)
                row_layout.addWidget(column_widget)

                self.edits[side].append(row_widgets)

            matrix_widget = QWidget()
            matrix_widget.setLayout(row_layout)

            side_layout.addWidget(matrix_widget, alignment=Qt.AlignmentFlag.AlignLeft)
            side_widget = QWidget()
            side_widget.setLayout(side_layout)
            layout.addWidget(side_widget, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)


class ConfigWidget(QWidget):
    def __init__(self, config: Config):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        first_column_layout = QVBoxLayout()
        first_column_widget = QFrame()
        first_column_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        first_column_widget.setLayout(first_column_layout)
        layout.addWidget(first_column_widget)

        second_column_layout = QVBoxLayout()
        second_column_widget = QFrame()
        second_column_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        second_column_widget.setLayout(second_column_layout)
        layout.addWidget(second_column_widget)

        third_column_layout = QVBoxLayout()
        third_column_widget = QFrame()
        third_column_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        third_column_widget.setLayout(third_column_layout)
        layout.addWidget(third_column_widget)

        fourth_column_layout = QVBoxLayout()
        fourth_column_widget = QFrame()
        fourth_column_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        fourth_column_widget.setLayout(fourth_column_layout)
        layout.addWidget(fourth_column_widget)

        LABEL_WIDTH = 120
        EDIT_WIDTH = 100

        # --- First column --------------------------------------------------------------------------------------------
        # Slice
        self.slice = LabeledEdit('Размер сетки', tip='70', value=str(config.Slice),
                                 label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        self.slice.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        first_column_layout.addWidget(self.slice, alignment=Qt.AlignmentFlag.AlignLeft)

        # Overlap
        overlap_layout = QVBoxLayout()
        self.overlap_leftup = LabeledEdit('Спереди слева', value=remove_trailing_zeros(config.Overlap.LeftUp),
                                          label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        overlap_layout.addWidget(self.overlap_leftup, alignment=Qt.AlignmentFlag.AlignLeft)
        self.overlap_rightup = LabeledEdit('Спереди справа', value=remove_trailing_zeros(config.Overlap.RightUp),
                                           label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        overlap_layout.addWidget(self.overlap_rightup, alignment=Qt.AlignmentFlag.AlignLeft)
        self.overlap_leftdown = LabeledEdit('Сзади слева', value=remove_trailing_zeros(config.Overlap.LeftDown),
                                            label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        overlap_layout.addWidget(self.overlap_leftdown, alignment=Qt.AlignmentFlag.AlignLeft)
        self.overlap_rightdown = LabeledEdit('Сзади справа', value=remove_trailing_zeros(config.Overlap.RightDown),
                                             label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        overlap_layout.addWidget(self.overlap_rightdown, alignment=Qt.AlignmentFlag.AlignLeft)

        overlap_group = QGroupBox()
        overlap_group.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        overlap_group.setTitle('Углы слияния')
        overlap_group.setLayout(overlap_layout)

        first_column_layout.addWidget(overlap_group, alignment=Qt.AlignmentFlag.AlignLeft)

        # Vehicle Size
        vehicle_size_layout = QVBoxLayout()
        self.vehicle_size_width = LabeledEdit('Ширина', value=remove_trailing_zeros(config.VehicleSize.Width),
                                              label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        vehicle_size_layout.addWidget(self.vehicle_size_width, alignment=Qt.AlignmentFlag.AlignLeft)
        self.vehicle_size_length = LabeledEdit('Длина', value=remove_trailing_zeros(config.VehicleSize.Length),
                                               label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        vehicle_size_layout.addWidget(self.vehicle_size_length, alignment=Qt.AlignmentFlag.AlignLeft)

        vehicle_size_group = QGroupBox()
        vehicle_size_group.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        vehicle_size_group.setTitle('Размеры борта')
        vehicle_size_group.setLayout(vehicle_size_layout)

        first_column_layout.addWidget(vehicle_size_group, alignment=Qt.AlignmentFlag.AlignLeft)

        # Vehicle Center
        vehicle_center_layout = QVBoxLayout()
        self.vehicle_center_x = LabeledEdit('X', value=remove_trailing_zeros(config.VehicleCenter.x),
                                            label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        vehicle_center_layout.addWidget(self.vehicle_center_x, alignment=Qt.AlignmentFlag.AlignLeft)
        self.vehicle_center_y = LabeledEdit('Y', value=remove_trailing_zeros(config.VehicleCenter.y),
                                            label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        vehicle_center_layout.addWidget(self.vehicle_center_y, alignment=Qt.AlignmentFlag.AlignLeft)

        vehicle_center_group = QGroupBox()
        vehicle_center_group.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        vehicle_center_group.setTitle('Координаты центра борта')
        vehicle_center_group.setLayout(vehicle_center_layout)

        first_column_layout.addWidget(vehicle_center_group, alignment=Qt.AlignmentFlag.AlignLeft)
        # Image Size
        image_size_layout = QVBoxLayout()
        self.image_size_width = LabeledEdit('X', value=str(config.ImSize.Width),
                                            label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        image_size_layout.addWidget(self.image_size_width, alignment=Qt.AlignmentFlag.AlignLeft)
        self.image_size_height = LabeledEdit('Y', value=str(config.ImSize.Height),
                                             label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        image_size_layout.addWidget(self.image_size_height, alignment=Qt.AlignmentFlag.AlignLeft)

        image_size_group = QGroupBox()
        image_size_group.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        image_size_group.setTitle('Размеры изображения')
        image_size_group.setLayout(image_size_layout)

        first_column_layout.addWidget(image_size_group, alignment=Qt.AlignmentFlag.AlignLeft)

        # --- Second column -------------------------------------------------------------------------------------------
        # Chessboard Square Size
        chessboard_square_size = LabeledEdit('Размер шахматного квадрата', value=str(config.CalibParams.ChessboardSquareSize),
                                            label_width=220, edit_width=EDIT_WIDTH)
        second_column_layout.addWidget(chessboard_square_size, alignment=Qt.AlignmentFlag.AlignLeft)

        # ChessBoard Size
        chessboard_size_layout = QVBoxLayout()
        self.chessboard_size_width = LabeledEdit('X', value=str(config.CalibParams.ChessboardSize[0]),
                                            label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        chessboard_size_layout.addWidget(self.chessboard_size_width, alignment=Qt.AlignmentFlag.AlignLeft)
        self.chessboard_size_height = LabeledEdit('Y', value=str(config.CalibParams.ChessboardSize[1]),
                                             label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        chessboard_size_layout.addWidget(self.chessboard_size_height, alignment=Qt.AlignmentFlag.AlignLeft)

        chessboard_size_group = QGroupBox()
        chessboard_size_group.setTitle('Размеры шахматной доски')
        chessboard_size_group.setLayout(chessboard_size_layout)

        second_column_layout.addWidget(chessboard_size_group, alignment=Qt.AlignmentFlag.AlignLeft)

        # Board Coordinates
        self.board_coordinates = SidedVectorEdit('Координаты установки полотен', config.CalibParams.ChessboardOrigin)
        second_column_layout.addWidget(self.board_coordinates, alignment=Qt.AlignmentFlag.AlignLeft)

        # Board Mount Height
        self.board_mount_height = SidedVectorEdit('Высоты установки полотен', config.CalibParams.ChessboardMountHeight)
        second_column_layout.addWidget(self.board_mount_height, alignment=Qt.AlignmentFlag.AlignLeft)

        # Camera Mount
        self.camera_mount = SidedVectorEdit('Координаты установки камер', config.CameraMount)
        second_column_layout.addWidget(self.camera_mount, alignment=Qt.AlignmentFlag.AlignLeft)

        # --- Third Column --------------------------------------------------------------------------------------------
        # Camera Matrix
        self.camera_matrix = SidedMatrixEdit('Матрицы камер', config.CalibParams.K)
        third_column_layout.addWidget(self.camera_matrix, alignment=Qt.AlignmentFlag.AlignLeft)

        # --- Fourth Column --------------------------------------------------------------------------------------------
        # Distortion Matrix
        self.distortion = SidedVectorEdit('Матрицы искажений', config.CalibParams.D)
        fourth_column_layout.addWidget(self.distortion, alignment=Qt.AlignmentFlag.AlignLeft)

        # Translation Matrix
        self.translation = SidedVectorEdit('Матрицы сдвигов', config.CalibParams.T)
        fourth_column_layout.addWidget(self.translation, alignment=Qt.AlignmentFlag.AlignLeft)

        # Rotation Matrix
        self.rotation = SidedVectorEdit('Матрицы поворотов', config.CalibParams.R)
        fourth_column_layout.addWidget(self.rotation, alignment=Qt.AlignmentFlag.AlignLeft)


class View360Widget(QFrame):
    def __init__(self, host: str):
        super().__init__()

        self.connector = ExternalConnector(host)

        buttons_layout = QHBoxLayout()

        get_button = QPushButton()
        get_button.setText('Получить конфигурацию')
        get_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_ArrowDown')))
        get_button.clicked.connect(self.get_config)
        set_button = QPushButton()
        set_button.setText('Установить конфигурацию')
        set_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_ArrowUp')))
        set_button.clicked.connect(self.set_config)
        file_load_button = QPushButton()
        file_load_button.setText('Загрузить из файла')
        file_load_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogOpenButton')))
        file_load_button.clicked.connect(self.load_file)
        file_save_button = QPushButton()
        file_save_button.setText('Сохранить в файл')
        file_save_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')))
        file_save_button.clicked.connect(self.save_file)
        calibrate_button = QPushButton()
        calibrate_button.setText('Калибровка')
        calibrate_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_CommandLink')))
        calibrate_button.clicked.connect(self.calibrate)

        buttons_layout.addWidget(get_button)
        buttons_layout.addWidget(set_button)
        buttons_layout.addWidget(file_load_button)
        buttons_layout.addWidget(file_save_button)
        buttons_layout.addWidget(calibrate_button)

        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)

        self.scroll_widget = QScrollArea()
        self.scroll_widget.setWidgetResizable(True)

        self.get_config()

        main_layout = QVBoxLayout()
        main_layout.addWidget(buttons_widget)
        main_layout.addWidget(self.scroll_widget)

        self.setLayout(main_layout)

    def get_config(self):
        self.scroll_widget.setWidget(ConfigWidget(self.connector.get_config()))
        # self.scroll_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_config(self):
        try:
            config = Config()

            self.connector.set_config(config)

            MessageBox('Успех', 'Конфигурация установлена.', QMessageBox.StandardButton.Ok,
                       QMessageBox.Icon.Information).exec()
        except IOError:
            MessageBox('Ошибка', 'Не удалось соединиться с сервером.', QMessageBox.StandardButton.Abort,
                       QMessageBox.Icon.Critical).exec()
        except RuntimeError as e:
            MessageBox('Ошибка', f'Не удалось установить конфигурацию ({e}).', QMessageBox.StandardButton.Abort,
                       QMessageBox.Icon.Critical).exec()
        except ValueError as e:
            MessageBox('Ошибка', f'Не удалось установить конфигурацию ({e}).', QMessageBox.StandardButton.Abort,
                       QMessageBox.Icon.Critical).exec()

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(caption='Загрузка конфигурации', filter="JSON (*.json)")

        try:
            with open(path, 'r') as f:
                config = parse(json.load(f))

        except ParseError as e:
            MessageBox('Ошибка', f'Не удалось загрузить конфигурацию ({e}).', QMessageBox.StandardButton.Abort,
                       QMessageBox.Icon.Critical).exec()

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(caption='Сохранение конфигурации', filter="JSON (*.json)")

        if path[-4:] != 'json':
            path += 'json'

        try:
            config = Config()

            with open(path, 'w') as f:
                f.write(json.dumps(pack(config), indent=2))
        except ValueError as e:
            MessageBox('Ошибка', f'Не удалось установить конфигурацию ({e}).', QMessageBox.StandardButton.Abort,
                       QMessageBox.Icon.Critical).exec()

    def calibrate(self):
        pass