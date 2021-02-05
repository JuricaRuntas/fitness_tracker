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

  '''def create_weight_panel(self):
    current_weight_layout = QHBoxLayout()
    self.current_weight_label = QLabel(" ".join(["Current Weight:", self.user_weight, self.units]))
    self.current_weight_label.setFont(QFont("Ariel", 15))
    edit_current_weight_button = QPushButton()
    edit_current_weight_button.setFlat(True)
    edit_current_weight_button.setIcon(QIcon(icons["pencil"]))
    edit_current_weight_button.setIconSize(QSize(16, 16))
    edit_current_weight_button.setCursor(QCursor(Qt.PointingHandCursor))
    edit_current_weight_button.clicked.connect(lambda: self.change_weight_dialog.show())
    current_weight_layout.addWidget(self.current_weight_label)
    current_weight_layout.addWidget(edit_current_weight_button)

    weight_layout = QVBoxLayout()
    weight_frame = QFrame()
    weight_frame.setFrameStyle(QFrame.Box)
    weight_frame.setLineWidth(3)
    weight_frame.setObjectName("frame")
    weight_frame.setStyleSheet("""#frame {color: #322d2d;}""")
    goal_weight_layout = QHBoxLayout()
    self.goal_weight_label = QLabel(" ".join(["Goal Weight:", self.user_goal_weight, self.units]))
    self.goal_weight_label.setFont(QFont("Ariel", 15))
    edit_goal_weight_button = QPushButton()
    edit_goal_weight_button.setFlat(True)
    edit_goal_weight_button.setIcon(QIcon(icons["pencil"]))
    edit_goal_weight_button.setIconSize(QSize(16, 16))
    edit_goal_weight_button.setCursor(QCursor(Qt.PointingHandCursor))
    edit_goal_weight_button.clicked.connect(lambda: self.change_weight_dialog.show())
    goal_weight_layout.addWidget(self.goal_weight_label)
    goal_weight_layout.addWidget(edit_goal_weight_button)

    weight_layout.addLayout(current_weight_layout)
    weight_layout.addLayout(goal_weight_layout)
    weight_frame.setLayout(weight_layout)
    return weight_frame'''