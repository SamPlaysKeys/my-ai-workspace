---
name: build-github-actions
description: Create GitHub Actions workflows for CI/CD, deployments, and automation. Covers Ansible, ArgoCD, RHACM, and container operations. Use when building or optimizing .github/workflows/*.yml files.
---

<essential_principles>
## GitHub Actions Fundamentals

### 1. Workflow Structure
```yaml
name: descriptive-name
on: [trigger]
jobs:
  job-name:
    runs-on: runner
    steps:
      - uses: actions/checkout@v4
      - run: command
```

### 2. Security First
- Never hardcode secrets - use `${{ secrets.NAME }}`
- Prefer OIDC over long-lived credentials for cloud providers
- Pin action versions to SHA for third-party actions
- Use `permissions:` to limit GITHUB_TOKEN scope

### 3. Efficiency Patterns
- Cache dependencies (`actions/cache`, `actions/setup-*` built-in caching)
- Use `concurrency:` to cancel redundant runs
- Fail fast with `continue-on-error: false` (default)
- Parallelize independent jobs

### 4. Maintainability
- Use workflow_call for reusable workflows
- Extract complex logic to scripts, not inline YAML
- Use environment variables for repeated values
- Add meaningful job and step names
</essential_principles>

<intake>
What would you like to build?

1. **CI/Build workflow** - Test, lint, build artifacts
2. **Deployment pipeline** - Deploy via Ansible, ArgoCD, RHACM, or containers
3. **Optimize existing workflow** - Improve performance, security, or maintainability

**Provide your choice or describe what you need.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "CI", "build", "test", "lint" | `workflows/create-workflow.md` |
| 2, "deploy", "pipeline", "ansible", "argocd", "rhacm", "docker" | `workflows/create-deploy-pipeline.md` |
| 3, "optimize", "improve", "review", "existing" | `workflows/optimize-workflow.md` |

**After reading the workflow, follow it exactly.**
</routing>

<reference_index>
## Domain Knowledge

All in `references/`:

**Patterns:** workflow-patterns.md, deploy-patterns.md
**Integrations:** ansible-integration.md, gitops-triggers.md, container-operations.md
**Advanced:** advanced-features.md, best-practices.md
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| create-workflow.md | Build CI/test/build workflows |
| create-deploy-pipeline.md | Build deployment pipelines |
| optimize-workflow.md | Improve existing workflows |
</workflows_index>

<success_criteria>
A well-built workflow:
- Uses appropriate triggers for the use case
- Follows security best practices (secrets, permissions, pinned versions)
- Is efficient (caching, concurrency, parallelization)
- Has clear job and step names
- Handles failures appropriately
</success_criteria>
