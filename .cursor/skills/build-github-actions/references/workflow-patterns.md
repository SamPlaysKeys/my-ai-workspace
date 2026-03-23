# Workflow Patterns

<ci_patterns>
## CI/Build Patterns

### Basic CI
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

### Matrix Testing
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

### Build and Upload Artifact
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 7
```
</ci_patterns>

<trigger_patterns>
## Trigger Patterns

### Path Filtering
```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

### Manual with Inputs
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy target'
        required: true
        type: choice
        options: [dev, staging, prod]
      dry_run:
        description: 'Dry run only'
        type: boolean
        default: false
```

### Scheduled
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily
```

### After Another Workflow
```yaml
on:
  workflow_run:
    workflows: [CI]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
```
</trigger_patterns>

<job_patterns>
## Job Patterns

### Job Dependencies
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: ...
  
  test:
    needs: build
    runs-on: ubuntu-latest
    steps: ...
  
  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    steps: ...
```

### Conditional Jobs
```yaml
jobs:
  deploy-prod:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
```

### Reusable Workflow Call
```yaml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable.yml
    with:
      environment: prod
    secrets: inherit
```
</job_patterns>

<output_patterns>
## Output Patterns

### Job Outputs
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.value }}
    steps:
      - id: version
        run: echo "value=$(cat VERSION)" >> $GITHUB_OUTPUT
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.version }}"
```

### Artifact Passing
```yaml
jobs:
  build:
    steps:
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/
  
  deploy:
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/
```
</output_patterns>
