from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()

  def create_panel(self):
    label = QLabel(self)
    label.setText("Main Panel")
    label.setAlignment(Qt.AlignCenter)
    
    grid = QGridLayout()
    grid.addWidget(label, 0, 0)
    self.setLayout(grid)
    self.setStyleSheet("background-color: green")
