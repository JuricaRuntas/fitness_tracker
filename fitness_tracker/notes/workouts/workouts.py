from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from fitness_tracker.homepage.side_panel import SidePanel
from .exercises.exercises import Exercises
from .exercises_and_workouts import ExercisesAndWorkouts
from .workout_planner import WorkoutPlanner

class WorkoutsNotes(QWidget):
  display_layout_signal = pyqtSignal(str)

  def __init__(self, layout_name):
    super().__init__()
    self.main_panel = ExercisesAndWorkouts() if layout_name == "Exercises and Workouts" else WorkoutPlanner()
    if layout_name == "Exercises and Workouts":
      self.main_panel.show_muscle_group_signal.connect(lambda muscle_group: self.show_muscle_group_layout(muscle_group))
    self.side_panel = SidePanel(self)
    self.side_panel.emit_layout_name.connect(lambda layout_name: self.emit_display_layout_signal(layout_name))
    self.create_grid()

  def create_grid(self):
    self.grid = QGridLayout()
    self.grid.addWidget(self.side_panel, 1, 0, 8, 1)
    self.grid.addWidget(self.main_panel, 1, 1, 8, 3)
    self.setLayout(self.grid)
  
  @pyqtSlot(str)
  def emit_display_layout_signal(self, layout_name):
    self.display_layout_signal.emit(layout_name)

  @pyqtSlot(str)
  def show_muscle_group_layout(self, muscle_group):
    self.grid.itemAt(1).widget().setParent(None)
    self.exercises = Exercises(self, muscle_group)
    self.exercises.show_exercise_signal.connect(lambda exercise_info: self.show_exercise_info_layout(exercise_info))
    self.grid.addWidget(self.exercises, 1, 1, 8, 3)
