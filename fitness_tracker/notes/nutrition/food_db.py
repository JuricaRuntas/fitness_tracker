from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from fitness_tracker.homepage.side_panel import SidePanel
from .food_database_panel import FoodDatabasePanel
from .search_results_panel import SearchResultsPanel
from .food_panel import FoodPanel

class FoodDB(QWidget):
  display_layout_signal = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    self.side_panel = SidePanel(self)
    self.side_panel.emit_layout_name.connect(lambda layout_name: self.emit_display_layout_signal(layout_name))
    self.create_grid()

  def create_grid(self):
    self.main_panel = FoodDatabasePanel(self)
    self.main_panel.search_signal.connect(lambda search: self.show_search_results(search))
    self.grid = QGridLayout()
    self.grid.setContentsMargins(0, 0, 0, 0)
    self.grid.addWidget(self.side_panel, 1, 0, 8, 1)
    self.grid.addWidget(self.main_panel, 1, 1, 8, 3)
    self.setLayout(self.grid)

  @pyqtSlot(str)
  def emit_display_layout_signal(self, layout_name):
    self.display_layout_signal.emit(layout_name)
  
  @pyqtSlot(object)
  def show_search_results(self, search_results):
    old_main_panel_reference = self.grid.itemAt(1).widget() 
    self.search_results_panel = SearchResultsPanel(self, search_results)
    self.search_results_panel.return_to_food_db_signal.connect(lambda signal: self.show_main_panel(signal))
    self.search_results_panel.food_panel_signal.connect(lambda food_id: self.show_food_panel(food_id))
    self.grid.replaceWidget(old_main_panel_reference, self.search_results_panel)
    self.main_panel.deleteLater()

  @pyqtSlot(str)
  def show_main_panel(self, signal):
    if signal:
      old_main_panel_reference = self.grid.itemAt(1).widget() 
      main_panel = FoodDatabase(self)
      main_panel.search_signal.connect(lambda search: self.show_search_results(search))
      self.grid.replaceWidget(old_main_panel_reference, main_panel)

  @pyqtSlot(int)
  def show_food_panel(self, food_id):
    old_main_panel_reference = self.grid.itemAt(1).widget() 
    food_panel = FoodPanel(self, food_id)
    self.grid.replaceWidget(old_main_panel_reference, food_panel)
    self.search_results_panel.deleteLater()
