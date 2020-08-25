from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QFont

from .header import Header
from .side_panel import SidePanel
from .main_panel import MainPanel

class Homepage(QWidget):
  def __init__(self, parent):
     super().__init__(parent)
     self.header = Header(self)
     self.side_panel = SidePanel(self)
     self.main_panel = MainPanel(self)
     self.create_grid()

  def create_grid(self):
    grid = QGridLayout()
    grid.addWidget(self.header, 0, 1, 1, 4)
    grid.addWidget(self.side_panel, 1, 1, 8, 1)
    grid.addWidget(self.main_panel, 1, 2, 8, 3)
    self.setLayout(grid)
