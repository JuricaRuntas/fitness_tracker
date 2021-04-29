from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QFrame, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Exercise(QWidget):
  def __init__(self, parent, exercise_info):
    super().__init__(parent)
    self.exercise_info = exercise_info
    self.grid = QGridLayout()
    self.setStyleSheet("""
    QWidget{
      color:#c7c7c7;
      font-weight: bold;
      font-size: 16px;
    }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
    }
    QPushButton:hover:!pressed{
      border: 2px solid;
      border-color: #747474;
    }
    QPushButton:pressed{
      border: 2px solid;
      background-color: #323232;
      border-color: #6C6C6C;
    }
    QComboBox{
      border-radius: 4px;
      font-size: 18px;
      font-weight: bold;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
      min-height: 28px;
      background-color: #440D0F;
    }
    QComboBox:down-arrow{
      width: 0px;
      height: 0px;
      background: #d3d3d3; 
      opacity:0
    }
    QComboBox:drop-down{
      background-color: #440D0F;
      border: 0px;
      opacity:0;
      border-radius: 0px;
      width: 0px;
      height: 0px;
    }
    QComboBox:hover:!pressed{
      background-color: #5D1A1D;
    }
    QComboBox:pressed{
      background-color: #551812;
    }
    QTextEdit{
      font-weight: normal;
      background-color: #232120;
      border: 2px solid;
      border-color: #110f00
    }
    QPlainTextEdit{
      font-weight: normal;
      background-color: #232120;
      border: 2px solid;
      border-color: #110f00
    }
    """)
    self.create_panel()
    self.setLayout(self.grid)

  def create_panel(self):
    self.grid.addLayout(self.create_title(), 0, 0, 1, 2)
    self.grid.addWidget(self.create_description(), 1, 0, 2, 1)
    self.grid.addWidget(self.create_muscle_targeted(), 1, 1, 1, 1)
    self.grid.addWidget(self.create_tips(), 2, 1, 1, 1)

  def create_title(self):
    layout = QVBoxLayout()
    
    label = QLabel(self.exercise_info["name"], self)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("""font-size: 30px;""")

    layout.addWidget(label)
    
    return layout

  def create_description(self):
    description_frame = QFrame()
    description_layout = QVBoxLayout()
    
    description_label = QLabel("Description", self)
    description_label.setAlignment(Qt.AlignLeft)
    
    description = QTextEdit()
    description.setHtml(self.exercise_info["description"])
    description.setReadOnly(True)

    description_layout.addWidget(description_label)
    description_layout.addWidget(description)
    description_frame.setLayout(description_layout)

    return description_frame

  def create_muscle_targeted(self):
    muscle_targeted_frame = QFrame()
    muscle_targeted_layout = QVBoxLayout()
    
    muscle_targeted_label = QLabel("Muscle Targeted", self)
    
    primary_muscles = ""
    for targeted in self.exercise_info["muscles_primary"]:
      if primary_muscles == "": primary_muscles += targeted
      else: primary_muscles += ", " + targeted
    primary_label = QLabel("Primary: %s" % primary_muscles,self)
    
    secondary_muscles = ""
    for targeted in self.exercise_info["muscles_secondary"]:
      if secondary_muscles == "": secondary_muscles += targeted
      else: secondary_muscles += ", " + targeted
    secondary_label = QLabel("Secondary: %s" % secondary_muscles, self)

    muscle_targeted_layout.addWidget(muscle_targeted_label)
    muscle_targeted_layout.addWidget(primary_label)
    muscle_targeted_layout.addWidget(secondary_label)
    muscle_targeted_frame.setLayout(muscle_targeted_layout)

    return muscle_targeted_frame

  def create_tips(self):
    tips_frame = QFrame()
    tips_layout = QVBoxLayout()

    tips_label = QLabel("Tips", self)
    tips = QPlainTextEdit()
    if len(self.exercise_info["comment"]) > 0: tips.appendPlainText(self.exercise_info["comment"])
    tips.setReadOnly(True)

    tips_layout.addWidget(tips_label)
    tips_layout.addWidget(tips)
    tips_frame.setLayout(tips_layout)

    return tips_frame
