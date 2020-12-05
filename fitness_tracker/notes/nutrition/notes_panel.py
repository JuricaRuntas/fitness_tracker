import os
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QLabel, QProgressBar,
                             QPushButton, QFrame, QHBoxLayout, QVBoxLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import Qt, QSize
from profile import profile_db
from .nutrition_db import table_exists, create_nutrition_table, fetch_nutrition_data, fetch_calorie_goal

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "icons")

icons = {"pencil": os.path.join(path, "pencil.png"),
         "plus": os.path.join(path, "plus.png"),
         "left": os.path.join(path, "left.png"),
         "right": os.path.join(path, "right.png")}

class NotesPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    if not table_exists():
      create_nutrition_table()
      fetch_nutrition_data()
    self.units = "kg" if profile_db.fetch_units() == "metric" else "lb"
    self.user_weight = profile_db.fetch_user_weight()
    self.calorie_goal = fetch_calorie_goal()
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_stats(), 0, 0, 1, 2)
    grid.addLayout(self.create_notes(), 1, 0)
    self.setLayout(grid)

  def create_stats(self):
    stats_layout = QHBoxLayout()
    
    calorie_goal_layout = QVBoxLayout()
    calorie_goal_frame = QFrame()
    calorie_goal_label = QLabel(" ".join(["Calorie Goal: \n", self.calorie_goal]))
    calorie_goal_label.setFixedHeight(40)
    calorie_goal_label.setFont(QFont("Ariel", 15))
    calorie_goal_label.setAlignment(Qt.AlignCenter)
     
    progress_bar = QProgressBar()
    progress_bar.setFormat("500 calories left")
    progress_bar.setStyleSheet("background-color:grey;")
    progress_bar.setMaximum(2500)
    progress_bar.setValue(2000)

    calorie_goal_layout.addWidget(calorie_goal_label)
    calorie_goal_layout.addWidget(progress_bar)
    calorie_goal_frame.setLayout(calorie_goal_layout)
    
    weight_layout = QVBoxLayout()
    weight_frame = QFrame()

    current_weight_layout = QHBoxLayout()
    current_weight_label = QLabel(" ".join(["Current Weight:", self.user_weight, self.units]))
    current_weight_label.setFont(QFont("Ariel", 15))
    edit_current_weight_button = QPushButton()
    edit_current_weight_button.setFlat(True)
    edit_current_weight_button.setIcon(QIcon(icons["pencil"]))
    edit_current_weight_button.setIconSize(QSize(16, 16))
    edit_current_weight_button.setCursor(QCursor(Qt.PointingHandCursor))
    current_weight_layout.addWidget(current_weight_label)
    current_weight_layout.addWidget(edit_current_weight_button)
    
    goal_weight_layout = QHBoxLayout()
    goal_weight_label = QLabel("Goal Weight: 85.3 kg")
    goal_weight_label.setFont(QFont("Ariel", 15))
    edit_goal_weight_button = QPushButton()
    edit_goal_weight_button.setFlat(True)
    edit_goal_weight_button.setIcon(QIcon(icons["pencil"]))
    edit_goal_weight_button.setIconSize(QSize(16, 16))
    edit_goal_weight_button.setCursor(QCursor(Qt.PointingHandCursor))
    goal_weight_layout.addWidget(goal_weight_label)
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
