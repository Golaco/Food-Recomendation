# Functional Requirements

## 1. Retrieve a list of recipes
- Endpoint: `GET /recipes`
- Description: Fetches recipes, optionally filtered by ingredients, maximum preparation time, cuisine type, and meal type.
- Query Parameters:
  - `ingredients`: comma-separated list of ingredients (optional)
  - `maxTime`: maximum preparation time in minutes (optional)
  - `cuisine`: cuisine type, e.g., Italian, Chinese (optional)
  - `mealType`: meal type, e.g., breakfast, dinner (optional)

## 2. Retrieve recipe details
- Endpoint: `GET /recipes/{recipe_id}`
- Description: Retrieves detailed information of a recipe given its ID.

## 3. Add a new recipe
- Endpoint: `POST /recipes`
- Description: Adds a new recipe to the database.
- Body Parameters:
  - `name`: name of the recipe
  - `ingredients`: list of ingredients
  - `steps`: list of preparation steps
  - `time`: estimated time (minutes)
  - `cuisine`: type of cuisine
  - `mealType`: type of meal

## 4. Get list of available cuisines
- Endpoint: `GET /cuisines`
- Description: Fetches the list of available cuisines in the database.

## 5. Get list of available meal types
- Endpoint: `GET /meal-types`
- Description: Fetches the list of available meal types.

## 6. Get list of available ingredients
- Endpoint: `GET /ingredients`
- Description: Fetches the list of ingredients available for recipe creation or filtering.

## 7. Suggest recipes based on smart filters
- Endpoint: `POST /suggest`
- Description: Suggests recipes that match the user's available ingredients, preferred cuisine, meal type, and preparation time.
- Body Parameters:
  - `ingredients`: list of available ingredients
  - `maxTime`: maximum preparation time (optional)
  - `cuisine`: preferred cuisine (optional)
  - `mealType`: preferred meal type (optional)
