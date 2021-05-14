import string
import json
import re
import os
from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QFont, QCursor, QFontDatabase, QImage, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from fitness_tracker.database_wrapper import DatabaseWrapper
import sys

icon_path = os.path.join(os.path.dirname(__file__), os.path.pardir, "icons", "ftarizonacalligraphy.png")
if getattr(sys, 'frozen', False):
    icon_path = os.path.join(os.path.dirname(sys.executable), "icons", "ftarizonacalligraphy.png")

class MainPanel(QWidget):
  emit_layout_name = pyqtSignal(str)

  def __init__(self, parent):
    super().__init__(parent)
    self.db_wrapper = DatabaseWrapper()
    self.setStyleSheet("""
    QWidget{
      background-position: center;
      color: #D9D9D9;
      font-family: Montserrat;
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
    title_layout.setAlignment(Qt.AlignCenter)
    signup_label = QLabel()
    pixmap = QPixmap(icon_path)
    signup_label.setPixmap(pixmap)
    signup_label.setAlignment(Qt.AlignCenter)
    #signup_label.setStyleSheet("font-size: 48px;")
    #signup_label.setFont(QFont("Cantonese"))
    #signup_label.setFixedHeight(70)

    title_layout.addWidget(signup_label)
    title_frame.setLayout(title_layout)

    signup_frame = QFrame()

    form_layout = self.create_form_layout()
    form_layout.setAlignment(Qt.AlignCenter)
    signup_frame.setLayout(form_layout)

    wrapper_layout = QVBoxLayout()
    wrapper_layout.setAlignment(Qt.AlignCenter)
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(signup_frame)
    return wrapper_layout

  def create_form_layout(self):
    form_layout = QFormLayout()
    form_layout.setFormAlignment(Qt.AlignCenter)

    sign_up_label = QLabel("Sign Up")
    sign_up_label.setAlignment(Qt.AlignCenter)
    sign_up_label.setFixedSize(115, 30) 

    self.login_button = QPushButton("Sign In", self)
    self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.login_button.clicked.connect(lambda: self.emit_layout_name.emit("Login"))
    self.login_button.setFixedSize(115, 30)

    self.email_entry = QLineEdit()
    self.email_entry.setPlaceholderText("Email")
    self.email_entry.setFixedSize(300, 30)
    
    self.password_entry = QLineEdit()
    self.password_entry.setPlaceholderText("Password")
    self.password_entry.setFixedSize(300, 30)
    self.password_entry.setEchoMode(QLineEdit.Password)

    self.confirm_password_entry = QLineEdit()
    self.confirm_password_entry.setPlaceholderText("Confirm Password")
    self.confirm_password_entry.setEchoMode(QLineEdit.Password)
    self.confirm_password_entry.setFixedSize(300, 30)
    
    self.continue_button = QPushButton("Continue", self)
    self.continue_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.continue_button.clicked.connect(lambda: self.continue_signup())
    self.continue_button.setFixedSize(300, 30)
    
    form_layout.addRow(self.login_button, sign_up_label)
    form_layout.addRow(self.email_entry)
    form_layout.addRow(self.password_entry)
    form_layout.addRow(self.confirm_password_entry)
    form_layout.addRow(self.continue_button)
    return form_layout

  def check_valid_email(self, email):
    # basic validation, checks for example@gmail.com and similar format
    # for real validation, email confirmation is needed
    email_regex = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,6}$")
    return not re.match(email_regex, email) == None
 
  def check_valid_password(self, password):
    valid = True
    valid_characters = set(string.ascii_letters + string.digits + '@#$%^&+=')
    if (len(password) < 8):
      valid = False
      print("Password is too short.")
    elif any(char not in valid_characters for char in password):
      valid = False
      print("Password contains invalid characters.")
    return valid
  
  def continue_signup(self):
    email = self.email_entry.text()
    password = self.password_entry.text()
    confirmed_password = self.confirm_password_entry.text()
    if (password == confirmed_password and self.check_valid_password(password)
        and self.check_valid_email(email) and self.db_wrapper.connection_exists):
      if not self.db_wrapper.check_user_exists(email):
        self.emit_layout_name.emit(json.dumps(["Continue", email, password]))
