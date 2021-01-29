from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from fitness_tracker.homepage.side_panel import SidePanel
from fitness_tracker.homepage.header import Header
from .main_panel import MainPanel

class OneRepMaxCalculator(QWidget):
  display_layout_signal = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    self.header = Header(self, "1 Rep Max         ") # space hacks
    self.main_panel = MainPanel(self)
    self.side_panel = SidePanel(self)
    self.side_panel.emit_layout_name.connect(lambda layout_name: self.emit_display_layout_signal(layout_name))
    self.create_grid()

  def create_grid(self):
    grid = QGridLayout()
    grid.setContentsMargins(0, 0, 0, 0)
    grid.addWidget(self.side_panel, 1, 1, 8, 1)
    grid.addWidget(self.main_panel, 1, 2, 8, 3)
    self.setLayout(grid)

  @pyqtSlot(str)
  def emit_display_layout_signal(self, layout_name):
    self.display_layout_signal.emit(layout_name) 