#!/bin/bash

# Setup OIDC IAM Role for GitHub Actions
# This script creates an IAM role for the ai-meal-recommendation repository

set -e

AWS_ACCOUNT_ID="928618160741"
ROLE_NAME="github-actions-frontend-role"
POLICY_NAME="github-actions-frontend-policy"
OIDC_PROVIDER_ARN="arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setting up OIDC IAM Role for GitHub Actions${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Step 1: Check if OIDC provider exists
echo -e "${YELLOW}Step 1: Checking OIDC Provider...${NC}"
if aws iam list-open-id-connect-providers --query "OpenIDConnectProviderList[?contains(Arn, 'token.actions.githubusercontent.com')]" --output text | grep -q "token.actions.githubusercontent.com"; then
    echo -e "${GREEN}✅ OIDC Provider already exists${NC}"
else
    echo -e "${RED}❌ OIDC Provider not found${NC}"
    echo "Creating OIDC Provider..."
    
    # Get GitHub thumbprint
    echo "Getting GitHub OIDC thumbprint..."
    THUMBPRINT=$(echo | openssl s_client -servername token.actions.githubusercontent.com \
      -showcerts -connect token.actions.githubusercontent.com:443 2>/dev/null | \
      openssl x509 -fingerprint -noout -sha1 | \
      sed 's/://g' | \
      cut -d'=' -f2 | \
      tr '[:upper:]' '[:lower:]')
    
    echo "Thumbprint: $THUMBPRINT"
    
    aws iam create-open-id-connect-provider \
      --url https://token.actions.githubusercontent.com \
      --client-id-list sts.amazonaws.com \
      --thumbprint-list "$THUMBPRINT"
    
    echo -e "${GREEN}✅ OIDC Provider created${NC}"
fi
echo ""

# Step 2: Create IAM Policy
echo -e "${YELLOW}Step 2: Creating IAM Policy...${NC}"
if aws iam get-policy --policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/${POLICY_NAME}" &>/dev/null; then
    echo -e "${YELLOW}⚠️  Policy already exists, updating...${NC}"
    POLICY_VERSION=$(aws iam create-policy-version \
      --policy-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:policy/${POLICY_NAME}" \
      --policy-document file://frontend-iam-policy.json \
      --set-as-default \
      --query 'PolicyVersion.VersionId' \
      --output text)
    echo -e "${GREEN}✅ Policy updated (Version: ${POLICY_VERSION})${NC}"
else
    aws iam create-policy \
      --policy-name "$POLICY_NAME" \
      --policy-document file://frontend-iam-policy.json \
      --description "Policy for GitHub Actions to deploy frontend to Elastic Beanstalk"
    echo -e "${GREEN}✅ Policy created${NC}"
fi
echo ""

# Step 3: Create IAM Role
echo -e "${YELLOW}Step 3: Creating IAM Role...${NC}"
if aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
    echo -e "${YELLOW}⚠️  Role already exists, updating trust policy...${NC}"
    aws iam update-assume-role-policy \
      --role-name "$ROLE_NAME" \
      --policy-document file://github-actions-trust-policy.json
    echo -e "${GREEN}✅ Role trust policy updated${NC}"
else
    aws iam create-role \
      --role-name "$ROLE_NAME" \
      --assume-role-policy-document file://github-actions-trust-policy.json \
      --description "IAM role for GitHub Actions to deploy frontend application"
    echo -e "${GREEN}✅ Role created${NC}"
fi
echo ""

# Step 4: Attach Policy to Role
echo -e "${YELLOW}Step 4: Attaching Policy to Role...${NC}"
POLICY_ARN="arn:aws:iam::${AWS_ACCOUNT_ID}:policy/${POLICY_NAME}"

# Check if policy is already attached
if aws iam list-attached-role-policies --role-name "$ROLE_NAME" --query "AttachedPolicies[?PolicyArn=='${POLICY_ARN}']" --output text | grep -q "$POLICY_ARN"; then
    echo -e "${GREEN}✅ Policy already attached${NC}"
else
    aws iam attach-role-policy \
      --role-name "$ROLE_NAME" \
      --policy-arn "$POLICY_ARN"
    echo -e "${GREEN}✅ Policy attached${NC}"
fi
echo ""

# Step 5: Output Role ARN
ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Role ARN:${NC}"
echo "$ROLE_ARN"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Add this ARN to GitHub Secrets:"
echo "   - Go to: Settings → Secrets and variables → Actions"
echo "   - Add secret: AWS_ROLE_ARN = $ROLE_ARN"
echo ""
echo "2. (Optional) Create separate roles for test/prod:"
echo "   - AWS_TEST_ROLE_ARN = $ROLE_ARN"
echo "   - AWS_PROD_ROLE_ARN = $ROLE_ARN"
echo ""
echo -e "${GREEN}========================================${NC}"

