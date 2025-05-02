## Functional Requirements

### FR-01: Search Recipe by Name
**Description**: The system must allow users to search for recipes by providing a name or part of a name. The search should return a list of matching recipes.
**Related Endpoint**: `GET /recipes?name=...` *(not implemented in your current OpenAPI, but could be added later)*

---

### FR-02: Filter Recipes by Preparation Time
**Description**: The system must allow users to filter recipes based on the maximum allowed preparation time (in minutes).
**Related Endpoint**: `GET /recipes?maxTime=...`

---

### FR-03: View Detailed Recipe Information
**Description**: The system must allow users to retrieve full details of a specific recipe, including ingredients, steps, preparation time, cuisine, and meal type.
**Related Endpoint**: `GET /recipes/{id}`

---

### FR-04: Suggest Recipes
**Description**: The system must provide smart recipe suggestions based on available ingredients, time, cuisine, and meal type. The suggestions should include a match score and missing ingredients.
**Related Endpoint**: `POST /suggest`

---

### FR-05: Add New Recipe
**Description**: The system must allow users to create and submit new recipes, including name, ingredients, preparation steps, time, cuisine, and meal type.
**Related Endpoint**: `POST /recipes`

---

### FR-06: Get Available Ingredients
**Description**: The system must provide a list of available ingredients that can be used for filtering or for creating new recipes.
**Related Endpoint**: `GET /ingredients`


## Application Architecture

The application consists of the following main components:

- **API Gateway**: Receives and routes all external HTTP requests to internal services.
- **Change/Update Service**: Service responsible for handling editions of the dataset, including adding new recipes and ingredients.
- **Search Service**: Service responsible for searching and filtering recipes based on user queries.
- **Recommendation Service**: Service responsible for providing recipe suggestions based on user preferences and available ingredients.
- **Database**: Stores all recipes, ingredients, and user interactions.
- **Load Balancer**: feature of using kubernetes to balance the load between multiple instances of the API Gateway and other services.


All communication is done through HTTP using REST principles. Data is exchanged in a JSON format.
Not all ports are exposed to the public internet.