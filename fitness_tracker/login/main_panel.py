from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QVBoxLayout, QFormLayout, QLineEdit,
                             QLabel, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal
from .login_helpers import check_password, fetch_user_info

class MainPanel(QWidget):
  emit_layout_name = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    self.setStyleSheet("""
    QWidget{
      background-position: center;
      font-family: Montserrat;
      color: #D9D9D9;
      font-size: 14px;
    }
    QPushButton{
      border-radius: 1px;
      background-color: #440D0F;
    }
    QPushButton:hover:!pressed{
      background-color: #5D1A1D
    }
    QPushButton:pressed{
      background-color: #551812
    }    
    QLineEdit{
      padding: 6px;
      background-color: rgb(33,33,33);
      border-radius: 2px;
    }
    """)
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.setContentsMargins(0, 0, 0, 0)
    grid.addLayout(self.create_login(), 0, 0, 1, 1)
    self.setLayout(grid)

  def create_login(self):
    title_frame = QFrame()
    title_layout = QVBoxLayout()

    #TEMP USED AS LOGO
    login_label = QLabel("ft", self)

    login_label.setAlignment(Qt.AlignCenter)
    login_label.setStyleSheet("font-size: 48px;")

    title_layout.addWidget(login_label)
    title_frame.setLayout(title_layout)

    form_layout = self.create_form_layout()

    wrapper_layout = QVBoxLayout()
    wrapper_vspacer = QSpacerItem(0, 150, QSizePolicy.Minimum, QSizePolicy.Expanding)
    wrapper_titleform_spacer = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
    wrapper_layout.setAlignment(Qt.AlignCenter)
    wrapper_layout.addItem(wrapper_vspacer)
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addItem(wrapper_titleform_spacer)
    wrapper_layout.addLayout(form_layout)
    wrapper_layout.addStretch(1)

    return wrapper_layout

  def create_form_layout(self):
    self.setContentsMargins(0,0,0,0)
    form_layout = QFormLayout()
    form_layout.setFormAlignment(Qt.AlignCenter)

    sign_in_label = QLabel("Sign In")
    sign_in_label.setAlignment(Qt.AlignCenter)
    sign_in_label.setFixedSize(115, 30)

    self.signup_button = QPushButton("Signup", self)
    self.signup_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.signup_button.clicked.connect(lambda: self.emit_layout_name.emit(self.signup_button.text()))
    self.signup_button.setFixedSize(115, 30)
     
    self.email_entry = QLineEdit()
    self.email_entry.setPlaceholderText("Email")
    self.email_entry.setFixedSize(300, 30)
    
    self.password_entry = QLineEdit()
    self.password_entry.setPlaceholderText("Password")
    self.password_entry.setEchoMode(QLineEdit.Password)
    self.password_entry.setFixedSize(300, 30)

    self.forgot_button = QPushButton("Forgot password?")
    self.forgot_button.setStyleSheet("""""")
    self.forgot_button.setFixedSize(134, 20)
    self.forgot_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.forgot_button.setStyleSheet("""
      background-color: rgba(255, 255, 255, 0);
      text-align: left;
      padding-left: 2%
    """)
    
    self.login_button = QPushButton("Login", self)
    self.login_button.clicked.connect(lambda: self.login())
    self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.login_button.setFixedSize(300, 30)
    self.login_button.frameGeometry().center()

    form_layout.addRow(sign_in_label, self.signup_button)
    form_layout.addRow(self.email_entry)
    form_layout.addRow(self.password_entry)
    form_layout.addRow(self.login_button)
    form_layout.addRow(self.forgot_button)

    return form_layout

  def login(self):
    email = self.email_entry.text()
    password = self.password_entry.text()
    if check_password(email, password):
      fetch_user_info(email, password)
      self.emit_layout_name.emit("Home")
