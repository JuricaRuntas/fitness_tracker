import requests
import os
import shutil

class WorkoutsAPI:
  def __init__(self):
    self.base_api_url = "https://wger.de/api/v2/"
    self.exercises_url = self.base_api_url + "exercise/"
    self.images_url = self.base_api_url + "exerciseimage/"
    self.exercise_info_url = self.base_api_url + "exerciseinfo/{ID}"
    self.language = 2 # English
    # exercise category: (exercise category id, [muscle group id])
    self.exercise_categories = {"Biceps": (8, [1, 13]), "Shoulders": (13, [2]),
                                "Chest": (11, [4]), "Triceps": (8, [5]),
                                "Legs": (9, [10, 11, 8]), "Calves": (14, [15, 7]),
                                "Back": (12, [12, 9]), "Core": (10, [6, 14, 3])}

    self.equipment = {"Barbell": 1, "EZ Bar": 2, "Dumbbell": 3, "Gym mat": 4,
                      "Swiss ball": 4, "Pull-up bar": 6, "Bodyweight": 7,
                      "Bench": 8, "Incline bench": 9, "Kettlebell": 10}
     
    self.muscle_category = {1: "Biceps brachii", 2: "Anterior deltoid",
                            3: "Serratus anterior", 4: "Pectoralis major",
                            5: "Triceps brachii", 6: "Rectus abdominis",
                            7: "Gastrocnemius", 8: "Gluteus maximus",
                            9: "Trapezius", 10: "Quadriceps femoris",
                            11: "Biceps femoris", 12: "Latissimus dorsi",
                            13: "Brachialis", 14: "Obliquus externus abdominis",
                            15: "Soleus"}
    
  def parse_exercises(self, fetched_exercises):
    parsed = []
    for exercise in fetched_exercises["results"]:
      parsed_exercise = {"exercise_id": exercise["id"], "category": exercise["category"],
                         "description": exercise["description"], "name": exercise["name"],
                         "equipment": exercise["equipment"]}
      if len(exercise["muscles"]) > 0 or len(exercise["muscles_secondary"]) > 0:
        primary, secondary = [], []
        for muscle_category in self.muscle_category:
          if muscle_category in exercise["muscles"]: primary.append(self.muscle_category[muscle_category])
          if muscle_category in exercise["muscles_secondary"]: secondary.append(self.muscle_category[muscle_category])
        parsed_exercise["muscles_primary"] = primary
        parsed_exercise["muscles_secondary"] = secondary
      if len(exercise["equipment"]) > 0:
        parsed_equipment = []
        for equipment in self.equipment:
          if self.equipment[equipment] in exercise["equipment"]: parsed_equipment.append(equipment)
        parsed_exercise["equipment"] = parsed_equipment
      parsed_exercise["image"] = self.fetch_images([parsed_exercise["exercise_id"]], single_image=True)
      fetch_comment = requests.get(url=self.exercise_info_url.format(ID=parsed_exercise["exercise_id"])).json()
      if len(fetch_comment["comments"]) > 0:
        parsed_exercise["comment"] = fetch_comment["comments"][0]["comment"]
      else:
        parsed_exercise["comment"] = []
      parsed.append(parsed_exercise)
    return parsed
   
  def fetch_exercises(self, exercise_category, equipment=None, limit=5, **kwargs):
    params = {"language": self.language, "muscles": self.exercise_categories[exercise_category][1],
              "category": self.exercise_categories[exercise_category][0], "limit": limit,
              **kwargs}
    if equipment != None:
      parse_equipment = []
      for i in equipment:
        parse_equipment.append(self.equipment[i])
      params["equipment"] = parse_equipment 
    fetched_exercises = requests.get(url=self.exercises_url, params=params).json()
    return self.parse_exercises(fetched_exercises)
  
  def fetch_images(self, exercises, single_image=False):
    urls = []
    params = {"is_main": True, "limit": 204}
    images = requests.get(self.images_url, params=params).json()
    if single_image: exercise_ids = exercises
    else: exercise_ids = [exercise["exercise_id"] for exercise in exercises]
    for exercise_id in exercise_ids:
      for image in images["results"]:
        if image["exercise"] == exercise_id:
          urls.append(image["image"])
    return urls

  def download_exercise_images(self, exercises):
    urls = self.fetch_images(exercises) 
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "exercises", "exercise_images")
    if not os.path.isdir(path): os.makedirs(path)
    for image in urls:
      image_name = os.path.basename(image)
      if os.path.isfile(os.path.join(path, image_name)): continue
      download = requests.get(image, stream=True)
      if download.ok:
        with open(os.path.join(path, image_name), "wb") as img_file:
          download.raw.deconde_content = True
          shutil.copyfileobj(download.raw, img_file)
