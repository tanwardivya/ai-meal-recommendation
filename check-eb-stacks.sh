#!/bin/bash

# Script to check available Elastic Beanstalk solution stacks

echo "Checking available Docker solution stacks in us-east-1..."
echo ""

# List all Docker solution stacks
aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
  --query 'SolutionStacks[?contains(@, `Docker`)]' \
  --output table

echo ""
echo "Most recent Docker stacks:"
aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
  --query 'SolutionStacks[?contains(@, `Docker`)]' \
  --output text | head -5

