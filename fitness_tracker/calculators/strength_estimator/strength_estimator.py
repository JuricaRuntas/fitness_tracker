from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont
from .main_panel import MainPanel
from fitness_tracker.homepage.header import Header
from fitness_tracker.homepage.side_panel import SidePanel

class StrengthEstimator(QWidget):
  def __init__(self, controller):
    super().__init__()
    self.controller = controller
    self.header = Header(self, "Strength Estimator     ")
    self.main_panel = MainPanel(self)
    self.side_panel = SidePanel(self, self.controller)
    self.panel_grid()

  def panel_grid(self):
    panel_grid = QGridLayout()
    panel_grid.addWidget(self.header, 0, 0, 1, 4)
    panel_grid.addWidget(self.side_panel, 1, 0, 8, 1)
    panel_grid.addWidget(self.main_panel, 1, 1, 8, 3)
    self.setLayout(panel_grid)
