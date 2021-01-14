from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont
from fitness_tracker.homepage.side_panel import SidePanel
from fitness_tracker.homepage.header import Header
from .main_panel import MainPanel

class BodyFatCalculator(QWidget):
  def __init__(self, controller):
    super().__init__()
    self.controller = controller
    self.header = Header(self, "Body Fat Calculator")
    self.main_panel = MainPanel(self)
    self.side_panel = SidePanel(self, self.controller)
    self.create_grid()

  def create_grid(self):
    grid = QGridLayout()
    grid.addWidget(self.header, 0, 1, 1, 4)
    grid.addWidget(self.side_panel, 1, 1, 8, 1)
    grid.addWidget(self.main_panel, 1, 2, 8, 3)
    self.setLayout(grid)
