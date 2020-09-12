from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.CreatePanel()

  def CreatePanel(self):
    main_panel_layout = QGridLayout()
    main_panel_layout.addLayout(self.CreateTopPanel(), 0, 0, 1, 1)
    main_panel_layout.addLayout(self.SettingsLayout(), 1, 0, 1, 1)
    self.setLayout(main_panel_layout)

  def CreateTopPanel(self):
    top_layout = QHBoxLayout()
    top_left_layout = QVBoxLayout()
    user_info_label = QLabel("User Info")
    user_info_label.setFont(QFont("Ariel", 16))
    top_left_layout.addWidget(user_info_label)

    height_label = QLabel("Height:")
    weight_label = QLabel("Weight:")
    age_label = QLabel("Age:")
    birthday_label = QLabel("Birthday:")
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

    return top_layout

  def SettingsLayout(self):
    settings_layout = QHBoxLayout()
    settings_left_layout = QVBoxLayout()
    settings_right_layout = QVBoxLayout()

    display_units = QHBoxLayout()
    display_units_label = QLabel("Display Units:")
    display_units_combobox = QComboBox()
    display_units_combobox.addItems(["Metric", "Imperial"])
    display_units.addWidget(display_units_label)
    display_units.addWidget(display_units_combobox)

    settings_left_layout.addLayout(display_units)

    settings_layout.addLayout(settings_left_layout)
    settings_layout.addLayout(settings_right_layout)
    return settings_layout
