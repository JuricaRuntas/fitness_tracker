from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from .preferred_lifts import PreferredLifts
from .update_1RM_window import Update1RMWindow
from .update_lifts_for_reps_window import UpdateLiftsForRepsWindow
from .lift_history import LiftHistory
from .big_lifts_helpers import BigLifts

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.interface = BigLifts()
    self.interface.create_big_lifts_table()
    if self.interface.table_is_empty():
      exercises = PreferredLifts().fetch_current_exercises()
      self.interface.insert_default_values(exercises)
    self.units = "kg" if self.interface.fetch_units() == "metric" else "lb"
    self.one_RM = [[lift, weight, self.units] for lift, weight in self.interface.fetch_one_rep_maxes().items()]
    self.lifts_reps = [[lift, weight, self.units] for lift, weight in self.interface.fetch_lifts_for_reps().items()]
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

    horizontal_press_label = QLabel(": ".join(self.one_RM[0]))
    horizontal_press_label.setFont(QFont("Ariel", 10))

    floor_pull_label = QLabel(": ".join(self.one_RM[1]))
    floor_pull_label.setFont(QFont("Ariel", 10))

    squat_label = QLabel(": ".join(self.one_RM[2]))
    squat_label.setFont(QFont("Ariel", 10))

    vertical_press_label = QLabel(": ".join(self.one_RM[3]))
    vertical_press_label.setFont(QFont("Ariel", 10))

    orm_buttons = QHBoxLayout()
    update_button = QPushButton("Update")
    update_button.clicked.connect(self.create_update_1RM_window)
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

    horizontal_press_label = QLabel(": ".join(self.lifts_reps[0]))
    horizontal_press_label.setFont(QFont("Ariel", 10))

    floor_pull_label = QLabel(": ".join(self.lifts_reps[1]))
    floor_pull_label.setFont(QFont("Ariel", 10))

    squat_label = QLabel(": ".join(self.lifts_reps[2]))
    squat_label.setFont(QFont("Ariel", 10))

    vertical_press_label = QLabel(": ".join(self.lifts_reps[3]))
    vertical_press_label.setFont(QFont("Ariel", 10))

    reps_buttons = QHBoxLayout()
    update_button = QPushButton("Update")
    update_button.clicked.connect(self.create_update_lifts_for_reps_window)
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
    lift_history_button.clicked.connect(self.create_lift_history_window)
    preferred_lists_button = QPushButton()
    preferred_lists_button.setText("Preferred Lifts")
    preferred_lists_button.clicked.connect(self.create_preferred_lists_window)

    buttons_panel.addWidget(lift_history_button)
    buttons_panel.addWidget(preferred_lists_button)
    return buttons_panel

  def create_preferred_lists_window(self):
    global plists_window
    plists_window = PreferredLifts()
    plists_window.show()

  def create_lift_history_window(self):
    global lift_history_window
    lift_history_window = LiftHistory()
    lift_history_window.setGeometry(100, 200, 300, 300)
    lift_history_window.show()

  def create_update_1RM_window(self):
    global update_1RM_window
    update_1RM_window = Update1RMWindow()
    update_1RM_window.setGeometry(100, 200, 300, 300)
    update_1RM_window.show()

  def create_update_lifts_for_reps_window(self):
    global lifts_for_reps
    lifts_for_reps = UpdateLiftsForRepsWindow()
    lifts_for_reps.setGeometry(100, 200, 300, 300)
    lifts_for_reps.show()
