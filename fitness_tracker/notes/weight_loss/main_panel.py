from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QFrame, QPushButton
from PyQt5.QtGui import QFont


class MainPanel(QWidget):
  def __init__(self, parent, sqlite_connection, pg_connection):
    super().__init__(parent)
    self.sqlite_connection = sqlite_connection
    self.sqlite_cursor = self.sqlite_connection.cursor()
    self.pg_connection = pg_connection
    self.pg_cursor = self.pg_connection.cursor()
    self.setStyleSheet("""
    QWidget{
      color:#c7c7c7;
      font-weight: bold;
    }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
    }
    QPushButton:hover:!pressed{
      border: 2px solid;
      border-color: #747474;
    }
    QPushButton:pressed{
      border: 2px solid;
      background-color: #323232;
      border-color: #6C6C6C;
    }
    QComboBox{
      border-radius: 4px;
      font-size: 18px;
      font-weight: bold;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
      min-height: 28px;
      background-color: #440D0F;
    }
    QComboBox:down-arrow{
      width: 24.54px;
      height: 10px;
      background: #d3d3d3; 
      opacity:0
    }
    QComboBox:drop-down{
      background-color: #440D0F;
      border: 0px;
      opacity:0;
      border-radius: 0px;
    }
    QComboBox:hover:!pressed{
      background-color: #5D1A1D;
    }
    QComboBox:pressed{
      background-color: #551812;
    }
    """) 

    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_description(), 0, 0, 1, 1)
    grid.addWidget(self.create_graph(), 1, 0, 4, 1)
    grid.addLayout(self.create_bottom_layout(), 5, 0, 3, 1)
    self.setLayout(grid)

  def create_description(self):
    description = QVBoxLayout()
    description_font = QFont("Montserrat", 12)
    description_label = QLabel("Keep notes and track your weight loss journey.", self)
    description_label.setFont(description_font)
    description_label.setFixedHeight(20)
    description.addWidget(description_label)
    return description

  def create_graph(self):
    graph_layout = QVBoxLayout()
    graph = QWidget()
    graph.setStyleSheet("background-color: yellow")

    combobox_layout = QHBoxLayout()
    months_combobox = QComboBox()
    months_combobox.addItems(["January", "February", "March", "April", "May", "June", "July",
                              "August", "September", "October", "November", "December"])
    
    change_year_combobox = QComboBox()
    change_year_combobox.addItems(["2020", "2021"])

    combobox_layout.addWidget(months_combobox)
    combobox_layout.addWidget(change_year_combobox)

    graph_layout.addWidget(graph)
    graph_layout.addLayout(combobox_layout)

    framed_graph = QFrame(self)
    framed_graph.setFrameStyle(QFrame.Box)
    framed_graph.setLineWidth(3)
    framed_graph.setLayout(graph_layout)

    return framed_graph

  def create_bottom_layout(self):
    bottom_layout = QHBoxLayout()
    bottom_layout.addWidget(self.create_weight_loss())
    bottom_layout.addWidget(self.create_cardio_notes())
    return bottom_layout
  
  def create_weight_loss(self):
    weight_loss = QVBoxLayout()
    main_label = QLabel("Weight Loss")
    main_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    current_weight_layout = QHBoxLayout()
    current_weight_label = QLabel("Current Weight 70 kg")
    update_current_weight_button = QPushButton("Update")
    current_weight_layout.addWidget(current_weight_label)
    current_weight_layout.addWidget(update_current_weight_button)

    weight_goal_layout = QHBoxLayout()
    weight_goal_label = QLabel("Weight Goal 65 kg")
    update_weight_goal_label = QPushButton("Update")
    weight_goal_layout.addWidget(weight_goal_label)
    weight_goal_layout.addWidget(update_weight_goal_label)
   
    loss_per_week_layout = QHBoxLayout()
    loss_per_week_label = QLabel("Loss Per Week 0.5") 
    update_loss_per_week_label = QPushButton("update")
    loss_per_week_layout.addWidget(loss_per_week_label)
    loss_per_week_layout.addWidget(update_loss_per_week_label)

    calorie_intake_layout = QHBoxLayout()
    calorie_intake_label = QLabel("Calorie Intake 2300 kcal")
    calorie_intake_layout.addWidget(calorie_intake_label)
    
    history_layout = QHBoxLayout()
    weight_loss_history_button = QPushButton("History")
    history_layout.addWidget(weight_loss_history_button)   
    
    weight_loss.addWidget(main_label)
    weight_loss.addLayout(calorie_intake_layout)
    weight_loss.addLayout(current_weight_layout)
    weight_loss.addLayout(weight_goal_layout)
    weight_loss.addLayout(loss_per_week_layout)
    weight_loss.addLayout(history_layout)

    weight_loss.setSpacing(5)
    framed_layout = QFrame()
    framed_layout.setObjectName("graphObj")
    framed_layout.setFrameStyle(QFrame.Box)
    framed_layout.setLineWidth(3)
    framed_layout.setStyleSheet("""#graphObj {color: #322d2d;}""")
    
    framed_layout.setLayout(weight_loss)
    
    return framed_layout

  def create_cardio_notes(self):
    cardio_notes = QVBoxLayout()
    main_label = QLabel("Cardio Notes")
    main_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))
    
    preferred_activity_layout = QHBoxLayout()
    preferred_activity_label = QLabel("Preferred Activity: Running")
    update_preferred_activity_label = QPushButton("Update")
    preferred_activity_layout.addWidget(preferred_activity_label)
    preferred_activity_layout.addWidget(update_preferred_activity_label)

    time_spent_layout = QHBoxLayout()
    time_spent_label = QLabel("Time Spent: 65 min.")
    update_time_spent_label = QPushButton("Update")
    time_spent_layout.addWidget(time_spent_label)
    time_spent_layout.addWidget(update_time_spent_label)

    calories_burnt_layout = QHBoxLayout()
    calories_burnt_label = QLabel("Calories Burnt: 504 kcal")
    update_calories_burnt_label = QPushButton("Update")
    calories_burnt_layout.addWidget(calories_burnt_label)
    calories_burnt_layout.addWidget(update_calories_burnt_label)

    distance_travelled_layout = QHBoxLayout()
    distance_travelled_label = QLabel("Distance Travelled: 3654 m")
    update_distance_travelled_label = QPushButton("Update")
    distance_travelled_layout.addWidget(distance_travelled_label)
    distance_travelled_layout.addWidget(update_distance_travelled_label)
    
    history_layout = QHBoxLayout()
    cardio_history_button = QPushButton("History")
    history_layout.addWidget(cardio_history_button)
    
    cardio_notes.addWidget(main_label)
    cardio_notes.addLayout(preferred_activity_layout)
    cardio_notes.addLayout(time_spent_layout)
    cardio_notes.addLayout(calories_burnt_layout)
    cardio_notes.addLayout(distance_travelled_layout)
    cardio_notes.addLayout(history_layout)

    cardio_notes.setSpacing(5)
    framed_layout = QFrame()
    framed_layout.setObjectName("graphObj")
    framed_layout.setFrameStyle(QFrame.Box)
    framed_layout.setLineWidth(3)
    framed_layout.setStyleSheet("""#graphObj {color: #322d2d;}""")
    
    framed_layout.setLayout(cardio_notes)
    
    return framed_layout
