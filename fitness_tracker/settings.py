from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QRadioButton, QComboBox, QCheckBox, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from configparser import ConfigParser
import os
config_path = os.path.join(os.path.dirname(__file__), "config", "settings.ini")
config = ConfigParser()
config.read(config_path)

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.colorize_background()
        self.setStyleSheet("""
        QWidget{
            color:#c7c7c7;
            background-color: #232120;
            font-weight: bold;
            font-family: Montserrat;
            font-size: 16px;
            }
        QPushButton{
            background-color: rgba(0, 0, 0, 0);
            border: 1px solid;
            font-size: 18px;
            font-weight: bold;
            border-color: #808080;
            min-height: 28px;
            white-space:nowrap;
            text-align: left;
            padding-left: 5%;
            font-family: Montserrat;
        }
        QPushButton:hover:!pressed{
            border: 2px solid;
            border-color: #747474;
        }
        QPushButton:pressed{
            border: 2px solid;
            background-color: #323232;
            border-color: #6C6C6C;
        }""")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        center_at_start_layout = QHBoxLayout()
        center_at_start_label = QLabel("Center Window At Startup")
        self.center_at_start = QCheckBox()
        self.center_at_start.stateChanged.connect(lambda:self.center_startup_setting(self.center_at_start))
        center_at_start_layout.addWidget(center_at_start_label)
        center_at_start_layout.addWidget(self.center_at_start)
        if config['WINDOW'].get('CenterAtStartup') == 'yes':
            self.center_at_start.setChecked(True)
        else:
            self.center_at_start.setChecked(False)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_win)
        self.label = QLabel("Settings:")

        #CLOSE LAUNCHER TO SYSTEM TRAY/CLOSE APPLICATION, LAUNCH AT STARTUP, VERSION INFO, UPDATE (AUTO, MANUAL, CHECK)

        layout.addWidget(self.label)
        layout.addLayout(center_at_start_layout)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

    def colorize_background(self):
        self.setAutoFillBackground(True)
        bg_palette = self.palette()
        bg_palette.setColor(self.backgroundRole(), QColor(23,21,20))
        self.setPalette(bg_palette)

    def close_win(self):
        self.close()

    def center_startup_setting(self, btn):
        if btn.isChecked() == True:
            config.set('WINDOW', 'CenterAtStartup', 'yes')
        if btn.isChecked() == False:
            config.set('WINDOW', 'CenterAtStartup', 'no')
        with open(os.path.join(os.path.dirname(__file__), "config", "settings.ini"), 'w') as configfile:
            config.write(configfile)

