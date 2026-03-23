# Best Practices

<security>
## Security

### Pin Third-Party Actions
```yaml
# Bad - mutable tag
- uses: some-org/action@v1

# Good - pinned to SHA
- uses: some-org/action@a1b2c3d4e5f6g7h8i9j0...

# OK for GitHub-owned actions
- uses: actions/checkout@v4
```

Find SHA: Go to action repo → Releases → Copy commit SHA

### Scope Permissions
```yaml
# Bad - uses defaults (often write-all)
jobs:
  build:
    runs-on: ubuntu-latest

# Good - explicit minimal permissions
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
```

Common permission scopes:
- `contents: read` - checkout code
- `packages: write` - push to GHCR
- `id-token: write` - OIDC authentication
- `pull-requests: write` - comment on PRs
- `issues: write` - create/update issues

### Never Hardcode Secrets
```yaml
# Bad
- run: curl -H "Authorization: Bearer ghp_xxxx" ...

# Good
- run: curl -H "Authorization: Bearer ${{ secrets.TOKEN }}" ...
```

### Mask Sensitive Output
```yaml
- run: |
    echo "::add-mask::${{ steps.get-token.outputs.token }}"
    echo "Token retrieved successfully"
```

### Use OIDC Over Long-Lived Credentials
OIDC tokens are short-lived and scoped to the workflow run.
```yaml
permissions:
  id-token: write

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
```
</security>

<performance>
## Performance

### Cache Dependencies
```yaml
# Built-in caching
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

# Manual caching
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### Use Concurrency
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Parallelize Independent Jobs
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: ...
  
  test:
    runs-on: ubuntu-latest  # Runs in parallel with lint
    steps: ...
  
  build:
    needs: [lint, test]  # Waits for both
    steps: ...
```

### Use Path Filters
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

### Set Timeouts
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - name: Long running step
        timeout-minutes: 10
        run: ...
```
</performance>

<maintainability>
## Maintainability

### Use Descriptive Names
```yaml
name: CI Pipeline  # Workflow name

jobs:
  run-unit-tests:  # Job name
    steps:
      - name: Install dependencies  # Step name
        run: npm ci
```

### Extract Environment Variables
```yaml
env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io

jobs:
  build:
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
```

### Use Reusable Workflows
```yaml
# Define once
# .github/workflows/ci-reusable.yml

# Use everywhere
jobs:
  ci:
    uses: ./.github/workflows/ci-reusable.yml
```

### Move Complex Scripts to Files
```yaml
# Bad - complex inline script
- run: |
    if [ "${{ github.event_name }}" == "push" ]; then
      # 50 lines of bash...
    fi

# Good - script file
- run: ./scripts/deploy.sh
  env:
    EVENT_NAME: ${{ github.event_name }}
```

### Comment Non-Obvious Logic
```yaml
- name: Wait for deployment
  run: sleep 30
  # DNS propagation takes ~30s in our environment
```
</maintainability>

<reliability>
## Reliability

### Handle Failures Gracefully
```yaml
- name: Optional step
  continue-on-error: true
  run: ./optional-check.sh

- name: Cleanup (always runs)
  if: always()
  run: ./cleanup.sh
```

### Add Retries for Flaky Operations
```yaml
- uses: nick-fields/retry@v2
  with:
    timeout_minutes: 5
    max_attempts: 3
    command: npm test
```

### Verify Deployments
```yaml
- name: Deploy
  run: ./deploy.sh

- name: Verify
  run: |
    for i in {1..10}; do
      curl -sf ${{ env.URL }}/health && exit 0
      sleep 5
    done
    exit 1
```

### Use Checkout Depth
```yaml
# Full history (needed for git operations)
- uses: actions/checkout@v4
  with:
    fetch-depth: 0

# Shallow clone (faster, default)
- uses: actions/checkout@v4
  # fetch-depth: 1 is default
```
</reliability>

<checklist>
## Pre-Merge Checklist

Before merging a workflow:

- [ ] Permissions explicitly scoped
- [ ] Third-party actions pinned (or justified)
- [ ] No hardcoded secrets
- [ ] Caching configured for dependencies
- [ ] Concurrency prevents redundant runs
- [ ] Timeouts set for jobs and long steps
- [ ] Job and step names are descriptive
- [ ] Path filters exclude irrelevant changes
- [ ] Failures handled appropriately
- [ ] Tested in a branch first
</checklist>
