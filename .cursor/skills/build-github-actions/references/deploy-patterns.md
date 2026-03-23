# Deployment Patterns

<strategies>
## Deployment Strategies

### Rolling Deployment
Deploy incrementally, replacing old instances with new ones.
```yaml
- name: Rolling deploy
  run: |
    for host in ${{ secrets.DEPLOY_HOSTS }}; do
      ssh user@$host "docker pull myapp:${{ github.sha }} && docker-compose up -d"
      sleep 30  # Wait for health check
    done
```

### Blue-Green Deployment
Run two identical environments, switch traffic after validation.
```yaml
jobs:
  deploy-green:
    steps:
      - name: Deploy to green
        run: ./deploy.sh green ${{ github.sha }}
      
      - name: Validate green
        run: ./health-check.sh green
      
      - name: Switch traffic to green
        run: ./switch-traffic.sh green
      
      - name: Keep blue as rollback
        run: echo "Blue environment retained for rollback"
```

### Canary Deployment
Route small percentage of traffic to new version first.
```yaml
- name: Deploy canary (10%)
  run: |
    kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
    kubectl patch deployment myapp -p '{"spec":{"replicas":1}}'

- name: Monitor canary
  run: ./monitor-metrics.sh --duration 10m --threshold 0.01

- name: Promote or rollback
  run: |
    if [ "${{ steps.monitor.outcome }}" == "success" ]; then
      kubectl scale deployment myapp --replicas=10
    else
      kubectl rollout undo deployment/myapp
    fi
```
</strategies>

<environment_promotion>
## Environment Promotion

### Sequential Promotion
```yaml
name: Promote through environments

on:
  workflow_dispatch:

jobs:
  deploy-dev:
    uses: ./.github/workflows/deploy.yml
    with:
      environment: dev
    secrets: inherit

  deploy-staging:
    needs: deploy-dev
    uses: ./.github/workflows/deploy.yml
    with:
      environment: staging
    secrets: inherit

  deploy-prod:
    needs: deploy-staging
    uses: ./.github/workflows/deploy.yml
    with:
      environment: prod
    secrets: inherit
```

### Manual Approval Gates
Configure in GitHub repository settings:
- Settings → Environments → [env] → Required reviewers

```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://prod.example.com
    # Job will wait for approval before running
```
</environment_promotion>

<rollback>
## Rollback Patterns

### Automatic Rollback on Failure
```yaml
- name: Deploy
  id: deploy
  run: ./deploy.sh
  continue-on-error: true

- name: Verify deployment
  id: verify
  if: steps.deploy.outcome == 'success'
  run: ./health-check.sh
  continue-on-error: true

- name: Rollback on failure
  if: steps.deploy.outcome == 'failure' || steps.verify.outcome == 'failure'
  run: ./rollback.sh ${{ env.PREVIOUS_VERSION }}
```

### Keep Previous Version Reference
```yaml
- name: Store current version before deploy
  run: |
    CURRENT=$(kubectl get deployment myapp -o jsonpath='{.spec.template.spec.containers[0].image}')
    echo "PREVIOUS_VERSION=$CURRENT" >> $GITHUB_ENV

- name: Deploy new version
  run: kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}

- name: Rollback if needed
  if: failure()
  run: kubectl set image deployment/myapp myapp=${{ env.PREVIOUS_VERSION }}
```
</rollback>

<verification>
## Deployment Verification

### Health Check Loop
```yaml
- name: Wait for healthy
  run: |
    for i in {1..30}; do
      if curl -sf ${{ env.DEPLOY_URL }}/health; then
        echo "Deployment healthy"
        exit 0
      fi
      echo "Attempt $i: Not ready yet..."
      sleep 10
    done
    echo "Deployment failed health check"
    exit 1
```

### Smoke Tests
```yaml
- name: Run smoke tests
  run: |
    npm run test:smoke -- --base-url=${{ env.DEPLOY_URL }}
```

### Kubernetes Rollout Status
```yaml
- name: Wait for rollout
  run: |
    kubectl rollout status deployment/myapp --timeout=300s
```
</verification>

<notifications>
## Deployment Notifications

### Slack Notification
```yaml
- name: Notify Slack
  if: always()
  uses: slackapi/slack-github-action@v1.26.0
  with:
    payload: |
      {
        "text": "Deployment to ${{ inputs.environment }}: ${{ job.status }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*${{ github.repository }}* deployed to *${{ inputs.environment }}*\nStatus: ${{ job.status }}\nCommit: ${{ github.sha }}"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### GitHub Deployment Status
```yaml
- name: Create deployment
  uses: chrnorm/deployment-action@v2
  id: deployment
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    environment: ${{ inputs.environment }}

- name: Update deployment status
  if: always()
  uses: chrnorm/deployment-status@v2
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    deployment-id: ${{ steps.deployment.outputs.deployment_id }}
    state: ${{ job.status }}
    environment-url: ${{ env.DEPLOY_URL }}
```
</notifications>
