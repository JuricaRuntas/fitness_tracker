import os
import json
from functools import partial
from datetime import datetime
from typing import ContextManager
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QMainWindow, QWidget, QGridLayout, QFrame, QLabel, QProgressBar,
                             QPushButton, QFrame, QHBoxLayout, QVBoxLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, 
                             QLineEdit, QScrollArea)
from PyQt5.QtGui import QDoubleValidator, QFont, QCursor, QIcon, QIntValidator
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal
from fitness_tracker.database_wrapper import DatabaseWrapper
from .change_weight_dialog import ChangeWeightDialog
from .spoonacular import FoodDatabase
from configparser import ConfigParser

config_path = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, "config", "settings.ini")
config = ConfigParser()
config.read(config_path)

path = os.path.abspath(os.path.dirname(__file__))
icons_path = os.path.join(path, "icons")

icons = {"pencil": os.path.join(icons_path, "pencil.png"),
         "plus": os.path.join(icons_path, "plus.png"),
         "left": os.path.join(icons_path, "left.png"),
         "right": os.path.join(icons_path, "right.png"),
         "search": os.path.join(icons_path, "search.png")}

class NotesPanel(QWidget):
  change_layout_signal = pyqtSignal(str)

  def __init__(self, parent):
    super().__init__(parent)
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Nutrition"
    self.db_wrapper.create_local_table("Nutrition")
    self.selected_week = "Present"
    self.selected_day = "Monday"
    self.selected_past_week = 0
    self.daily_summary = True
    self.write_default_settings()
    if self.db_wrapper.local_table_is_empty(self.table_name): self.db_wrapper.insert_default_values(self.table_name)
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
    }
    QTableWidget{
      background-color: rgba(135, 41, 41, 20%);  
      border: 0px;
      font-size: 14px;
    }
    QHeaderView:section{
      background-color: rgb(96,58,54);  
      border: 1px solid;
      border-color: #3C2323
    }
    QProgressBar{
      border: 1px solid;
      border-color: #d7d7d7;
      background-color: #d7d7d7;
    }
    QProgressBar:chunk{
      background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #434343, stop: 1 #440d0f);    
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
    self.meal_plans = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "meal_plans"))
    #if datetime.now().strftime("%V") != self.meal_plans["Current Week Number"]:
    #  self.db_wrapper.rotate_meals(self.meal_plans)
    self.units = "kg" if self.db_wrapper.fetch_local_column("Users", "units") == "metric" else "lb"
    
    self.user_data = self.db_wrapper.fetch_local_user_info()
    self.user_weight = self.user_data["Weight"]
    self.user_goal_weight = self.user_data["Weight Goal"]
    self.goal_parameters = self.user_data["Goal Params"]
    self.calorie_goal = self.db_wrapper.fetch_local_column(self.table_name, "calorie_goal")
    self.gender = self.user_data["Gender"]
    self.user_height = self.user_data["Height"]
    self.user_age = self.user_data["Age"]
    self.loss_per_week = self.goal_parameters[1]
    self.user_activity = self.goal_parameters[0]
    self.change_weight_dialog = ChangeWeightDialog()
    self.change_weight_dialog.change_current_weight_signal.connect(lambda weight: self.change_current_weight(weight))
    self.change_weight_dialog.change_goal_weight_signal.connect(lambda weight: self.change_goal_weight(weight))
    self.change_weight_dialog.change_calorie_goal_signal.connect(lambda calorie_goal: self.change_calorie_goal(calorie_goal))
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")

  @pyqtSlot(str)
  def change_current_weight(self, weight):
    self.current_weight_label.setText(" ".join(["Current Weight:", weight, self.units]))
  
  @pyqtSlot(str)
  def change_goal_weight(self, weight):
    self.goal_weight_label.setText(" ".join(["Current Weight:", weight, self.units]))

  @pyqtSlot(str)
  def change_calorie_goal(self, calorie_goal):
    self.calorie_goal_label.setText(" ".join(["Calorie Goal: \n", calorie_goal]))
    self.progress_bar.setMaximum(int(calorie_goal))
    calories_left = self.progress_bar.maximum() - self.progress_bar.value()
    self.progress_bar.setFormat(" ".join([str(calories_left), "calories left"]))

  def create_panel(self):
    grid = QGridLayout()
    grid.setContentsMargins(2, 0, 8, 8)
    grid.addWidget(self.create_description(), 0, 0, 1, 3)
    #grid.addLayout(self.create_swap_buttons(), 0, 1, 1, 1)
    grid.addLayout(self.create_stats(), 6, 0, 6, 1)
    grid.addWidget(self.create_nutrition_summary(), 6, 1, 6, 1)
    grid.addLayout(self.create_notes(), 16, 0, 10, 3)
    self.setLayout(grid)

  def create_description(self):
    self.description = QLabel("Improve your diet and eating habits by tracking what you eat and searching through our database for healthy \nfood.")
    return self.description

  def create_nutrients_panel(self):
    global nutrients
    self.nutrients = NutrientsPanel(self)
    self.nutrients.show()

  def create_nutrition_summary(self):
    nsummary_layout = QVBoxLayout()
    daily_monthlyavg_buttons = QHBoxLayout()
    daily_monthlyavg_buttons.addStretch(0)
    dm_style = """
    QPushButton{
      background-color: #440D0F;
      border: 1px solid;
      border-color: #603a36;
    }
    QPushButton:hover:!pressed{
      background-color: #5D1A1D
    }
    QPushButton:pressed{
      background-color: #551812
    }
    """
    dm_style_selected = """"""
    daily_button = QPushButton("Daily")
    daily_button.clicked.connect(lambda:self.set_daily())
    daily_button.setFixedWidth(130)
    daily_button.setStyleSheet(dm_style)
    monthly_button = QPushButton("Monthly")
    monthly_button.setFixedWidth(130)
    monthly_button.setStyleSheet(dm_style)
    monthly_button.clicked.connect(lambda:self.set_monthly())
    nutrients_button = QPushButton("Nutrients")
    nutrients_button.clicked.connect(lambda:self.create_nutrients_panel())
    nutrients_button.setFixedWidth(145)
    daily_monthlyavg_buttons.addWidget(daily_button)
    daily_monthlyavg_buttons.addWidget(monthly_button)
    daily_monthlyavg_buttons.addWidget(nutrients_button)

    self.nutrients = (["Calories", 1, 'kcal'], ["Protein", 21, 'g'], ["Carbohydrates", 32, 'g'], ["Fat", 24, 'g'], ["Fiber", 13, 'g'], ["Sugar", 6, 'g'])
    nsummary_layout.addLayout(daily_monthlyavg_buttons)
    self.options = config.items('NUTRITION')
    self.totals = [0] * len(self.nutrients)
    self.nutrition_labels = [None] * len(self.nutrients)
    for i in range(len(self.nutrition_labels)):
      if config['NUTRITION'].get(self.options[i][0]) == 'yes':
        for item in self.meal_plans['Present']['Monday']:
          for subitem in self.meal_plans['Present']['Monday'][item]:
            self.totals[i] += int(self.get_nutrient(subitem, self.nutrients[i][0]))
            #self.totals[i] += int(self.get_nutrient(subitem["nutrition"]["nutrients"][self.nutrients[i][1]]["amount"]))
        self.nutrition_labels[i] = QLabel(self.nutrients[i][0] + ": " + str(self.totals[i]) + self.nutrients[i][2])
        self.nutrition_labels[i].setAlignment(Qt.AlignCenter)
        nsummary_layout.addWidget(self.nutrition_labels[i])
      else:
        self.nutrition_labels[i] = QLabel("")
        self.nutrition_labels[i].setFixedHeight(0)
        self.nutrition_labels[i].setAlignment(Qt.AlignCenter)
        nsummary_layout.addWidget(self.nutrition_labels[i])

    #temp_label = QLabel("Proteins: 30g \nCarbs: 300g \nCalories: 2000kcal")
    #temp_label.setAlignment(Qt.AlignCenter)
    #nsummary_layout.addWidget(temp_label) # Temp

    nsummary_layout_framed = QFrame()
    nsummary_layout_framed.setLayout(nsummary_layout)
    nsummary_layout_framed.setFrameStyle(QFrame.Box)
    nsummary_layout_framed.setLineWidth(3)
    nsummary_layout_framed.setObjectName("frame")
    nsummary_layout_framed.setStyleSheet("""#frame {color: #322d2d;}""")
    return nsummary_layout_framed

  def create_stats(self):
    stats_layout = QHBoxLayout()
    
    calorie_goal_layout = QVBoxLayout()
    calorie_goal_frame = QFrame()
    self.dci_label = QLabel("Daily Calorie Intake")
    self.dci_label.setAlignment(Qt.AlignCenter)
    self.calorie_goal_label = QLabel(" ".join(["Daily Goal: ", self.calorie_goal, "kcal"]))
    self.calorie_goal_label.setFont(QFont("Ariel", 15))
    self.calorie_goal_label.setAlignment(Qt.AlignCenter)

    self.total_day_calorie = 0
    for i in self.meal_plans[self.selected_week][self.selected_day]:
      for item in self.meal_plans[self.selected_week][self.selected_day][i]:
        self.total_day_calorie += item["nutrition"]["nutrients"][1]["amount"]
     
    self.progress_bar = QProgressBar()
    self.progress_bar.setStyleSheet("background-color:grey;")
    self.progress_bar.setMaximum(int(self.calorie_goal))
    self.progress_bar.setValue(self.total_day_calorie)
    if int(self.total_day_calorie) > int(self.calorie_goal):
      self.progress_bar.setValue(int(self.calorie_goal))
    calories_left = self.progress_bar.maximum() - self.total_day_calorie
    self.progress_bar.setFormat("")
    self.progress_bar.setAlignment(Qt.AlignCenter)
    self.progress_bar.setMaximumHeight(18)
    self.calorie_label = QLabel(str(calories_left) + " calories left from goal")
    if int(self.total_day_calorie) > int(self.calorie_goal):
      self.calorie_label.setText(str(abs(calories_left)) + " calories over goal")
    self.calorie_label.setAlignment(Qt.AlignCenter)

    intake_button_layout = QHBoxLayout()
    self.calculate_intake = QPushButton("Calculate Daily Intake")
    self.calculate_intake.clicked.connect(lambda: self.calculate_calorie_intake(float(self.user_weight), float(self.user_height), float(self.user_age), self.gender, self.user_activity, self.loss_per_week))
    self.edit_intake = QPushButton("Edit Daily Intake")
    self.edit_intake.clicked.connect(lambda: self.show_intake_entry())
    intake_button_layout.addWidget(self.calculate_intake)
    intake_button_layout.addWidget(self.edit_intake)

    calorie_goal_layout.addWidget(self.dci_label)
    calorie_goal_layout.addWidget(self.progress_bar)
    calorie_goal_layout.addWidget(self.calorie_label)
    calorie_goal_layout.addWidget(self.calorie_goal_label)
    calorie_goal_layout.addLayout(intake_button_layout)

    calorie_goal_frame.setLayout(calorie_goal_layout)
    calorie_goal_frame.setFrameStyle(QFrame.Box)
    calorie_goal_frame.setLineWidth(3)
    calorie_goal_frame.setObjectName("frame")
    calorie_goal_frame.setStyleSheet("""#frame {color: #322d2d;}""")
    stats_layout.addWidget(calorie_goal_frame)

    return stats_layout

  def create_notes(self):    
    meals = self.meal_plans['Present']['Monday']
    number_of_meals = len(meals)

    self.table = QTableWidget(16, number_of_meals)
    self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.table.verticalHeader().setVisible(False)
    for i in range(self.table.rowCount()):
      self.table.setRowHeight(i, 50)

    meal_entries = [None] * number_of_meals
    plus_button = [None] * number_of_meals
    for i in range(number_of_meals):
      plus_button[i] = QPushButton("+")
    
    buttons = plus_button
    j = i = k = 0
    for item in meals:
      buttons[i].setFlat(True)
      buttons[i].clicked.connect(partial(self.add_button_func, self.selected_week, self.selected_day, item))
      self.table.setHorizontalHeaderItem(i, QTableWidgetItem(item))
      self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
      for key in meals[item]:
        widget = QLabel(str(int(key['amount'])) + "g " + key['name'])
        remove_widget = QPushButton("x")
        remove_widget.setFixedSize(24, 24)
        remove_widget.clicked.connect(partial(self.remove_food, key, item))
        helper_layout = QHBoxLayout()
        helper_layout.addWidget(widget)
        helper_layout.addWidget(remove_widget)
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(helper_layout)
        self.table.setCellWidget(k, j, wrapper_widget)
        k += 1
      self.table.setCellWidget(k, j, buttons[i])
      j += 1
      i += 1
      k = 0

    for i in range(2):
      self.table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
    table_title_layout = QHBoxLayout()
    style = """QPushButton{background-color: rgba(88, 41, 41, 20%);
               border: 0px solid;
               text-align: center;}
               QPushButton:hover:!pressed {
                 background-color: rgba(120, 55, 55, 20%);
               }
               QPushButton:pressed {
                 background-color: rgba(166, 55, 55, 20%);
               }
             """
    self.past_combobox = QComboBox()
    self.past_combobox.addItems(["1 Week Ago", "2 Weeks Ago", "3 Weeks Ago", "4 Weeks Ago", "5 Weeks Ago", "6 Weeks Ago", "7 Weeks Ago", "8 Weeks Ago"])
    self.past_combobox.activated[str].connect(self.index_past_week)
    thisweek_button = QPushButton("This Week")
    thisweek_button.setStyleSheet(style)
    thisweek_button.setCursor(QCursor(Qt.PointingHandCursor))
    thisweek_button.clicked.connect(lambda:self.change_week("Present", 0))
    nextweek_button = QPushButton("Next Week")
    nextweek_button.setStyleSheet(style)
    nextweek_button.setCursor(QCursor(Qt.PointingHandCursor))
    nextweek_button.clicked.connect(lambda:self.change_week("Future", 0))
    manage_meals = QPushButton("Manage Meals")
    manage_meals.setStyleSheet(style)
    manage_meals.setCursor(QCursor(Qt.PointingHandCursor))
    manage_meals.clicked.connect(lambda:self.open_meal_manager())
    self.day_combobox = QComboBox()
    self.day_combobox.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    self.day_combobox.activated.connect(lambda:self.change_day(self.day_combobox.currentText()))

    table_title_layout.addWidget(self.past_combobox)
    table_title_layout.addWidget(thisweek_button)
    table_title_layout.addWidget(nextweek_button)
    table_title_layout.addWidget(manage_meals)
    table_title_layout.addWidget(self.day_combobox)

    table_wrapper = QVBoxLayout()
    table_wrapper.addWidget(self.table)
    
    grid = QGridLayout()
    grid.setVerticalSpacing(0)
    grid.addLayout(table_title_layout, 0, 0)
    grid.addLayout(table_wrapper, 1, 0)

    framed_grid = QFrame()
    framed_grid.setFrameStyle(QFrame.Box)
    framed_grid.setLineWidth(3)
    framed_grid.setObjectName("frame")
    framed_grid.setStyleSheet("""#frame {color: #322d2d;}""")
    framed_grid.setLayout(grid)

    framed_layout = QVBoxLayout()
    framed_layout.addWidget(framed_grid)
    
    return framed_layout

  def write_default_settings(self):
    nutrients = ["Calories", "Protein", "Carbohydrates", "Fat", "Fiber", "Sugar"]
    if config.has_section('NUTRITION') == False:
      config.add_section('NUTRITION')
      config.set('NUTRITION', 'ShowCalories', 'yes')
      config.set('NUTRITION', 'ShowProtein', 'yes')
      config.set('NUTRITION', 'ShowCarbohydrates', 'yes')
      config.set('NUTRITION', 'ShowFat', 'no')
      config.set('NUTRITION', 'ShowFiber', 'no')
      config.set('NUTRITION', 'ShowSugar', 'no')
      with open(config_path, 'w') as configfile:
        config.write(configfile)   
    for i in range(len(nutrients)):
      if config.has_option('NUTRITION', "Show" + nutrients[i]) == False:
        config.set('NUTRITION', "Show" + nutrients[i], 'yes')        
        with open(config_path, 'w') as configfile:
          config.write(configfile)   

  def set_monthly(self):
    self.daily_summary = False
    self.calculate_monthly_totals()

  def set_daily(self):
    self.daily_summary = True
    self.recalculate_daily_totals()   

  def recalculate_daily_totals(self):
    for i in range(len(self.totals)):
      self.totals[i] = 0
    for i in range(len(self.nutrition_labels)):
      if config['NUTRITION'].get(self.options[i][0]) == 'yes':
        if self.selected_week == 'Past':
          for item in self.meal_plans[self.selected_week][self.selected_past_week][self.selected_day]:
            for subitem in self.meal_plans[self.selected_week][self.selected_past_week][self.selected_day][item]:
              self.totals[i] += int(self.get_nutrient(subitem, self.nutrients[i][0]))
        else:
          for item in self.meal_plans[self.selected_week][self.selected_day]:
            for subitem in self.meal_plans[self.selected_week][self.selected_day][item]:
              self.totals[i] += int(self.get_nutrient(subitem, self.nutrients[i][0]))
        if self.nutrition_labels[i] != None: self.nutrition_labels[i].setText(self.nutrients[i][0] + ": " + str(self.totals[i]) + self.nutrients[i][2]) 

  def update_nutrient_labels(self):
    temp_nutrients = (["Calories", 1, 'kcal'], ["Protein", 21, 'g'], ["Carbohydrates", 32, 'g'], ["Fat", 24, 'g'], ["Fiber", 13, 'g'], ["Sugar", 6, 'g'])
    for i in range(len(self.nutrition_labels)):
      if config['NUTRITION'].get(self.options[i][0]) == 'yes':
        self.nutrition_labels[i].setText(temp_nutrients[i][0] + ": " + str(self.totals[i]) + temp_nutrients[i][2])
        self.nutrition_labels[i].setAlignment(Qt.AlignCenter)
        self.nutrition_labels[i].setFixedHeight(32)
      else:
        self.nutrition_labels[i].setText("")
        self.nutrition_labels[i].setFixedHeight(0)
        self.nutrition_labels[i].setAlignment(Qt.AlignCenter)

  def calculate_monthly_totals(self):
    for i in range(len(self.totals)):
      self.totals[i] = 0
    for i in range(len(self.nutrition_labels)):
      if config['NUTRITION'].get(self.options[i][0]) == 'yes':
        for item in self.meal_plans['Past'][0]:
          for subitem in self.meal_plans['Past'][0][item]:
            for subsubitem in self.meal_plans['Past'][0][item][subitem]:
              self.totals[i] += int(self.get_nutrient(subsubitem, self.nutrients[i][0]))
        for item in self.meal_plans['Past'][1]:
          for subitem in self.meal_plans['Past'][1][item]:
            for subsubitem in self.meal_plans['Past'][1][item][subitem]:
              self.totals[i] += int(self.get_nutrient(subsubitem, self.nutrients[i][0]))
        for item in self.meal_plans['Past'][2]:
          for subitem in self.meal_plans['Past'][2][item]:
            for subsubitem in self.meal_plans['Past'][2][item][subitem]:
              self.totals[i] += int(self.get_nutrient(subsubitem, self.nutrients[i][0]))
        for item in self.meal_plans['Present']:
          for subitem in self.meal_plans['Present'][item]:
            for subsubitem in self.meal_plans['Present'][item][subitem]:
              self.totals[i] += int(self.get_nutrient(subsubitem, self.nutrients[i][0]))
        self.totals[i] /= 28
        self.totals[i] = int(self.totals[i])
        if self.nutrition_labels[i] != None: self.nutrition_labels[i].setText(self.nutrients[i][0] + ": " + str(self.totals[i]) + self.nutrients[i][2])  

  def open_meal_manager(self):
    global manager
    if self.selected_week != "Past":
      manager = MealPlanPanel(self, self.selected_week, self.selected_day)
      manager.show()

  def index_past_week(self, week_string):
    week = "Past"
    index = 0
    items = [self.past_combobox.itemText(i) for i in range(self.past_combobox.count())]
    for item in items:
      if (item == week_string):
        break
      index += 1
    self.change_week(week, index)

  def update_calorie_goal(self):
    self.meal_plans = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "meal_plans")) 
    self.calorie_goal = self.db_wrapper.fetch_local_column(self.table_name, "calorie_goal")
    self.progress_bar.setMaximum(int(self.calorie_goal))
    self.calorie_goal_label.setText(" ".join(["Daily Goal: ", self.calorie_goal, "kcal"]))
    self.total_day_calorie = 0
    if self.selected_week != "Past":
      for i in self.meal_plans[self.selected_week][self.selected_day]:
        for item in self.meal_plans[self.selected_week][self.selected_day][i]:
         self.total_day_calorie += item["nutrition"]["nutrients"][1]["amount"]
    else:
      for i in self.meal_plans[self.selected_week][self.selected_past_week][self.selected_day]:
        for item in self.meal_plans[self.selected_week][self.selected_past_week][self.selected_day][i]:
         self.total_day_calorie += item["nutrition"]["nutrients"][1]["amount"]
    self.progress_bar.setValue(self.total_day_calorie)
    if int(self.total_day_calorie) > int(self.calorie_goal):
      self.progress_bar.setValue(int(self.calorie_goal))
    calories_left = self.progress_bar.maximum() - self.total_day_calorie
    self.calorie_label.setText((str(calories_left) + " calories left from goal"))
    if int(self.total_day_calorie) > int(self.calorie_goal):
      self.calorie_label.setText(str(abs(calories_left)) + " calories over goal")

  def change_week(self, week, past_week_index):
    self.selected_week = week
    self.selected_past_week = past_week_index
    if self.daily_summary == True:
      self.recalculate_daily_totals()
    self.repopulate_table()
    self.update_calorie_goal()

  def change_day(self, day):
    self.selected_day = day
    self.recalculate_daily_totals()
    self.repopulate_table()
    self.update_calorie_goal()

  def repopulate_table(self):
    self.meal_plans = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "meal_plans"))
    for i in range (self.table.rowCount()):
      for j in range(self.table.columnCount()):
        self.table.removeCellWidget(i, j)

    if self.selected_week == "Past":
      meals = self.meal_plans[self.selected_week][self.selected_past_week][self.selected_day]
    else: 
      meals = self.meal_plans[self.selected_week][self.selected_day]
    number_of_meals = len(meals)
    meal_entries = [None] * number_of_meals
    plus_button = [None] * number_of_meals
    for i in range(number_of_meals):
      plus_button[i] = QPushButton("+")

    while self.table.columnCount() < number_of_meals:
      self.table.insertColumn(1)
    while self.table.columnCount() > number_of_meals:
      self.table.removeColumn(1)

    buttons = plus_button
    j = i = k = 0
    for item in meals:
      buttons[i].setFlat(True)
      buttons[i].clicked.connect(partial(self.add_button_func, self.selected_week, self.selected_day, item))
      self.table.setHorizontalHeaderItem(i, QTableWidgetItem(item))
      self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
      for key in meals[item]:
        widget = QLabel(str(int(key['amount'])) + "g " + key['name'])
        remove_widget = QPushButton("x")
        remove_widget.setFixedSize(24, 24)
        remove_widget.clicked.connect(partial(self.remove_food, key, item))
        helper_layout = QHBoxLayout()
        helper_layout.addWidget(widget)
        helper_layout.addWidget(remove_widget)
        wrapper_widget = QWidget()
        wrapper_widget.setLayout(helper_layout)
        self.table.setCellWidget(k, j, wrapper_widget)
        k += 1
      if self.selected_week != 'Past':
        self.table.setCellWidget(k, j, buttons[i])
      j += 1
      i += 1
      k = 0
    self.update_calorie_goal()

  def remove_food(self, food, meal):
    if self.selected_week == "Present":
      self.db_wrapper.delete_food_from_meal(food['name'], meal, self.selected_day, True, False)
    if self.selected_week == "Future":
      self.db_wrapper.delete_food_from_meal(food, meal, self.selected_day, False, True)
    self.meal_plans = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "meal_plans"))
    if self.daily_summary == True:
      self.recalculate_daily_totals()
    else:
      self.calculate_monthly_totals()
    self.repopulate_table()

  def get_nutrient(self, info, nutrient):
    index = 0
    for i in info["nutrition"]["nutrients"]:
      if info["nutrition"]["nutrients"][index]["title"] == nutrient:
        return info["nutrition"]["nutrients"][index]["amount"]
      index += 1
    return 0      

  def add_button_func(self, week, day, meal):
    global panel
    panel = FoodDBSearchPanel(self, week, day, meal)
    panel.show()

  def calculate_calorie_intake(self, weight, height, age, gender, activity, weight_goal):
    bmr = self.calculate_bmr(weight, height, age, gender)
    #maintain 100%, 0.25kg/w 90%, 0.5kg/w 79%, 1kg/w 59%
    #"Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"
    if activity == "Sedentary":
      sedentary_factor = 1.2
      bmr *= sedentary_factor
    elif activity == "Lightly active":
      light_factor = 1.375
      bmr *= light_factor
    elif activity == "Moderately active":
      moderate_factor = 1.465
      bmr *= moderate_factor
    elif activity == "Active":
      active_factor = 1.55
      bmr *= active_factor
    elif activity == "Very active":
      very_active_factor = 1.725
      bmr *= very_active_factor
    elif activity == "Extra active":
      extra_active_factor = 1.9
      bmr *= extra_active_factor
    if weight_goal == "0.25":
      bmr *= 0.9
    elif weight_goal == "0.5":
      bmr *= 0.79
    elif weight_goal == "1":
      bmr *= 0.59
    self.db_wrapper.update_table_column(self.table_name, "calorie_goal", int(bmr))
    self.calorie_goal = bmr
    self.calorie_goal = int(self.calorie_goal)
    self.calorie_goal = str(self.calorie_goal)
    self.calorie_goal_label.setText(" ".join(["Daily Goal: ", self.calorie_goal, "kcal"]))
    self.update_calorie_goal()

  def calculate_bmr(self, weight, height, age, gender):
    #Only calculates base BMR, depending on exercise level, BMR will be multiplied
    #Mifflin-St Jeor Equation
    weight *= 10
    height *= 6.25
    age *= 5
    bmr = weight + height - age
    if gender == "female":
      bmr -= 161
    else:
      bmr += 5
    return int(bmr)

  def show_intake_entry(self):
    global entry
    entry = EditDailyIntake(self)
    entry.show()

