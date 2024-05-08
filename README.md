## AI MEAL RECOMMENDATION

This project is submmitted as part of course CPSC-597 Project. In this project, we focus into three areas:

    1. Quantative Evaluation of AI generated recipes
    2. Frontend ReactJS based application
    3. Backend FastAPI based service


### Quantative Evaluation of AI generated recipes

 <table style="border: 1px solid white;">
  <tr>
    <th style="border: 1px solid white;">Experiment</th>
    <th style="border: 1px solid white;">Notebook Link</th>
  </tr>
  <tr>
    <td style="border: 1px solid white;">Recipe Comparison</td>
    <td style="border: 1px solid white;"><a href="notebooks/gpt4_1106_recipe_diabetic.ipynb">Notebook</a></td>
  </tr>
  <tr>
    <td style="border: 1px solid white;">Recipe Authenticity</td>
    <td style="border: 1px solid white;"><a href="notebooks/gpt_authenticity_recipe_scrapped_data.ipynb">Notebook</a></td>
  </tr>
  <tr>
    <td style="border: 1px solid white;">Recipe Total Calories Estimation</td>
    <td style="border: 1px solid white;"><a href="notebooks/gpt4_turbo_recipe_generation.ipynb">Notebook1</a>, <a href="notebooks/gpt4_turbo_recipe_aggregation.ipynb">Notebook2</a>, <a href="notebooks/total_calorie_estimation.ipynb">Notebook3</a></td>
  </tr>
 </table>

### Frontend ReactJS based application

#### Prerequisite
- NodeJS 18.2.0
- OS(Mac, Ubuntu)

#### Install
```bash
cd frontend
npm install
```

#### Run application
```bash
npm run dev
```
#### Docker Build
```docker
docker build . -t divyatanwar/agent:recipe-assistant-frontend --no-cache
```

#### Docker Run
```docker
docker run --detach --publish 8080:8080 divyatanwar/agent:recipe-assistant-frontend
```

#### Azure Container Apps Deployment
```az
az login
az add extension containerapp
export RESOURCE_GROUP='<RESOURCE_GROUP>' 
export LOCATION='<LOCATION>'
export CONTAINERAPPS_ENVIRONMENT='<CONTAINERAPPS_ENVIRONMENT>'
az containerapp up \  --name recipe-agent-frontend \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINERAPPS_ENVIRONMENT \
  --image divyatanwar/agent:recipe-assistant-frontend \
  --target-port 8080 \
  --ingress 'external' \
  --query properties.configuration.ingress.fqdn
```

### Backend FastAPI based service

#### Prerequisite
- Python 3.11
- OS(Mac, Ubuntu)
- Docker
- Azure CLI
- Azure Account
- OpenAI API Key
- USDA Food API Key
- Mongo DB Atlas Account Key
- Postman(Optional)

#### Install
Install prerequisites mentioned above
```bash
cd backend/recipe-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

#### Run application
```bash
./scripts/run.sh
```

#### Docker build
```docker
docker build --tag divyatanwar/agent:recipe-assistant .           
```

#### Docker Run
```docker
docker run --detach --publish 3100:3100 --env-file ../../.vscode/.env  divyatanwar/agent:recipe-assistant
```

#### Azure Container App Deployment
```az
az login
az add extension containerapp
export RESOURCE_GROUP='<RESOURCE_GROUP>' 
export LOCATION='<LOCATION>'
export CONTAINERAPPS_ENVIRONMENT='<CONTAINERAPPS_ENVIRONMENT>'
az containerapp create \
  --name recipe-agent-app \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINERAPPS_ENVIRONMENT \
  --image divyatanwar/agent:recipe-assistant \
  --target-port 3100 \
  --ingress 'external' \
  --query properties.configuration.ingress.fqdn \
  --env-vars 'OPENAI_API_KEY'='<OPENAI_API_KEY>' 'JWT_SECRET'='<JWT_SECRET>' 'MONGODB_CONNECTION_STRING'='<MONGODB_CONNECTION_STRING>' 'OPENAI_MODEL_NAME'='gpt-4-turbo-2024-04-09'
```