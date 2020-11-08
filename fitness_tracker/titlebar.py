from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont, QImage

class TitleBar(QWidget):
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("Fitness Tracker")

        title_font_size = 11
        title_font_color = 0, 0, 0
        title_font = QFont("Meiryo", title_font_size)
        self.title.setFont(title_font)
        self.layout.addWidget(self.title)

        close_image = QImage()
        minimise_image = QImage()

        self.setLayout(self.layout)