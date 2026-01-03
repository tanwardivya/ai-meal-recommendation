#!/bin/bash

# Script to clean up a failed Elastic Beanstalk environment
# This is needed when an environment is in CREATE_FAILED state

ENV_NAME="${1:-frontend-test-env}"
APP_NAME="${2:-frontend-test}"
REGION="${3:-us-east-1}"

echo "=========================================="
echo "Cleaning up failed Elastic Beanstalk environment"
echo "=========================================="
echo "Environment: $ENV_NAME"
echo "Application: $APP_NAME"
echo "Region: $REGION"
echo ""

# Check if environment exists
ENV_STATUS=$(aws elasticbeanstalk describe-environments \
  --environment-names "$ENV_NAME" \
  --region "$REGION" \
  --query 'Environments[0].Status' \
  --output text 2>/dev/null)

if [ "$ENV_STATUS" == "None" ] || [ -z "$ENV_STATUS" ]; then
  echo "✅ Environment '$ENV_NAME' not found. Nothing to clean up."
  exit 0
fi

echo "Current environment status: $ENV_STATUS"
echo ""

if [ "$ENV_STATUS" == "Terminated" ]; then
  echo "✅ Environment is already terminated."
  exit 0
fi

# Terminate the failed environment
echo "⚠️  Terminating failed environment..."
aws elasticbeanstalk terminate-environment \
  --environment-name "$ENV_NAME" \
  --region "$REGION" \
  --force-terminate

if [ $? -eq 0 ]; then
  echo "✅ Environment termination initiated."
  echo ""
  echo "⏳ Waiting for environment to be fully terminated..."
  echo "   This may take a few minutes..."
  
  # Wait for termination
  while true; do
    STATUS=$(aws elasticbeanstalk describe-environments \
      --environment-names "$ENV_NAME" \
      --region "$REGION" \
      --query 'Environments[0].Status' \
      --output text 2>/dev/null)
    
    # Terminated is a valid final state - environment is cleaned up
    if [ "$STATUS" == "Terminated" ] || [ "$STATUS" == "None" ] || [ -z "$STATUS" ]; then
      echo "✅ Environment has been terminated."
      break
    fi
    
    # If status is still Terminating, continue waiting
    if [ "$STATUS" == "Terminating" ]; then
      echo "   Current status: $STATUS (waiting...)"
      sleep 10
    else
      # Unexpected status
      echo "   Current status: $STATUS (waiting...)"
      sleep 10
    fi
  done
else
  echo "❌ Failed to terminate environment."
  echo ""
  echo "You may need to terminate it manually:"
  echo "  aws elasticbeanstalk terminate-environment --environment-name $ENV_NAME --region $REGION --force-terminate"
  exit 1
fi

echo ""
echo "=========================================="
echo "✅ Cleanup complete!"
echo "=========================================="
echo ""
echo "You can now re-run the deployment workflow."

