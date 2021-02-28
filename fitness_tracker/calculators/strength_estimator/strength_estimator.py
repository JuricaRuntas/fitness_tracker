from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from .main_panel import MainPanel
from fitness_tracker.homepage.header import Header
from fitness_tracker.homepage.side_panel import SidePanel

class StrengthEstimator(QWidget):
  display_layout_signal = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    self.header = Header(self, "Strength Estimator     ")
    self.main_panel = MainPanel(self)
    self.side_panel = SidePanel(self)
    self.side_panel.emit_layout_name.connect(lambda layout_name: self.emit_display_layout_signal(layout_name))
    self.panel_grid()

  def panel_grid(self):
    panel_grid = QGridLayout()
    panel_grid.setContentsMargins(0, 0, 0, 0)
    panel_grid.addWidget(self.side_panel, 1, 0, 8, 1)
    panel_grid.addWidget(self.main_panel, 1, 1, 8, 3)
    self.setLayout(panel_grid)

  @pyqtSlot(str)
  def emit_display_layout_signal(self, layout_name):
    self.display_layout_signal.emit(layout_name)