import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QSizeGrip
from PyQt5.QtGui import QFont, QIcon, QPainter, QBrush, QColor
from PyQt5.QtCore import QPoint, Qt, QSize
from fitness_tracker.user_profile.profile_db import fetch_username
from fitness_tracker.settings import SettingsWindow

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "icons")

icons = {"close": os.path.join(path, "close.bmp"),
         "min": os.path.join(path, "min.bmp"),
         "max": os.path.join(path, "max.bmp"),
         "small": os.path.join(path, "small.bmp"),
         "settings": os.path.join(path, "settings.png")}



class TitleBar(QWidget):
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("Fitness Tracker")
        self.username = fetch_username()
        if self.username == None:
            self.version = QLabel()
        else:
            self.version = QLabel("-" + self.username)
        self.setFixedHeight(25)

        self.gridlayout = QHBoxLayout()
        self.gridlayout.setContentsMargins(0, 0, 0, 0)

        slight_indent = QSpacerItem(4, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        version_space = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        title_font_size = 14
        title_font = QFont('Ubuntu', title_font_size)
        self.title.setFont(title_font)

        self.version.setFont(title_font)
        self.version.setStyleSheet("color: #A5A5A5;")

        icon_max_size_x = 32
        icon_max_size_y = 24

        self.close_icon = QIcon(icons["close"])
        self.close_button = QPushButton()
        self.close_button.clicked.connect(self.close_click)
        self.close_button.setIcon(self.close_icon)
        self.close_button.setMaximumSize(icon_max_size_x, icon_max_size_y)
        self.close_button.setStyleSheet(
            "QPushButton{ background-color: rgba(237, 17, 17, 0); }"
            "QPushButton:hover{ background-color: rgba(237, 17, 17, 75); }"
            "QPushButton:pressed{ background-color: rgba(255, 0, 0, 100); }")

        self.minimise_icon = QIcon(icons["min"])
        self.minimise_button = QPushButton()
        self.minimise_button.clicked.connect(self.min_click)
        self.minimise_button.setIcon(self.minimise_icon)
        self.minimise_button.setMaximumSize(icon_max_size_x, icon_max_size_y)
        self.minimise_button.setStyleSheet(
            "QPushButton{ background-color: rgba(255, 255, 255, 0); }"
            "QPushButton:hover{ background-color: rgba(255, 255, 255, 70); }"
            "QPushButton:pressed{ background-color: rgba(255, 255, 255, 40); }")

        self.maximize_icon = QIcon(icons["max"])
        self.unmax_icon = QIcon(icons["small"])
        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.clicked.connect(self.max_click)
        self.maximize_button.setMaximumSize(icon_max_size_x, icon_max_size_y)
        self.maximize_button.setStyleSheet(
            "QPushButton{ background-color: rgba(255, 255, 255, 0); }"
            "QPushButton:hover{ background-color: rgba(255, 255, 255, 70); }"
            "QPushButton:pressed{ background-color: rgba(255, 255, 255, 40); }")

        self.settings_icon = QIcon(icons["settings"])
        self.settings_button = QPushButton()
        self.settings_button.setIcon(self.settings_icon)
        self.settings_button.setMaximumSize(icon_max_size_x, icon_max_size_y)
        self.settings_button.setStyleSheet(
            "QPushButton{ background-color: rgba(255, 255, 255, 0); }"
            "QPushButton:hover{ background-color: rgba(255, 255, 255, 70); }"
            "QPushButton:pressed{ background-color: rgba(255, 255, 255, 40); }")
        self.settings_button.clicked.connect(self.showSettings)

        self.settings_button.setObjectName("SettingsButton")

        self.layout.addItem(slight_indent)
        self.layout.addWidget(self.title)
        self.layout.addItem(version_space)
        self.layout.addWidget(self.version)
        self.layout.addStretch(-1)

        self.gridlayout.addLayout(self.layout)
        self.gridlayout.addStretch(1)
        self.gridlayout.setSpacing(0)
        self.gridlayout.addWidget(self.settings_button)
        self.gridlayout.addWidget(self.minimise_button)
        self.gridlayout.addWidget(self.maximize_button)
        self.gridlayout.addWidget(self.close_button)
        self.setLayout(self.gridlayout)

        self.start = QPoint(0, 0)
        self.pressing = False
        self.maximized = False

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing & self.maximized is False:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
            self.mapToGlobal(self.movement).y(),
            self.parent.width(),
            self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def close_click(self):
        self.parent.close()

    def max_click(self):
        if self.maximized:
            self.maximized = False
            self.parent.showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.maximized = True
            self.maximize_button.setIcon(self.unmax_icon)
            self.parent.showMaximized()

    def min_click(self):
        self.parent.showMinimized()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(68, 13, 15, 255)))

    def removeSettingsButton(self):
        self.layout.removeWidget("SettingsButton")

    def showSettings(self):
        global w 
        w = SettingsWindow()
        w.show()
