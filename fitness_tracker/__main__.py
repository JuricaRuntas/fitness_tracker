import sys
import os
import importlib
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QVBoxLayout, QWidget, QSpacerItem, QSizeGrip, QSizePolicy
from PyQt5.QtCore import Qt, QObject, pyqtSlot
from PyQt5.QtGui import QColor, QFontDatabase
from fitness_tracker.homepage.homepage import Homepage
from fitness_tracker.user_profile.profile import Profile
from fitness_tracker.calculators.one_rep_max.one_rep_max import OneRepMaxCalculator
from fitness_tracker.calculators.body_fat.body_fat import BodyFatCalculator
from fitness_tracker.calculators.strength_estimator.strength_estimator import StrengthEstimator
from fitness_tracker.notes.compound_exercises.compound_exercises import BigLiftsNotes
from fitness_tracker.notes.weight_loss.weight_loss import WeightLossNotes
from fitness_tracker.notes.workouts.workouts import WorkoutsNotes
from fitness_tracker.notes.nutrition.nutrition import NutritionNotes
from fitness_tracker.notes.nutrition.food_db import FoodDB
from fitness_tracker.login.login import Login
from fitness_tracker.signup.signup import Signup
from fitness_tracker.signup.signup_questions_panel import SignupQuestions
from fitness_tracker.titlebar import TitleBar
from fitness_tracker.config import db_path
from configparser import ConfigParser
config_path = os.path.join(os.path.dirname(__file__), "config", "settings.ini")
config = ConfigParser()
config.read(config_path)

class FitnessTracker(QMainWindow):
  def __init__(self):
    super().__init__()
    QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), "font", "Montserrat-Regular.ttf"))
    QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), "font", "Ubuntu-Regular.ttf"))
    self.create_window()
    self.create_db_file()
    self.cw = Homepage() if self.users_table_exists() else Login()
    self.cw.display_layout_signal.connect(lambda layout: self.display_layout(layout))
    self.layouts = {"Login": Login, "Signup": Signup, "Continue": SignupQuestions,
                    "Home": Homepage, "Profile": Profile, "Logout": Login,
                    "Compound Exercises": BigLiftsNotes, "Workouts": WorkoutsNotes, "Nutrition": NutritionNotes,
                    "Weight Loss": WeightLossNotes, "1 Rep Max Calculator": OneRepMaxCalculator,
                    "Body Fat Calculator": BodyFatCalculator, "Strength Estimator": StrengthEstimator,
                    "Food Database": FoodDB}
    self.colorize_background()
    self.colorize_foreground()
    self.setup_borders()
    self.title_bar = TitleBar(self)
    self.setMouseTracking(True)
    #add funct that generates default config file if 'settings.ini' isn't found
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
    windowX = config['WINDOW'].get('WindowX')
    windowY = config['WINDOW'].get('WindowY')
    self.resize(int(windowX), int(windowY))
    if config['WINDOW'].get('CenterAtStartup') == 'yes':
      self.center()
    elif config['WINDOW'].get('CenterAtStartup') == 'no':
      windowXPos = config['WINDOW'].get('WindowXPosition')
      windowYPos = config['WINDOW'].get('WindowYPosition')
      self.move(int(windowXPos), int(windowYPos))
    else:
      #use raw config parser or other opt
      config.set('WINDOW', 'CenterAtStartup', 'yes')
      with open(os.path.join(os.path.dirname(__file__), "config", "settings.ini"), 'w') as configfile:
        config.write(configfile)
      self.center()
    self.show()

  def setup_borders(self):
    self.setWindowFlags(Qt.FramelessWindowHint)
    self.show()

  def setup_main_layout(self):
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    main_layout.addWidget(self.title_bar)
    main_layout.addWidget(self.cw)
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

  def users_table_exists(self):
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='users'")
      if cursor.fetchone()[0] == 0: return False
      else:
        cursor.execute("SELECT COUNT(*) from 'users' WHERE logged_in='YES'")
        if cursor.fetchone()[0] != 1: return False
      return True

  def create_db_file(self):
    db_file = os.path.join(os.path.dirname(importlib.util.find_spec("fitness_tracker").origin), "fitness_tracker.db")
    if not os.path.isfile(db_file): open(db_file, "w")

if __name__ == "__main__":
  app = QApplication(sys.argv)
  ft = FitnessTracker()
  sys.exit(app.exec_())
