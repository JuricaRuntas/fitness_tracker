from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont
from .user_database import UserDatabase

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()

  def create_panel(self):
    main_panel_layout = QGridLayout()
    main_panel_layout.addWidget(self.create_top_panel(), 0, 0, 1, 1)
    main_panel_layout.addLayout(self.settings_layout(), 1, 0, 1, 1)
    self.setLayout(main_panel_layout)

  def create_top_panel(self):
    top_layout = QHBoxLayout()
    top_left_layout = QVBoxLayout()
    user_info_label = QLabel("User Info")
    user_info_label.setFont(QFont("Ariel", 16))
    top_left_layout.addWidget(user_info_label)

    height_label = QLabel("Height:")
    height_label.setFont(QFont("Ariel", 10))
    weight_label = QLabel("Weight:")
    weight_label.setFont(QFont("Ariel", 10))
    age_label = QLabel("Age:")
    age_label.setFont(QFont("Ariel", 10))
    birthday_label = QLabel("Birthday:")
    birthday_label.setFont(QFont("Ariel", 10))
    height_line_edit = QLineEdit()
    height_unit = QComboBox()
    weight_line_edit = QLineEdit()
    weight_unit = QLabel()
    age_value = QLabel("20")
    edit_age_button = QPushButton("Edit Age")
    birthday_day_combobox = QComboBox()
    birthday_month_combobox = QComboBox()

    height_layout = QHBoxLayout()
    height_layout.addWidget(height_label)
    height_layout.addWidget(height_line_edit)
    height_layout.addWidget(height_unit)

    weight_layout = QHBoxLayout()
    weight_layout.addWidget(weight_label)
    weight_layout.addWidget(weight_line_edit)
    weight_layout.addWidget(weight_unit)

    age_layout = QHBoxLayout()
    age_layout.addWidget(age_label)
    age_layout.addWidget(age_value)
    age_layout.addWidget(edit_age_button)

    birthday_layout = QHBoxLayout()
    birthday_layout.addWidget(birthday_label)
    birthday_layout.addWidget(birthday_day_combobox)
    birthday_layout.addWidget(birthday_month_combobox)

    top_left_layout.addLayout(height_layout)
    top_left_layout.addLayout(weight_layout)
    top_left_layout.addLayout(age_layout)
    top_left_layout.addLayout(birthday_layout)

    top_layout.addLayout(top_left_layout)

    framed_top_layout = QFrame()
    framed_top_layout.setFrameStyle(QFrame.StyledPanel)
    framed_top_layout.setLayout(top_layout)

    return framed_top_layout

  def settings_layout(self):
    settings = QVBoxLayout()
    settings_label = QLabel("Settings")
    settings_label.setFont(QFont("Ariel", 14))
    settings.addWidget(settings_label)
    settings_layout = QHBoxLayout()
    settings_left_layout = QVBoxLayout()
    settings_right_layout = QVBoxLayout()

    display_units = QHBoxLayout()
    display_units_label = QLabel("Display Units:")
    display_units_label.setFont(QFont("Ariel", 10))
    self.display_units_combobox = QComboBox()
    self.display_units_combobox.addItems(["Metric", "Imperial"])
    current_index = 0 if self.current_units() ==  "metric" else 1
    self.display_units_combobox.setCurrentIndex(current_index)
    self.display_units_combobox.activated.connect(self.change_units)
    
    display_units.addWidget(display_units_label)
    display_units.addWidget(self.display_units_combobox)

    app_style = QHBoxLayout()
    app_style_label = QLabel("Theme")

    settings_left_layout.addLayout(display_units)

    framed_left_layout = QFrame()
    framed_left_layout.setFrameStyle(QFrame.StyledPanel)
    framed_left_layout.setLayout(settings_left_layout)

    settings_layout.addWidget(framed_left_layout)
    settings_layout.addLayout(settings_right_layout)

    settings.addLayout(settings_layout)

    return settings

  def change_units(self):
    UserDatabase().update_units()

  def current_units(self):
    return UserDatabase().fetch_units() 
