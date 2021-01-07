import os
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QCalendarWidget, QPushButton
from PyQt5.QtGui import QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QLocale, QSize, pyqtSignal
from .exercises.exercises import Exercises

path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
muscle_groups_path = os.path.join(path, "muscle_groups")

muscle_groups = {"Chest": os.path.join(muscle_groups_path, "chest.svg"),
                 "Back": os.path.join(muscle_groups_path, "back.svg"),
                 "Core": os.path.join(muscle_groups_path, "core.svg"),
                 "Biceps": os.path.join(muscle_groups_path, "biceps.svg"),
                 "Triceps": os.path.join(muscle_groups_path, "triceps.svg"),
                 "Quadriceps": os.path.join(muscle_groups_path, "quads.svg"),
                 "Calves": os.path.join(muscle_groups_path, "calves.svg"),
                 "Shoulders": os.path.join(muscle_groups_path, "shoulders.svg"),
                 "Gluteus": os.path.join(muscle_groups_path, "gluteus.svg"),
                 "Hamstrings": os.path.join(muscle_groups_path, "hamstrings.svg")}

class MainPanel(QWidget):
  show_muscle_group_signal = pyqtSignal(str)

  def __init__(self, parent):
    super().__init__()
    self.create_panel()
    
  def create_panel(self):
    self.grid = QGridLayout()
    self.grid.addWidget(self.create_stats(), 0, 0, 1, 2)
    self.grid.addWidget(self.create_calendar_workouts(), 1, 0, 1, 2)
    self.grid.addWidget(self.create_exercises(), 2, 0, 1, 2)
    self.setLayout(self.grid)
    
  def create_stats(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)

    current_workout_frame = QFrame()
    current_workout_frame.setFrameStyle(QFrame.StyledPanel)
    current_workout_layout = QVBoxLayout()

    current_workout_label = QLabel("Current workout plan", self)
    current_workout_label.setAlignment(Qt.AlignCenter)
    current_workout_label2 = QLabel("Push Pull Legs", self)
    current_workout_label2.setAlignment(Qt.AlignCenter)

    current_workout_layout.addWidget(current_workout_label)
    current_workout_layout.addWidget(current_workout_label2)

    current_workout_frame.setLayout(current_workout_layout)

    last_workout_frame = QFrame()
    last_workout_frame.setFrameStyle(QFrame.StyledPanel)
    last_workout_layout = QVBoxLayout()

    last_workout_label = QLabel("Last workout", self)
    last_workout_label.setAlignment(Qt.AlignCenter)
    last_workout_label2 = QLabel("Monday, 9.2.2017", self)
    last_workout_label2.setAlignment(Qt.AlignCenter)

    last_workout_layout.addWidget(last_workout_label)
    last_workout_layout.addWidget(last_workout_label2)

    last_workout_frame.setLayout(last_workout_layout)

    number_of_workouts_frame = QFrame()
    number_of_workouts_frame.setFrameStyle(QFrame.StyledPanel)
    number_of_workouts_layout = QVBoxLayout()

    number_of_workouts_label = QLabel("Total number of workouts", self)
    number_of_workouts_label.setAlignment(Qt.AlignCenter)
    number_of_workouts_label2 = QLabel("31", self)
    number_of_workouts_label2.setAlignment(Qt.AlignCenter)

    number_of_workouts_layout.addWidget(number_of_workouts_label)
    number_of_workouts_layout.addWidget(number_of_workouts_label2)

    number_of_workouts_frame.setLayout(number_of_workouts_layout)

    wrapper = QHBoxLayout()
    wrapper.addWidget(current_workout_frame)
    wrapper.addWidget(last_workout_frame)
    wrapper.addWidget(number_of_workouts_frame)
    frame.setLayout(wrapper)
    return frame

  def create_calendar_workouts(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)
    layout = QHBoxLayout()
    
    calendar = QCalendarWidget(self)
    calendar.setLocale(QLocale(QLocale.English))
    calendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)

    my_workouts_frame = QFrame()
    my_workouts_frame.setFrameStyle(QFrame.StyledPanel)
    my_workouts_layout = QVBoxLayout()
    my_workouts_label = QLabel("My Workouts", self)

    workout1_frame = QFrame()
    workout1_frame.setFrameStyle(QFrame.StyledPanel)
    workout1_layout = QHBoxLayout()
    workout1_name_label = QLabel("Upper Lower", self)
    workout1_days_label = QLabel("4 days", self)
    workout1_delete = QPushButton(QIcon("".join([path, "/icons/x.png"])), "", self)
    workout1_delete.setStyleSheet("border: none")
    workout1_delete.setCursor(QCursor(Qt.PointingHandCursor))

    workout1_layout.addWidget(workout1_name_label)
    workout1_layout.addWidget(workout1_days_label)
    workout1_layout.addWidget(workout1_delete)
    workout1_frame.setLayout(workout1_layout)
     
    workout2_frame = QFrame()
    workout2_frame.setFrameStyle(QFrame.StyledPanel)
    workout2_layout = QHBoxLayout()
    workout2_name_label = QLabel("Push Pull Legs", self)
    workout2_days_label = QLabel("6 days", self)
    workout2_delete = QPushButton(QIcon("".join([path, "/icons/x.png"])), "", self)
    workout2_delete.setStyleSheet("border: none")
    workout2_delete.setCursor(QCursor(Qt.PointingHandCursor))

    workout2_layout.addWidget(workout2_name_label)
    workout2_layout.addWidget(workout2_days_label)
    workout2_layout.addWidget(workout2_delete)
    workout2_frame.setLayout(workout2_layout)

    workout3_frame = QFrame()
    workout3_frame.setFrameStyle(QFrame.StyledPanel)
    workout3_layout = QHBoxLayout()
    workout3_name_label = QLabel("My Workout1", self)
    workout3_days_label = QLabel("3 days", self)
    workout3_delete = QPushButton(QIcon("".join([path, "/icons/x.png"])), "", self)
    workout3_delete.setStyleSheet("border: none")
    workout3_delete.setCursor(QCursor(Qt.PointingHandCursor))

    workout3_layout.addWidget(workout3_name_label)
    workout3_layout.addWidget(workout3_days_label)
    workout3_layout.addWidget(workout3_delete)
    workout3_frame.setLayout(workout3_layout)

    add_workout_button = QPushButton("Add Workout", self)
    add_workout_button.setCursor(QCursor(Qt.PointingHandCursor)) 
    my_workouts_layout.addWidget(my_workouts_label)
    my_workouts_layout.addWidget(workout1_frame)
    my_workouts_layout.addWidget(workout2_frame)
    my_workouts_layout.addWidget(workout3_frame)
    my_workouts_layout.addWidget(add_workout_button)
    my_workouts_frame.setLayout(my_workouts_layout)

    layout.addWidget(calendar)
    layout.addWidget(my_workouts_frame)
    frame.setLayout(layout)
    return frame

  def create_exercises(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)
    exercises_layout = QVBoxLayout()

    label = QLabel("Exercises", self)
    label.setFont(QFont("Ariel", 15))
    
    first_row = QHBoxLayout()

    chest_muscle_group = QVBoxLayout()
    chest_image = QPushButton(self)
    chest_image.setIcon(QIcon(muscle_groups["Chest"]))
    chest_image.setIconSize(QSize(100, 60))
    chest_image.resize(100, 60)
    chest_image.setStyleSheet("border: none")
    chest_image.setCursor(Qt.PointingHandCursor)
    chest_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Chest"))

    chest_label = QLabel("Chest", self)
    chest_label.setAlignment(Qt.AlignCenter)
    chest_muscle_group.addWidget(chest_image)
    chest_muscle_group.addWidget(chest_label)
    
    back_muscle_group = QVBoxLayout()
    back_image = QPushButton(self)
    back_image.setIcon(QIcon(muscle_groups["Back"]))
    back_image.setIconSize(QSize(100, 60))
    back_image.resize(100, 60)
    back_image.setStyleSheet("border: none")
    back_image.setCursor(Qt.PointingHandCursor)
    back_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Back"))
    
    back_label = QLabel("Back", self)
    back_label.setAlignment(Qt.AlignCenter)
    back_muscle_group.addWidget(back_image)
    back_muscle_group.addWidget(back_label)
    
    triceps_muscle_group = QVBoxLayout()
    triceps_image = QPushButton(self)
    triceps_image.setIcon(QIcon(muscle_groups["Triceps"]))
    triceps_image.setIconSize(QSize(100, 60))
    triceps_image.resize(100, 60)
    triceps_image.setStyleSheet("border: none")
    triceps_image.setCursor(Qt.PointingHandCursor)
    triceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Triceps"))

    triceps_label = QLabel("Triceps", self)
    triceps_label.setAlignment(Qt.AlignCenter)
    triceps_muscle_group.addWidget(triceps_image)
    triceps_muscle_group.addWidget(triceps_label)

    biceps_muscle_group = QVBoxLayout()
    biceps_image = QPushButton(self)
    biceps_image.setIcon(QIcon(muscle_groups["Biceps"]))
    biceps_image.setIconSize(QSize(100, 60))
    biceps_image.resize(100, 60)
    biceps_image.setStyleSheet("border: none")
    biceps_image.setCursor(Qt.PointingHandCursor)
    biceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Biceps"))
    
    biceps_label = QLabel("Biceps", self)
    biceps_label.setAlignment(Qt.AlignCenter)
    biceps_muscle_group.addWidget(biceps_image)
    biceps_muscle_group.addWidget(biceps_label)
    
    shoulders_muscle_group = QVBoxLayout()
    shoulders_image = QPushButton(self)
    shoulders_image.setIcon(QIcon(muscle_groups["Shoulders"]))
    shoulders_image.setIconSize(QSize(100, 60))
    shoulders_image.resize(100, 60)
    shoulders_image.setStyleSheet("border: none")
    shoulders_image.setCursor(Qt.PointingHandCursor)
    shoulders_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Shoulders"))
    
    shoulders_label = QLabel("Shoulders", self)
    shoulders_label.setAlignment(Qt.AlignCenter)
    shoulders_muscle_group.addWidget(shoulders_image)
    shoulders_muscle_group.addWidget(shoulders_label)

    first_row.addLayout(chest_muscle_group)
    first_row.addLayout(back_muscle_group)
    first_row.addLayout(triceps_muscle_group)
    first_row.addLayout(biceps_muscle_group)
    first_row.addLayout(shoulders_muscle_group)
    
    second_row = QHBoxLayout()
    
    core_muscle_group = QVBoxLayout()
    core_image = QPushButton(self)
    core_image.setIcon(QIcon(muscle_groups["Core"]))
    core_image.setIconSize(QSize(100, 60))
    core_image.resize(100, 60)
    core_image.setStyleSheet("border: none")
    core_image.setCursor(Qt.PointingHandCursor)
    core_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Core"))
    
    core_label = QLabel("Core", self)
    core_label.setAlignment(Qt.AlignCenter)
    core_muscle_group.addWidget(core_image)
    core_muscle_group.addWidget(core_label)
    
    gluteus_muscle_group = QVBoxLayout()
    gluteus_image = QPushButton(self)
    gluteus_image.setIcon(QIcon(muscle_groups["Gluteus"]))
    gluteus_image.setIconSize(QSize(100, 60))
    gluteus_image.resize(100, 60)
    gluteus_image.setStyleSheet("border: none")
    gluteus_image.setCursor(Qt.PointingHandCursor)
    gluteus_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Legs"))
    
    gluteus_label = QLabel("Gluteus", self)
    gluteus_label.setAlignment(Qt.AlignCenter)
    gluteus_muscle_group.addWidget(gluteus_image)
    gluteus_muscle_group.addWidget(gluteus_label)

    quadriceps_muscle_group = QVBoxLayout()
    quadriceps_image = QPushButton(self)
    quadriceps_image.setIcon(QIcon(muscle_groups["Quadriceps"]))
    quadriceps_image.setIconSize(QSize(100, 60))
    quadriceps_image.resize(100, 60)
    quadriceps_image.setStyleSheet("border: none")
    quadriceps_image.setCursor(Qt.PointingHandCursor)
    quadriceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Legs"))
    
    quadriceps_label = QLabel("Quadriceps", self)
    quadriceps_label.setAlignment(Qt.AlignCenter)
    quadriceps_muscle_group.addWidget(quadriceps_image)
    quadriceps_muscle_group.addWidget(quadriceps_label)

    calves_muscle_group = QVBoxLayout()
    calves_image = QPushButton(self)
    calves_image.setIcon(QIcon(muscle_groups["Calves"]))
    calves_image.setIconSize(QSize(100, 60))
    calves_image.resize(100, 60)
    calves_image.setStyleSheet("border: none")
    calves_image.setCursor(Qt.PointingHandCursor)
    calves_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Calves"))
    
    calves_label = QLabel("Calves", self)
    calves_label.setAlignment(Qt.AlignCenter)
    calves_muscle_group.addWidget(calves_image)
    calves_muscle_group.addWidget(calves_label)
    
    hamstrings_group = QVBoxLayout()
    hamstrings_image = QPushButton(self)
    hamstrings_image.setIcon(QIcon(muscle_groups["Hamstrings"]))
    hamstrings_image.setIconSize(QSize(100, 60))
    hamstrings_image.resize(100, 60)
    hamstrings_image.setStyleSheet("border: none")
    hamstrings_image.setCursor(Qt.PointingHandCursor)
    hamstrings_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Legs"))
    
    hamstrings_label = QLabel("Hamstrings", self)
    hamstrings_label.setAlignment(Qt.AlignCenter)
    hamstrings_group.addWidget(hamstrings_image)
    hamstrings_group.addWidget(hamstrings_label)
    
    second_row.addLayout(core_muscle_group)
    second_row.addLayout(gluteus_muscle_group)
    second_row.addLayout(quadriceps_muscle_group)
    second_row.addLayout(calves_muscle_group)
    second_row.addLayout(hamstrings_group)

    exercises_layout.addWidget(label)
    exercises_layout.addLayout(first_row)
    exercises_layout.addLayout(second_row)
    frame.setLayout(exercises_layout)
    return frame
