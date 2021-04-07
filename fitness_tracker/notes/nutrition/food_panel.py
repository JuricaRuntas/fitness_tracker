import os
from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QFrame, QVBoxLayout,
                             QTableWidget, QAbstractItemView, QTableWidgetItem,
                             QHeaderView, QHBoxLayout, QAbstractScrollArea)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from .spoonacular import FoodDatabase
from .macronutrients_graph import MacronutrientsGraph

path = os.path.abspath(os.path.dirname(__file__))
food_images_path = os.path.join(path, "food_images")

class FoodPanel(QWidget):
  def __init__(self, parent, food_id):
    super().__init__()
    self.api = FoodDatabase()
    self.food_info = self.api.food_info(food_id)
    self.food_name = self.food_info["name"]
    self.nutrients = {nutrient["title"]: " ".join([str(nutrient["amount"]), nutrient["unit"]])
                      for nutrient in self.food_info["nutrition"]["nutrients"]}
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")

  def create_panel(self):
    grid = QGridLayout()
    grid.addWidget(self.create_food_and_title(), 0, 0)
    grid.addWidget(self.create_food_info(), 1, 0)
    self.setLayout(grid)

  def create_food_and_title(self):
    frame = QFrame()

    section_layout = QVBoxLayout()
    section_layout.setAlignment(Qt.AlignCenter)

    food_title = QLabel(self.food_info["name"].capitalize())
    food_title.setFont(QFont("Ariel", 25))
    
    image_layout = QHBoxLayout()

    food_image = QLabel()
    food_pixmap = QPixmap(os.path.join(food_images_path, self.food_info["image"]))
    food_image.setPixmap(food_pixmap)
    
    nutrition_table = QTableWidget(15, 1)
    nutrition_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    nutrition_table.horizontalHeader().setVisible(False)
    nutrition_table.setStyleSheet("background-color:white;")
    amount = " ".join([str(self.food_info["amount"]), self.food_info["unit"]])
    nutrients = list(self.nutrients.keys())
    nutrient_values = list(self.nutrients.values())
    
    for i, nutrient in enumerate(nutrients):
      if nutrient == "Calories": nutrient += " (%s)" % amount
      nutrition_table.setVerticalHeaderItem(i, QTableWidgetItem(nutrient))
    
    for i, value in enumerate(nutrient_values):
      nutrition_table.setItem(i, 0, QTableWidgetItem(value))

    nutrition_table.resizeRowsToContents()
    nutrition_table.setFixedSize(300, 300)
    
    image_layout.addWidget(food_image)
    image_layout.addWidget(nutrition_table)

    section_layout.addWidget(food_title)
    section_layout.addLayout(image_layout)

    frame.setLayout(section_layout)
    
    return frame

  def create_food_info(self):
    frame = QFrame()
    section_layout = QVBoxLayout()
    section_layout.setAlignment(Qt.AlignCenter)

    macro_graph = MacronutrientsGraph(self.food_name, self.food_info["nutrition"]["nutrients"], self)

    section_layout.addWidget(macro_graph)
    
    frame.setLayout(section_layout)
    
    return frame
