import os
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QLabel, QProgressBar,
                             QPushButton, QFrame, QHBoxLayout, QVBoxLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from fitness_tracker.user_profile.profile_db import fetch_units, fetch_user_weight, fetch_goal_weight
from fitness_tracker.config import get_db_paths
from .nutrition_db import table_exists, create_nutrition_table, fetch_nutrition_data, fetch_calorie_goal
from .change_weight_dialog import ChangeWeightDialog

db_paths = get_db_paths("profile.db")
path = os.path.abspath(os.path.dirname(__file__))
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
    self.setStyleSheet(   
    """QWidget{
      color:#c7c7c7;
      font-weight: bold;
      font-family: "Ubuntu";
      font-size: 16px;
      }
      """)
    self.units = "kg" if fetch_units(db_paths["profile.db"]) == "metric" else "lb"
    self.user_weight = fetch_user_weight(db_paths["profile.db"])
    self.user_goal_weight = fetch_goal_weight(db_paths["profile.db"])
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
    grid.setContentsMargins(2, 0, 8, 8)
    grid.addWidget(self.create_description(), 0, 0, 1, 3)
    grid.addLayout(self.create_stats(), 6, 0, 6, 1)
    grid.addWidget(self.create_nutrition_summary(), 6, 1, 6, 1)
    grid.addWidget(self.create_weight_panel(), 7, 2, 5, 1)
    grid.addLayout(self.create_notes(), 16, 0, 10, 3)
    self.setLayout(grid)

  def create_description(self):
    self.description = QLabel("Improve your diet and eating habits by tracking what you eat and searching through our database for healthy \nfoods.")
    return self.description

  def create_nutrition_summary(self):
    nsummary_layout = QVBoxLayout()
    daily_monthlyavg_buttons = QHBoxLayout()
    daily_button = QPushButton("Daily")
    monthly_button = QPushButton("Monthly")
    daily_monthlyavg_buttons.addWidget(daily_button)
    daily_monthlyavg_buttons.addWidget(monthly_button)

    nsummary_layout.addLayout(daily_monthlyavg_buttons)
    
    temp_label = QLabel("Proteins: 30g \nCarbs: 300g \nCalories: 2000kcal")
    nsummary_layout.addWidget(temp_label) # Temp

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
    #self.calorie_goal_label.setFixedHeight(40)
    self.calorie_goal_label.setFont(QFont("Ariel", 15))
    self.calorie_goal_label.setAlignment(Qt.AlignCenter)
     
    self.progress_bar = QProgressBar()
    self.progress_bar.setStyleSheet("background-color:grey;")
    self.progress_bar.setMaximum(int(self.calorie_goal))
    self.progress_bar.setValue(500)
    calories_left = self.progress_bar.maximum() - self.progress_bar.value()
    self.progress_bar.setFormat("")
    self.progress_bar.setAlignment(Qt.AlignCenter)
    self.progress_bar.setMaximumHeight(12)
    self.calorie_label = QLabel(str(calories_left) + " calories left from goal")
    self.calorie_label.setAlignment(Qt.AlignCenter)

    intake_button_layout = QHBoxLayout()
    self.calculate_intake = QPushButton("Calculate Daily Intake")
    self.edit_intake = QPushButton("Edit Daily Intake")
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

  def create_weight_panel(self):
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

    weight_layout = QVBoxLayout()
    weight_frame = QFrame()
    weight_frame.setFrameStyle(QFrame.Box)
    weight_frame.setLineWidth(3)
    weight_frame.setObjectName("frame")
    weight_frame.setStyleSheet("""#frame {color: #322d2d;}""")
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
    return weight_frame

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
