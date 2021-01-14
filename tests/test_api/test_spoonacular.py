import unittest
from fitness_tracker.notes.nutrition.spoonacular import Spoonacular

API_KEY = "a81edb3273024befa02bf3e368f60246"

class TestSpoonacular(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.api = Spoonacular(API_KEY)
    cls.err_msg = "Response status != 200"
  
  def test_complex_recipe_search(self):
    query = "pasta"
    params = {"maxFat": 25, "number": 2}
    result = self.api.complex_recipe_search(query, **params)
    self.assertEqual(result.status_code, 200, self.err_msg)
    
  def test_search_recipes_by_nutrients(self):
    params = {"minCarbs": 10, "maxCarbs": 50, "number": 2}
    result = self.api.search_recipes_by_nutrients(**params)
    self.assertEqual(result.status_code, 200, self.err_msg)

  def test_search_recipes_by_ingredients(self):
    ingredients = "apples, flour, sugar"
    params = {"number": 2}
    result = self.api.search_recipes_by_ingredients(ingredients, **params)
    self.assertEqual(result.status_code, 200, self.err_msg)

  def test_get_recipe_information(self):
    ID = 716429
    include_nutrition = False
    result = self.api.get_recipe_information(ID, include_nutrition)
    self.assertEqual(result.status_code, 200, self.err_msg)

  def test_get_similar_recipes(self):
    ID = 715538
    result = self.api.get_similar_recipes(ID)
    self.assertEqual(result.status_code, 200, self.err_msg)

  def test_autocomplete_recipe_search(self):
    query = "chick"
    number = 10
    result = self.api.autocomplete_recipe_search(query, number)
    self.assertEqual(result.status_code, 200, self.err_msg)

  def test_get_analyzed_recipe_instructions(self):
    ID = 324694
    result = self.api.get_analyzed_recipe_instructions(ID)
    self.assertEqual(result.status_code, 200, self.err_msg)

  def test_ingredient_search(self):
    query = "banan"
    number = 1
    result = self.api.ingredient_search(query, number)
    self.assertEqual(result.status_code, 200, self.err_msg)

  def test_get_ingredient_information(self):
    ID = 9266
    params = {"amount": 1, "unit": "g"}
    result = self.api.get_ingredient_information(ID, **params)
    self.assertEqual(result.status_code, 200, self.err_msg)
    
  def test_generate_meal_plan(self):
    params = {"timeFrame": "day"}
    result = self.api.generate_meal_plan(**params)
    self.assertEqual(result.status_code, 200, self.err_msg)

if __name__ == "__main__":
  unittest.main()
