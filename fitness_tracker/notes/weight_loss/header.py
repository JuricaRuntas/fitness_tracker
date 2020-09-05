from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QRadioButton, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Header(QWidget):
  def __init__(self, parent, title):
    super().__init__(parent)
    self.title = title
    self.create_header()
  
  def create_header(self):
    grid = QGridLayout()
    self.setLayout(grid)
    
    title_layout = QHBoxLayout()
    title_label = QLabel(self.title, self)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setFont(QFont("Arial", 25))
    title_layout.addWidget(title_label)

    header_frame = QFrame()
    header_frame.setFrameStyle(QFrame.StyledPanel)
    header_layout = QHBoxLayout()

    current_weight_frame = QFrame()
    current_weight_frame.setFrameStyle(QFrame.StyledPanel)
    current_weight_layout = QVBoxLayout()
    
    current_weight_label = QLabel("Current Weight", self)
    current_weight_label.setAlignment(Qt.AlignCenter)
    current_weight_label2 = QLabel("90.0 kg", self)
    current_weight_label2.setAlignment(Qt.AlignCenter)

    current_weight_layout.addWidget(current_weight_label)
    current_weight_layout.addWidget(current_weight_label2)

    current_weight_frame.setLayout(current_weight_layout)
    
    desired_weight_frame = QFrame()
    desired_weight_frame.setFrameStyle(QFrame.StyledPanel)
    desired_weight_layout = QVBoxLayout()

    desired_weight_label = QLabel("Desired Weight", self)
    desired_weight_label.setAlignment(Qt.AlignCenter)
    desired_weight_label2 = QLabel("85.0 kg", self)
    desired_weight_label2.setAlignment(Qt.AlignCenter)

    desired_weight_layout.addWidget(desired_weight_label)
    desired_weight_layout.addWidget(desired_weight_label2)
    desired_weight_frame.setLayout(desired_weight_layout) 
    
    bmi_frame = QFrame()
    bmi_frame.setFrameStyle(QFrame.StyledPanel)
    bmi_layout = QVBoxLayout()

    bmi_label = QLabel("BMI", self)
    bmi_label.setAlignment(Qt.AlignCenter)
    bmi_label2 = QLabel("25.8", self)
    bmi_label2.setAlignment(Qt.AlignCenter)
    
    bmi_layout.addWidget(bmi_label)
    bmi_layout.addWidget(bmi_label2)
    bmi_frame.setLayout(bmi_layout)

    body_fat_frame = QFrame()
    body_fat_frame.setFrameStyle(QFrame.StyledPanel)
    body_fat_layout = QVBoxLayout()

    body_fat_label = QLabel("Body Fat", self)
    body_fat_label.setAlignment(Qt.AlignCenter)
    body_fat_label2 = QLabel("25.7%", self)
    body_fat_label2.setAlignment(Qt.AlignCenter)

    body_fat_layout.addWidget(body_fat_label)
    body_fat_layout.addWidget(body_fat_label2)
    body_fat_frame.setLayout(body_fat_layout)
    
    units_frame = QFrame()
    units_frame.setFrameStyle(QFrame.StyledPanel)
    units_layout = QVBoxLayout()
    units_group = QGroupBox()
    units_group.setFixedHeight(100)
    m_radio = QRadioButton("Metric")
    m_radio.setChecked(True)
    i_radio = QRadioButton("Imperial")
     
    units_layout.addWidget(m_radio)
    units_layout.addWidget(i_radio)

    units_group.setLayout(units_layout)

    groupbox_layout = QHBoxLayout()
    groupbox_layout.addWidget(units_group)
    units_frame.setLayout(groupbox_layout)

    header_layout.addWidget(current_weight_frame)
    header_layout.addWidget(desired_weight_frame)
    header_layout.addWidget(bmi_frame)
    header_layout.addWidget(body_fat_frame)
    header_layout.addWidget(units_frame)
    header_frame.setLayout(header_layout)
    grid.addLayout(title_layout, 0, 0, 1, 1)
    grid.addWidget(header_frame, 0, 3, 1, 3)
