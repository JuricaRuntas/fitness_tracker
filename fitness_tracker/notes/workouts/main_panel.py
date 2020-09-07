from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QCalendarWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QFileInfo

path = QFileInfo(__file__).absolutePath()

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__()
    self.create_panel()
  
  def create_panel(self):
    grid = QGridLayout()
    grid.addWidget(self.create_stats(), 0, 0, 1, 2)
    grid.addWidget(self.create_calendar_workouts(), 1, 0, 1, 2)
    grid.addWidget(self.create_exercises(), 2, 0, 1, 2)
    self.setLayout(grid)

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

    my_workouts_frame = QFrame()
    my_workouts_frame.setFrameStyle(QFrame.StyledPanel)
    my_workouts_layout = QVBoxLayout()
    my_workouts_label = QLabel("My Workouts", self)

    workout1_frame = QFrame()
    workout1_frame.setFrameStyle(QFrame.StyledPanel)
    workout1_layout = QHBoxLayout()
    workout1_name_label = QLabel("Upper Lower", self)
    workout1_days_label = QLabel("4 days", self)
    
    workout1_layout.addWidget(workout1_name_label)
    workout1_layout.addWidget(workout1_days_label)
    workout1_frame.setLayout(workout1_layout)
    
    workout2_frame = QFrame()
    workout2_frame.setFrameStyle(QFrame.StyledPanel)
    workout2_layout = QHBoxLayout()
    workout2_name_label = QLabel("Push Pull Legs", self)
    workout2_days_label = QLabel("6 days", self)

    workout2_layout.addWidget(workout2_name_label)
    workout2_layout.addWidget(workout2_days_label)
    workout2_frame.setLayout(workout2_layout)

    workout3_frame = QFrame()
    workout3_frame.setFrameStyle(QFrame.StyledPanel)
    workout3_layout = QHBoxLayout()
    workout3_name_label = QLabel("My Workout1", self)
    workout3_days_label = QLabel("3 days", self)

    workout3_layout.addWidget(workout3_name_label)
    workout3_layout.addWidget(workout3_days_label)
    workout3_frame.setLayout(workout3_layout)

    my_workouts_layout.addWidget(my_workouts_label)
    my_workouts_layout.addWidget(workout1_frame)
    my_workouts_layout.addWidget(workout2_frame)
    my_workouts_layout.addWidget(workout3_frame)
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
    
    chest_image = QLabel(self)
    chest_pixmap = QPixmap("".join([path, "/muscle_groups/chest_muscles.png"]))
    chest_image.setPixmap(chest_pixmap)
    
    chest_label = QLabel("Chest", self)
    chest_label.setAlignment(Qt.AlignCenter)
    chest_muscle_group.addWidget(chest_image)
    chest_muscle_group.addWidget(chest_label)
    
    back_muscle_group = QVBoxLayout()
    back_label = QLabel("Back", self)
    back_muscle_group.addWidget(back_label)
    
    triceps_muscle_group = QVBoxLayout()
    triceps_label = QLabel("Triceps", self)
    triceps_muscle_group.addWidget(triceps_label)

    biceps_muscle_group = QVBoxLayout()
    biceps_label = QLabel("Biceps", self)
    biceps_muscle_group.addWidget(biceps_label)
    
    shoulders_muscle_group = QVBoxLayout()
    shoulders_label = QLabel("Shoulders", self)
    shoulders_muscle_group.addWidget(shoulders_label)

    first_row.addLayout(chest_muscle_group)
    first_row.addLayout(back_muscle_group)
    first_row.addLayout(triceps_muscle_group)
    first_row.addLayout(biceps_muscle_group)
    first_row.addLayout(shoulders_muscle_group)
    
    second_row = QHBoxLayout()
    
    core_muscle_group = QVBoxLayout()
    
    core_image = QLabel(self)
    core_pixmap = QPixmap("".join([path, "/muscle_groups/core_muscles.jpg"]))
    core_image.setPixmap(core_pixmap)

    core_label = QLabel("Core", self)
    core_label.setAlignment(Qt.AlignCenter)
    core_muscle_group.addWidget(core_image)
    core_muscle_group.addWidget(core_label)
    
    forearms_muscle_group = QVBoxLayout()
    forearms_label = QLabel("Forearms", self)
    forearms_muscle_group.addWidget(forearms_label)

    upper_legs_muscle_group = QVBoxLayout()
    upper_legs_label = QLabel("Upper Legs", self)
    upper_legs_muscle_group.addWidget(upper_legs_label)

    calves_muscle_group = QVBoxLayout()
    calves_label = QLabel("Calves", self)
    calves_muscle_group.addWidget(calves_label)
    
    cardio_group = QVBoxLayout()
    cardio_label = QLabel("Cardio", self)
    cardio_group.addWidget(cardio_label)
    
    second_row.addLayout(core_muscle_group)
    second_row.addLayout(forearms_muscle_group)
    second_row.addLayout(upper_legs_muscle_group)
    second_row.addLayout(calves_muscle_group)
    second_row.addLayout(cardio_group)

    exercises_layout.addWidget(label)
    exercises_layout.addLayout(first_row)
    exercises_layout.addLayout(second_row)
    frame.setLayout(exercises_layout)

    return frame
