from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QFormLayout, QLineEdit, QHBoxLayout

class Update1RMWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Update One Rep Max Lifts")
    self.setLayout(self.create_panel())

  def create_panel(self):
    form_layout = QFormLayout()

    exercise_label = QLabel("Exercise")
    weight_label = QLabel("Weight")
    
    units_label = QLabel("kg")
    horizontal_press_label = QLabel("Bench Press")
    horizontal_press_edit = QLineEdit()
    hbox = QHBoxLayout()
    hbox.addWidget(horizontal_press_edit)
    hbox.addWidget(units_label)

    units_label1 = QLabel("kg")
    floor_pull_label = QLabel("Deadlift")
    floor_pull_edit = QLineEdit()
    hbox1 = QHBoxLayout()
    hbox1.addWidget(floor_pull_edit)
    hbox1.addWidget(units_label1)

    units_label2 = QLabel("kg")
    squat_label = QLabel("Back Squat")
    squat_edit = QLineEdit()
    hbox2 = QHBoxLayout()
    hbox2.addWidget(squat_edit)
    hbox2.addWidget(units_label2)

    units_label3 = QLabel("kg")
    vertical_press_label = QLabel("Overhead Press")
    vertical_press_edit = QLineEdit()
    hbox3 = QHBoxLayout()
    hbox3.addWidget(vertical_press_edit)
    hbox3.addWidget(units_label3)

    save_button = QPushButton("Save")
    cancel_button = QPushButton("Cancel")

    form_layout.addRow(exercise_label, weight_label)
    form_layout.addRow(horizontal_press_label, hbox)
    form_layout.addRow(floor_pull_label, hbox1)
    form_layout.addRow(squat_label, hbox2)
    form_layout.addRow(vertical_press_label, hbox3)
    form_layout.addRow(save_button, cancel_button)
    return form_layout
