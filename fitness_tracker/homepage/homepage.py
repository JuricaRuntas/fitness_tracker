from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QFont
from .header import Header

class Homepage(QWidget):
  def __init__(self, parent):
     super().__init__(parent)
     header = Header(self)
  
  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setPen(QPen(Qt.black, 2))
    painter.drawLine(0, 80, 10000, 80)
    painter.drawLine(248, 0, 248, 78)
    painter.drawLine(732, 0, 732, 78)