class EditDailyIntake(QWidget):
  def __init__(self, parent):
    super().__init__()
    self.this_parent = parent
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Nutrition"
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
    entry_label = QLabel("Edit Intake")

    self.calorie_line_edit = QLineEdit()
    self.calorie_line_edit.setValidator(QIntValidator())

    helper_layout = QHBoxLayout()

    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close_button())

    confirm_button = QPushButton("Confirm")
    confirm_button.clicked.connect(lambda: self.confirm_button())

    helper_layout.addWidget(cancel_button)
    helper_layout.addWidget(confirm_button)

    layout.addWidget(entry_label)
    layout.addWidget(self.calorie_line_edit)
    layout.addLayout(helper_layout)

    return layout

  def close_button(self):
    self.close()

  def confirm_button(self):
    if self.calorie_line_edit.text() != "":
      self.db_wrapper.update_table_column(self.table_name, "calorie_goal", self.calorie_line_edit.text())
      self.this_parent.update_calorie_goal()
      self.close()

class FoodDBSearchPanel(QWidget):
  def __init__(self, parentobj, week, day, meal):
    super().__init__()
    self.db_wrapper = DatabaseWrapper()
    self.parentobj = parentobj
    self.week = week
    self.day = day
    self.meal = meal
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
    self.setWindowModality(Qt.ApplicationModal)
    self.setMinimumWidth(430)
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
    }
    QScrollArea{
      background-color: #1A1A1A;
    }""")
    layout = QVBoxLayout()
    layout.addLayout(self.create_search_bar())
    layout.addWidget(self.create_search_results())
    layout.addLayout(self.create_confirm_cancel())
    self.setLayout(layout)

  def create_search_bar(self):
    search_bar_layout = QHBoxLayout()
    search_bar_line_edit = QLineEdit()
    search_bar_line_edit.setPlaceholderText("Search")

    self.search_bar_amount = QLineEdit()
    self.search_bar_amount.setPlaceholderText("Amount")
    self.search_bar_amount.setFixedWidth(120)
    self.search_bar_amount.setValidator(QDoubleValidator())

    search_icon = QIcon(icons["search"])

    search_bar_button = QPushButton()
    search_bar_button.setIcon(search_icon)
    search_bar_button.clicked.connect(lambda:self.update_search_results(search_bar_line_edit.text()))

    search_bar_layout.addWidget(search_bar_line_edit)
    search_bar_layout.addWidget(self.search_bar_amount)
    search_bar_layout.addWidget(search_bar_button)

    return search_bar_layout

  def create_search_results(self):
    self.result_layout = QVBoxLayout()
    self.result_layout.setAlignment(Qt.AlignTop)
    
    #with open('temp.json', 'r') as datafile:
    #  food_info_temp = json.load(datafile)
    #response_button = [None] * len(food_info_temp)
    #for i in range(len(food_info_temp)):
    #  response_button[i] = QPushButton(str(food_info_temp[i]["name"]) + " " + str(self.get_nutrient(food_info_temp[i], "Calories")))
    #  response_button[i].clicked.connect(partial(self.result_to_data, food_info_temp[i]))
    #  self.result_layout.addWidget(response_button[i])
    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    widg = QWidget()
    widg.setLayout(self.result_layout)
    self.scroll_area.setWidget(widg)
    self.scroll_area.setFixedSize(415, 550)
    return self.scroll_area

  def get_nutrient(self, info, nutrient):
    index = 0
    for i in info["nutrition"]["nutrients"]:
      if info["nutrition"]["nutrients"][index]["title"] == nutrient:
        return info["nutrition"]["nutrients"][index]["amount"]
      index += 1
    return 0

  def update_search_results(self, query):
    for i in reversed(range(self.result_layout.count())): 
      self.result_layout.itemAt(i).widget().setParent(None)
    api = FoodDatabase()
    response = api.food_search(query, 512)
    response_button = [None] * len(response)
    food_info = [None] * len(response)
    for i in range(len(response)):
      food_info[i] = api.food_info(response[i]["id"], "g", float(self.search_bar_amount.text()))
      response_button[i] = QPushButton(str(food_info[i]["name"]) + " " + str(self.get_nutrient(food_info[i], "Calories")))
      response_button[i].clicked.connect(partial(self.result_to_data, food_info[i]))
      self.result_layout.addWidget(response_button[i])

  def create_confirm_cancel(self):
    layout = QHBoxLayout()

    cancel = QPushButton("Cancel")
    cancel.clicked.connect(lambda:self.closefunc())

    confirm = QPushButton("Confirm")
    confirm.clicked.connect(lambda:self.closefunc())

    layout.addWidget(cancel)
    #layout.addWidget(confirm)

    return layout

  def result_to_data(self, select_response):
    if self.week == "Present":
      self.db_wrapper.update_meal(self.meal, select_response, self.day, True, False)
    elif self.week == "Future":
      self.db_wrapper.update_meal(self.meal, select_response, self.day, False, True)
    #test stage
    self.parentobj.meal_plans = json.loads(self.db_wrapper.fetch_local_column(self.parentobj.table_name, "meal_plans"))
    self.parentobj.repopulate_table()
    if self.parentobj.daily_summary == True:
      self.parentobj.recalculate_daily_totals()
    else:
      self.parentobj.calculate_monthly_totals()
    self.close()
    return

  def closefunc(self):
    self.close()

class MealPlanPanel(QWidget):
  def __init__(self, parent, week, day):
    super().__init__()
    self.this_parent = parent
    self.week = week
    self.day = day
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
    self.setWindowModality(Qt.ApplicationModal)
    self.db_wrapper = DatabaseWrapper()
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
    }
    QScrollArea{
      background-color: #1A1A1A;
    }""")
    self.table_name = "Nutrition"
    self.meal_plans = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "meal_plans"))
    self.this_layout = self.create_main_panel()
    self.setFixedSize(250, 500)
    #self.layout.addLayout(self.create_main_panel())
    self.setLayout(self.this_layout)

  def create_main_panel(self):
    layout = QVBoxLayout()
    self.meal_number = len(self.meal_plans[self.week][self.day])
    self.horizontal_layouts = [None] * len(self.meal_plans[self.week][self.day])
    self.meal_labels = [None] * len(self.meal_plans[self.week][self.day])
    self.meal_rename = [None] * len(self.meal_plans[self.week][self.day])
    self.meal_remove = [None] * len(self.meal_plans[self.week][self.day])
    add_button = QPushButton("Add (" + str(self.meal_number) + "/7)")
    add_button.clicked.connect(lambda:self.add_meal())
    close_button = QPushButton("Close")
    close_button.clicked.connect(lambda:self.close())
    j = 0
    for i in self.meal_plans[self.week][self.day]:
      self.horizontal_layouts[j] = QHBoxLayout()
      self.meal_labels[j] = QLabel(i)
      self.meal_remove[j] = QPushButton("-")
      self.meal_remove[j].setFixedSize(32, 32)
      self.meal_rename[j] = QPushButton("E")
      self.meal_rename[j].setFixedSize(32, 32)
      self.meal_remove[j].clicked.connect(partial(self.remove_meal, i))
      self.meal_rename[j].clicked.connect(partial(self.open_rename_query, i))
      self.horizontal_layouts[j].addWidget(self.meal_labels[j])
      self.horizontal_layouts[j].addWidget(self.meal_rename[j])
      self.horizontal_layouts[j].addWidget(self.meal_remove[j])
      layout.addLayout(self.horizontal_layouts[j])
      j += 1
    layout.addWidget(add_button)
    layout.addWidget(close_button)
    return layout

  def update(self):            
    self.meal_plans = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "meal_plans"))
    self.meal_number = len(self.meal_plans[self.week][self.day])
    for i in range(len(self.horizontal_layouts)):
      for j in reversed(range(self.horizontal_layouts[i].count())):
        self.horizontal_layouts[i].itemAt(j).widget().setParent(None)
    for i in reversed(range(self.this_layout.count())):
      item = self.this_layout.itemAt(i)
      if item.widget() != None:
        item.widget().setParent(None)
    self.horizontal_layouts = [None] * len(self.meal_plans[self.week][self.day])
    self.meal_labels = [None] * len(self.meal_plans[self.week][self.day])
    self.meal_rename = [None] * len(self.meal_plans[self.week][self.day])
    self.meal_remove = [None] * len(self.meal_plans[self.week][self.day])
    add_button = QPushButton("Add (" + str(self.meal_number) + "/7)")
    add_button.clicked.connect(lambda:self.add_meal())
    close_button = QPushButton("Close")
    close_button.clicked.connect(lambda:self.close())
    j = 0
    for i in self.meal_plans[self.week][self.day]:
      self.horizontal_layouts[j] = QHBoxLayout()
      self.meal_labels[j] = QLabel(i)
      self.meal_remove[j] = QPushButton("-")
      self.meal_remove[j].setFixedSize(32, 32)
      self.meal_rename[j] = QPushButton("E")
      self.meal_rename[j].setFixedSize(32, 32)
      self.meal_remove[j].clicked.connect(partial(self.remove_meal, i))
      self.meal_rename[j].clicked.connect(partial(self.open_rename_query, i))
      self.horizontal_layouts[j].addWidget(self.meal_labels[j])
      self.horizontal_layouts[j].addWidget(self.meal_rename[j])
      self.horizontal_layouts[j].addWidget(self.meal_remove[j])
      self.this_layout.addLayout(self.horizontal_layouts[j])
      j += 1
    self.this_layout.addWidget(add_button)
    self.this_layout.addWidget(close_button)


  def open_rename_query(self, meal):
    global query
    query = RenameMeal(self, self.week, self.day, meal)
    query.show()

  def remove_meal(self, meal):
    if self.week == "Present":
      self.db_wrapper.modify_meal("Delete", meal, self.day, None, True, False)
    elif self.week == "Future":
      self.db_wrapper.modify_meal("Delete", meal, self.day, None, False, True)
    self.this_parent.repopulate_table()
    self.update()

  def add_meal(self):
    if self.meal_number < 7:
      meal_string = "Meal #" + str((self.meal_number + 1))
      if self.week == "Present":
        self.db_wrapper.modify_meal("Add", meal_string, self.day, None, True, False)
      elif self.week == "Future":
        self.db_wrapper.modify_meal("Add", meal_string, self.day, None, False, True)
    self.this_parent.repopulate_table()
    self.update()

