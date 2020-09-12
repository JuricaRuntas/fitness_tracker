from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QLineEdit, QGridLayout, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QScrollArea, QTableWidget\
  , QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.CreatePanel()

  def CreatePanel(self):
    main_panel_layout = QGridLayout()
    main_panel_layout.addLayout(self.description(), 0, 0, 1, 1)
    main_panel_layout.addLayout(self.calculator(), 2, 0, 2, 1)
    main_panel_layout.addLayout(self.strength_standards(), 6, 0, 4, 1)
    self.setLayout(main_panel_layout)

  def description(self):
    description_layout = QVBoxLayout()
    description_label = QLabel("Take a quick test and see where you are standing compared to other lifters.")
    description_label.setFixedHeight(30)
    description_layout.addWidget(description_label)

    return description_layout

  def calculator(self):
    calculator_layout = QHBoxLayout()
    data_layout = QHBoxLayout()
    print_layout = QVBoxLayout()

    data_labels = QVBoxLayout()
    data_inputs = QVBoxLayout()

    gender_age_label = QLabel("Gender/Age")
    gender_age_label.setFont(QFont("Ariel", 10))
    bodyweight_label = QLabel("Bodyweight")
    bodyweight_label.setFont(QFont("Ariel", 10))
    exercise_label = QLabel("Exercise")
    exercise_label.setFont(QFont("Ariel", 10))
    weight_label = QLabel("Weight")
    weight_label.setFont(QFont("Ariel", 10))
    repetition_label = QLabel("Repetitions")
    repetition_label.setFont(QFont("Ariel", 10))
    data_labels.addWidget(gender_age_label)
    data_labels.addWidget(bodyweight_label)
    data_labels.addWidget(exercise_label)
    data_labels.addWidget(weight_label)
    data_labels.addWidget(repetition_label)

    gender_combobox = QComboBox(self)
    gender_combobox.addItems(["Male", "Female"])
    age_combobox = QComboBox(self)
    age_combobox.addItems(["14-17", "18-23", "24-30", "31-39", "40-49", "50-59", "60-69", "70+"])
    gender_age_layout = QHBoxLayout()
    gender_age_layout.addWidget(gender_combobox)
    gender_age_layout.addWidget(age_combobox)

    bodyweight_line_edit = QLineEdit()
    exercise_combobox = QComboBox()
    #exercise_combobox.addItems()

    weight_line_edit = QLineEdit()
    repetitions_line_edit = QLineEdit()

    data_inputs.addLayout(gender_age_layout)
    data_inputs.addWidget(bodyweight_line_edit)
    data_inputs.addWidget(exercise_combobox)
    data_inputs.addWidget(weight_line_edit)
    data_inputs.addWidget(repetitions_line_edit)

    data_layout.addLayout(data_labels)
    data_layout.addLayout(data_inputs)

    strength_estimator_exercise_label = QLabel("Your strength level for deadlift is")
    strength_estimator_exercise_label.setFont(QFont("Ariel", 14))

    strength_level_exercise_label = QLabel("****Advanced")
    strength_level_exercise_label.setFont(QFont("Ariel", 14))

    strength_to_bodyweight_label = QLabel("Your lift is 1.88 times your bodyweight")
    strength_to_bodyweight_label.setFont(QFont("Ariel", 14))

    print_layout.addWidget(strength_estimator_exercise_label)
    print_layout.addWidget(strength_level_exercise_label)
    print_layout.addWidget(strength_to_bodyweight_label)

    calculator_layout.addLayout(data_layout)
    calculator_layout.addLayout(print_layout)

    return calculator_layout

  def strength_standards(self):
    strength_standards_layout = QVBoxLayout()
    standards_label = QLabel("Strength Standards")
    standards_label.setFont(QFont("Ariel", 18))
    strength_standards_layout.addWidget(standards_label)

    standards_info_layout = QHBoxLayout()
    male_button = QRadioButton("Male")
    male_button.setChecked(True)
    standards_info_layout.addWidget(male_button)
    female_button = QRadioButton("Female")
    standards_info_layout.addWidget(female_button)

    age_combobox = QComboBox(self)
    age_combobox.addItems(["14-17", "18-23", "24-30", "31-39", "40-49", "50-59", "60-69", "70+"])
    age_combobox.setFixedWidth(80)
    exercise_combobox = QComboBox()
    exercise_combobox.setFixedWidth(120)
    standards_info_layout.addWidget(age_combobox)
    standards_info_layout.addWidget(exercise_combobox)
    standards_info_layout.addStretch(1)
    standards_info_layout.setSpacing(10)

    strength_standards_layout.addLayout(standards_info_layout)

    standards_table_scroll_area = QScrollArea()


    standards_table = QTableWidget()
    standards_table.setRowCount(20)
    standards_table.setColumnCount(6)
    standards_table.horizontalHeader().setVisible(False)
    standards_table.verticalHeader().setVisible(False)

    standards_table_info = [["Bodyweight", "Beginner", "Novice", "Intermediate", "Advanced", "Elite"],
            ["50", "43", "64", "91", "123", "158"],
            ["55", "50", "64", "91", "123", "158"],
            ["60", "57", "64", "91", "123", "158"],
            ["65", "65", "64", "91", "123", "158"],
            ["70", "72", "64", "91", "123", "158"],
            ["75", "79", "64", "91", "123", "158"],
            ["80", "85", "64", "91", "123", "158"],
            ["85", "92", "64", "91", "123", "158"],
            ["90", "98", "64", "91", "123", "158"],
            ["95", "105", "64", "91", "123", "158"],
            ["100", "111", "64", "91", "123", "158"],
            ["105", "117", "64", "91", "123", "158"],
            ["110", "123", "64", "91", "123", "158"],
            ["115", "129", "64", "91", "123", "158"],
            ["120", "134", "64", "91", "123", "158"],
            ["125", "140", "64", "91", "123", "158"],
            ["130", "145", "64", "91", "123", "158"],
            ["135", "151", "64", "91", "123", "158"],
            ["140", "156", "64", "91", "123", "158"]]

    currentRow = 0
    for row in standards_table_info:
      currentColumn = 0
      for item in row:
        table_item = QTableWidgetItem(item)
        table_item.setFlags(Qt.ItemIsEnabled)
        standards_table.setItem(currentRow, currentColumn, table_item)
        currentColumn += 1
      currentRow += 1

    standards_table_scroll_area.setWidget(standards_table)
    standards_table_scroll_area.setWidgetResizable(True)

    strength_standards_layout.addWidget(standards_table_scroll_area)
    return strength_standards_layout
