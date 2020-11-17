import json
from PyQt5.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSlot
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
    if self.interface.table_is_empty(): self.interface.insert_default_values()
    self.units = "kg" if self.interface.fetch_units() == "metric" else "lb"
    self.one_RM = [[lift, " ".join([weight, self.units])] for lift, weight in json.loads(self.interface.fetch_one_rep_maxes()).items()]
    self.lifts_reps = [[lift, " ".join(["x".join(weight), self.units])] for lift, weight in json.loads(self.interface.fetch_lifts_for_reps()).items()]
 
    self.lift_history_window = LiftHistory()
    self.lift_history_window.setGeometry(100, 200, 300, 300)   
    
    self.plists_window = PreferredLifts()
    self.plists_window.change_lifts_signal.connect(self.changed_preferred_lifts)
    
    self.update_1RM_window = Update1RMWindow()
    self.update_1RM_window.change_1RM_lifts_signal.connect(self.changed_1RM_lifts)
    self.update_1RM_window.history_signal.connect(
    lambda signal: self.lift_history_window.create_history(signal))
    
    self.lifts_for_reps = UpdateLiftsForRepsWindow()
    self.lifts_for_reps.change_lifts_for_reps_signal.connect(self.changed_lifts_for_reps)
    self.lifts_for_reps.history_signal.connect(lambda signal: self.lift_history_window.create_history(signal))

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

    self.horizontal_press_label_ORM = QLabel(": ".join(self.one_RM[0]))
    self.horizontal_press_label_ORM.setFont(QFont("Ariel", 10))

    self.floor_pull_label_ORM = QLabel(": ".join(self.one_RM[1]))
    self.floor_pull_label_ORM.setFont(QFont("Ariel", 10))

    self.squat_label_ORM = QLabel(": ".join(self.one_RM[2]))
    self.squat_label_ORM.setFont(QFont("Ariel", 10))

    self.vertical_press_label_ORM = QLabel(": ".join(self.one_RM[3]))
    self.vertical_press_label_ORM.setFont(QFont("Ariel", 10))

    orm_buttons = QHBoxLayout()
    update_button = QPushButton("Update")
    update_button.clicked.connect(lambda: self.update_1RM_window.show())
    clear_button = QPushButton("Clear")
    clear_button.clicked.connect(lambda: self.clear_one_rep_maxes())
    orm_buttons.addWidget(update_button)
    orm_buttons.addWidget(clear_button)

    orm_panel.addWidget(main_label)
    orm_panel.addWidget(self.horizontal_press_label_ORM)
    orm_panel.addWidget(self.floor_pull_label_ORM)
    orm_panel.addWidget(self.squat_label_ORM)
    orm_panel.addWidget(self.vertical_press_label_ORM)
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

    self.horizontal_press_label_reps = QLabel(": ".join(self.lifts_reps[0]))
    self.horizontal_press_label_reps.setFont(QFont("Ariel", 10))

    self.floor_pull_label_reps = QLabel(": ".join(self.lifts_reps[1]))
    self.floor_pull_label_reps.setFont(QFont("Ariel", 10))

    self.squat_label_reps = QLabel(": ".join(self.lifts_reps[2]))
    self.squat_label_reps.setFont(QFont("Ariel", 10))

    self.vertical_press_label_reps = QLabel(": ".join(self.lifts_reps[3]))
    self.vertical_press_label_reps.setFont(QFont("Ariel", 10))

    reps_buttons = QHBoxLayout()
    update_button = QPushButton("Update")
    update_button.clicked.connect(lambda: self.lifts_for_reps.show())
    clear_button = QPushButton("Clear")
    clear_button.clicked.connect(lambda: self.clear_lifts_for_reps())
    reps_buttons.addWidget(update_button)
    reps_buttons.addWidget(clear_button)

    reps_panel.addWidget(main_label)
    reps_panel.addWidget(self.horizontal_press_label_reps)
    reps_panel.addWidget(self.floor_pull_label_reps)
    reps_panel.addWidget(self.squat_label_reps)
    reps_panel.addWidget(self.vertical_press_label_reps)
    reps_panel.addLayout(reps_buttons)

    framed_layout = QFrame()
    framed_layout.setFrameStyle(QFrame.StyledPanel)
    framed_layout.setLayout(reps_panel)

    return framed_layout

  def create_function_buttons(self):
    buttons_panel = QHBoxLayout()
    lift_history_button = QPushButton()
    lift_history_button.setText("Lift History")
    lift_history_button.clicked.connect(lambda: self.lift_history_window.show())
    preferred_lists_button = QPushButton()
    preferred_lists_button.setText("Preferred Lifts")
    preferred_lists_button.clicked.connect(lambda: self.plists_window.show())

    buttons_panel.addWidget(lift_history_button)
    buttons_panel.addWidget(preferred_lists_button)
    return buttons_panel
  
  @pyqtSlot(bool)
  def changed_preferred_lifts(self, changed):
    if changed:
      fetch_lifts = self.interface.fetch_preferred_lifts()
      parsed_lifts = list(json.loads(fetch_lifts).values())
      one_RM_labels = [self.horizontal_press_label_ORM, self.floor_pull_label_ORM,
                       self.squat_label_ORM, self.vertical_press_label_ORM]

      lifts_for_reps_labels = [self.horizontal_press_label_reps, self.floor_pull_label_reps,
                               self.squat_label_reps, self.vertical_press_label_reps]
      
      for i, label in enumerate(one_RM_labels):
        label_text = label.text().split(":")
        label_text[0] = parsed_lifts[i]
        label.setText(": ".join(label_text))

      for i, label in enumerate(lifts_for_reps_labels):
        label_text = label.text().split(":")
        label_text[0] = parsed_lifts[i]
        label.setText(": ".join(label_text))
  
  @pyqtSlot(bool)
  def changed_1RM_lifts(self, changed):
    if changed:
      fetch_weight = list(json.loads(self.interface.fetch_one_rep_maxes()).values())
      self.set_1RM_labels_text(fetch_weight)

  @pyqtSlot(bool)
  def changed_lifts_for_reps(self, changed):
    if changed:
      fetch_reps_and_weight = list(json.loads(self.interface.fetch_lifts_for_reps()).values())
      self.set_lifts_for_reps_labels_text(fetch_reps_and_weight)
  
  def set_lifts_for_reps_labels_text(self, text):
    lifts_for_reps_labels = [self.horizontal_press_label_reps, self.floor_pull_label_reps,
                             self.squat_label_reps, self.vertical_press_label_reps]
      
    for i, label in enumerate(lifts_for_reps_labels):
      label_text = label.text().split(": ")
      label_text[1] = " ".join(["x".join(text[i]), self.units])
      label.setText(": ".join(label_text))
  
  def set_1RM_labels_text(self, text):
    one_RM_labels = [self.horizontal_press_label_ORM, self.floor_pull_label_ORM,
                       self.squat_label_ORM, self.vertical_press_label_ORM]
    for i, label in enumerate(one_RM_labels):
      label_text = label.text().split(": ")
      label_text[1] = " ".join([text[i], self.units])
      label.setText(": ".join(label_text))

  def clear_one_rep_maxes(self):
    self.interface.clear_one_rep_maxes()
    fetch_weight = list(json.loads(self.interface.fetch_one_rep_maxes()).values())
    self.set_1RM_labels_text(fetch_weight)
    self.update_1RM_window.set_line_edit_values()
   
  def clear_lifts_for_reps(self):
    self.interface.clear_lifts_for_reps()
    fetch_reps_and_weight = list(json.loads(self.interface.fetch_lifts_for_reps()).values())
    self.set_lifts_for_reps_labels_text(fetch_reps_and_weight)
    self.lifts_for_reps.set_line_edit_values()
