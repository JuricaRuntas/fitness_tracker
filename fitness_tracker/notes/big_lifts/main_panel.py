from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from .preferred_lifts import PreferredLifts

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()

  def create_panel(self):
    main_panel_grid = QGridLayout()
    main_panel_grid.addLayout(self.description(), 0, 0, 1, 1)
    main_panel_grid.addWidget(self.create_time_graph(), 1, 0, 4, 1)
    main_panel_grid.addLayout(self.create_bottom_layout(), 5, 0, 3, 1)
    main_panel_grid.addLayout(self.create_function_buttons(), 8, 0, 1, 1)
    self.setLayout(main_panel_grid)

  def description(self):
    panel_description = QVBoxLayout()
    description_label = QLabel("Keep notes and track progress of your preferred big lifts here.", self)
    description_label.setFixedHeight(30)

    panel_description.addWidget(description_label)
    return panel_description

  def create_time_graph(self):
    time_graph = QVBoxLayout()
    timeline_combobox = QComboBox(self)
    timeline_combobox.addItems(["Daily", "Weekly", "Monthly", "Yearly"])

    time_graph_graph = QWidget(self)
    time_graph_graph.setStyleSheet("background-color: red")

    time_graph.addWidget(time_graph_graph)
    time_graph.addWidget(timeline_combobox)
    framed_graph = QFrame(self)
    framed_graph.setFrameStyle(QFrame.StyledPanel)
    framed_graph.setLayout(time_graph)

    return framed_graph

  def create_bottom_layout(self):
    bottom_layout = QHBoxLayout()
    bottom_layout.addWidget(self.create_one_rep_max())
    bottom_layout.addWidget(self.create_lifts_for_reps())
    return bottom_layout

  def create_one_rep_max(self):
    orm_panel = QVBoxLayout()
    main_label = QLabel("One Rep Max")
    main_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    horizontal_press_label = QLabel("Bench Press: 80 kg")
    horizontal_press_label.setFont(QFont("Ariel", 10))

    floor_pull_label = QLabel("Deadlift: 140 kg")
    floor_pull_label.setFont(QFont("Ariel", 10))

    squat_label = QLabel("Front Squat: 90 kg")
    squat_label.setFont(QFont("Ariel", 10))

    vertical_press_label = QLabel("Military Press: 55 kg")
    vertical_press_label.setFont(QFont("Ariel", 10))

    orm_buttons = QHBoxLayout()
    update_button = QPushButton("Update")
    clear_button = QPushButton("Clear")
    orm_buttons.addWidget(update_button)
    orm_buttons.addWidget(clear_button)

    orm_panel.addWidget(main_label)
    orm_panel.addWidget(horizontal_press_label)
    orm_panel.addWidget(floor_pull_label)
    orm_panel.addWidget(squat_label)
    orm_panel.addWidget(vertical_press_label)
    orm_panel.addLayout(orm_buttons)

    orm_panel.setSpacing(5)
    framed_layout = QFrame()
    framed_layout.setFrameStyle(QFrame.StyledPanel)
    framed_layout.setLayout(orm_panel)

    return framed_layout

  def create_lifts_for_reps(self):
    reps_panel = QVBoxLayout()
    main_label = QLabel("Lifts For Reps")
    main_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    horizontal_press_label = QLabel("Bench Press: 70 kg, 4 reps")
    horizontal_press_label.setFont(QFont("Ariel", 10))

    floor_pull_label = QLabel("Deadlift: 120 kg, 5 reps")
    floor_pull_label.setFont(QFont("Ariel", 10))

    squat_label = QLabel("Front Squat: 70 kg, 7 reps")
    squat_label.setFont(QFont("Ariel", 10))

    vertical_press_label = QLabel("Military Press: 50 kg, 2 reps")
    vertical_press_label.setFont(QFont("Ariel", 10))

    reps_buttons = QHBoxLayout()
    update_button = QPushButton("Update")
    clear_button = QPushButton("Clear")
    reps_buttons.addWidget(update_button)
    reps_buttons.addWidget(clear_button)

    reps_panel.addWidget(main_label)
    reps_panel.addWidget(horizontal_press_label)
    reps_panel.addWidget(floor_pull_label)
    reps_panel.addWidget(squat_label)
    reps_panel.addWidget(vertical_press_label)
    reps_panel.addLayout(reps_buttons)

    framed_layout = QFrame()
    framed_layout.setFrameStyle(QFrame.StyledPanel)
    framed_layout.setLayout(reps_panel)

    return framed_layout

  def create_function_buttons(self):
    buttons_panel = QHBoxLayout()
    lift_history_button = QPushButton()
    lift_history_button.setText("Lift History")
    preferred_lists_button = QPushButton()
    preferred_lists_button.setText("Preferred Lifts")
    preferred_lists_button.clicked.connect(self.create_preferred_lists_window)

    buttons_panel.addWidget(lift_history_button)
    buttons_panel.addWidget(preferred_lists_button)
    return buttons_panel

  def create_preferred_lists_window(self):
    global plists_window
    plists_window = PreferredLifts()
    plists_window.setGeometry(100, 200, 300, 300)
    plists_window.show()



