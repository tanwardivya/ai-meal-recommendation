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
POLICY_ARN="arn:aws:iam::${AWS_ACCOUNT_ID}:policy/${POLICY_NAME}"

if aws iam get-policy --policy-arn "$POLICY_ARN" &>/dev/null; then
    echo -e "${YELLOW}⚠️  Policy already exists, updating...${NC}"
    
    # Check if we're at the version limit (5 versions max)
    VERSION_COUNT=$(aws iam list-policy-versions \
      --policy-arn "$POLICY_ARN" \
      --query 'length(Versions)' \
      --output text)
    
    if [ "$VERSION_COUNT" -ge 5 ]; then
        echo -e "${YELLOW}⚠️  Policy has ${VERSION_COUNT} versions (max 5). Deleting oldest non-default version...${NC}"
        
        # Get the default version (this is the current active version - we MUST keep it)
        DEFAULT_VERSION=$(aws iam get-policy \
          --policy-arn "$POLICY_ARN" \
          --query 'Policy.DefaultVersionId' \
          --output text)
        
        echo -e "${GREEN}✅ Current default version: ${DEFAULT_VERSION} (will be preserved)${NC}"
        
        # List all versions and find the oldest non-default one
        # We need to delete one to make room for the new version
        ALL_VERSIONS=$(aws iam list-policy-versions \
          --policy-arn "$POLICY_ARN" \
          --query "Versions[?VersionId!='${DEFAULT_VERSION}'] | sort_by(@, &CreateDate)" \
          --output json)
        
        # Extract the oldest non-default version ID
        OLDEST_VERSION=$(echo "$ALL_VERSIONS" | grep -o '"VersionId": "[^"]*"' | head -1 | cut -d'"' -f4)
        
        if [ -n "$OLDEST_VERSION" ] && [ "$OLDEST_VERSION" != "None" ] && [ "$OLDEST_VERSION" != "$DEFAULT_VERSION" ]; then
            echo -e "${YELLOW}Deleting oldest non-default version: ${OLDEST_VERSION}${NC}"
            aws iam delete-policy-version \
              --policy-arn "$POLICY_ARN" \
              --version-id "$OLDEST_VERSION"
            echo -e "${GREEN}✅ Deleted old version: ${OLDEST_VERSION}${NC}"
            echo -e "${GREEN}✅ Default version ${DEFAULT_VERSION} is preserved${NC}"
        else
            echo -e "${RED}⚠️  Warning: Could not find a non-default version to delete${NC}"
            echo -e "${YELLOW}This should not happen. All versions might be marked as default.${NC}"
            echo -e "${YELLOW}Attempting to delete the oldest version (excluding current default)...${NC}"
            
            # Fallback: get all versions, sort by date, exclude default, take oldest
            OLDEST_VERSION=$(aws iam list-policy-versions \
              --policy-arn "$POLICY_ARN" \
              --query "Versions[?VersionId!='${DEFAULT_VERSION}'] | sort_by(@, &CreateDate) | [0].VersionId" \
              --output text)
            
            if [ -n "$OLDEST_VERSION" ] && [ "$OLDEST_VERSION" != "None" ] && [ "$OLDEST_VERSION" != "$DEFAULT_VERSION" ]; then
                echo -e "${YELLOW}Deleting version: ${OLDEST_VERSION}${NC}"
                aws iam delete-policy-version \
                  --policy-arn "$POLICY_ARN" \
                  --version-id "$OLDEST_VERSION"
                echo -e "${GREEN}✅ Deleted old version: ${OLDEST_VERSION}${NC}"
            else
                echo -e "${RED}❌ Error: Cannot safely delete a version. Please delete manually.${NC}"
                echo -e "${YELLOW}Current default version: ${DEFAULT_VERSION}${NC}"
                exit 1
            fi
        fi
    fi
    
    # Now create the new version
    POLICY_VERSION=$(aws iam create-policy-version \
      --policy-arn "$POLICY_ARN" \
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


