from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from .main_panel import MainPanel

class Signup(QWidget):
  display_layout_signal = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    self.main_panel = MainPanel(self)
    self.main_panel.emit_layout_name.connect(lambda layout_name: self.emit_display_layout_signal(layout_name)) 
    self.create_grid()

  def create_grid(self):
    grid = QGridLayout()
    grid.addWidget(self.main_panel, 0, 0, 8, 4)
    self.setLayout(grid)

  @pyqtSlot(str)
  def emit_display_layout_signal(self, layout_name):
    self.display_layout_signal.emit(layout_name)
