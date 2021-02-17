from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton,
                            QFrame, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QFont, QCursor, QIntValidator
from PyQt5.QtCore import Qt
from .profile_db import *
import json

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.username = fetch_username()
    self.gender = fetch_gender()
    self.age = fetch_age()
    self.weight = fetch_user_weight()
    self.weight_goal = fetch_goal_weight()
    self.goal_params = json.loads(fetch_goal_params())
    self.user_height = fetch_height()
    self.goal = fetch_goal()
    self.setStyleSheet(   
    """QWidget{
      color:#c7c7c7;
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
    self.create_panel()

  def create_panel(self):
    main_panel_layout = QGridLayout()
    main_panel_layout.addWidget(self.create_top_panel(), 0, 0, 1, 1)
    main_panel_layout.addLayout(self.settings_layout(), 1, 0, 1, 1)
    self.setLayout(main_panel_layout)

  def create_top_panel(self):
    layout = QGridLayout()
    self.username_layout = QHBoxLayout()
    self.name_label = QLabel()
    self.name_label.setText(" ".join(["Username:", self.username]))
    self.edit_username_button = QPushButton("Edit")
    self.edit_username_button.setFixedSize(60, 30)
    self.username_layout.addWidget(self.name_label)
    self.username_layout.addWidget(self.edit_username_button)

    framed_layout_username = QFrame()
    framed_layout_username.setLayout(self.username_layout)
    framed_layout_username = self.setup_frame(framed_layout_username)

    self.age_layout = QHBoxLayout()
    self.age_label = QLabel()
    self.age_label.setText(" ".join(["Age:", self.age]))
    self.edit_age_button = QPushButton("Edit")
    self.edit_age_button.setFixedSize(60, 30)
    self.age_layout.addWidget(self.age_label)
    self.age_layout.addWidget(self.edit_age_button)
    self.edit_age_button.clicked.connect(lambda:self.update_age())

    framed_layout_age = QFrame()
    framed_layout_age.setLayout(self.age_layout)
    framed_layout_age = self.setup_frame(framed_layout_age)

    self.height_layout = QHBoxLayout()
    self.height_label = QLabel()
    self.height_label.setText(" ".join(["Height:", self.user_height]))
    self.edit_height_button = QPushButton("Edit")
    self.edit_height_button.setFixedSize(60, 30)
    self.height_layout.addWidget(self.height_label)
    self.height_layout.addWidget(self.edit_height_button)
    self.edit_height_button.clicked.connect(lambda:self.update_height())

    framed_layout_height = QFrame()
    framed_layout_height.setLayout(self.height_layout)
    framed_layout_height = self.setup_frame(framed_layout_height)

    self.weight_layout = QHBoxLayout()
    self.weight_label = QLabel()
    self.weight_label.setText(" ".join(["Weight:", self.weight]))
    self.edit_weight_button = QPushButton("Edit")
    self.edit_weight_button.setFixedSize(60, 30)
    self.weight_layout.addWidget(self.weight_label)
    self.weight_layout.addWidget(self.edit_weight_button)
    self.edit_weight_button.clicked.connect(lambda:self.update_weight())

    framed_layout_weight = QFrame()
    framed_layout_weight.setLayout(self.weight_layout)
    framed_layout_weight = self.setup_frame(framed_layout_weight)

    layout.setHorizontalSpacing(70)
    layout.addWidget(framed_layout_username, 0, 0, 1, 1)
    layout.addWidget(framed_layout_age, 1, 0, 1, 1)
    layout.addWidget(framed_layout_height, 0, 1, 1, 1)
    layout.addWidget(framed_layout_weight, 1, 1, 1, 1)

    framed_layout = QFrame()
    framed_layout.setLayout(layout)
    framed_layout = self.setup_frame(framed_layout)

    return framed_layout

  def setup_frame(self, frame):
    frame.setFrameStyle(QFrame.Box)
    frame.setLineWidth(3)
    frame.setObjectName("frame")
    frame.setStyleSheet("""#frame {color: #322d2d;}""")
    return frame

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
    self.display_units_combobox.setCursor(QCursor(Qt.PointingHandCursor))
    self.display_units_combobox.addItems(["Metric", "Imperial"])
    
    current_index = 0 if fetch_units() == "metric" else 1
    self.display_units_combobox.setCurrentIndex(current_index)
    self.display_units_combobox.activated.connect(lambda: self.change_units(self.display_units_combobox.currentText()))
    
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

  def change_units(self, selected_units):
    # don't do anything if current units are metric or imperial
    # and users clicks again on metric or imperial
    if selected_units == "Metric" and self.user_data[2] == "metric":
      pass
    elif selected_units ==  "Imperial" and self.user_data[2] == "imperial":
      pass
    else:
      # update units in user table
      update_units()
      # get updated units
      updated_units = fetch_units()
      current_weight = float(self.user_data[4])
      converted_weight = convert_weight(self.user_data[3], current_weight)
      # update self.user_data
      self.user_data[4] = converted_weight
      self.user_data[3] = updated_units
      # update weight in user table
      update_weight(converted_weight)
      self.weight.setText(set_weight(self.user_data))

  def update_weight(self):
    global weight_edit
    weight_edit = EditButtonLine("weight")
    weight_edit.show()

  def update_goal(self, goal):
    update_goal(goal)

  def update_goal_params(self, goal_params):
    update_goal_parameters(goal_params)

  def update_height(self):
    global height_edit
    height_edit = EditButtonLine("height")
    height_edit.show()

  def update_age(self):
    global age_edit
    age_edit = EditButtonLine("age")
    age_edit.show()

class EditButtonLine(QWidget):
  def __init__(self, edit_func):
    super().__init__()
    self.edit_func = edit_func
    self.setStyleSheet(   
    """QWidget{
      background-color: #232120;
      color:#c7c7c7;
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
    }
    QLineEdit{
      padding: 6px;
      background-color: rgb(33,33,33);
      border: 1px solid;
      border-color: #cdcdcd;
    }""")
    dialog_layout = QVBoxLayout()
    self.setWindowFlags(Qt.FramelessWindowHint)
    dialog_layout.addLayout(self.create_input_window())
    self.setLayout(dialog_layout)

  def create_input_window(self):
    layout = QVBoxLayout()
    entry_label = QLabel("Edit ")

    self.line_edit = QLineEdit()
    self.line_edit.setValidator(QIntValidator())

    helper_layout = QHBoxLayout()

    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close_button())

    confirm_button = QPushButton("Confirm")
    if self.edit_func == "weight":
      entry_label.setText("Weight")
      confirm_button.clicked.connect(lambda: self.confirm_weight())
    if self.edit_func == "height":
      entry_label.setText("Height")
      confirm_button.clicked.connect(lambda: self.confirm_height())
    if self.edit_func == "age":
      entry_label.setText("Age")
      confirm_button.clicked.connect(lambda: self.confirm_age())

    helper_layout.addWidget(cancel_button)
    helper_layout.addWidget(confirm_button)

    layout.addWidget(entry_label)
    layout.addWidget(self.line_edit)
    layout.addLayout(helper_layout)

    return layout

  def close_button(self):
    self.close()

  def confirm_height(self):
    if self.line_edit.text() != "":
      update_height(self.line_edit.text())
      self.close()

  def confirm_weight(self):
    if self.line_edit.text() != "":
      update_weight(self.line_edit.text())
      self.close()

  def confirm_age(self):
    if self.line_edit.text() != "":
      update_age(self.line_edit.text())
      self.close()

