from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont

from homepage.side_panel import SidePanel

class WorkoutsNotes(QWidget):
  def __init__(self, controller):
    super().__init__()
    self.controller = controller
    label = QLabel("Workouts", self)
    label.move(300, 300)
    label.setFont(QFont("Ariel", 30))
    self.side_panel = SidePanel(self, self.controller)
