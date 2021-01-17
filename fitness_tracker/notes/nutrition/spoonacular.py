import requests
import os
import shutil

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
  
  def ingredient_search(self, query, number, intolerances=None, meta=True):
    endpoint = "food/ingredients/autocomplete"
    params = {"query": query, "number": number,
              "metaInformation": meta, "intolerances": intolerances}
    return self.make_request(endpoint, params)

  def get_ingredient_information(self, ID, amount, unit):
    endpoint = "food/ingredients/{ID}/information".format(ID=ID)
    params = {"amount": amount, "unit": unit}
    return self.make_request(endpoint, params)

  def generate_meal_plan(self, **kwargs):
    endpoint = "mealplanner/generate"
    params = {**kwargs}
    return self.make_request(endpoint, params)

class FoodDatabase(Spoonacular):
  def __init__(self, api_key=os.environ["SPOONACULAR_API_KEY"]):
    Spoonacular.__init__(self, api_key)

  def food_search(self, food, number, intolerances=None):
    results = self.ingredient_search(food, number, intolerances).json()
    search_results = [{"id": food["id"], "name": food["name"], "image": food["image"]} for food in results]
    return search_results

  def food_info(self, food_id, units="g", amount=100):
    results = self.get_ingredient_information(food_id, amount, units).json()
    info = {"name": results["name"], "amount": results["amount"],
            "unit": results["unit"], "image": results["image"],
            "nutrition": results["nutrition"]}
    return info

  def download_food_images(self, search_results, size):
    assert size == 100 or size == 250 or size == 500, "invalid size, valid image sizes are 100, 250 and 500"
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "food_images")
    size = str(size) + "x" + str(size)
    download_url = "https://spoonacular.com/cdn/ingredients_{size}/".format(size=size)
    if not os.path.isdir(path): os.makedirs(path)
    for food in search_results:
      if os.path.isfile(os.path.join(path, food["image"])): continue
      download = requests.get(download_url+food["image"], stream=True)
      if download.ok:
        with open(os.path.join(path, food["image"]), "wb") as img_file:
          download.raw.decode_content = True
          shutil.copyfileobj(download.raw, img_file)
        
class RecipeDatabase(Spoonacular):
  pass
