from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

import sys
from homepage.homepage import Homepage
from user_physique.user_physique import UserPhysique
from calculators import *
from notes import *
from statistics import *

class FitnessTracker(QMainWindow):
  def __init__(self):
    super().__init__()
    self.create_window()
    self.cw = Homepage(self)
    self.setCentralWidget(self.cw)
    self.layouts = {"Home": Homepage, "User Physique": UserPhysique, "Big Lifts": BigLiftsNotes,
                    "Workouts": WorkoutsNotes, "Nutrition": CaloriesNotes,
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

if __name__ == "__main__":
  app = QApplication(sys.argv)
  ft = FitnessTracker()
  sys.exit(app.exec_())
