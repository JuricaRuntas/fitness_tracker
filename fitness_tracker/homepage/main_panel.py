from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()
  
  def create_panel(self): 
    grid = QGridLayout()
    grid.addWidget(self.create_graph_layout(), 0, 0 , 3, 2)
    grid.addWidget(self.create_max_layout(), 4, 0, 1, 1)
    grid.addWidget(self.create_strongest_layout(), 5, 0, 1, 1)
    grid.addWidget(self.create_general_layout(), 4, 1, 2, 1)
    self.setLayout(grid)
  
  def create_graph_layout(self):
    graph_layout = QVBoxLayout()
    
    graph = QWidget(self)
    graph.setStyleSheet("background-color: red")
    
    graph_dropdowns_layout = QHBoxLayout()
    
    time_period_dropdown = QComboBox()
    time_period_dropdown.addItems(["Daily", "Weekly", "Monthly", "Yearly"])

    exercise_dropdown = QComboBox()
    exercise_dropdown.addItems(["Deadlift", "Bench", "Squat", "Military Press", "Barbell Rows"])
    
    graph_dropdowns_layout.addWidget(time_period_dropdown)
    graph_dropdowns_layout.addWidget(exercise_dropdown)

    graph_layout.addWidget(graph)
    graph_layout.addLayout(graph_dropdowns_layout)
   
    graph_frame = QFrame()
    graph_frame.setFrameStyle(QFrame.StyledPanel)
    graph_frame.setLayout(graph_layout)
 
    return graph_frame
  
  def create_max_layout(self):
    max_layout = QVBoxLayout()
     
    one_rep_label = QLabel("One Rep Max", self)
    one_rep_label.setFont(QFont("Ariel", 15))
    one_rep_label.setAlignment(Qt.AlignLeft)
    one_rep_label.setFixedSize(135, 25)
     
    max_bench = QLabel("Bench: 80kg", self)
    max_bench.setAlignment(Qt.AlignLeft)
    max_bench.setFixedSize(120, 20)

    max_deadlift = QLabel("Deadlift: 180kg", self)
    max_deadlift.setAlignment(Qt.AlignLeft)
    max_deadlift.setFixedSize(120, 20)

    max_squat = QLabel("Squat: 80kg", self)
    max_squat.setAlignment(Qt.AlignLeft)
    max_squat.setFixedSize(120, 20)

    max_layout.addWidget(one_rep_label)
    max_layout.addWidget(max_bench)
    max_layout.addWidget(max_deadlift)
    max_layout.addWidget(max_squat)
    
    max_frame = QFrame()
    max_frame.setFrameStyle(QFrame.StyledPanel)
    max_frame.setLayout(max_layout) 
    
    return max_frame

  def create_strongest_layout(self):
    strongest_layout = QVBoxLayout()

    strongest_lift = QLabel("Strongest lift: Deadlift", self)
    strongest_lift.setAlignment(Qt.AlignLeft)
    strongest_lift.setFixedSize(200, 20)

    weakest_lift = QLabel("Weakest lift: Squat", self)
    weakest_lift.setAlignment(Qt.AlignLeft)
    weakest_lift.setFixedSize(200, 20)

    strongest_layout.addWidget(strongest_lift)
    strongest_layout.addWidget(weakest_lift)

    strongest_frame = QFrame()
    strongest_frame.setFrameStyle(QFrame.StyledPanel)
    
    strongest_frame.setLayout(strongest_layout)
    
    return strongest_frame

  def create_general_layout(self):
    general_layout = QVBoxLayout()
    
    general_label = QLabel("General", self)
    general_label.setFont(QFont("Ariel", 15))
    general_label.setAlignment(Qt.AlignLeft)
    general_label.setFixedSize(135, 25)
     
    stats_one = QLabel("Chin up count: 10", self)
    stats_one.setAlignment(Qt.AlignLeft)
    stats_one.setFixedSize(200, 20)

    stats_two = QLabel("Dip count: 12", self)
    stats_two.setAlignment(Qt.AlignLeft)
    stats_two.setFixedSize(200, 20)

    stats_three = QLabel("Last updated physique: 4 days ago", self)
    stats_three.setAlignment(Qt.AlignLeft)
    stats_three.setFixedSize(250, 20)
    
    general_layout.addWidget(general_label)
    general_layout.addWidget(stats_one)
    general_layout.addWidget(stats_two)
    general_layout.addWidget(stats_three)

    general_frame = QFrame()
    general_frame.setFrameStyle(QFrame.StyledPanel)
    general_frame.setLayout(general_layout) 

    return general_frame
