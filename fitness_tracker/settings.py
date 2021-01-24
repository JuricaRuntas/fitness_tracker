from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QRadioButton, QComboBox, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.colorize_background()
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setFixedSize(300, 500)
        layout = QVBoxLayout()

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_win)
        self.label = QLabel("Temp")

        layout.addWidget(self.label)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

    def colorize_background(self):
        self.setAutoFillBackground(True)
        bg_palette = self.palette()
        bg_palette.setColor(self.backgroundRole(), QColor(25,23,22))
        self.setPalette(bg_palette)

    def close_win(self):
        self.close()