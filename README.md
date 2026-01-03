## AI MEAL RECOMMENDATION

This project is submitted as part of course CPSC-597 Project. In this project, we focus into three areas:

1. Quantitative Evaluation of AI generated recipes
2. Frontend ReactJS based application
3. Backend FastAPI based service

### Quantitative Evaluation of AI generated recipes

| Experiment                       | Notebook Link |
|----------------------------------|---------------|
| Recipe Comparison                | [Notebook](./notebooks/gpt4_1106_recipe_diabetic.ipynb) |
| Recipe Authenticity              | [Notebook](./notebooks/gpt_authenticity_recipe_scrapped_data.ipynb) |
| Recipe Total Calories Estimation | [Notebook1](./notebooks/gpt4_turbo_recipe_generation.ipynb), [Notebook2](./notebooks/gpt4_turbo_recipe_aggregation.ipynb), [Notebook3](./notebooks/total_calorie_estimation.ipynb) |

---

## Frontend ReactJS Application

### Local Development

#### Prerequisites
- NodeJS 18.2.0+
- OS (Mac, Ubuntu)

#### Install
```bash
cd frontend
npm install
```

#### Run Application
```bash
npm run dev
```

#### Docker Build
```bash
docker build . -t divyatanwar/agent:recipe-assistant-frontend --no-cache
```

#### Docker Run
```bash
docker run --detach --publish 8080:8080 divyatanwar/agent:recipe-assistant-frontend
```

### AWS Elastic Beanstalk Deployment

The frontend is deployed to AWS Elastic Beanstalk using Pulumi for infrastructure provisioning and GitHub Actions for CI/CD.

#### Architecture

- **Infrastructure as Code**: Pulumi (Python)
- **CI/CD**: GitHub Actions with OIDC authentication
- **Container Registry**: AWS ECR
- **Deployment Platform**: AWS Elastic Beanstalk (Docker platform)
- **Image Build**: Multi-stage Docker build (Node.js + Nginx)

#### Quick Start

1. **Initial Setup** (one-time):
   ```bash
   # Setup OIDC for GitHub Actions
   ./setup-oidc-role.sh
   
   # Add GitHub Secrets:
   # - AWS_ROLE_ARN (from setup script output)
   # - PULUMI_ACCESS_TOKEN
   # - ECR_REPO_NAME (optional, defaults to frontend-test)
   ```

2. **Initialize Pulumi Stacks**:
   ```bash
   cd infrastructure
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   
   # Initialize test stack
   pulumi stack init test
   
   # Initialize production stack (optional)
   pulumi stack init prod
   ```

3. **Deploy**:
   - **PR Workflow**: Automatically builds and pushes Docker images on PR creation/update
   - **Deploy Workflow**: Manually trigger from GitHub Actions to deploy to test/production

#### Deployment Workflows

**PR Workflow** (`build-frontend-pr.yml`):
- Triggers: PR opened/updated
- Actions:
  - Runs Pulumi preview
  - Builds Docker image
  - Pushes to ECR with tag: `pr-<PR_NUMBER>-<COMMIT_SHA>`
  - Comments on PR with image details

**Deploy Workflow** (`deploy-frontend-test.yml` / `deploy-frontend-prod.yml`):
- Triggers: Manual dispatch only
- Actions:
  - Refreshes Pulumi state
  - Creates/updates infrastructure (ECR, Elastic Beanstalk)
  - Reuses existing Docker image or builds new one
  - Deploys to Elastic Beanstalk environment

#### Infrastructure Components

- **ECR Repository**: Stores Docker images
- **Elastic Beanstalk Application**: Application container
- **Elastic Beanstalk Environment**: Running environment with:
  - Application Load Balancer
  - Auto Scaling Group
  - EC2 Instances (Docker platform)
  - CloudWatch alarms

#### Configuration

Stack configurations are in:
- `Pulumi.test.yaml` - Test environment
- `Pulumi.prod.yaml` - Production environment

Key settings:
- Instance type: `t3.small` (test), `t3.medium` (prod)
- Auto Scaling: Min 1, Max 2-4 instances
- Solution Stack: Dynamically detected (Docker on Amazon Linux 2)

#### Troubleshooting

**Failed Environment**:
```bash
# Clean up failed environment
./cleanup-failed-eb-env.sh frontend-test-env frontend-test us-east-1
```

**Update IAM Policy**:
```bash
# After updating frontend-iam-policy.json
./setup-oidc-role.sh
```

**Check Environment Status**:
```bash
aws elasticbeanstalk describe-environments \
  --environment-names frontend-test-env \
  --region us-east-1
```

#### Documentation

- [OIDC Setup Guide](./OIDC_SETUP.md) - Setting up GitHub Actions authentication
- [Pulumi Setup Guide](./INITIALIZE_PULUMI.md) - Initializing Pulumi stacks
- [Workflow Architecture](./WORKFLOW_ARCHITECTURE.md) - CI/CD workflow details

---

## Backend FastAPI Service

### Prerequisites
- Python 3.11
- OS (Mac, Ubuntu)
- Docker
- Azure CLI
- Azure Account
- OpenAI API Key
- USDA Food API Key
- MongoDB Atlas Account Key
- Postman (Optional)

### Install
```bash
cd backend/recipe-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Run Application
```bash
./scripts/run.sh
```

### Docker Build
```bash
docker build --tag divyatanwar/agent:recipe-assistant .
```

### Docker Run
```bash
docker run --detach --publish 3100:3100 --env-file ../../.vscode/.env divyatanwar/agent:recipe-assistant
```

### Azure Container App Deployment
```bash
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

---

## Project Structure

```
ai-meal-recommendation/
├── frontend/              # React frontend application
│   ├── src/              # Source code
│   ├── Dockerfile        # Multi-stage Docker build
│   └── README.md         # Frontend-specific docs
├── backend/              # FastAPI backend service
│   ├── recipe-assistant/ # Backend application
│   └── README.md         # Backend-specific docs
├── infrastructure/       # Pulumi infrastructure code
│   ├── components/       # Reusable Pulumi components
│   ├── config_types/     # Configuration dataclasses
│   └── __main__.py       # Main Pulumi program
├── notebooks/            # Jupyter notebooks for experiments
├── .github/workflows/    # GitHub Actions workflows
│   ├── build-frontend-pr.yml    # PR build workflow
│   ├── deploy-frontend-test.yml # Test deployment
│   └── deploy-frontend-prod.yml # Production deployment
├── setup-oidc-role.sh   # OIDC setup script
├── cleanup-failed-eb-env.sh # Environment cleanup script
└── README.md            # This file
```

---

## License

This project is part of CPSC-597 coursework.
