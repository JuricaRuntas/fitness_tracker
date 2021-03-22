from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt, pyqtSignal
from fitness_tracker.user_profile.profile_db import update_user_info_parameter

class WeightLossEditDialog(QWidget):
  update_label_signal = pyqtSignal(bool)

  def __init__(self, to_edit, old_value, sqlite_connection, pg_connection, fitness_goal=None):
    super().__init__()
    assert to_edit in ("Current Weight", "Weight Goal", "Loss Per Week")
    if to_edit == "Loss Per Week":
      assert fitness_goal != None
      self.fitness_goal = fitness_goal

    self.to_edit = to_edit
    self.old_value = old_value
    self.sqlite_connection = sqlite_connection
    self.pg_connection = pg_connection
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
    self.layout = QVBoxLayout()
    self.layout.addLayout(self.create_layout())
    self.setLayout(self.layout)

  def create_layout(self):
    layout = QVBoxLayout()
    self.line_edit = QLineEdit()
    
    buttons_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.update_to_edit())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())
    buttons_layout.addWidget(save_button)
    buttons_layout.addWidget(cancel_button)
    
    if self.to_edit in ("Current Weight", "Weight Goal"): 
      self.line_edit.setValidator(QIntValidator())
    elif self.to_edit == "Loss Per Week":
      self.line_edit.setValidator(QDoubleValidator())
    self.line_edit.setText(str(self.old_value))

    layout.addWidget(self.line_edit)
    layout.addLayout(buttons_layout)

    return layout

  def update_to_edit(self):
    mappings = {"Current Weight": "weight", "Weight Goal": "goalweight", "Loss Per Week": "goalparams"}
    if self.to_edit != "Loss Per Week":
      update_user_info_parameter(self.sqlite_connection, self.pg_connection, mappings[self.to_edit], self.line_edit.text())
    elif self.to_edit == "Loss Per Week":
      update_user_info_parameter(self.sqlite_connection, self.pg_connection, mappings[self.to_edit], [self.fitness_goal, self.line_edit.text()])
    self.update_label_signal.emit(True)
    self.close()
