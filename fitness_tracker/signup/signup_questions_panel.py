from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QVBoxLayout, QFormLayout, QLineEdit,
                             QLabel, QPushButton, QGroupBox, QRadioButton, QHBoxLayout)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt
from .signup_helpers import get_table_name, create_user_info_after_signup

class SignupQuestions(QWidget):
  def __init__(self, controller):
    super().__init__()
    self.controller = controller
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_login(), 0, 0, 1, 1)
    self.setLayout(grid)

  def create_login(self):
    title_frame = QFrame()
    title_layout = QVBoxLayout()

    signup_label = QLabel("Signup", self)
    signup_label.setFont(QFont("Ariel", 15))
    signup_label.setFixedHeight(70)

    title_layout.addWidget(signup_label)
    title_frame.setLayout(title_layout)

    signup_frame = QFrame()
    signup_frame.setFrameStyle(QFrame.StyledPanel)

    form_layout = self.create_form_layout()
    signup_frame.setLayout(form_layout)

    wrapper_layout = QVBoxLayout()
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(signup_frame)
    return wrapper_layout

  def create_form_layout(self):
    form_layout = QFormLayout()

    name_label = QLabel("Name", self)
    self.name_entry = QLineEdit()
    
    gender = QGroupBox()
    gender_layout = QHBoxLayout()
    gender_layout.setAlignment(Qt.AlignCenter)

    gender_label = QLabel("Gender", self)
    self.male_button = QRadioButton("Male")
    self.male_button.setChecked(True)
    self.female_button = QRadioButton("Female")
    gender_layout.addWidget(self.male_button)
    gender_layout.addWidget(self.female_button)
    gender.setLayout(gender_layout)
    
    units = QGroupBox()
    units_layout = QHBoxLayout()
    units_layout.setAlignment(Qt.AlignCenter)

    units_label = QLabel("Units", self)
    self.metric_button = QRadioButton("Metric")
    self.metric_button.setChecked(True)
    self.imperial_button = QRadioButton("Imperial")
    units_layout.addWidget(self.metric_button)
    units_layout.addWidget(self.imperial_button)
    units.setLayout(units_layout)
    
    weight_label = QLabel("Weight", self)
    self.weight_entry = QLineEdit()

    self.signup_button = QPushButton("Signup", self)
    self.signup_button.clicked.connect(lambda: self.signup())
    self.signup_button.setCursor(QCursor(Qt.PointingHandCursor))
    
    form_layout.addRow(name_label, self.name_entry)
    form_layout.addRow(gender_label, gender)
    form_layout.addRow(units_label, units)
    form_layout.addRow(weight_label, self.weight_entry)
    form_layout.addRow(self.signup_button)
    return form_layout

  def signup(self):
    gender = "male" if self.male_button.isChecked() else "female"
    units = "metric" if self.metric_button.isChecked() else "imperial"
    user_info = {"name": self.name_entry.text(),
                 "gender": gender, "units": units,
                 "weight": float(self.weight_entry.text())}
    if not gender == "" and not units == "" and not self.name_entry.text() == "" and not self.weight_entry.text() == "":
      table_name = get_table_name()
      create_user_info_after_signup(user_info, table_name)
      self.controller.display_layout("Home")