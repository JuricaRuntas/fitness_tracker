import os
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont, QPixmap
from .spoonacular import FoodDatabase

path = os.path.abspath(os.path.dirname(__file__))
food_images_path = os.path.join(path, "food_images")

class FoodPanel(QWidget):
  def __init__(self, parent, food_id):
    super().__init__()
    self.api = FoodDatabase()
    self.food_info = self.api.food_info(food_id)
    self.nutrients = {nutrient["title"]: " ".join([str(nutrient["amount"]), nutrient["unit"]])
                      for nutrient in self.food_info["nutrition"]["nutrients"]}
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_left_section(), 0, 0)
    grid.addLayout(self.create_right_section(), 0, 1)
    self.setLayout(grid)

  def create_left_section(self):
    section_layout = QVBoxLayout()

    food_title = QLabel(self.food_info["name"].capitalize())
    food_title.setFont(QFont("Ariel", 25))
    
    food_image = QLabel()
    food_pixmap = QPixmap(os.path.join(food_images_path, self.food_info["image"]))
    food_image.setPixmap(food_pixmap)
    
    section_layout.addWidget(food_title)
    section_layout.addWidget(food_image)

    return section_layout

  def create_right_section(self):
    section_layout = QVBoxLayout()

    food_info_label = QLabel("*important food info*")
    food_info_label.setFont(QFont("Ariel", 25))

    graph = QLabel()
    graph.setStyleSheet("background-color: white;")
    graph_pixmap = QPixmap(os.path.join(path, "/chart_placeholder.png"))
    graph.setPixmap(graph_pixmap)

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

    section_layout.addWidget(food_info_label)
    section_layout.addWidget(graph)
    section_layout.addWidget(nutrition_table)
    
    return section_layout
