import requests

API_KEY = "a81edb3273024befa02bf3e368f60246"

class Spoonacular:
  def complex_recipe_search(self):
    """
    Search through hundreds of thousands of recipes using advanced filtering and ranking.
    https://spoonacular.com/food-api/docs#Search-Recipes-Complex
    """
    pass

  def search_recipes_by_nutrients(self):
    """
    Find a set of recipes that adhere to the given nutritional limits.
    You may set limits for macronutrients (calories, protein, fat, and carbohydrate) and/or many micronutrients.
    https://spoonacular.com/food-api/docs#Search-Recipes-by-Nutrients
    """
    pass

  def search_recipes_by_ingredients(self):
    """
    Ever wondered what recipes you can cook with the ingredients you have in your fridge or pantry?
    This endpoint lets you find recipes that either maximize the usage of 
    ingredients you have at hand (pre shopping) or minimize the ingredients that you don't currently have (post shopping).
    """
    pass

  def get_recipe_information(self):
    """
    Use a recipe id to get full information about a recipe, such as ingredients, nutrition, diet and allergen information, etc.
    https://spoonacular.com/food-api/docs#Get-Recipe-Information
    """
    pass
  
  def get_similar_recipes(self):
    """
    Find recipes which are similar to the given one.
    https://spoonacular.com/food-api/docs#Get-Similar-Recipes
    """
    pass
  
  def autocomplete_recipe_search(self):
    """
    Autocomplete a partial input to suggest possible recipe names.
    """
    pass
  
  def get_analyzed_recipe_instructions(self):
    """
    Get an analyzed breakdown of a recipe's instructions. Each step is enriched with the ingredients and equipment required.
    https://spoonacular.com/food-api/docs#Get-Analyzed-Recipe-Instructions
    """
    pass
  
  def ingredient_search(self):
    """
    Search for simple whole foods (e.g. fruits, vegetables, nuts, grains, meat, fish, dairy etc.).
    """
    pass

  def get_ingredient_information(self):
    """
    Get information about a certain food (ingredient)
    https://spoonacular.com/food-api/docs#Get-Ingredient-Information
    """
    pass
  
  def autocomplete_ingredient_search(self):
    """
    Autocomplete a search for an ingredient.
    https://spoonacular.com/food-api/docs#Autocomplete-Ingredient-Search
    """
    pass 
  
  def generate_meal_plan(self):
    """
    Generate a meal plan with three meals per day (breakfast, lunch and dinner).
    https://spoonacular.com/food-api/docs#Generate-meal-plan
    """
    pass

class FoodDatabase(Spoonacular):
  pass

class RecipeDatabase(Spoonacular):
  pass
