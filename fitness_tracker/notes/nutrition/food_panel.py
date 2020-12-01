from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QTableWidget, QAbstractItemView, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QFileInfo

path = QFileInfo(__file__).absolutePath()

class FoodPanel(QWidget):
  def __init__(self, parent):
    super().__init__()
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_left_section(), 0, 0)
    grid.addLayout(self.create_right_section(), 0, 1)
    self.setLayout(grid)

  def create_left_section(self):
    section_layout = QVBoxLayout()

    food_title = QLabel("Scrambled Eggs")
    food_title.setFont(QFont("Ariel", 25))
    
    food_image = QLabel()
    food_pixmap = QPixmap("".join([path, "/placeholder_images/scrambled_eggs_2.jpg"]))
    food_image.setPixmap(food_pixmap)

    food_description = QLabel("""
                              <html><head/><body><p>Lorem ipsum dolor sit amet, consectetur.</p>
                              <p>Praesent laoreet rutrum odio eget convallis. </p>
                              <p>Etiam tristique imperdiet molestie. Donec</p><p>eu mattis odio euismod in. </p>
                              <p>Sed rutrum luctus ex, non vehicula elit facilisis vitae. </p>
                              <p>Maecenas sollicitudin mauris eu ultricies tincidunt. </p>
                              <p>Praesent laoreet velit et congue efficitur.</p></body></html> 
                              """)

    section_layout.addWidget(food_title)
    section_layout.addWidget(food_image)
    section_layout.addWidget(food_description)

    return section_layout

  def create_right_section(self):
    section_layout = QVBoxLayout()

    food_info_label = QLabel("High Protein")
    food_info_label.setFont(QFont("Ariel", 25))

    graph = QLabel()
    graph.setStyleSheet("background-color: white;")
    graph_pixmap = QPixmap("".join([path, "/placeholder_images/eggs_chart.png"]))
    graph.setPixmap(graph_pixmap)

    nutrition_table = QTableWidget(15, 1)
    nutrition_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    nutrition_table.horizontalHeader().setVisible(False)
    nutrition_table.setStyleSheet("background-color:white;")

    items = ["Calories", "Fat", "Saturated Fat", "Trans Fat",
             "Cholesterol", "Sodium", "Potassium", "Carbohydrates",
             "Dietary Fiber", "Sugars", "Protein", "Vitamin A",
             "Vitamin C", "Calcium", "Iron"]
    
    for i, item in enumerate(items):
      nutrition_table.setVerticalHeaderItem(i, QTableWidgetItem(item))

    section_layout.addWidget(food_info_label)
    section_layout.addWidget(graph)
    section_layout.addWidget(nutrition_table)
    
    return section_layout
