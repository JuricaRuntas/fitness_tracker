from functools import partial
import json
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt
from fitness_tracker.database_wrapper import DatabaseWrapper

class LiftHistory(QScrollArea):
  def __init__(self):
    super().__init__()
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Compound Exercises"
    self.setStyleSheet("""
    QWidget{
      background-color: #232120;
      font-weight: bold;
      color:#c7c7c7;
    }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: center;
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
    }
    """)
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
    self.setWindowModality(Qt.ApplicationModal)
    self.units = "kg" if self.db_wrapper.fetch_local_column("Users", "units") == "metric" else "lb"
    self.setWindowTitle("Lift History")
    
    widget = QWidget()
    self.layout = QFormLayout(widget)
    
    self.setWidget(widget)
    self.setWidgetResizable(True)
    self.create_history(True, True)

  @pyqtSlot(bool)
  def create_history(self, create, init_layout=False):
    exercise_label = QLabel("Exercise")
    exercise_label.setAlignment(Qt.AlignCenter)
    delete_label = QLabel("Delete")
    delete_label.setAlignment(Qt.AlignCenter)
    self.layout.addRow(exercise_label, delete_label)
    
    self.lift_history = self.db_wrapper.fetch_local_column(self.table_name, "lift_history")
    if create and not self.lift_history == None:
      if not init_layout: 
        self.delete_history()
      lift_history = json.loads(self.lift_history)
      self.labels = [None] * len(lift_history)
      self.delete_buttons = [None] * len(lift_history)

      for i in range(len(lift_history)):
        self.labels[i] = QLabel(self)
        self.delete_buttons[i] = QPushButton("X", self)
      
      for j, exercise in enumerate(lift_history):
        try:
          self.labels[j].setText(": ".join([exercise[0], " ".join([exercise[1], self.units])]))
        except TypeError: # joining lift for reps as 1RM lift 
          self.labels[j].setText(": ".join([exercise[0], " ".join(["x".join(exercise[1]), self.units])]))
        
        self.delete_buttons[j].setProperty("entry_index", exercise[-1])
        self.delete_buttons[j].clicked.connect(partial(self.delete_history_entry_from_layout, j, self.delete_buttons[j].property("entry_index")))
        
        self.layout.addRow(self.labels[j], self.delete_buttons[j])

    close_button = QPushButton("Close")
    close_button.clicked.connect(lambda:self.close())
    self.layout.addRow(close_button)

  def delete_history(self):
    for i in reversed(range(self.layout.count())):
      self.layout.itemAt(i).widget().setParent(None)
  
  def delete_history_entry_from_layout(self, i, entry_index):
    self.labels[i].setParent(None)
    self.delete_buttons[i].setParent(None)
    history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "lift_history"))
    lift_history = [lift for lift in history if not lift[-1] == entry_index]
    if len(lift_history) == 0: lift_history = None
    else: lift_history = json.dumps(lift_history)
    self.db_wrapper.update_table_column(self.table_name, "lift_history", lift_history, True)
