from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal
from .login_helpers import check_password, fetch_user_info

class MainPanel(QWidget):
  emit_layout_name = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_login(), 0, 0, 1, 1)
    self.setLayout(grid)

  def create_login(self):
    title_frame = QFrame()
    title_layout = QVBoxLayout()

    login_label = QLabel("Login", self)
    login_label.setFont(QFont("Ariel", 15))
    login_label.setFixedHeight(70)

    title_layout.addWidget(login_label)
    title_frame.setLayout(title_layout)

    login_frame = QFrame()
    login_frame.setFrameStyle(QFrame.StyledPanel)

    form_layout = self.create_form_layout()
    login_frame.setLayout(form_layout)

    wrapper_layout = QVBoxLayout()
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(login_frame)
    return wrapper_layout

  def create_form_layout(self):
    form_layout = QFormLayout()

    email_label = QLabel("Email", self)
    self.email_entry = QLineEdit()
    
    password_label = QLabel("Password", self)
    self.password_entry = QLineEdit()
    self.password_entry.setEchoMode(QLineEdit.Password)
    
    self.login_button = QPushButton("Login", self)
    self.login_button.clicked.connect(lambda: self.login())
    self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
    
    signup_label = QLabel("Don't have an account?")
    self.signup_button = QPushButton("Signup", self)
    self.signup_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.signup_button.clicked.connect(lambda: self.emit_layout_name.emit(self.signup_button.text()))

    form_layout.addRow(email_label, self.email_entry)
    form_layout.addRow(password_label, self.password_entry)
    form_layout.addRow(self.login_button)
    form_layout.addRow(signup_label, self.signup_button)
    return form_layout

  def login(self):
    email = self.email_entry.text()
    password = self.password_entry.text()
    if check_password(email, password):
      fetch_user_info(email, password)
      self.emit_layout_name.emit("Home")