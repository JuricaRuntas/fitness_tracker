from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from PyQt5.QtGui import  QFont

class PreferredLifts(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle("Preferred Lifts")
    label_name = QLabel("Name", self)