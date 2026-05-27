# ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QStackedWidget, QLabel
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RF-Platform Tools")

        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)

        # Верхняя панель
        topbar = QHBoxLayout()

        self.btn_start_game = QPushButton("Запустить игру")
        self.btn_close_game = QPushButton("Закрыть игру")
        self.btn_update_client = QPushButton("Обновить клиент")
        self.btn_upload_scripts = QPushButton("Залить скрипты")

        topbar.addWidget(self.btn_start_game)
        topbar.addWidget(self.btn_close_game)
        topbar.addWidget(self.btn_update_client)
        topbar.addWidget(self.btn_upload_scripts)
        topbar.addStretch()

        main_layout.addLayout(topbar)

        # Основная область
        body = QHBoxLayout()
        main_layout.addLayout(body)

        # Левая панель
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(230)

        self.sidebar.addItem("Клиент")
        self.sidebar.addItem("Патчи")
        self.sidebar.addItem("EFF редактор")
        self.sidebar.addItem("Скрипты сервера")
        self.sidebar.addItem("База данных")
        self.sidebar.addItem("Excel / EDF")
        self.sidebar.addItem("Логи")
        self.sidebar.addItem("Настройки")

        body.addWidget(self.sidebar)

        # Центральные страницы
        self.pages = QStackedWidget()
        body.addWidget(self.pages)

        self.pages.addWidget(QLabel("Клиент"))
        self.pages.addWidget(QLabel("Патчи"))
        self.pages.addWidget(QLabel("EFF редактор"))
        self.pages.addWidget(QLabel("Скрипты сервера"))
        self.pages.addWidget(QLabel("База данных"))
        self.pages.addWidget(QLabel("Excel / EDF"))
        self.pages.addWidget(QLabel("Логи"))
        self.pages.addWidget(QLabel("Настройки"))

        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.sidebar.setCurrentRow(0)