# Workflow: Create CI/Build Workflow

<required_reading>
**Read these reference files NOW:**
1. references/workflow-patterns.md
2. references/best-practices.md
</required_reading>

<process>
## Step 1: Identify Requirements

Ask if not clear from context:
- What language/framework? (affects setup actions and caching)
- What triggers? (push, PR, schedule, manual)
- What checks? (lint, test, build, security scan)
- What artifacts? (binaries, packages, reports)

## Step 2: Select Triggers

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```

Common patterns:
- `push` + `pull_request` for CI
- `workflow_dispatch` for manual runs
- `schedule` for nightly builds
- Path filters to skip irrelevant changes

## Step 3: Configure Runner and Permissions

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      # Add others only if needed
```

Use `ubuntu-latest` unless specific OS needed. Always scope permissions.

## Step 4: Build the Steps

Standard CI structure:
```yaml
steps:
  - uses: actions/checkout@v4
  
  - name: Setup [language]
    uses: actions/setup-[language]@v[X]
    with:
      [language]-version: 'X.Y'
      cache: '[package-manager]'
  
  - name: Install dependencies
    run: [install-command]
  
  - name: Lint
    run: [lint-command]
  
  - name: Test
    run: [test-command]
  
  - name: Build
    run: [build-command]
```

## Step 5: Add Caching (if not built into setup action)

```yaml
- uses: actions/cache@v4
  with:
    path: [cache-path]
    key: ${{ runner.os }}-[tool]-${{ hashFiles('[lock-file]') }}
    restore-keys: |
      ${{ runner.os }}-[tool]-
```

## Step 6: Add Artifacts (if needed)

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
    retention-days: 5
```

## Step 7: Add Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Step 8: Write the Complete Workflow

Combine all elements into `.github/workflows/[name].yml`
</process>

<success_criteria>
Workflow is complete when:
- [ ] Triggers match the use case
- [ ] Permissions are scoped (not using defaults)
- [ ] Dependencies are cached
- [ ] All checks run (lint, test, build as needed)
- [ ] Concurrency prevents redundant runs
- [ ] Job and step names are descriptive
</success_criteria>
