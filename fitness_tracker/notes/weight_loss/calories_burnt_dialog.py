from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QRadioButton, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, pyqtSignal

class CaloriesBurntDialog(QWidget):
  update_calories_label_signal = pyqtSignal(str)

  def __init__(self, to_edit, old_value, time_spent, distance, exercise, user_weight):
    super().__init__()
    self.to_edit = to_edit
    self.old_value = old_value
    self.time_spent = time_spent
    self.distance = distance
    self.exercise = exercise
    self.user_weight = user_weight
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

    self.setWindowModality(Qt.ApplicationModal)
    self.setWindowTitle("".join(["Edit ", self.to_edit]))
    self.setLayout(self.create_layout())

  def create_layout(self):
    layout = QVBoxLayout()

    groupbox = QGroupBox()
    groupbox_layout = QHBoxLayout()
    self.update_button = QRadioButton("Update")
    self.update_button.setChecked(True)
    self.update_button.toggled.connect(lambda: self.change_enabled_items("Update"))
    self.calculate_radio_button = QRadioButton("Calculate")
    self.calculate_radio_button.toggled.connect(lambda: self.change_enabled_items("Calculate"))

    groupbox_layout.addWidget(self.update_button)
    groupbox_layout.addWidget(self.calculate_radio_button)
    groupbox.setLayout(groupbox_layout)
    
    mid_layout = QHBoxLayout()

    update_layout = QVBoxLayout()
    update_line_label = QLabel("Update Calories Burnt")
    self.update_line_edit = QLineEdit()
    self.update_line_edit.setValidator(QIntValidator())
    update_layout.addWidget(update_line_label)
    update_layout.addWidget(self.update_line_edit)

    calculate_layout = QVBoxLayout()
    self.calculate_label = QLabel("Estimated Calories Burnt:")
    self.calculate_button = QPushButton("Calculate")
    self.calculate_button.clicked.connect(lambda: self.calculate_calories())
    self.calculate_button.setEnabled(False)
    calculate_layout.addWidget(self.calculate_label)
    calculate_layout.addWidget(self.calculate_button)

    mid_layout.addLayout(update_layout)
    mid_layout.addLayout(calculate_layout)
    
    buttons_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_calories())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())
    buttons_layout.addWidget(save_button)
    buttons_layout.addWidget(cancel_button)

    layout.addWidget(groupbox)
    layout.addLayout(mid_layout)
    layout.addLayout(buttons_layout)

    return layout

  def change_enabled_items(self, enable):
    if enable == "Update":
      self.calculate_button.setEnabled(False)
      self.update_line_edit.setEnabled(True)
    elif enable == "Calculate":
      self.update_line_edit.setEnabled(False)
      self.calculate_button.setEnabled(True)

  def calculate_calories(self):
    MET = {"Running": 9.8, "Cycling": 9.5, "Walking": 3.8, "Swimming": 8}
    self.result = str(int(int(self.time_spent)*60*MET[self.exercise]*3.5*int(self.user_weight)/(200*60)))
    self.calculate_label.setText(" ".join(["Estimated Calories Burnt:", self.result]))

  def save_calories(self):
    if self.update_button.isChecked():
      self.update_calories_label_signal.emit(self.update_line_edit.text())
    elif self.calculate_radio_button.isChecked():
      self.update_calories_label_signal.emit(self.result)
    self.close()
