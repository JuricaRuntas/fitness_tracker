import os
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QLabel, QProgressBar,
                             QPushButton, QFrame, QHBoxLayout, QVBoxLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from fitness_tracker.user_profile.profile_db import fetch_units, fetch_user_weight, fetch_goal_weight
from .nutrition_db import table_exists, create_nutrition_table, fetch_nutrition_data, fetch_calorie_goal
from .change_weight_dialog import ChangeWeightDialog

path = os.path.abspath(os.path.dirname(__file__))
profile_db = os.path.sep.join([*path.split(os.path.sep)[:-3], "db", "profile.db"])
icons_path = os.path.join(path, "icons")

icons = {"pencil": os.path.join(icons_path, "pencil.png"),
         "plus": os.path.join(icons_path, "plus.png"),
         "left": os.path.join(icons_path, "left.png"),
         "right": os.path.join(icons_path, "right.png")}

class NotesPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    if not table_exists():
      create_nutrition_table()
      fetch_nutrition_data()
    self.units = "kg" if fetch_units(profile_db) == "metric" else "lb"
    self.user_weight = fetch_user_weight(profile_db)
    self.user_goal_weight = fetch_goal_weight(profile_db)
    self.calorie_goal = fetch_calorie_goal()
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
    grid.addLayout(self.create_stats(), 0, 0, 1, 2)
    grid.addLayout(self.create_notes(), 1, 0)
    self.setLayout(grid)

  def create_stats(self):
    stats_layout = QHBoxLayout()
    
    calorie_goal_layout = QVBoxLayout()
    calorie_goal_frame = QFrame()
    self.calorie_goal_label = QLabel(" ".join(["Calorie Goal: \n", self.calorie_goal]))
    self.calorie_goal_label.setFixedHeight(40)
    self.calorie_goal_label.setFont(QFont("Ariel", 15))
    self.calorie_goal_label.setAlignment(Qt.AlignCenter)
     
    self.progress_bar = QProgressBar()
    self.progress_bar.setStyleSheet("background-color:grey;")
    self.progress_bar.setMaximum(int(self.calorie_goal))
    self.progress_bar.setValue(0)
    calories_left = self.progress_bar.maximum() - self.progress_bar.value()
    self.progress_bar.setFormat(" ".join([str(calories_left), "calories left"]))

    calorie_goal_layout.addWidget(self.calorie_goal_label)
    calorie_goal_layout.addWidget(self.progress_bar)
    calorie_goal_frame.setLayout(calorie_goal_layout)
    
    weight_layout = QVBoxLayout()
    weight_frame = QFrame()

    current_weight_layout = QHBoxLayout()
    self.current_weight_label = QLabel(" ".join(["Current Weight:", self.user_weight, self.units]))
    self.current_weight_label.setFont(QFont("Ariel", 15))
    edit_current_weight_button = QPushButton()
    edit_current_weight_button.setFlat(True)
    edit_current_weight_button.setIcon(QIcon(icons["pencil"]))
    edit_current_weight_button.setIconSize(QSize(16, 16))
    edit_current_weight_button.setCursor(QCursor(Qt.PointingHandCursor))
    edit_current_weight_button.clicked.connect(lambda: self.change_weight_dialog.show())
    current_weight_layout.addWidget(self.current_weight_label)
    current_weight_layout.addWidget(edit_current_weight_button)
    
    goal_weight_layout = QHBoxLayout()
    self.goal_weight_label = QLabel(" ".join(["Goal Weight:", self.user_goal_weight, self.units]))
    self.goal_weight_label.setFont(QFont("Ariel", 15))
    edit_goal_weight_button = QPushButton()
    edit_goal_weight_button.setFlat(True)
    edit_goal_weight_button.setIcon(QIcon(icons["pencil"]))
    edit_goal_weight_button.setIconSize(QSize(16, 16))
    edit_goal_weight_button.setCursor(QCursor(Qt.PointingHandCursor))
    edit_goal_weight_button.clicked.connect(lambda: self.change_weight_dialog.show())
    goal_weight_layout.addWidget(self.goal_weight_label)
    goal_weight_layout.addWidget(edit_goal_weight_button)

    weight_layout.addLayout(current_weight_layout)
    weight_layout.addLayout(goal_weight_layout)
    weight_frame.setLayout(weight_layout)
    
    stats_layout.addWidget(calorie_goal_frame)
    stats_layout.addWidget(weight_frame)

    return stats_layout

  def create_notes(self):
    
    table = QTableWidget(2, 4)
    table.setStyleSheet("background-color: #603A40;color:white;")
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.verticalHeader().setVisible(False)
    
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    
    plus_button = QPushButton(QIcon(icons["plus"]), "Add Food", self)
    plus_button1 = QPushButton(QIcon(icons["plus"]), "Add Food", self)
    plus_button2 = QPushButton(QIcon(icons["plus"]), "Add Food", self)
    plus_button3 = QPushButton(QIcon(icons["plus"]), "Add Food", self)
    
    buttons = [plus_button, plus_button1, plus_button2, plus_button3]
    j = i = 0
    for item in meals:
      buttons[i].setFlat(True)
      table.setHorizontalHeaderItem(i, QTableWidgetItem(item))
      table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
      table.setCellWidget(0, j, buttons[i])
      j += 1
      i += 1

    for i in range(2):
      table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    label = QLabel("Monday, 31.2.2005", self)
    label.setAlignment(Qt.AlignCenter)
    
    table_title_layout = QHBoxLayout()
    
    left_button = QPushButton(QIcon(icons["left"]), "", self)
    left_button.setFlat(True)
    left_button.setFixedWidth(20)
    left_button.setCursor(QCursor(Qt.PointingHandCursor))
    right_button = QPushButton(QIcon(icons["right"]), "",self)
    right_button.setFlat(True)
    right_button.setFixedWidth(20)
    right_button.setCursor(QCursor(Qt.PointingHandCursor))

    table_title_layout.addWidget(left_button)
    table_title_layout.addWidget(label)
    table_title_layout.addWidget(right_button)
    
    title_frame = QFrame()
    title_frame.setStyleSheet("background-color: #603A40;")
    title_frame.setFrameStyle(QFrame.StyledPanel)
    title_frame.setLayout(table_title_layout)

    table_wrapper = QVBoxLayout()
    table_wrapper.addWidget(table)
    
    grid = QGridLayout()
    grid.addWidget(title_frame, 0, 0)
    grid.addLayout(table_wrapper, 1, 0)
    
    return grid
