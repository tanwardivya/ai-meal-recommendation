# ai-meal-recommendation
- GPT4-1106 prompt instruction
```
You are helpful recipe assistant. You generate recipe in below format:
<recipe>
<recipe_name> {row['recipe_name']} </recipe_name>
<ingredients> {row['ingredients']} </ingredients>
<directions> {row['directions']} </directions>
<nutrition> {row['nutrition']} </nutrition> 
</recipe>
Always use above format to give recipe.
```

- Steps followed for experiment:
    - Extract recipes names from dataset
    - Generate recipes from GPT4 model
    - Convert recipe into json format
    - Generate embeddings for ingredients and directions
    - cpmpared original directions and ingredients from the generated directions and ingredients from the GPT model from cosine similarity 
    - calculated the calories from the original recipe and generated recipe from GPT4 