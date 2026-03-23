# Workflow: Create Deployment Pipeline

<required_reading>
**Read based on deployment target:**
- Ansible: references/ansible-integration.md
- ArgoCD/RHACM: references/gitops-triggers.md
- Docker/Containers: references/container-operations.md
- General: references/deploy-patterns.md, references/best-practices.md
</required_reading>

<process>
## Step 1: Identify Deployment Target

Ask if not clear:
- **Ansible** - Run playbooks against inventory
- **ArgoCD** - Trigger GitOps sync
- **RHACM** - Manage multi-cluster deployments
- **Docker** - Build/push images, rebuild hosts
- **Multiple** - Combine approaches (e.g., build image → trigger ArgoCD)

## Step 2: Determine Trigger Strategy

| Use Case | Recommended Trigger |
|----------|---------------------|
| Deploy on merge to main | `push: branches: [main]` |
| Deploy on release | `release: types: [published]` |
| Manual deploy with env selection | `workflow_dispatch` with inputs |
| Deploy after CI passes | `workflow_run` |

For environment promotion:
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options: [dev, staging, prod]
```

## Step 3: Configure Environments and Approvals

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment }}
      url: https://${{ inputs.environment }}.example.com
```

Configure environment protection rules in GitHub for approval gates.

## Step 4: Build Deployment Job

### For Ansible:
```yaml
- name: Run Ansible playbook
  uses: dawidd6/action-ansible-playbook@v2
  with:
    playbook: deploy.yml
    inventory: inventory/${{ inputs.environment }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    options: |
      --extra-vars "version=${{ github.sha }}"
```

Or run directly:
```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'

- name: Install Ansible
  run: pip install ansible

- name: Run playbook
  env:
    ANSIBLE_HOST_KEY_CHECKING: 'false'
  run: |
    echo "${{ secrets.SSH_PRIVATE_KEY }}" > key.pem
    chmod 600 key.pem
    ansible-playbook -i inventory/${{ inputs.environment }} \
      --private-key key.pem \
      deploy.yml
```

### For ArgoCD:
```yaml
- name: Trigger ArgoCD sync
  run: |
    argocd app sync ${{ env.APP_NAME }} \
      --server ${{ secrets.ARGOCD_SERVER }} \
      --auth-token ${{ secrets.ARGOCD_TOKEN }} \
      --grpc-web
```

Or update image tag to trigger GitOps:
```yaml
- name: Update image tag
  run: |
    yq -i '.spec.source.helm.parameters[0].value = "${{ github.sha }}"' \
      argocd/apps/${{ inputs.environment }}.yaml

- name: Commit and push
  run: |
    git config user.name "github-actions"
    git config user.email "github-actions@github.com"
    git add .
    git commit -m "Deploy ${{ github.sha }} to ${{ inputs.environment }}"
    git push
```

### For RHACM:
```yaml
- name: Apply RHACM policy
  run: |
    oc login --token=${{ secrets.OCP_TOKEN }} --server=${{ secrets.OCP_SERVER }}
    oc apply -f rhacm/policies/deploy-${{ inputs.environment }}.yaml
```

### For Docker:
```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: |
      ghcr.io/${{ github.repository }}:${{ github.sha }}
      ghcr.io/${{ github.repository }}:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Step 5: Add Deployment Verification

```yaml
- name: Verify deployment
  run: |
    for i in {1..30}; do
      if curl -sf https://${{ inputs.environment }}.example.com/health; then
        echo "Deployment healthy"
        exit 0
      fi
      sleep 10
    done
    echo "Deployment verification failed"
    exit 1
```

## Step 6: Add Rollback Option (optional)

```yaml
- name: Rollback on failure
  if: failure()
  run: |
    # Tool-specific rollback command
```

## Step 7: Assemble Complete Pipeline

Combine authentication, deployment, and verification into final workflow.
</process>

<success_criteria>
Pipeline is complete when:
- [ ] Trigger matches deployment strategy (manual, on-merge, on-release)
- [ ] Environment protection configured for sensitive targets
- [ ] Credentials handled via secrets (never hardcoded)
- [ ] Deployment verification confirms success
- [ ] Rollback strategy defined (if required)
- [ ] Appropriate tool integration (Ansible/ArgoCD/RHACM/Docker)
</success_criteria>
