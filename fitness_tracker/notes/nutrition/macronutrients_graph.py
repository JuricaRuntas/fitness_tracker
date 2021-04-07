import json
import numpy as np
import matplotlib
from fitness_tracker.database_wrapper import DatabaseWrapper
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy

class MacronutrientsGraph(FigureCanvas):
  def __init__(self, food_name, food_nutrients, parent=None, width=5, height=4, dpi=100):
    fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
    FigureCanvas.__init__(self, fig)
    self.food_name = food_name.capitalize()
    self.food_info = food_nutrients
    del self.food_info[0] # remove calories
    self.axes = fig.subplots(nrows=1, ncols=1)
    self.create_figure()
    self.set_parent = parent
    FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

  def create_figure(self):
    parsed_macronutrients = self.parse_macronutrients()
    macro_n = parsed_macronutrients[0]
    macro_amounts = parsed_macronutrients[1]
    
    explode = [0]*len(macro_n)
    explode[np.argmax(macro_amounts)] = 0.05
    wedges, texts = self.axes.pie(macro_amounts, explode=np.array(explode), startangle=90, shadow=True)
    percentages = [round(macro/np.sum(macro_amounts)*100, 1) for macro in macro_amounts]

    percentage_label = "%s (%1.1f %%)"
    labels = [percentage_label % (macro, percentage) for (macro, percentage) in zip(macro_n, percentages)]
    for i, (wedge, label) in enumerate(zip(wedges, labels)):
      labels[i] = (wedge, label)

    labels.sort(key=lambda x: float(x[1].split(" ")[-2][1:]), reverse=True)

    sorted_wedges = [label[0] for label in labels]
    sorted_labels = [label[1] for label in labels]

    self.axes.legend(sorted_wedges, sorted_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    self.axes.set_title("Macronutrients")
 
  def parse_macronutrients(self):
    macronutrients_list = ["Fat", "Saturated Fat", "Carbohydrates",
                           "Net Carbohydrates", "Sugar", "Cholesterol", "Protein"]
    
    macro_n, macro_amounts = [], []
    
    for nutrient in self.food_info:
      if nutrient["title"] in macronutrients_list:
        macro_n.append(nutrient["title"])
        if nutrient["unit"] != "g" and nutrient["unit"] == "mg":
          nutrient_amount = nutrient["amount"] / 1000
        else:
          nutrient_amount = nutrient["amount"]
        macro_amounts.append(nutrient_amount)
   
    return [macro_n, macro_amounts]
