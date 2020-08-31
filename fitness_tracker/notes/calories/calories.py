from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont

from .main_panel import MainPanel
from homepage.side_panel import SidePanel
from .header import Header

class CaloriesNotes(QWidget):
  def __init__(self, controller):
    super().__init__()
    self.controller = controller
    self.header = Header(self, "Nutrition           ")
    self.main_panel = MainPanel(self)
    self.side_panel = SidePanel(self, self.controller)
    self.create_grid()

  def create_grid(self):
    grid = QGridLayout()
    grid.addWidget(self.header, 0, 0, 1, 4)
    grid.addWidget(self.side_panel, 1, 0, 8, 1)
    grid.addWidget(self.main_panel, 1, 1, 8, 3)
    self.setLayout(grid)
