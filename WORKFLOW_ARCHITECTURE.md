# Workflow Architecture

## Overview

We have separated the build and deploy workflows for better efficiency:

1. **Build Workflow** (`build-frontend-pr.yml`) - Runs on PRs, builds and pushes Docker images
2. **Deploy Workflow** (`deploy-frontend-test.yml`) - Runs manually, reuses existing images or builds if needed

## Workflow Flow

```
┌─────────────────┐
│  PR Created/    │
│  Updated        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ build-frontend-pr.yml   │
│  ├─ Get ECR repo        │
│  ├─ Build Docker image  │
│  ├─ Tag: pr-<N>-<SHA>   │
│  └─ Push to ECR         │
└─────────────────────────┘
         │
         │ Image stored in ECR
         │
         ▼
┌─────────────────────────┐
│ Manual Deploy Trigger   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ deploy-frontend-test.yml│
│  ├─ Check if image      │
│  │  exists in ECR       │
│  ├─ If exists: reuse   │
│  ├─ If not: build new  │
│  └─ Deploy to EB        │
└─────────────────────────┘
```

## Image Tagging Strategy

### PR Build (`build-frontend-pr.yml`)
- **Primary Tag**: `pr-<PR_NUMBER>-<COMMIT_SHA>`
  - Example: `pr-123-abc12345`
- **Secondary Tag**: `pr-<PR_NUMBER>`
  - Example: `pr-123`
- **Purpose**: Unique identification per PR and commit

### Deploy (`deploy-frontend-test.yml`)
- **Checks for images in this order**:
  1. `pr-<PR_NUMBER>-<COMMIT_SHA>` (if PR number available)
  2. `pr-<PR_NUMBER>` (if PR number available)
  3. `<COMMIT_SHA>` (fallback)
  4. Generated tag based on context
- **If found**: Reuses existing image (no rebuild)
- **If not found**: Builds new image

## Benefits

1. **Faster Deployments**: No rebuild during deployment if image exists
2. **Cost Savings**: Build once, deploy multiple times
3. **Consistency**: Same image used for testing and deployment
4. **Flexibility**: Can still build during deploy if image missing

## Workflow Files

### `build-frontend-pr.yml`
- **Triggers**: PR opened/updated (not on close)
- **Purpose**: Build and push Docker images
- **Output**: Image in ECR with PR-specific tags
- **Comments**: Posts image info on PR

### `deploy-frontend-test.yml`
- **Triggers**: Manual dispatch only
- **Purpose**: Deploy to Elastic Beanstalk
- **Image Strategy**: Reuse if exists, build if not
- **Steps**:
  1. Check ECR for existing image
  2. Build if not found
  3. Deploy to EB

## Usage

### During Development

1. **Create PR** → Build workflow runs automatically
2. **Image built** → Stored in ECR with PR tag
3. **PR comment** → Shows image details

### During Deployment

1. **Manual trigger** → Deploy workflow starts
2. **Image check** → Looks for existing image
3. **Reuse or build** → Uses existing or builds new
4. **Deploy** → Updates Elastic Beanstalk

## Image Lifecycle

- **PR builds**: Images tagged with PR number
- **Deploy**: Reuses PR images when possible
- **Cleanup**: ECR lifecycle policy keeps last N images
- **Manual builds**: Can still build during deploy if needed

