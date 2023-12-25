import json

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QScrollArea, QGroupBox, QPushButton, QStyle, \
    QHBoxLayout, QMessageBox, QFileDialog
from adas.config import ParseError

from adas.config.video_server import ExternalConnector, Config, StreamConfig, Shape, pack, parse

from adas.editor.gui.utils import LabeledEdit, MessageBox


class StreamConfigWidget(QFrame):
    def __init__(self, config: StreamConfig = None, video_server=None):
        super().__init__()

        self.video_server = video_server
        self.setFrameStyle(QFrame.Shape.Box)
        self.setFixedWidth(510)

        LABEL_WIDTH = 150
        EDIT_WIDTH = 300
        FRAME_EDIT_WIDTH = 100

        self.identifier = LabeledEdit('Идентификатор', tip='front', label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)

        stream_box = QGroupBox()
        stream_box.setTitle('Параметры потока')
        stream_layout = QVBoxLayout()
        self.source = LabeledEdit('Источник', tip='rtspsrc', label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        self.parser = LabeledEdit('Парсер', label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        self.decoder = LabeledEdit('Декодер', tip='decodebin', label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        self.postprocessor = LabeledEdit('Обработчик', label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)
        self.sink = LabeledEdit('Потребитель', tip='appsink', label_width=LABEL_WIDTH, edit_width=EDIT_WIDTH)

        stream_layout.addWidget(self.source, alignment=Qt.AlignmentFlag.AlignLeft)
        stream_layout.addWidget(self.parser, alignment=Qt.AlignmentFlag.AlignLeft)
        stream_layout.addWidget(self.decoder, alignment=Qt.AlignmentFlag.AlignLeft)
        stream_layout.addWidget(self.postprocessor, alignment=Qt.AlignmentFlag.AlignLeft)
        stream_layout.addWidget(self.sink, alignment=Qt.AlignmentFlag.AlignLeft)
        stream_box.setLayout(stream_layout)

        frame_box = QGroupBox()
        frame_box.setTitle('Размеры изображения')
        frame_layout = QVBoxLayout()
        self.width = LabeledEdit('Ширина кадра', tip='1280', label_width=LABEL_WIDTH, edit_width=FRAME_EDIT_WIDTH)
        self.height = LabeledEdit('Высота кадра', tip='720', label_width=LABEL_WIDTH, edit_width=FRAME_EDIT_WIDTH)
        self.channels = LabeledEdit('Каналы кадра', tip='3', label_width=LABEL_WIDTH, edit_width=FRAME_EDIT_WIDTH)

        frame_layout.addWidget(self.width, alignment=Qt.AlignmentFlag.AlignLeft)
        frame_layout.addWidget(self.height, alignment=Qt.AlignmentFlag.AlignLeft)
        frame_layout.addWidget(self.channels, alignment=Qt.AlignmentFlag.AlignLeft)
        frame_box.setLayout(frame_layout)

        delete_button = QPushButton()
        delete_button.setText('Удалить')
        delete_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogDiscardButton')))
        delete_button.clicked.connect(self.delete)

        layout = QVBoxLayout()
        layout.addWidget(self.identifier, alignment=Qt.AlignmentFlag.AlignLeft, stretch=100)
        layout.addWidget(stream_box)
        layout.addWidget(frame_box)
        layout.addWidget(delete_button)

        self.setLayout(layout)

        self.config = config

        if config is not None:
            self.identifier.set(config.identifier)
            self.source.set(config.source)
            self.parser.set(config.parser)
            self.decoder.set(config.decoder)
            self.postprocessor.set(config.postprocessor)
            self.sink.set(config.sink)
            self.width.set(config.frame.width)
            self.height.set(config.frame.height)
            self.channels.set(config.frame.channels)

    def get_config(self) -> StreamConfig:
        return StreamConfig(self.identifier.get(), self.source.get(), self.parser.get(),
                            self.decoder.get(), self.postprocessor.get(), self.sink.get(),
                            Shape(int(self.width.get()), int(self.height.get()), int(self.channels.get())))

    def delete(self):
        if self.video_server is not None:
            self.video_server.delete_stream(self)


class VideoServerWidget(QFrame):
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
        add_stream_button = QPushButton()
        add_stream_button.setText('Добавить поток')
        add_stream_button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_CommandLink')))
        add_stream_button.clicked.connect(self.add_stream)

        buttons_layout.addWidget(get_button)
        buttons_layout.addWidget(set_button)
        buttons_layout.addWidget(file_load_button)
        buttons_layout.addWidget(file_save_button)
        buttons_layout.addWidget(add_stream_button)

        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)

        self.streams_layout = QHBoxLayout()
        self.streams = []

        self.get_config()

        streams_widget = QWidget()
        streams_widget.setLayout(self.streams_layout)

        scroll_widget = QScrollArea()
        scroll_widget.setWidget(streams_widget)
        scroll_widget.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(buttons_widget)
        main_layout.addWidget(scroll_widget)

        self.setLayout(main_layout)

    def get_config(self):
        for widget in self.streams:
            self.streams_layout.removeWidget(widget)
            widget.setParent(None)

        self.streams.clear()

        config = self.connector.get_config()
        for stream in config.streams:
            widget = StreamConfigWidget(stream, video_server=self)
            self.streams.append(widget)
            self.streams_layout.addWidget(widget)

    def set_config(self):
        try:
            config = Config()
            for widget in self.streams:
                config.streams.append(widget.get_config())

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

            for widget in self.streams:
                self.streams_layout.removeWidget(widget)
                widget.setParent(None)

            self.streams.clear()

            config = self.connector.get_config()
            for stream in config.streams:
                widget = StreamConfigWidget(stream, video_server=self)
                self.streams.append(widget)
                self.streams_layout.addWidget(widget)

        except ParseError as e:
            MessageBox('Ошибка', f'Не удалось загрузить конфигурацию ({e}).', QMessageBox.StandardButton.Abort,
                       QMessageBox.Icon.Critical).exec()

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(caption='Сохранение конфигурации', filter="JSON (*.json)")

        if path[-4:] != 'json':
            path += 'json'

        try:
            config = Config()
            for widget in self.streams:
                config.streams.append(widget.get_config())

            with open(path, 'w') as f:
                f.write(json.dumps(pack(config), indent=2))
        except ValueError as e:
            MessageBox('Ошибка', f'Не удалось установить конфигурацию ({e}).', QMessageBox.StandardButton.Abort,
                       QMessageBox.Icon.Critical).exec()

    def add_stream(self):
        widget = StreamConfigWidget(video_server=self)
        self.streams.append(widget)
        self.streams_layout.addWidget(widget)

    def delete_stream(self, widget: StreamConfigWidget):
        self.streams.remove(widget)
        self.streams_layout.removeWidget(widget)
        widget.setParent(None)
