# Initialize Pulumi Stacks

## Prerequisites

1. **Pulumi CLI installed**
   ```bash
   # Install if not already installed
   curl -fsSL https://get.pulumi.com | sh
   ```

2. **Logged into Pulumi**
   ```bash
   pulumi login
   ```

3. **Python virtual environment set up**
   ```bash
   cd infrastructure
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

## Initialize Test Stack

```bash
cd infrastructure
source .venv/bin/activate

# Initialize the test stack
pulumi stack init test

# The stack will use Pulumi.test.yaml for configuration
# Verify configuration
pulumi config

# Preview what will be created (without applying)
pulumi preview
```

## Initialize Production Stack

```bash
cd infrastructure
source .venv/bin/activate

# Initialize the production stack
pulumi stack init prod

# The stack will use Pulumi.prod.yaml for configuration
# Verify configuration
pulumi config

# Preview what will be created (without applying)
pulumi preview
```

## Select a Stack

To switch between stacks:

```bash
# Select test stack
pulumi stack select test

# Select production stack
pulumi stack select prod

# Check current stack
pulumi stack
```

## Verify Configuration

After initializing, verify the configuration matches your needs:

```bash
# List all configuration
pulumi config

# Get specific config value
pulumi config get aws:region
pulumi config get frontend-infrastructure:ebApplicationName

# Set a config value (if needed)
pulumi config set frontend-infrastructure:ebInstanceType t3.medium
```

## First Deployment

After initializing and previewing:

```bash
# Deploy infrastructure
pulumi up

# This will:
# 1. Show a preview
# 2. Ask for confirmation
# 3. Create all resources (ECR, Elastic Beanstalk, IAM roles, etc.)
```

## Troubleshooting

### Error: "no stack named 'test' found"

**Solution**: Initialize the stack first:
```bash
cd infrastructure
source .venv/bin/activate
pulumi stack init test
```

### Error: "PULUMI_ACCESS_TOKEN not set"

**Solution**: Set the token or login:
```bash
# Option 1: Login interactively
pulumi login

# Option 2: Set token as environment variable
export PULUMI_ACCESS_TOKEN="your-token-here"
```

### Error: "Could not find a Pulumi.yaml file"

**Solution**: Make sure you're in the infrastructure directory:
```bash
cd infrastructure
pulumi stack init test
```

### Error: "Module not found" or import errors

**Solution**: Install dependencies:
```bash
cd infrastructure
source .venv/bin/activate
uv pip install -e ".[dev]"
```


