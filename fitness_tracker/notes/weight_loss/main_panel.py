from datetime import datetime
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QFrame, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
from fitness_tracker.user_profile.profile_db import fetch_local_user_data, fetch_units
from fitness_tracker.notes.nutrition.nutrition_db import fetch_calorie_goal
from .weight_loss_edit_dialog import WeightLossEditDialog
from .weight_loss_history import WeightLossHistory
from .weight_loss_db import (table_is_empty, create_weight_loss_table, insert_default_weight_loss_values,
                             fetch_preferred_activity)

class MainPanel(QWidget):
  def __init__(self, parent, sqlite_connection, pg_connection):
    super().__init__(parent)
    self.sqlite_connection = sqlite_connection
    self.sqlite_cursor = self.sqlite_connection.cursor()
    self.pg_connection = pg_connection
    self.pg_cursor = self.pg_connection.cursor()
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
    
    create_weight_loss_table(self.sqlite_connection)
    
    if table_is_empty(self.sqlite_cursor): insert_default_weight_loss_values(self.sqlite_connection, self.pg_connection)
    
    self.fetch_user_data()
    self.date = datetime.today().strftime("%d/%m/%Y")
    self.calorie_goal = fetch_calorie_goal(self.sqlite_cursor)
    self.units = "kg" if fetch_units(self.sqlite_cursor) == "metric" else "lb"
    self.preferred_activity = fetch_preferred_activity(self.sqlite_cursor)
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_description(), 0, 0, 1, 1)
    grid.addWidget(self.create_graph(), 1, 0, 4, 1)
    grid.addLayout(self.create_bottom_layout(), 5, 0, 3, 1)
    self.setLayout(grid)

  def create_description(self):
    description = QVBoxLayout()
    description_font = QFont("Montserrat", 12)
    description_label = QLabel("Keep notes and track your weight loss journey.", self)
    description_label.setFont(description_font)
    description_label.setFixedHeight(20)
    description.addWidget(description_label)
    return description

  def create_graph(self):
    graph_layout = QVBoxLayout()
    graph = QWidget()
    graph.setStyleSheet("background-color: yellow")

    combobox_layout = QHBoxLayout()
    months_combobox = QComboBox()
    months_combobox.addItems(["January", "February", "March", "April", "May", "June", "July",
                              "August", "September", "October", "November", "December"])
    
    change_year_combobox = QComboBox()
    change_year_combobox.addItems(["2020", "2021"])

    combobox_layout.addWidget(months_combobox)
    combobox_layout.addWidget(change_year_combobox)

    graph_layout.addWidget(graph)
    graph_layout.addLayout(combobox_layout)

    framed_graph = QFrame(self)
    framed_graph.setFrameStyle(QFrame.Box)
    framed_graph.setLineWidth(3)
    framed_graph.setLayout(graph_layout)

    return framed_graph

  def create_bottom_layout(self):
    bottom_layout = QHBoxLayout()
    bottom_layout.addWidget(self.create_weight_loss())
    bottom_layout.addWidget(self.create_cardio_notes())
    return bottom_layout
  
  def create_weight_loss(self):
    weight_loss = QVBoxLayout()
    main_label = QLabel("Weight Loss")
    main_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    current_weight_layout = QHBoxLayout()
    self.current_weight_label = QLabel(" ".join(["Current Weight:", self.current_weight, self.units]))
    update_current_weight_button = QPushButton("Update")
    update_current_weight_button.clicked.connect(lambda: self.update_value("Current Weight", self.current_weight))
    current_weight_layout.addWidget(self.current_weight_label)
    current_weight_layout.addWidget(update_current_weight_button)

    weight_goal_layout = QHBoxLayout()
    self.weight_goal_label = QLabel(" ".join(["Weight Goal:",  self.goal_weight, self.units]))
    update_weight_goal_label = QPushButton("Update")
    update_weight_goal_label.clicked.connect(lambda: self.update_value("Weight Goal", self.goal_weight))
    weight_goal_layout.addWidget(self.weight_goal_label)
    weight_goal_layout.addWidget(update_weight_goal_label)
   
    loss_per_week_layout = QHBoxLayout()
    self.loss_per_week_label = QLabel(" ".join(["Loss Per Week:", str(self.loss_per_week), self.units])) 
    update_loss_per_week_label = QPushButton("Update")
    update_loss_per_week_label.clicked.connect(lambda: self.update_value("Loss Per Week", self.loss_per_week))
    loss_per_week_layout.addWidget(self.loss_per_week_label)
    loss_per_week_layout.addWidget(update_loss_per_week_label)

    calorie_intake_layout = QHBoxLayout()
    calorie_intake_label = QLabel(" ".join(["Calorie Intake:", str(self.calorie_goal), "kcal"]))
    calorie_intake_layout.addWidget(calorie_intake_label)
    
    history_layout = QHBoxLayout()
    weight_loss_history_button = QPushButton("History")
    weight_loss_history_button.clicked.connect(lambda: self.show_weight_history())
    history_layout.addWidget(weight_loss_history_button)   
    
    weight_loss.addWidget(main_label)
    weight_loss.addLayout(calorie_intake_layout)
    weight_loss.addLayout(current_weight_layout)
    weight_loss.addLayout(weight_goal_layout)
    weight_loss.addLayout(loss_per_week_layout)
    weight_loss.addLayout(history_layout)

    weight_loss.setSpacing(5)
    framed_layout = QFrame()
    framed_layout.setObjectName("graphObj")
    framed_layout.setFrameStyle(QFrame.Box)
    framed_layout.setLineWidth(3)
    framed_layout.setStyleSheet("""#graphObj {color: #322d2d;}""")
    
    framed_layout.setLayout(weight_loss)
    
    return framed_layout

  def create_cardio_notes(self):
    cardio_notes = QVBoxLayout()
    main_label = QLabel("Cardio Notes")
    main_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))
    
    preferred_activity_layout = QHBoxLayout()
    preferred_activity_label = QLabel(" ".join(["Preferred Activity:", self.preferred_activity]))
    update_preferred_activity_label = QPushButton("Update")
    preferred_activity_layout.addWidget(preferred_activity_label)
    preferred_activity_layout.addWidget(update_preferred_activity_label)

    time_spent_layout = QHBoxLayout()
    time_spent_label = QLabel("Time Spent: 65 min.")
    update_time_spent_label = QPushButton("Update")
    time_spent_layout.addWidget(time_spent_label)
    time_spent_layout.addWidget(update_time_spent_label)

    calories_burnt_layout = QHBoxLayout()
    calories_burnt_label = QLabel("Calories Burnt: 504 kcal")
    update_calories_burnt_label = QPushButton("Update")
    calories_burnt_layout.addWidget(calories_burnt_label)
    calories_burnt_layout.addWidget(update_calories_burnt_label)

    distance_travelled_layout = QHBoxLayout()
    distance_travelled_label = QLabel("Distance Travelled: 3654 m")
    update_distance_travelled_label = QPushButton("Update")
    distance_travelled_layout.addWidget(distance_travelled_label)
    distance_travelled_layout.addWidget(update_distance_travelled_label)
    
    history_layout = QHBoxLayout()
    cardio_history_button = QPushButton("History")
    history_layout.addWidget(cardio_history_button)
    
    cardio_notes.addWidget(main_label)
    cardio_notes.addLayout(preferred_activity_layout)
    cardio_notes.addLayout(time_spent_layout)
    cardio_notes.addLayout(calories_burnt_layout)
    cardio_notes.addLayout(distance_travelled_layout)
    cardio_notes.addLayout(history_layout)

    cardio_notes.setSpacing(5)
    framed_layout = QFrame()
    framed_layout.setObjectName("graphObj")
    framed_layout.setFrameStyle(QFrame.Box)
    framed_layout.setLineWidth(3)
    framed_layout.setStyleSheet("""#graphObj {color: #322d2d;}""")
    
    framed_layout.setLayout(cardio_notes)
    
    return framed_layout

  def update_value(self, to_edit, old_value):
    fitness_goal = None
    date = None
    if to_edit == "Loss Per Week": fitness_goal = self.user_data["Goal Params"][0]
    elif to_edit == "Current Weight": date = self.date
    dialog = WeightLossEditDialog(to_edit, old_value, self.sqlite_connection, self.pg_connection, fitness_goal, date)
    dialog.update_label_signal.connect(lambda label_to_update: self.update_weight_loss_label(label_to_update))
    dialog.show()
  
  @pyqtSlot(bool)
  def update_weight_loss_label(self, signal):
    if signal:
      self.fetch_user_data()
      self.current_weight_label.setText(" ".join(["Current Weight:", str(self.current_weight), self.units]))
      self.weight_goal_label.setText(" ".join(["Weight Goal:", str(self.goal_weight), self.units]))
      self.loss_per_week_label.setText(" ".join(["Loss Per Week:", str(self.loss_per_week), self.units]))

  def fetch_user_data(self):
    self.user_data = fetch_local_user_data(self.sqlite_cursor)
    self.current_weight = self.user_data["Weight"]
    self.goal_weight = self.user_data["Weight Goal"]
    self.loss_per_week = self.user_data["Goal Params"][1]

  def show_weight_history(self):
    self.history = WeightLossHistory(self.sqlite_connection, self.pg_connection)
    self.history.update_weight_loss_label_signal.connect(lambda signal: self.update_weight_loss_label(signal))
    self.history.setGeometry(100, 200, 300, 300) 
    self.history.show()
