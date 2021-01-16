from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from fitness_tracker.homepage.side_panel import SidePanel

class StrengthStats(QWidget):
  display_layout_signal = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    label = QLabel("Strength Statistics", self)
    label.move(300, 300)
    label.setFont(QFont("Ariel", 30))
    self.side_panel = SidePanel(self)
    self.side_panel.emit_layout_name.connect(lambda layout_name: self.emit_display_layout_signal(layout_name))

  @pyqtSlot(str)
  def emit_display_layout_signal(self, layout_name):
    self.display_layout_signal.emit(layout_name)
