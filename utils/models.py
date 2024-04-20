from pydantic import BaseModel
from typing import  Optional, List


class USDAFoodIngredient(BaseModel):
    fdc_id: int
    name: str
    nutrition_id: int
    energy: float
    unit: str 

from typing import  List
class Nutrition(BaseModel):
    fat: Optional[str] = None
    protein: Optional[str] = None
    carbohydrate: Optional[str] = None

class Recipe(BaseModel):
    id: str
    recipe_name:str
    ingredients: List[dict]
    directions: str
    nutrition: Nutrition
    total_calories_estimation: str  

class Recipes(BaseModel):
    recipes: List[Recipe] = []

class Ingredient(BaseModel):
    name: str
    quantity: str
    ner_name: str

class EnrichRecipe(BaseModel):
    id: str
    recipe_name:str
    ingredients: List[Ingredient]
    directions: str
    nutrition: Nutrition
    total_calories_estimation: str  

class EnrichRecipes(BaseModel):
    recipes: List[EnrichRecipe] = []

class IngredientWithEngergy(BaseModel):
    name: str
    quantity: str
    ner_name: str
    usda_food_ingredient:Optional[USDAFoodIngredient]=None

class EnrichRecipeWithEnergy(BaseModel):
    id: str
    recipe_name:str
    ingredients: List[IngredientWithEngergy]
    directions: str
    nutrition: Nutrition
    total_calories_estimation: str 

class EnrichRecipesWithEnergy(BaseModel):
    recipes: List[EnrichRecipeWithEnergy] = []

class IngredientUnitPortion(BaseModel):
    name: str
    clean_name: str
    quantity: str
    portion: str|float
    unit: str
    weight: float|str

class IngredientEnrich(BaseModel):
    recipe_id: int
    ingredient_unit_portion:List[IngredientUnitPortion]=[]

class IngredientsEnrich(BaseModel):
    ingredients:List[IngredientEnrich]=[]