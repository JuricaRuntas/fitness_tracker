import json
import matplotlib
from fitness_tracker.notes.big_lifts.big_lifts_db import fetch_user_rm_history, fetch_preferred_lifts
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy

class OneRMGraphCanvas(FigureCanvas):
  def __init__(self, lift_type, rm_history, year, parent=None, width=5, height=4, dpi=100):
    assert lift_type in ["Horizontal Press", "Floor Pull", "Squat", "Vertical Press"], "Invalid lift type: '%s'" % lift_type
    self.lift_type = lift_type
    self.rm_history = rm_history
    self.year = year
    
    fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
    FigureCanvas.__init__(self, fig)
    
    self.axes = fig.subplots(nrows=1, ncols=1)
    self.create_figure()
    self.set_parent = parent
    FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)
  
  def create_figure(self):
    self.parsed_exercises = self.parse_data()
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    self.axes.plot(months, self.parsed_exercises[self.preferred_lifts[self.lift_type]], marker='o')
    self.axes.set_yticks(self.parsed_exercises[self.preferred_lifts[self.lift_type]])
    for label in self.axes.get_xticklabels():
      label.set_rotation(45)
    self.axes.grid()
    self.axes.set_title(self.preferred_lifts[self.lift_type])
     
  def parse_data(self):
    self.preferred_lifts = json.loads(fetch_preferred_lifts())
    parsed_exercises = {self.preferred_lifts["Horizontal Press"]: [], self.preferred_lifts["Floor Pull"]: [],
                        self.preferred_lifts["Squat"]: [], self.preferred_lifts["Vertical Press"]: []}

    horizontal_press = self.preferred_lifts["Horizontal Press"]
    floor_pull = self.preferred_lifts["Floor Pull"]
    squat = self.preferred_lifts["Squat"]
    vertical_press = self.preferred_lifts["Vertical Press"]

    for month in self.rm_history[self.year]:
      current_month = self.rm_history[self.year][month]
      horizontal_press_values = list(map(float, current_month["Horizontal Press"][horizontal_press]))
      floor_pull_values = list(map(float, current_month["Floor Pull"][floor_pull]))
      squat_values = list(map(float, current_month["Squat"][squat]))
      vertical_press_values = list(map(float, current_month["Vertical Press"][vertical_press]))

      max_horizontal_press = max(horizontal_press_values) if len(horizontal_press_values) >= 1 else 0
      max_floor_pull = max(floor_pull_values) if len(floor_pull_values) >= 1 else 0
      max_squat = max(squat_values) if len(squat_values) >= 1 else 0
      max_vertical_press = max(vertical_press_values) if len(vertical_press_values) >= 1 else 0

      parsed_exercises[horizontal_press].append(max_horizontal_press)
      parsed_exercises[floor_pull].append(max_floor_pull)
      parsed_exercises[squat].append(max_squat)
      parsed_exercises[vertical_press].append(max_vertical_press)
  
    return parsed_exercises
