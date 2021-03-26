from functools import partial
import json
from PyQt5.QtWidgets import QWidget, QScrollArea, QFormLayout, QLabel, QPushButton, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from fitness_tracker.database_wrapper import DatabaseWrapper
from .weight_loss_edit_dialog import WeightLossEditDialog

class WeightLossHistory(QScrollArea):
  update_weight_loss_label_signal = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Weight Loss"
    self.setStyleSheet("""
    QWidget{
      background-color: #322d2d;
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
    self.units = "kg" if self.db_wrapper.fetch_local_column("Users", "units") == "metric" else "lb"
    self.weight_history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "weight_history"))
    self.setWindowModality(Qt.ApplicationModal)
    self.setWindowFlags(Qt.Tool)
    self.setWindowTitle("Weight History")

    widget = QWidget()
    self.layout = QGridLayout(widget)
    self.setWidget(widget)
    self.setWidgetResizable(True)

    self.create_history(True, True)
  
  @pyqtSlot(bool)
  def create_history(self, create, init_layout=False):
    if create and len(self.weight_history) > 0:
      if not init_layout:
        self.update_weight_loss_label_signal.emit(True)
        self.delete_history()
      
      date_label = QLabel("Date")
      date_label.setAlignment(Qt.AlignCenter)
      weight_label = QLabel("Weight")
      weight_label.setAlignment(Qt.AlignCenter)
      
      edit_label = QLabel("Edit")
      edit_label.setAlignment(Qt.AlignCenter)
      delete_label = QLabel("Delete")
      delete_label.setAlignment(Qt.AlignCenter)
      
      self.layout.addWidget(date_label, 0, 0)
      self.layout.addWidget(weight_label, 0, 1)
      self.layout.addWidget(edit_label, 0, 2)
      self.layout.addWidget(delete_label, 0, 3)
      
      self.date_labels = [None] * len(self.weight_history)
      self.weight_labels = [None] * len(self.weight_history)
      self.edit_buttons = [None] * len(self.weight_history)
      self.delete_buttons = [None] * len(self.weight_history)

      for i in range(len(self.weight_history)):
        self.date_labels[i] = QLabel(self)
        self.weight_labels[i] = QLabel(self)
        self.edit_buttons[i] = QPushButton("Edit", self)
        self.delete_buttons[i] = QPushButton("X", self)
      
      row = 1
      for j, date in enumerate(list(reversed(self.weight_history))):
        self.weight_labels[j].setText(" ".join([self.weight_history[date], self.units]))
        self.date_labels[j].setText(date)
        self.edit_buttons[j].setProperty("date", date)
        self.edit_buttons[j].clicked.connect(partial(self.edit_weight_dialog, "Current Weight",
                                                     self.weight_history[date], self.edit_buttons[j].property("date")))
        self.delete_buttons[j].setProperty("date", date)
        self.delete_buttons[j].clicked.connect(partial(self.delete_history_entry_from_layout, j, self.delete_buttons[j].property("date")))

        self.layout.addWidget(self.date_labels[j], row, 0, 1, 1)
        self.layout.addWidget(self.weight_labels[j], row, 1, 1, 1)
        self.layout.addWidget(self.edit_buttons[j], row, 2, 1, 1)
        self.layout.addWidget(self.delete_buttons[j], row, 3, 1, 1)
        row += 1

  def edit_weight_dialog(self, to_edit, value, date):
    self.edit_weight_dialog_window = WeightLossEditDialog(to_edit, value, date=date)
    self.edit_weight_dialog_window.update_weight_signal.connect(lambda signal: self.create_history(signal))
    self.edit_weight_dialog_window.show()

  def delete_history(self):
    self.weight_history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "weight_history"))
    for i in reversed(range(self.layout.count())):
      self.layout.itemAt(i).widget().setParent(None)

  def delete_history_entry_from_layout(self, i, date):
    self.date_labels[i].setParent(None)
    self.weight_labels[i].setParent(None)
    self.edit_buttons[i].setParent(None)
    self.delete_buttons[i].setParent(None)
    if date in self.weight_history: del self.weight_history[date]
    self.db_wrapper.update_table_column(self.table_name, "weight_history", json.dumps(self.weight_history))
