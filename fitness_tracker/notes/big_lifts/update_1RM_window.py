from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from PyQt5.QtGui import QFont

class Update1RMWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle("Update One Rep Max Lifts")
    label = QLabel("Label")
