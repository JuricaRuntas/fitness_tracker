import json
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt, pyqtSignal
from fitness_tracker.database_wrapper import DatabaseWrapper

class WeightLossEditDialog(QWidget):
  update_label_signal = pyqtSignal(bool)
  update_weight_signal = pyqtSignal(bool)
  update_cardio_notes_signal = pyqtSignal(str)
  update_graph_signal = pyqtSignal(bool)

  def __init__(self, to_edit, old_value, fitness_goal=None, date=None):
    super().__init__()
    assert to_edit in ("Current Weight", "Weight Goal", "Loss Per Week", "Time Spent", "Distance Travelled")
    if to_edit == "Loss Per Week":
      assert fitness_goal != None
      self.fitness_goal = fitness_goal
    elif to_edit == "Current Weight":
      assert date != None
      self.date = date

    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Weight Loss"
    self.to_edit = to_edit
    self.old_value = old_value
    self.current_date = datetime.today().strftime("%d/%m/%Y") 
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
    
    if self.to_edit in ("Current Weight", "Weight Goal", "Time Spent", "Distance Travelled"): 
      self.line_edit.setValidator(QIntValidator())
    elif self.to_edit == "Loss Per Week":
      self.line_edit.setValidator(QDoubleValidator())
    self.line_edit.setText(str(self.old_value))

    layout.addWidget(self.line_edit)
    layout.addLayout(buttons_layout)

    return layout

  def update_to_edit(self):
    mappings = {"Current Weight": "weight", "Weight Goal": "goalweight", "Loss Per Week": "goalparams"}
    if self.to_edit == "Current Weight":
      weight_history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "weight_history"))
      weight_history[self.date] = self.line_edit.text()
      self.db_wrapper.update_table_column(self.table_name, "weight_history", json.dumps(weight_history))
      self.update_graph_signal.emit(True)
      if self.current_date == self.date:
        self.db_wrapper.update_table_column("Users", "weight", self.line_edit.text())
      self.update_weight_signal.emit(True)
    elif self.to_edit == "Weight Goal":
      self.db_wrapper.update_table_column("Users", "goalweight", self.line_edit.text())
    elif self.to_edit == "Loss Per Week":
      self.db_wrapper.update_table_column("Users", "goalparams", json.dumps([self.fitness_goal, self.line_edit.text()]))
    else:
      self.update_cardio_notes_signal.emit(self.line_edit.text())
    self.update_label_signal.emit(True)
    self.close()
