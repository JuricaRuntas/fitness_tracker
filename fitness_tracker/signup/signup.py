from PyQt5.QtWidgets import QWidget, QGridLayout
from .main_panel import MainPanel

class Signup(QWidget):
  def __init__(self, controller):
    super().__init__()
    self.main_panel = MainPanel(self, controller)
    self.controller = controller
    self.create_grid()

  def create_grid(self):
    grid = QGridLayout()
    grid.addWidget(self.main_panel, 0, 0, 8, 4)
    self.setLayout(grid)