class RenameMeal(QWidget):
  def __init__(self, parent, week, day, meal):
    super().__init__()
    self.week = week
    self.this_parent = parent
    self.day = day
    self.meal = meal
    self.db_wrapper = DatabaseWrapper()
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
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
    self.setWindowModality(Qt.ApplicationModal)
    dialog_layout.addLayout(self.create_input_window())
    self.setLayout(dialog_layout)

  def create_input_window(self):
    layout = QVBoxLayout()
    entry_label = QLabel("Rename")

    self.meal_rename_line_edit = QLineEdit()

    helper_layout = QHBoxLayout()

    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close_button())

    confirm_button = QPushButton("Confirm")
    confirm_button.clicked.connect(lambda: self.confirm_button())

    helper_layout.addWidget(cancel_button)
    helper_layout.addWidget(confirm_button)

    layout.addWidget(entry_label)
    layout.addWidget(self.meal_rename_line_edit)
    layout.addLayout(helper_layout)

    return layout

  def close_button(self):
    self.close()

  def confirm_button(self):
    if self.meal_rename_line_edit.text() != "":
      if self.week == "Present":
        self.db_wrapper.modify_meal("Rename", self.meal, self.day, self.meal_rename_line_edit.text(), True, False)
      if self.week == "Future":
        self.db_wrapper.modify_meal("Rename", self.meal, self.day, self.meal_rename_line_edit.text(), False, True)
      self.this_parent.update()
      self.close()

