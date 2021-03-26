import json
import matplotlib
from calendar import monthrange
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy
from fitness_tracker.database_wrapper import DatabaseWrapper

class WeightLossGraphCanvas(FigureCanvas):
  def __init__(self, month, year, parent=None, width=5, height=4, dpi=100):
    figure = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
    FigureCanvas.__init__(self, figure)
    self.current_month = month
    self.current_year = year
    self.set_parent = parent
    self.db_wrapper = DatabaseWrapper()
    self.weight_history = json.loads(self.db_wrapper.fetch_local_column("Weight Loss", "weight_history"))

    self.axes = figure.subplots(nrows=1, ncols=1)
    self.create_figure()
    FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)
  
  def create_figure(self):
    self.parsed_weight_entries = self.parse_weight_history()
    days_in_a_month = [monthrange(int(self.current_year), month)[1] for month in range(1, 13)]
    self.axes.plot(self.parsed_weight_entries, marker='o')
    days = list(range(1, days_in_a_month[list(self.db_wrapper.months_mappings.keys()).index(self.current_month)]))
    self.axes.set_xticks(days)
    self.axes.set_yticks(self.parsed_weight_entries)
    self.axes.grid(self.current_month)
    self.axes.set_title(self.current_month)

  def parse_weight_history(self):
    weights = []
    for entry in self.weight_history:
      entry = entry.split("/")
      if entry[1] == self.db_wrapper.months_mappings[self.current_month] and entry[2] == str(self.current_year):
        weights.append(float(self.weight_history["/".join(entry)])) 
    return weights
