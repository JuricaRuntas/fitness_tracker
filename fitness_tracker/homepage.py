from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont

class Homepage(QWidget):
  def __init__(self, parent):
     super().__init__(parent)
     self.create_homepage()

  def create_homepage(self):
    label = QLabel(self)
    label.setText("Fitness Tracker")
    label.setAlignment(Qt.AlignLeft)
    label.setFont(QFont("Arial", 25))
 
    hbox = QHBoxLayout()
    hbox.addWidget(label)
    self.setLayout(hbox)
 
  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setPen(QPen(Qt.black, 2))
    painter.drawLine(0, 60, 10000, 60)
    painter.drawLine(248, 0, 248, 58)
