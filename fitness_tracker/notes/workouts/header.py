from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Header(QWidget):
  def __init__(self, parent, title):
    super().__init__(parent)
    self.title = title
    self.create_header()
  
  def create_header(self):
    grid = QGridLayout()
    self.setLayout(grid)
    
    title_layout = QHBoxLayout()
    title_label = QLabel(self.title, self)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setFont(QFont("Arial", 25))
    title_layout.addWidget(title_label)

    header_frame = QFrame()
    header_frame.setFrameStyle(QFrame.StyledPanel)
    header_layout = QHBoxLayout()

    description = QLabel("Store your workouts here. \nTrack your progress with graphs. Explore exercises in our exercises database. \nYou can create your workouts.", self)
    description.setAlignment(Qt.AlignCenter)
    header_layout.addWidget(description)
    header_frame.setLayout(header_layout)
    
    grid.addLayout(title_layout, 0, 0, 1, 1)
    grid.addWidget(header_frame, 0, 3, 1, 3)
