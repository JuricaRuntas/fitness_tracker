from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QRadioButton
from PyQt5.QtGui import QFont

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
    title_label.setFont(QFont("Arial", 25))
    title_layout.addWidget(title_label)

    qw_layout = QHBoxLayout()
    qw_group = QGroupBox("Quick View:")
    radio_layout = QHBoxLayout()
    
    s_radio = QRadioButton("Strength")
    s_radio.setChecked(True)
    wp_radio = QRadioButton("Weight progression")
    n_radio = QRadioButton("Nutrition")

    radio_layout.addWidget(s_radio)
    radio_layout.addWidget(wp_radio)
    radio_layout.addWidget(n_radio)
    
    qw_group.setLayout(radio_layout)
    qw_layout.addWidget(qw_group)

    u_layout = QHBoxLayout()
    units_layout = QVBoxLayout()
    units_group = QGroupBox("Units:")

    m_radio = QRadioButton("Metric")
    m_radio.setChecked(True)
    i_radio = QRadioButton("Imperial")

    units_layout.addWidget(m_radio)
    units_layout.addWidget(i_radio)

    units_group.setLayout(units_layout)
    u_layout.addWidget(units_group)

    grid.addLayout(title_layout, 0, 0, 1, 1)
    grid.addLayout(qw_layout, 0, 3, 1, 3)
    grid.addLayout(u_layout, 0, 7, 1, 1)
