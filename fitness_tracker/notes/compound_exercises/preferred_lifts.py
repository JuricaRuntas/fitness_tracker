import json
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QFormLayout, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import  QFont
from PyQt5.QtCore import pyqtSignal, Qt
from fitness_tracker.database_wrapper import DatabaseWrapper

class PreferredLifts(QWidget):
  change_lifts_signal = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Compound Exercises"
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
    QComboBox{
      border-radius: 4px;
      font-size: 18px;
      font-weight: bold;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
      min-height: 28px;
      background-color: #440D0F;
    }
    QComboBox:down-arrow{
      width: 24.54px;
      height: 10px;
      background: #d3d3d3; 
      opacity:0
    }
    QComboBox:drop-down{
      background-color: #440D0F;
      border: 0px;
      opacity:0;
      border-radius: 0px;
    }
    QComboBox:hover:!pressed{
      background-color: #5D1A1D;
    }
    QComboBox:pressed{
      background-color: #551812;
    }
    """) 
    self.setWindowModality(Qt.ApplicationModal)
    self.setWindowTitle("Edit Preferred Lifts")
    self.preferred_lifts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "preferred_lifts"))
    self.setLayout(self.create_panel())
    self.set_preferred_lifts()
  
  def create_panel(self):
    form_layout = QFormLayout()

    horizontal_press_label = QLabel("Horizontal Press")
    self.horizontal_press_dropdown = QComboBox()
    self.horizontal_press_dropdown.addItems(["Bench Press", "Incline Bench Press"])

    floor_pull_label = QLabel("Floor Pull")
    self.floor_pull_dropdown = QComboBox()
    self.floor_pull_dropdown.addItems(["Deadlift", "Sumo Deadlift"])

    squat_label = QLabel("Squat")
    self.squat_dropdown = QComboBox()
    self.squat_dropdown.addItems(["Back Squat", "Front Squat"])

    vertical_press_label = QLabel("Vertical Press")
    self.vertical_press_dropdown = QComboBox()
    self.vertical_press_dropdown.addItems(["Overhead Press", "Push Press"])
    
    buttons_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_preferred_lifts())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())
    buttons_layout.addWidget(save_button)
    buttons_layout.addWidget(cancel_button)

    form_layout.addRow(horizontal_press_label, self.horizontal_press_dropdown)
    form_layout.addRow(floor_pull_label, self.floor_pull_dropdown)
    form_layout.addRow(squat_label, self.squat_dropdown)
    form_layout.addRow(vertical_press_label, self.vertical_press_dropdown)
   
    main_layout = QVBoxLayout()
    main_layout.addLayout(form_layout)
    main_layout.addLayout(buttons_layout)

    return main_layout

  def set_preferred_lifts(self):
    horizontal_press_index = self.horizontal_press_dropdown.findText(self.preferred_lifts["Horizontal Press"])
    floor_pull_index = self.floor_pull_dropdown.findText(self.preferred_lifts["Floor Pull"])
    squat_index = self.squat_dropdown.findText(self.preferred_lifts["Squat"])
    vertical_press_index = self.vertical_press_dropdown.findText(self.preferred_lifts["Vertical Press"])

    self.horizontal_press_dropdown.setCurrentIndex(horizontal_press_index)
    self.floor_pull_dropdown.setCurrentIndex(floor_pull_index)
    self.squat_dropdown.setCurrentIndex(squat_index)
    self.vertical_press_dropdown.setCurrentIndex(vertical_press_index)

  def save_preferred_lifts(self):
    horizontal_press = str(self.horizontal_press_dropdown.currentText())
    floor_pull = str(self.floor_pull_dropdown.currentText())
    squat = str(self.squat_dropdown.currentText())
    vertical_press = str(self.vertical_press_dropdown.currentText())
    new_preferred_lifts = {"Horizontal Press": horizontal_press, "Floor Pull":floor_pull,
                           "Squat": squat, "Vertical Press": vertical_press}
    self.db_wrapper.update_table_column(self.table_name, "preferred_lifts", new_preferred_lifts)

    new_preferred_lifts = list(new_preferred_lifts.values())
    one_rep_maxes = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "one_rep_maxes"))
    lifts_for_reps = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "lifts_for_reps"))

    new_one_rep_maxes = {new_preferred_lifts[i]:value for i, value in enumerate(one_rep_maxes.values())}
    new_lifts_for_reps = {new_preferred_lifts[i]:value for i, value in enumerate(lifts_for_reps.values())}
    
    self.db_wrapper.update_table_column(self.table_name, "one_rep_maxes", new_one_rep_maxes)
    self.db_wrapper.update_table_column(self.table_name, "lifts_for_reps", new_lifts_for_reps)
    
    self.change_lifts_signal.emit(True)
    self.close()
