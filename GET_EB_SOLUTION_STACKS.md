# Get Available Elastic Beanstalk Solution Stacks

If you need to find the correct solution stack name, use this command:

```bash
aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
  --query 'SolutionStacks[?contains(@, `Docker`) && contains(@, `Amazon Linux 2023`)]' \
  --output table
```

Or to see all Docker solution stacks:

```bash
aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
  --query 'SolutionStacks[?contains(@, `Docker`)]' \
  --output table
```

## Common Docker Solution Stacks

- **Amazon Linux 2023**: `64bit Amazon Linux 2023 v4.3.0 running Docker`
- **Amazon Linux 2**: `64bit Amazon Linux 2 v3.8.0 running Docker` (older)

## Update Configuration

The solution stack is configured in:
- `Pulumi.test.yaml` - Test environment
- `Pulumi.prod.yaml` - Production environment
- `infrastructure/config_types/elasticbeanstalk_config.py` - Default value

