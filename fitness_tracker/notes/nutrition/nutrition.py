from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from .notes_panel import NotesPanel
from .food_database_panel import FoodDatabasePanel
from .search_results_panel import SearchResultsPanel
from .food_panel import FoodPanel
from fitness_tracker.homepage.side_panel import SidePanel
from .header import Header

class NutritionNotes(QWidget):
  display_layout_signal = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    self.notes_panel = NotesPanel(self)
    self.header = Header(self)
    self.side_panel = SidePanel(self)
    self.side_panel.emit_layout_name.connect(lambda layout_name: self.emit_display_layout_signal(layout_name))
    self.create_grid()
    self.header.change_layout_signal.connect(lambda name: self.change_layout(name))
       
  def create_grid(self):
    self.grid = QGridLayout()
    self.grid.setContentsMargins(0, 0, 0, 0)
    self.grid.addWidget(self.side_panel, 0, 0, 1, 1)
    #self.grid.addWidget(self.header, 0, 1, 1, 2)
    self.grid.addWidget(self.notes_panel, 0, 1, 1, 1)
    self.setLayout(self.grid)
  
  @pyqtSlot(str)
  def emit_display_layout_signal(self, layout_name):
    self.display_layout_signal.emit(layout_name)
  
  @pyqtSlot(str)
  def change_layout(self, name):
    grid_items = list(reversed([type(self.grid.itemAt(i).widget()).__name__ for i in reversed(range(self.grid.count()))]))
    if name == "Food Database" and not "FoodDatabasePanel" in grid_items or name == "Return to FoodDatabase":
      if "NotesPanel" in grid_items or "SearchResultsPanel" in grid_items or "FoodPanel" in grid_items:
        self.grid.itemAt(2).widget().setParent(None)
        self.food_database_panel = FoodDatabasePanel(self)
        self.food_database_panel.emit_search_results.connect(lambda search_results: self.save_search_results(search_results))
        self.food_database_panel.search_signal.connect(lambda name: self.change_layout(name))
        self.grid.addWidget(self.food_database_panel, 1, 1, 8, 3)
        self.header.set_current_layout_button(name)

    elif name == "Notes" and not "NotesPanel" in grid_items:
      if "FoodDatabasePanel" in grid_items or "SearchResultsPanel" in grid_items or "FoodPanel" in grid_items:
       self.grid.itemAt(2).widget().setParent(None)
       self.grid.addWidget(self.notes_panel, 1, 1, 8, 3)
       self.header.set_current_layout_button(name)

    elif name == "Search" and "FoodDatabasePanel" in grid_items:
      self.grid.itemAt(2).widget().setParent(None)  
      self.search_results_panel = SearchResultsPanel(self, self.search_results)
      self.search_results_panel.return_to_food_db_signal.connect(lambda name: self.change_layout(name))
      self.search_results_panel.food_panel_signal.connect(lambda food_id: self.show_food_panel(food_id))
      self.grid.addWidget(self.search_results_panel, 1, 1, 8, 3)
  
  @pyqtSlot(object)
  def save_search_results(self, search_results):
    self.search_results = search_results

  @pyqtSlot(int)
  def show_food_panel(self, food_id):
    self.grid.itemAt(2).widget().setParent(None)
    self.food_panel = FoodPanel(self, food_id)
    self.grid.addWidget(self.food_panel, 1, 1, 8, 3)
