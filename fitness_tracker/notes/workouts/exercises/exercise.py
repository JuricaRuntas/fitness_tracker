from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QFrame, QVBoxLayout, QPlainTextEdit, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QFileInfo
from .exercise_database import *
import os

path = QFileInfo(__file__).absolutePath()

db_path = path.split(os.path.sep)[:-4]
db_path = os.path.sep.join([os.path.sep.join(db_path), "db", "chest_exercises.db"])

class Exercise(QWidget):
  def __init__(self, parent, exercise, db):
    super().__init__(parent)
    if db == "Chest Exercises":
      self.db = ChestExercisesDB(db_path)
      self.db.fetch_info(exercise)
    self.name = self.db.fetch_name()
    self.description = self.db.fetch_description()
    self.muscles_targeted = self.db.fetch_muscles_targeted()
    self.instructions = self.db.fetch_instructions()
    self.tips = self.db.fetch_tips()

    self.grid = QGridLayout()
    self.create_panel()
    self.setLayout(self.grid)

  def create_panel(self):
    self.grid.addLayout(self.create_title_and_image(), 0, 0, 1, 2)
    self.grid.addWidget(self.create_description(), 1, 0, 1, 1)
    self.grid.addWidget(self.create_muscle_targeted(), 1, 1, 1, 1)
    self.grid.addWidget(self.create_instructions(), 2, 0, 1, 1)
    self.grid.addWidget(self.create_tips(), 2, 1, 1, 1)

  def create_title_and_image(self):
    layout = QVBoxLayout()
    
    label = QLabel(self.name, self)
    label.setAlignment(Qt.AlignCenter)
    label.setFont(QFont("Ariel", 30))

    exercise = QPushButton(self)
    exercise.setIcon(QIcon("".join([path, "/chest_exercises/flat_barbell_bp.jpg"])))
    exercise.setIconSize(QSize(200, 200))
    exercise.resize(200, 200)
    exercise.setStyleSheet("border: none")
    
    layout.addWidget(label)
    layout.addWidget(exercise)
    
    return layout

  def create_description(self):
    description_frame = QFrame()
    description_layout = QVBoxLayout()
    
    description_label = QLabel("Description", self)
    description_label.setAlignment(Qt.AlignLeft)
    
    description = QPlainTextEdit()
    description.appendPlainText(self.description)
    description.setReadOnly(True)

    description_layout.addWidget(description_label)
    description_layout.addWidget(description)
    description_frame.setLayout(description_layout)

    return description_frame

  def create_muscle_targeted(self):
    muscle_targeted_frame = QFrame()
    muscle_targeted_layout = QVBoxLayout()
    
    muscle_targeted_label = QLabel("Muscle Targeted", self)
    primary_label = QLabel("Primary: %s" % self.muscles_targeted[0], self)
    secondary_label = QLabel("Secondary: %s" % self.muscles_targeted[1], self)

    muscle_targeted_layout.addWidget(muscle_targeted_label)
    muscle_targeted_layout.addWidget(primary_label)
    muscle_targeted_layout.addWidget(secondary_label)
    muscle_targeted_frame.setLayout(muscle_targeted_layout)

    return muscle_targeted_frame

  def create_instructions(self):
    instructions_frame = QFrame()
    instructions_layout = QVBoxLayout()

    instructions_label = QLabel("Instructions", self)
    instructions = QPlainTextEdit()
    instructions.appendPlainText(self.instructions)
    instructions.setReadOnly(True)

    instructions_layout.addWidget(instructions_label)
    instructions_layout.addWidget(instructions)
    instructions_frame.setLayout(instructions_layout)

    return instructions_frame

  def create_tips(self):
    tips_frame = QFrame()
    tips_layout = QVBoxLayout()

    tips_label = QLabel("Tips", self)
    tips = QPlainTextEdit()
    tips.appendPlainText(self.tips)
    tips.setReadOnly(True)

    tips_layout.addWidget(tips_label)
    tips_layout.addWidget(tips)
    tips_frame.setLayout(tips_layout)

    return tips_frame
