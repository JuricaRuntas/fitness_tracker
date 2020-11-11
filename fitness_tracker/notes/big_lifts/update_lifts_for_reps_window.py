from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from PyQt5.QtGui import QFont

class UpdateLiftsForRepsWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle("Update Lifts For Reps")
    label = QLabel("Label")
