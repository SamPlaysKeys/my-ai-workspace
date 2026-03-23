# Workflow: Optimize Existing Workflow

<required_reading>
**Read these reference files NOW:**
1. references/advanced-features.md
2. references/best-practices.md
</required_reading>

<process>
## Step 1: Review Current Workflow

Ask user to provide the workflow file or path. Analyze for:
- Performance issues (missing cache, sequential jobs that could parallelize)
- Security issues (unpinned actions, overly broad permissions, exposed secrets)
- Maintainability issues (inline scripts, magic values, unclear names)
- Reliability issues (missing error handling, no timeout, flaky steps)

## Step 2: Check Performance

**Caching:**
- Dependencies cached? (`actions/cache` or built-in)
- Docker layers cached? (`cache-from/cache-to`)
- Build artifacts cached between jobs?

**Parallelization:**
- Independent jobs running in parallel?
- Matrix builds for multi-version testing?
- Unnecessary sequential dependencies?

**Concurrency:**
- `concurrency` group defined?
- Redundant runs cancelled?

## Step 3: Check Security

**Actions:**
```yaml
# Bad - mutable tag
- uses: actions/checkout@v4

# Good - pinned SHA (for third-party actions)
- uses: some-org/action@a1b2c3d4e5f6...
```

Pin third-party actions to SHA. GitHub-owned actions (`actions/*`) are safe with version tags.

**Permissions:**
```yaml
# Bad - default (often write-all)
jobs:
  build:
    runs-on: ubuntu-latest

# Good - explicit minimal permissions
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
```

**Secrets:**
- Using OIDC instead of long-lived credentials?
- Secrets scoped to environments?
- No secrets in logs? (`::add-mask::`)

## Step 4: Check Maintainability

**Naming:**
- Jobs and steps have descriptive names?
- Workflow name reflects purpose?

**DRY:**
- Repeated values extracted to `env:`?
- Reusable workflows for shared logic?
- Complex scripts moved to files?

**Documentation:**
- Workflow has comments for non-obvious logic?
- README documents manual triggers and inputs?

## Step 5: Check Reliability

**Timeouts:**
```yaml
jobs:
  build:
    timeout-minutes: 30
    steps:
      - name: Long step
        timeout-minutes: 10
        run: ...
```

**Error handling:**
```yaml
- name: Optional step
  continue-on-error: true
  run: ...

- name: Cleanup (always runs)
  if: always()
  run: ...
```

**Retries:**
```yaml
- uses: nick-fields/retry@v2
  with:
    timeout_minutes: 5
    max_attempts: 3
    command: flaky-command
```

## Step 6: Apply Improvements

Generate optimized workflow with changes annotated. Explain each improvement.

## Step 7: Validate Changes

Ensure optimizations don't break functionality:
- Triggers still correct?
- All required steps present?
- Dependencies between jobs preserved?
</process>

<success_criteria>
Optimization complete when:
- [ ] Caching implemented for dependencies and builds
- [ ] Independent jobs parallelized
- [ ] Concurrency prevents redundant runs
- [ ] Permissions explicitly scoped
- [ ] Third-party actions pinned (or documented why not)
- [ ] Timeouts set for jobs and long steps
- [ ] Names are clear and descriptive
- [ ] Changes explained to user
</success_criteria>
