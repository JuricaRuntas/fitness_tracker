from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QVBoxLayout, QLabel, QRadioButton
from PyQt5.QtGui import QFont

class Header(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_header()
  
  def create_header(self):
    grid = QGridLayout()
    self.setLayout(grid)

    title_label = QLabel(self)
    title_label.setText("Fitness Tracker  ")
    title_label.setFont(QFont("Arial", 25))

    qw_label = QLabel(self)
    qw_label.setText("Quick view:")
    qw_label.setFont(QFont("Arial", 18))

    u_label = QLabel(self)
    u_label.setText("Units: ")
    u_label.setFont(QFont("Arial", 18))
    
    s_radio = QRadioButton("Strength")
    wp_radio = QRadioButton("Weight progression")
    n_radio = QRadioButton("Nutrition")

    header_widgets = [title_label, qw_label, s_radio,
                      wp_radio, n_radio, u_label]
    
    positions = [y for y in range(6)]
    
    for y, widget in enumerate(header_widgets):
      grid.addWidget(widget, 0, positions[y])
      
    vbox = QVBoxLayout()
    m_radio = QRadioButton("Metric")
    i_radio = QRadioButton("Imperial")
    m_radio.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    i_radio.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    vbox.addWidget(m_radio)
    vbox.addWidget(i_radio)
    grid.addLayout(vbox, 0, 6)

