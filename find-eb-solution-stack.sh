#!/bin/bash

# Script to find the correct Elastic Beanstalk Docker solution stack

echo "Finding available Docker solution stacks in us-east-1..."
echo ""

# Get the most recent Docker solution stack
SOLUTION_STACK=$(aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
  --query 'SolutionStacks[?contains(@, `Docker`) && contains(@, `Amazon Linux 2`)] | [0]' \
  --output text)

if [ -z "$SOLUTION_STACK" ]; then
  echo "❌ No Docker solution stack found for Amazon Linux 2"
  echo ""
  echo "Trying Amazon Linux 2023..."
  SOLUTION_STACK=$(aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
    --query 'SolutionStacks[?contains(@, `Docker`) && contains(@, `Amazon Linux 2023`)] | [0]' \
    --output text)
fi

if [ -z "$SOLUTION_STACK" ]; then
  echo "❌ No Docker solution stack found"
  echo ""
  echo "Listing all Docker stacks:"
  aws elasticbeanstalk list-available-solution-stacks --region us-east-1 \
    --query 'SolutionStacks[?contains(@, `Docker`)]' \
    --output table
  exit 1
fi

echo "✅ Found solution stack:"
echo ""
echo "$SOLUTION_STACK"
echo ""
echo "To use this, update Pulumi.test.yaml and Pulumi.prod.yaml:"
echo "  frontend-infrastructure:ebSolutionStack: \"$SOLUTION_STACK\""
echo ""

