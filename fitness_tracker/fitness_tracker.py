from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtCore import QFileInfo
import sys
import sqlite3
import os
from homepage.homepage import Homepage
from user_physique.user_physique import UserPhysique
from calculators import *
from notes import *
from statistics import *
from login.login import Login
from signup.signup import Signup
from signup.signup_questions_panel import SignupQuestions

class FitnessTracker(QMainWindow):
  def __init__(self):
    super().__init__()
    self.create_window()
    self.cw = Homepage(self) if self.user_info_exists() else Login(self)
    self.setCentralWidget(self.cw)
    self.layouts = {"Login": Login, "Signup": Signup, "Continue": SignupQuestions,
                    "Home": Homepage, "User Data and Settings": UserPhysique,
                    "Big Lifts": BigLiftsNotes, "Workouts": WorkoutsNotes, "Nutrition": CaloriesNotes,
                    "Weight Loss Notes": WeightLossNotes, "1 Rep Max": OneRepMaxCalculator,
                    "Body Fat": BodyFatCalculator, "Strength Estimator": StrengthEstimator,
                    "Strength": StrengthStats, "Weight Loss": WeightLossStats}
  
  def create_window(self):
    self.setWindowTitle("Fitness Tracker")
    self.resize(900, 600)
    self.center()
    self.show()
  
  def center(self):
    window = self.frameGeometry()
    center_point = QDesktopWidget().availableGeometry().center()
    window.moveCenter(center_point)
    self.move(window.topLeft())
  
  def display_layout(self, layout):
    for key, value in self.layouts.items():
      if layout == key:
        self.setCentralWidget(value(self))

  def user_info_exists(self):
    table_exists = True
    path = os.path.normpath(QFileInfo(__file__).absolutePath())
    db_path = path.split(os.path.sep)[:-1]
    db_path = os.path.sep.join([os.path.sep.join(db_path), "db", "user_info.db"])
    
    with sqlite3.connect(db_path) as conn:
      check_for_tables = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
      cursor = conn.cursor()
      cursor.execute(check_for_tables)
      if cursor.fetchone() == None:
        table_exists = False
    return table_exists
        
if __name__ == "__main__":
  app = QApplication(sys.argv)
  ft = FitnessTracker()
  sys.exit(app.exec_())
