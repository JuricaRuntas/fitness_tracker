from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QIcon

class TitleBar(QWidget):
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("Fitness Tracker")
        self.version = QLabel("v1.0")

        self.gridlayout = QHBoxLayout()
        self.gridlayout.setContentsMargins(0, 0, 0, 0)

        slight_indent = QSpacerItem(4, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        version_space = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        title_font_size = 11
        title_font_color = 0, 0, 0
        title_font = QFont("Meiryo", title_font_size)
        self.title.setFont(title_font)

        self.version.setFont(title_font)
        self.version.setStyleSheet("color: #A5A5A5;")

        self.close_icon = QIcon('icons/close.bmp')
        self.close_button = QPushButton()
        self.close_button.setIcon(self.close_icon)

        self.layout.addItem(slight_indent)
        self.layout.addWidget(self.title)
        self.layout.addItem(version_space)
        self.layout.addWidget(self.version)

        self.layout.addStretch(-1)

        self.gridlayout.addLayout(self.layout)
        self.gridlayout.addStretch(1)
        self.gridlayout.addWidget(self.close_button)
        self.setLayout(self.gridlayout)