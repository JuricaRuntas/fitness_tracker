from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QSize, Qt, QFileInfo

path = QFileInfo(__file__).absolutePath()

class ChestExercises(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()
    
  def create_panel(self):
    grid = QGridLayout()

    search_bar_layout = QHBoxLayout()
    search_bar_label = QLabel("Search", self)
    search_bar = QLineEdit(self)
    search_bar_layout.addWidget(search_bar_label)
    search_bar_layout.addWidget(search_bar)
    
    flat_barbell_bp_layout = QVBoxLayout()
    flat_barbell_bp = QPushButton(self)
    flat_barbell_bp.setIcon(QIcon("".join([path, "/chest_exercises/flat_barbell_bp.jpg"])))
    flat_barbell_bp.setIconSize(QSize(250, 150))
    flat_barbell_bp.resize(250, 150)
    flat_barbell_bp.setStyleSheet("border: none")
    flat_barbell_bp.setCursor(Qt.PointingHandCursor)
    
    flat_barbell_bp_label = QLabel("Flat Barbell Bench Press", self)
    flat_barbell_bp_label.setAlignment(Qt.AlignCenter)
    flat_barbell_bp_layout.addWidget(flat_barbell_bp)
    flat_barbell_bp_layout.addWidget(flat_barbell_bp_label)
    
    flat_dumbbell_bp_layout = QVBoxLayout()
    flat_dumbbell_bp = QPushButton(self)
    flat_dumbbell_bp.setIcon(QIcon("".join([path, "/chest_exercises/flat_dumbbell_bp.jpg"])))
    flat_dumbbell_bp.setIconSize(QSize(250, 150))
    flat_dumbbell_bp.resize(250, 150)
    flat_dumbbell_bp.setStyleSheet("border: none")
    flat_dumbbell_bp.setCursor(Qt.PointingHandCursor)

    flat_dumbbell_bp_label = QLabel("Flat Dumbbell Bench Press", self)
    flat_dumbbell_bp_label.setAlignment(Qt.AlignCenter)
    flat_dumbbell_bp_layout.addWidget(flat_dumbbell_bp)
    flat_dumbbell_bp_layout.addWidget(flat_dumbbell_bp_label)
    
    incline_dumbbell_bp_layout = QVBoxLayout()
    incline_dumbbell_bp = QPushButton(self)
    incline_dumbbell_bp.setIcon(QIcon("".join([path, "/chest_exercises/incline_dumbbell_bp.jpeg"])))
    incline_dumbbell_bp.setIconSize(QSize(250, 150))
    incline_dumbbell_bp.resize(250, 150)
    incline_dumbbell_bp.setStyleSheet("border: none")
    incline_dumbbell_bp.setCursor(Qt.PointingHandCursor)
    
    incline_dumbbell_bp_label = QLabel("Incline Dumbbell Bench Press", self)
    incline_dumbbell_bp_label.setAlignment(Qt.AlignCenter)
    incline_dumbbell_bp_layout.addWidget(incline_dumbbell_bp)
    incline_dumbbell_bp_layout.addWidget(incline_dumbbell_bp_label)
    
    incline_barbell_bp_layout = QVBoxLayout()
    incline_barbell_bp = QPushButton(self)
    incline_barbell_bp.setIcon(QIcon("".join([path, "/chest_exercises/incline_barbell_bp.jpg"])))
    incline_barbell_bp.setIconSize(QSize(250, 150))
    incline_barbell_bp.resize(250, 150)
    incline_barbell_bp.setStyleSheet("border: none")
    incline_barbell_bp.setCursor(Qt.PointingHandCursor)
    
    incline_barbell_bp_label = QLabel("Incline Barbell Bench Press", self)
    incline_barbell_bp_label.setAlignment(Qt.AlignCenter)
    incline_barbell_bp_layout.addWidget(incline_barbell_bp)
    incline_barbell_bp_layout.addWidget(incline_barbell_bp_label)
    
    push_ups_layout = QVBoxLayout()
    push_ups = QPushButton(self)
    push_ups.setIcon(QIcon("".join([path, "/chest_exercises/push_ups.png"])))
    push_ups.setIconSize(QSize(250, 150))
    push_ups.resize(250, 150)
    push_ups.setStyleSheet("border: none")
    push_ups.setCursor(Qt.PointingHandCursor)

    push_ups_label = QLabel("Push Ups", self)
    push_ups_label.setAlignment(Qt.AlignCenter)
    push_ups_layout.addWidget(push_ups)
    push_ups_layout.addWidget(push_ups_label)

    machine_chest_fly_layout = QVBoxLayout()
    machine_chest_fly = QPushButton(self)
    machine_chest_fly.setIcon(QIcon("".join([path, "/chest_exercises/machine_chest_fly.jpeg"])))
    machine_chest_fly.setIconSize(QSize(250, 150))
    machine_chest_fly.resize(250, 150)
    machine_chest_fly.setStyleSheet("border: none")
    machine_chest_fly.setCursor(Qt.PointingHandCursor)

    machine_chest_fly_label = QLabel("Machine Chest Fly", self)
    machine_chest_fly_label.setAlignment(Qt.AlignCenter)
    machine_chest_fly_layout.addWidget(machine_chest_fly)
    machine_chest_fly_layout.addWidget(machine_chest_fly_label)

    grid.addLayout(search_bar_layout, 0, 0, 1, 4)
    grid.addLayout(flat_barbell_bp_layout, 1, 0)
    grid.addLayout(flat_dumbbell_bp_layout, 1, 1)
    grid.addLayout(incline_dumbbell_bp_layout, 1, 2)
    grid.addLayout(incline_barbell_bp_layout, 2, 0)
    grid.addLayout(push_ups_layout, 2, 1)
    grid.addLayout(machine_chest_fly_layout, 2, 2)
    self.setLayout(grid)
