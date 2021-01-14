import unittest
import requests
from fitness_tracker.notes.workouts.workouts_api import WorkoutsAPI

class TestWorkoutsAPI(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.api = WorkoutsAPI()
    cls.err_msg = "Response status != 200"
    cls.exercises_url = "https://wger.de/api/v2/exercise/"
    # muscles: 4 -> Pectoralis major
    # category: 11 -> Chest
    # equipment: [1, 8, 9] -> barbell, bench, incline bench
    cls.params = {"language": 2, "muscles": 4,
                  "category": 11, "limit": 2,
                  "equipment": [1, 8, 9]}
  
  def setUp(self):
    fetch_exercises = requests.get(url=self.exercises_url, params=self.params)
    self.assertEqual(fetch_exercises.status_code, 200, self.err_msg)
    self.exercises = fetch_exercises.json()
  
  def test_parse_exercises(self):
    parsed = self.api.parse_exercises(self.exercises)
    
    for parsed_exercise in parsed:
      self.assertIn("exercise_id", parsed_exercise)
      self.assertIn("muscles_primary", parsed_exercise)
      self.assertIn("muscles_secondary", parsed_exercise)
      self.assertIn("muscles_primary", parsed_exercise)
      self.assertIn("equipment", parsed_exercise)
      self.assertIn("name", parsed_exercise)
      self.assertIn("description", parsed_exercise)
      self.assertIn("image", parsed_exercise)
      self.assertIn("comment", parsed_exercise)
      self.assertEqual(len(parsed_exercise), 9)
 
  def test_fetch_exercises(self):
    parsed = self.api.parse_exercises(self.exercises)
    exercises = self.api.fetch_exercises("Chest", equipment=["Barbell","Bench","Incline bench"],limit=2)
    for exercise in exercises:
      self.assertIn(exercise, parsed)
    self.assertEqual(parsed, exercises)

if __name__ == "__main__":
  unittest.main()
