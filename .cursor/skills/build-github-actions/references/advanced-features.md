# Advanced Features

<matrix>
## Matrix Builds

### Basic Matrix
```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

### Matrix with Include/Exclude
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20]
    include:
      - os: ubuntu-latest
        node: 22
        experimental: true
    exclude:
      - os: windows-latest
        node: 18
```

### Dynamic Matrix
```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: |
          echo "matrix={\"include\":[{\"project\":\"api\"},{\"project\":\"web\"}]}" >> $GITHUB_OUTPUT

  build:
    needs: setup
    strategy:
      matrix: ${{ fromJson(needs.setup.outputs.matrix) }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building ${{ matrix.project }}"
```

### Fail-Fast Control
```yaml
strategy:
  fail-fast: false  # Continue other matrix jobs if one fails
  matrix:
    node: [18, 20, 22]
```
</matrix>

<environments>
## Environments

### Environment Configuration
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
```

### Environment Secrets
Secrets scoped to environments override repository secrets:
```yaml
steps:
  - run: echo "Using ${{ secrets.API_KEY }}"
    # Uses production API_KEY if job has environment: production
```

### Environment Variables
```yaml
jobs:
  deploy:
    environment: production
    env:
      DEPLOY_URL: ${{ vars.DEPLOY_URL }}  # Environment variable
```
</environments>

<concurrency>
## Concurrency Control

### Cancel In-Progress
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Queue Deployments
```yaml
concurrency:
  group: deploy-${{ inputs.environment }}
  cancel-in-progress: false  # Queue instead of cancel
```

### Per-Environment Concurrency
```yaml
concurrency:
  group: deploy-${{ github.ref }}-${{ inputs.environment }}
  cancel-in-progress: ${{ inputs.environment != 'production' }}
```
</concurrency>

<oidc>
## OIDC Authentication

### AWS OIDC
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/github-actions
      aws-region: us-east-1
```

### Azure OIDC
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

### GCP OIDC
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: google-github-actions/auth@v2
    with:
      workload_identity_provider: projects/123/locations/global/workloadIdentityPools/github/providers/github
      service_account: github-actions@project.iam.gserviceaccount.com
```
</oidc>

<reusable_workflows>
## Reusable Workflows

### Define Reusable Workflow
```yaml
# .github/workflows/deploy-reusable.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - run: ./deploy.sh ${{ inputs.version }}
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

### Call Reusable Workflow
```yaml
jobs:
  deploy-staging:
    uses: ./.github/workflows/deploy-reusable.yml
    with:
      environment: staging
      version: ${{ github.sha }}
    secrets:
      DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}
```

### Inherit Secrets
```yaml
jobs:
  deploy:
    uses: ./.github/workflows/deploy-reusable.yml
    with:
      environment: production
    secrets: inherit  # Pass all secrets
```
</reusable_workflows>

<composite_actions>
## Composite Actions (local)

### Define Composite Action
```yaml
# .github/actions/setup-project/action.yml
name: Setup Project
description: Setup Node.js and install dependencies

inputs:
  node-version:
    description: Node.js version
    default: '20'

runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    
    - run: npm ci
      shell: bash
```

### Use Composite Action
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-project
    with:
      node-version: '22'
```
</composite_actions>

<expressions>
## Expressions and Functions

### Conditionals
```yaml
- if: github.event_name == 'push'
- if: contains(github.event.head_commit.message, '[skip ci]') == false
- if: github.ref == 'refs/heads/main'
- if: always()  # Run even if previous steps failed
- if: failure()  # Run only if previous steps failed
- if: success()  # Run only if previous steps succeeded (default)
```

### String Functions
```yaml
- run: echo ${{ contains('hello world', 'hello') }}  # true
- run: echo ${{ startsWith(github.ref, 'refs/tags/') }}
- run: echo ${{ format('Hello {0}!', 'World') }}
```

### JSON Functions
```yaml
- run: echo '${{ toJson(github.event) }}'
- run: echo ${{ fromJson(needs.setup.outputs.config).key }}
```
</expressions>
