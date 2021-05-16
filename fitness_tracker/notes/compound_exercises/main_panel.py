import json
import sqlite3
import matplotlib
from datetime import datetime
from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, pyqtSlot
from fitness_tracker.common.units_conversion import kg_to_pounds, pounds_to_kg
from fitness_tracker.notes.compound_exercises.one_rm_graphs import OneRMGraphCanvas
from fitness_tracker.database_wrapper import DatabaseWrapper
from .preferred_lifts import PreferredLifts
from .update_1RM_window import Update1RMWindow
from .update_lifts_for_reps_window import UpdateLiftsForRepsWindow
from .lift_history import LiftHistory
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

matplotlib.use("Qt5Agg")

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Compound Exercises"
    self.setStyleSheet("""
    QWidget{
      color:#c7c7c7;
      font-weight: bold;
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
      width: 0px;
      height: 0px;
      background: #d3d3d3; 
      opacity:0
    }
    QComboBox:drop-down{
      background-color: #440D0F;
      border: 0px;
      opacity:0;
      border-radius: 0px;
      width: 0px;
      height: 0px;
    }
    QComboBox:hover:!pressed{
      background-color: #5D1A1D;
    }
    QComboBox:pressed{
      background-color: #551812;
    }
    """)
    self.current_year = str(datetime.now().year)
    self.db_wrapper.create_local_table(self.table_name)
    if self.db_wrapper.local_table_is_empty(self.table_name):
      self.db_wrapper.insert_default_values(self.table_name)
    
    self.units = "kg" if self.db_wrapper.fetch_local_column("Users", "units") == "metric" else "lb"
    big_lifts_units = "kg" if self.db_wrapper.fetch_local_column(self.table_name, "units") == "metric" else "lb"
    
    one_rep_maxes = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "one_rep_maxes"))
    lifts_for_reps = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "lifts_for_reps"))
    self.rm_history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "rm_history"))
    
    if not self.current_year in self.rm_history:
      self.add_year_to_rm_history(self.current_year)
      self.rm_history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "rm_history"))

    if self.units != big_lifts_units:
      units_name = "metric" if self.units == "kg" else "imperial"
      self.db_wrapper.update_table_column(self.table_name, "units", units_name)
      if units_name == "metric":
        for exercise, weight in one_rep_maxes.items():
          one_rep_maxes[exercise] = str(pounds_to_kg(weight))
        for exercise, reps_and_weight in lifts_for_reps.items():
          lifts_for_reps[exercise] = [reps_and_weight[0], str(pounds_to_kg(reps_and_weight[1]))] 
      
      elif units_name == "imperial":
        for exercise, weight in one_rep_maxes.items():
          one_rep_maxes[exercise] = str(kg_to_pounds(weight))
        for exercise, reps_and_weight in lifts_for_reps.items():
          lifts_for_reps[exercise] = [reps_and_weight[0], str(kg_to_pounds(reps_and_weight[1]))] 
    
      for year in self.rm_history:
        for month in self.rm_history[year]:
          for exercise_type in list(self.rm_history[year][month]):
            for exercise in list(self.rm_history[year][month][exercise_type]):
              for i, weight in enumerate(self.rm_history[year][month][exercise_type][exercise]):
                if units_name == "imperial":
                  self.rm_history[year][month][exercise_type][exercise][i] = str(kg_to_pounds(weight))
                elif units_name == "metric":
                  self.rm_history[year][month][exercise_type][exercise][i] = str(pounds_to_kg(weight))

      self.db_wrapper.update_table_column(self.table_name, "one_rep_maxes", one_rep_maxes)
      self.db_wrapper.update_table_column(self.table_name, "lifts_for_reps", lifts_for_reps)
      self.convert_lift_history_weight(self.units)
    
    self.one_RM = [[lift, " ".join([weight, self.units])] for lift, weight in one_rep_maxes.items()]
    self.lifts_reps = [[lift, " ".join(["x".join(weight), self.units])] for lift, weight in lifts_for_reps.items()]
    
    self.lift_history_window = LiftHistory()
    self.lift_history_window.setGeometry(100, 200, 300, 300) 
    
    self.plists_window = PreferredLifts()
    self.plists_window.change_lifts_signal.connect(self.changed_preferred_lifts)
    
    self.update_1RM_window = Update1RMWindow()
    self.update_1RM_window.change_1RM_lifts_signal.connect(self.changed_1RM_lifts)
    self.update_1RM_window.history_signal.connect(lambda signal: self.lift_history_window.create_history(signal))
    self.update_1RM_window.update_graph_signal.connect(lambda signal: self.refresh_graph(signal))

    self.lifts_for_reps = UpdateLiftsForRepsWindow()
    self.lifts_for_reps.change_lifts_for_reps_signal.connect(self.changed_lifts_for_reps)
    self.lifts_for_reps.history_signal.connect(lambda signal: self.lift_history_window.create_history(signal))
     
    self.preferred_lifts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "preferred_lifts"))
    self.one_rep_maxes = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "one_rep_maxes"))
    self.create_panel()

  def create_panel(self):
    main_panel_grid = QGridLayout()
    main_panel_grid.addLayout(self.description(), 0, 0, 1, 1)
    main_panel_grid.addWidget(self.create_time_graph(), 1, 0, 4, 1)
    main_panel_grid.addLayout(self.create_bottom_layout(), 5, 0, 3, 1)
    main_panel_grid.addLayout(self.create_function_buttons(), 8, 0, 1, 1)
    self.setLayout(main_panel_grid)

  def description(self):
    panel_description = QVBoxLayout()
    desc_font = QFont("Montserrat", 12)
    description_label = QLabel("Keep notes and track progress of your preferred big lifts here.", self)
    description_label.setFont(desc_font)
    description_label.setFixedHeight(20)
    panel_description.addWidget(description_label)
    return panel_description

  def create_time_graph(self):
    self.graph_layout = QVBoxLayout()

    graph = OneRMGraphCanvas("Horizontal Press", self.rm_history, self.current_year, self) 
    
    combobox_layout = QHBoxLayout()
    self.lifts_combobox = QComboBox(self)
    self.lifts_combobox.addItems(list(self.preferred_lifts.values()))
    self.lifts_combobox.currentTextChanged.connect(lambda lift: self.change_exercise_graph(lift))
     
    self.change_year_combobox = QComboBox(self)
    self.change_year_combobox.addItems(list(self.rm_history.keys()))
    self.change_year_combobox.setCurrentText(self.current_year)
    self.change_year_combobox.currentTextChanged.connect(lambda year: self.change_graph_year(year))

    combobox_layout.addWidget(self.change_year_combobox)
    combobox_layout.addWidget(self.lifts_combobox)

    toolbar = NavigationToolbar(graph, self)
    toolbar.setStyleSheet("background-color: white;")
    
    self.graph_layout.addWidget(toolbar)
    self.graph_layout.addWidget(graph)
    self.graph_layout.addLayout(combobox_layout)
    
    framed_graph = QFrame(self)
    framed_graph.setFrameStyle(QFrame.Box)
    framed_graph.setLineWidth(3)
    framed_graph.setLayout(self.graph_layout)
    
    return framed_graph
  
  def create_bottom_layout(self):
    bottom_layout = QHBoxLayout()
    bottom_layout.addWidget(self.create_one_rep_max())
    bottom_layout.addWidget(self.create_lifts_for_reps())
    return bottom_layout

  def create_one_rep_max(self):
    orm_panel = QVBoxLayout()
    main_label = QLabel("One Rep Max")
    main_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    self.horizontal_press_label_ORM = QLabel(": ".join(self.one_RM[0]))
    self.horizontal_press_label_ORM.setFont(QFont("Ariel", 10))

    self.floor_pull_label_ORM = QLabel(": ".join(self.one_RM[1]))
    self.floor_pull_label_ORM.setFont(QFont("Ariel", 10))

    self.squat_label_ORM = QLabel(": ".join(self.one_RM[2]))
    self.squat_label_ORM.setFont(QFont("Ariel", 10))

    self.vertical_press_label_ORM = QLabel(": ".join(self.one_RM[3]))
    self.vertical_press_label_ORM.setFont(QFont("Ariel", 10))

    orm_buttons = QHBoxLayout()
    update_button = QPushButton("Update")
    update_button.clicked.connect(lambda: self.update_1RM_window.show())
    clear_button = QPushButton("Clear")
    clear_button.clicked.connect(lambda: self.clear_one_rep_maxes())
    orm_buttons.addWidget(update_button)
    orm_buttons.addWidget(clear_button)

    orm_panel.addWidget(main_label)
    orm_panel.addWidget(self.horizontal_press_label_ORM)
    orm_panel.addWidget(self.floor_pull_label_ORM)
    orm_panel.addWidget(self.squat_label_ORM)
    orm_panel.addWidget(self.vertical_press_label_ORM)
    orm_panel.addLayout(orm_buttons)

    orm_panel.setSpacing(5)
    framed_layout = QFrame()
    framed_layout.setObjectName("graphObj")
    framed_layout.setFrameStyle(QFrame.Box)
    framed_layout.setLineWidth(3)
    framed_layout.setStyleSheet("""#graphObj {color: #322d2d;}""")
    framed_layout.setLayout(orm_panel)

    return framed_layout

  def create_lifts_for_reps(self):
    reps_panel = QVBoxLayout()
    main_label = QLabel("Lifts For Reps")
    main_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    self.horizontal_press_label_reps = QLabel(": ".join(self.lifts_reps[0]))
    self.horizontal_press_label_reps.setFont(QFont("Ariel", 10))

    self.floor_pull_label_reps = QLabel(": ".join(self.lifts_reps[1]))
    self.floor_pull_label_reps.setFont(QFont("Ariel", 10))

    self.squat_label_reps = QLabel(": ".join(self.lifts_reps[2]))
    self.squat_label_reps.setFont(QFont("Ariel", 10))

    self.vertical_press_label_reps = QLabel(": ".join(self.lifts_reps[3]))
    self.vertical_press_label_reps.setFont(QFont("Ariel", 10))

    reps_buttons = QHBoxLayout()
    update_button = QPushButton("Update")
    update_button.clicked.connect(lambda: self.lifts_for_reps.show())
    clear_button = QPushButton("Clear")
    clear_button.clicked.connect(lambda: self.clear_lifts_for_reps())
    reps_buttons.addWidget(update_button)
    reps_buttons.addWidget(clear_button)

    reps_panel.addWidget(main_label)
    reps_panel.addWidget(self.horizontal_press_label_reps)
    reps_panel.addWidget(self.floor_pull_label_reps)
    reps_panel.addWidget(self.squat_label_reps)
    reps_panel.addWidget(self.vertical_press_label_reps)
    reps_panel.addLayout(reps_buttons)

    framed_layout = QFrame()
    framed_layout.setObjectName("graphObj")
    framed_layout.setFrameStyle(QFrame.Box)
    framed_layout.setLineWidth(3)
    framed_layout.setStyleSheet("""#graphObj {color: #322d2d;}""")
    framed_layout.setLayout(reps_panel)

    return framed_layout

  def create_function_buttons(self):
    buttons_panel = QHBoxLayout()
    lift_history_button = QPushButton()
    lift_history_button.setText("Lift History")
    lift_history_button.clicked.connect(lambda: self.lift_history_window.show())
    preferred_lists_button = QPushButton()
    preferred_lists_button.setText("Preferred Lifts")
    preferred_lists_button.clicked.connect(lambda: self.plists_window.show())

    buttons_panel.addWidget(lift_history_button)
    buttons_panel.addWidget(preferred_lists_button)
    return buttons_panel
  
  @pyqtSlot(bool)
  def changed_preferred_lifts(self, changed):
    if changed:
      self.preferred_lifts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "preferred_lifts"))
      parsed_lifts = list(self.preferred_lifts.values())
      
      one_RM_labels = [self.horizontal_press_label_ORM, self.floor_pull_label_ORM,
                       self.squat_label_ORM, self.vertical_press_label_ORM]

      lifts_for_reps_labels = [self.horizontal_press_label_reps, self.floor_pull_label_reps,
                               self.squat_label_reps, self.vertical_press_label_reps]
       
      for i, label in enumerate(one_RM_labels):
        label_text = label.text().split(":")
        label_text[0] = parsed_lifts[i]
        label.setText(": ".join(label_text))

      for i, label in enumerate(lifts_for_reps_labels):
        label_text = label.text().split(":")
        label_text[0] = parsed_lifts[i]
        label.setText(": ".join(label_text))
  
      self.refresh_graph(True)
  
  @pyqtSlot(bool)
  def changed_1RM_lifts(self, changed):
    if changed:
      fetch_weight = list(json.loads(self.db_wrapper.fetch_local_column(self.table_name, "one_rep_maxes")).values())
      self.set_1RM_labels_text(fetch_weight)

  @pyqtSlot(bool)
  def changed_lifts_for_reps(self, changed):
    if changed:
      fetch_reps_and_weight = list(json.loads(self.db_wrapper.fetch_local_column(self.table_name, "lifts_for_reps")).values())
      self.set_lifts_for_reps_labels_text(fetch_reps_and_weight)
  
  def set_lifts_for_reps_labels_text(self, text):
    lifts_for_reps_labels = [self.horizontal_press_label_reps, self.floor_pull_label_reps,
                             self.squat_label_reps, self.vertical_press_label_reps]
      
    for i, label in enumerate(lifts_for_reps_labels):
      label_text = label.text().split(": ")
      label_text[1] = " ".join(["x".join(text[i]), self.units])
      label.setText(": ".join(label_text))
  
  def set_1RM_labels_text(self, text):
    one_RM_labels = [self.horizontal_press_label_ORM, self.floor_pull_label_ORM,
                     self.squat_label_ORM, self.vertical_press_label_ORM]
    for i, label in enumerate(one_RM_labels):
      label_text = label.text().split(": ")
      label_text[1] = " ".join([text[i], self.units])
      label.setText(": ".join(label_text))

  def clear_one_rep_maxes(self):
    for exercise, value in self.one_rep_maxes.items():
      self.one_rep_maxes[exercise] = "0"
    self.db_wrapper.update_table_column(self.table_name, "one_rep_maxes", self.one_rep_maxes)
    self.set_1RM_labels_text(list(self.one_rep_maxes.values()))
    self.update_1RM_window.set_line_edit_values()
   
  def clear_lifts_for_reps(self):
    lifts_for_reps = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "lifts_for_reps"))
    for exercise in lifts_for_reps:
      lifts_for_reps[exercise] = ["0", "0"]
    self.db_wrapper.update_table_column(self.table_name, "lifts_for_reps", lifts_for_reps)
    self.set_lifts_for_reps_labels_text(list(lifts_for_reps.values()))
    self.lifts_for_reps.set_line_edit_values()
  
  def replace_graph(self, lift_type):
    new_graph = OneRMGraphCanvas(lift_type, self.rm_history, self.current_year, self)
    new_toolbar = NavigationToolbar(new_graph, self)
    new_toolbar.setStyleSheet("background-color: white;")

    old_toolbar_reference = self.graph_layout.itemAt(0).widget()
    old_graph_reference = self.graph_layout.itemAt(1).widget()
    
    self.graph_layout.replaceWidget(old_toolbar_reference, new_toolbar)
    self.graph_layout.replaceWidget(old_graph_reference, new_graph)
    
    old_toolbar_reference.deleteLater()
    old_graph_reference.deleteLater()

  def change_exercise_graph(self, exercise_name):
    lift_type = None
    for l_type, exercise in self.preferred_lifts.items():
      if exercise == exercise_name: lift_type = l_type
    self.replace_graph(lift_type)

  def change_graph_year(self, year):
    self.current_year = year
    lift_type = None
    for l_type, exercise in self.preferred_lifts.items():
      if exercise == str(self.lifts_combobox.currentText()): lift_type = l_type
    self.replace_graph(lift_type)
    self.change_year_combobox.setCurrentText(self.current_year)
  
  @pyqtSlot(bool)
  def refresh_graph(self, signal):
    if signal:
      self.rm_history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "rm_history"))
      lift_type = None
      for l_type, exercise in self.preferred_lifts.items():
        if exercise == str(self.lifts_combobox.currentText()): lift_type = l_type
      self.replace_graph(lift_type)

  def convert_lift_history_weight(self, convert_to_units):
    try:
      lift_history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "lift_history"))
    except TypeError: # lift history is empty
      return
    if convert_to_units == "kg":
      for lift in lift_history:
        if isinstance(lift[1], list): # second element of history entry is list, it is lifts_for_reps entry
          lift[1][1] = str(pounds_to_kg(float(lift[1][1])))
        else:
          lift[1] = str(pounds_to_kg(float(lift[1])))
    elif convert_to_units == "lb":
      for lift in lift_history:
        if isinstance(lift[1], list):
          lift[1][1] = str(kg_to_pounds(float(lift[1][1])))
        else:
          lift[1] = str(kg_to_pounds(float(lift[1])))
    lift_history = json.dumps(lift_history)
    self.db_wrapper.update_table_column(self.table_name, "lift_history", lift_history, convert_lift_history_units=True)

  def add_year_to_rm_history(self, year):
    new_year = {}
    for month in self.db_wrapper.months:
      exercises_dict = {}
      for lift_type in self.preferred_lifts:
        exercises_dict[lift_type] = {self.preferred_lifts[lift_type]:[]}
      new_year[month] = exercises_dict
    self.rm_history[str(year)] = new_year
    self.rm_history = json.dumps(self.rm_history)
    self.db_wrapper.update_table_column(self.table_name, "rm_history", self.rm_history)
