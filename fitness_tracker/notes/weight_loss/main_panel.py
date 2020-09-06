from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QCalendarWidget, QFrame, QComboBox
from PyQt5.QtCore import Qt

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    
    calendar_frame = QFrame()
    calendar_frame.setFixedHeight(210)
    calendar_frame.setFrameStyle(QFrame.StyledPanel)
    
    calendar_layout = QHBoxLayout()
    calendar_layout.addLayout(self.create_description())
    calendar_layout.addWidget(self.create_calendar())
    calendar_frame.setLayout(calendar_layout)
    
    grid.addWidget(calendar_frame, 0, 0, 1, 1)
    grid.addWidget(self.create_graphs(), 1, 0, 4, 2)
    self.setLayout(grid)

  def create_description(self):
    notes_description = QVBoxLayout()
    notes_label = QLabel("Store your progress to desired weight. \nWeight loss notes offer you simple way of \ntracking your weight progress. \nYou can see your progression visualized on graphs.")
    notes_label.setFixedHeight(100)
    notes_description.addWidget(notes_label)
    return notes_description

  def create_calendar(self):
    calendar_frame = QFrame()
    calendar_layout = QVBoxLayout()
    calendar = QCalendarWidget(self)
    calendar_layout.addWidget(calendar)
    calendar_frame.setLayout(calendar_layout)
    return calendar_frame

  def create_graphs(self):
    graph_layout = QHBoxLayout()

    graph1_layout = QVBoxLayout()
    graph1 = QWidget()
    graph1.setStyleSheet("background-color: gold")
    dropdown1 = QComboBox()
    dropdown1.addItems(["Daily", "Weekly", "Monthly", "Yearly"])
    graph1_layout.addWidget(graph1)
    graph1_layout.addWidget(dropdown1)
    
    graph2_layout = QVBoxLayout()
    graph2 = QWidget()
    graph2.setStyleSheet("background-color: orange")
    dropdown2 = QComboBox()
    dropdown2.addItems(["Daily", "Weekly", "Monthly", "Yearly"])
    graph2_layout.addWidget(graph2)
    graph2_layout.addWidget(dropdown2)

    graph_layout.addLayout(graph1_layout)
    graph_layout.addLayout(graph2_layout)
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)
    frame.setLayout(graph_layout)
    return frame
