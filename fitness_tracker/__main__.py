import sys
import sqlite3
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QVBoxLayout, QWidget, QSpacerItem, QSizeGrip, QSizePolicy
from PyQt5.QtCore import Qt, QObject, pyqtSlot
from PyQt5.QtGui import QColor, QFontDatabase
from homepage.homepage import Homepage
from user_profile.profile import Profile
from calculators.one_rep_max.one_rep_max import OneRepMaxCalculator
from calculators.body_fat.body_fat import BodyFatCalculator
from calculators.strength_estimator.strength_estimator import StrengthEstimator
from notes.big_lifts.big_lifts import BigLiftsNotes
from notes.weight_loss.weight_loss import WeightLossNotes
from notes.workouts.workouts import WorkoutsNotes
from notes.nutrition.nutrition import NutritionNotes
from statistics.strength.strength import StrengthStats
from statistics.weight_loss.weight_loss import WeightLossStats
from login.login import Login
from signup.signup import Signup
from signup.signup_questions_panel import SignupQuestions
from titlebar import TitleBar

class FitnessTracker(QMainWindow):
  def __init__(self):
    super().__init__()
    self.create_window()
    self.cw = Homepage() if self.user_info_exists() else Login()
    self.cw.display_layout_signal.connect(lambda layout: self.display_layout(layout))
    self.layouts = {"Login": Login, "Signup": Signup, "Continue": SignupQuestions,
                    "Home": Homepage, "Profile": Profile, "Logout": Login,
                    "Big Lifts": BigLiftsNotes, "Workouts": WorkoutsNotes, "Nutrition": NutritionNotes,
                    "Weight Loss Notes": WeightLossNotes, "1 Rep Max Calculator": OneRepMaxCalculator,
                    "Body Fat Calculator": BodyFatCalculator, "Strength Estimator": StrengthEstimator,
                    "Strength Statistics": StrengthStats, "Weight Loss Stats": WeightLossStats}
    self.colorize_background()
    self.colorize_foreground()
    self.setup_borders()
    self.title_bar = TitleBar(self)
    self.setMouseTracking(True)
    main_widget = self.setup_main_layout()
    self.setCentralWidget(main_widget)

  def colorize_background(self):
    self.setAutoFillBackground(True)
    bg_palette = self.palette()
    bg_palette.setColor(self.backgroundRole(), QColor(25,23,22))
    self.setPalette(bg_palette)

  def colorize_foreground(self):
    fg_palette = self.palette()
    fg_palette.setColor(self.foregroundRole(), QColor(255,255,255))
    self.setPalette(fg_palette)

  def create_window(self):
    self.setWindowTitle("Fitness Tracker")
    self.resize(1126, 733)
    self.setMinimumSize(1126, 733)
    self.center()
    self.show()

  def setup_borders(self):
    self.setWindowFlags(Qt.FramelessWindowHint)
    self.setMouseTracking(True)
    self.show()

  def setup_main_layout(self):
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    main_layout.addWidget(self.title_bar)
    main_layout.addWidget(self.cw)
    #sizegrip = QSizeGrip(self)
    #sizegrip.setMaximumWidth(16)
    #main_layout.addWidget(sizegrip)
    main_widget = QWidget()
    main_widget.setLayout(main_layout)
    return main_widget
  
  def center(self):
    window = self.frameGeometry()
    center_point = QDesktopWidget().availableGeometry().center()
    window.moveCenter(center_point)
    self.move(window.topLeft())
  
  @pyqtSlot(str)
  def display_layout(self, layout_name):
      self.cw = self.layouts[layout_name]()
      self.cw.display_layout_signal.connect(lambda layout_name: self.display_layout(layout_name))
      self.layout = QWidget()
      self.layout = self.setup_main_layout()
      self.setCentralWidget(self.layout)

  def user_info_exists(self):
    table_exists = True
    path = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.sep.join([*path.split(os.path.sep)[:-1], "db"])
    user_info_path = os.path.sep.join([db_path, "profile.db"])
    if not os.path.isdir(db_path): os.makedirs(db_path)
    with sqlite3.connect(user_info_path) as conn:
      check_for_tables = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
      cursor = conn.cursor()
      cursor.execute(check_for_tables)
      if cursor.fetchone() == None:
        table_exists = False
        os.remove(user_info_path)
    return table_exists
        
if __name__ == "__main__":
  app = QApplication(sys.argv)
  ft = FitnessTracker()
  sys.exit(app.exec_())
