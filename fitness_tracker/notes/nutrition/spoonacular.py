import requests

API_KEY = "a81edb3273024befa02bf3e368f60246"

class Spoonacular:
  def __init__(self, api_key):
    self.base_api_url = "https://api.spoonacular.com/"
    self.api_key = api_key
  
  def make_request(self, path, params):
    uri = self.base_api_url + path
    params["apiKey"] = self.api_key
    request = requests.get(uri, params=params)
    return request

  def complex_recipe_search(self, query, **kwargs):
    endpoint = "recipes/complexSearch"
    params = {"query": query, **kwargs}
    return self.make_request(endpoint, params)

  def search_recipes_by_nutrients(self, **kwargs):
    endpoint = "recipes/findByNutrients"
    params = {**kwargs}
    return self.make_request(endpoint, params)

  def search_recipes_by_ingredients(self, ingredients, **kwargs):
    endpoint = "recipes/findByIngredients"
    params = {"ingredients": ingredients, **kwargs}
    return self.make_request(endpoint, params)

  def get_recipe_information(self, ID, include_nutrition):
    endpoint = "recipes/{ID}/information".format(ID=ID)
    params = {"includeNutrition": include_nutrition}
    return self.make_request(endpoint, params)

  def get_similar_recipes(self, ID, number=1):
    endpoint = "recipes/{ID}/similar".format(ID=ID)
    params = {"number": number}
    return self.make_request(endpoint, params)
    
  def autocomplete_recipe_search(self, query, number=1):
    endpoint = "recipes/autocomplete"
    params = {"query": query, "number": number}
    return self.make_request(endpoint, params)

  def get_analyzed_recipe_instructions(self, ID, stepBreakdown=False):
    endpoint = "recipes/{ID}/analyzedInstructions".format(ID=ID)
    params = {"stepBreakdown": stepBreakdown}
    return self.make_request(endpoint, params)
  
  def ingredient_search(self, query, **kwargs):
    endpoint = "food/ingredients/search"
    params = {"query": query, **kwargs}
    return self.make_request(endpoint, params)

  def get_ingredient_information(self, ID, **kwargs):
    endpoint = "food/ingredients/{ID}/information".format(ID=ID)
    params = {**kwargs}
    return self.make_request(endpoint, params)

  def autocomplete_ingredient_search(self, query, **kwargs):
    endpoint = "food/ingredients/autocomplete"
    params = {"query": query, **kwargs}
    return self.make_request(endpoint, params)

  def generate_meal_plan(self, **kwargs):
    endpoint = "mealplanner/generate"
    params = {**kwargs}
    return self.make_request(endpoint, params)

class FoodDatabase(Spoonacular):
  pass

class RecipeDatabase(Spoonacular):
  pass
