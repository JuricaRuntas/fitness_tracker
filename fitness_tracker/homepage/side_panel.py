from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt

class SidePanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()

  def create_panel(self):
    label = QLabel()
    label.setAlignment(Qt.AlignCenter)
    label.setText("Side Panel")
    
    grid = QGridLayout()
    grid.addWidget(label, 0, 0)
    self.setLayout(grid)
    self.setStyleSheet("background-color: red")