class NutrientsPanel(QWidget):
  def __init__(self, parent):
    super().__init__()
    self.this_parent = parent
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
    layout = QVBoxLayout()
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
    self.setWindowModality(Qt.ApplicationModal)

    layout.addLayout(self.create_main_layout())
    self.setLayout(layout)

  def create_main_layout(self):
    layout = QVBoxLayout()

    nutrients = (["Calories", 1], ["Protein", 21], ["Carbohydrates", 32], ["Fat", 24], ["Fiber", 13], ["Sugar", 6])

    labels = [None] * len(nutrients)
    checkbox = [None] * len(nutrients)
    helper_layouts = [None] * len(nutrients)
    for i in range(len(labels)):
      labels[i] = QLabel("Show " + nutrients[i][0] + ": ")
      checkbox[i] = QCheckBox()
      checkbox[i].clicked.connect(partial(self.show_nutrients, checkbox[i], nutrients[i][0]))
      helper_layouts[i] = QHBoxLayout()     
      helper_layouts[i].addWidget(labels[i])
      helper_layouts[i].addWidget(checkbox[i])
      if config['NUTRITION'].get('Show' + nutrients[i][0]) == 'yes':
        checkbox[i].setChecked(True)
      layout.addLayout(helper_layouts[i])

    layout.addStretch(0)
    close_button = QPushButton("Close")
    close_button.clicked.connect(lambda:self.close())
    layout.addWidget(close_button)

    return layout
  
  def show_nutrients(self, btn, nutrient):
    if btn.isChecked() == True:
      config.set('NUTRITION', 'Show' + nutrient, 'yes')
    if btn.isChecked() == False:
      config.set('NUTRITION', 'Show' + nutrient, 'no')
    with open(config_path, 'w') as configfile:
      config.write(configfile)
    self.this_parent.update_nutrient_labels()