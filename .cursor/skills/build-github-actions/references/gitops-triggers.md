# GitOps Triggers

<argocd>
## ArgoCD Integration

### ArgoCD CLI Sync
```yaml
- name: Install ArgoCD CLI
  run: |
    curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
    chmod +x argocd
    sudo mv argocd /usr/local/bin/

- name: Sync application
  run: |
    argocd app sync ${{ env.APP_NAME }} \
      --server ${{ secrets.ARGOCD_SERVER }} \
      --auth-token ${{ secrets.ARGOCD_TOKEN }} \
      --grpc-web \
      --prune
```

### ArgoCD with Wait
```yaml
- name: Sync and wait
  run: |
    argocd app sync ${{ env.APP_NAME }} \
      --server ${{ secrets.ARGOCD_SERVER }} \
      --auth-token ${{ secrets.ARGOCD_TOKEN }} \
      --grpc-web
    
    argocd app wait ${{ env.APP_NAME }} \
      --server ${{ secrets.ARGOCD_SERVER }} \
      --auth-token ${{ secrets.ARGOCD_TOKEN }} \
      --grpc-web \
      --timeout 300
```

### ArgoCD API (no CLI)
```yaml
- name: Trigger sync via API
  run: |
    curl -X POST \
      -H "Authorization: Bearer ${{ secrets.ARGOCD_TOKEN }}" \
      -H "Content-Type: application/json" \
      "https://${{ secrets.ARGOCD_SERVER }}/api/v1/applications/${{ env.APP_NAME }}/sync" \
      -d '{"prune": true}'
```

### Update Image Tag (GitOps pattern)
```yaml
- name: Update image tag in GitOps repo
  run: |
    git clone https://x-access-token:${{ secrets.GITOPS_TOKEN }}@github.com/org/gitops-repo.git
    cd gitops-repo
    
    yq -i '.spec.template.spec.containers[0].image = "myapp:${{ github.sha }}"' \
      apps/${{ inputs.environment }}/deployment.yaml
    
    git config user.name "github-actions"
    git config user.email "github-actions@github.com"
    git add .
    git commit -m "Deploy ${{ github.sha }} to ${{ inputs.environment }}"
    git push
```

### Update Helm Values
```yaml
- name: Update Helm values
  run: |
    yq -i '.image.tag = "${{ github.sha }}"' \
      charts/myapp/values-${{ inputs.environment }}.yaml
```

### ApplicationSet Refresh
```yaml
- name: Refresh ApplicationSet
  run: |
    argocd appset get ${{ env.APPSET_NAME }} \
      --server ${{ secrets.ARGOCD_SERVER }} \
      --auth-token ${{ secrets.ARGOCD_TOKEN }} \
      --grpc-web \
      --refresh
```
</argocd>

<rhacm>
## Red Hat ACM Integration

### RHACM via oc CLI
```yaml
- name: Install oc CLI
  run: |
    curl -sSL https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/openshift-client-linux.tar.gz | tar xz
    sudo mv oc /usr/local/bin/

- name: Login to hub cluster
  run: |
    oc login --token=${{ secrets.OCP_TOKEN }} --server=${{ secrets.OCP_SERVER }}
```

### Apply RHACM Policy
```yaml
- name: Apply policy
  run: |
    oc apply -f rhacm/policies/deploy-policy.yaml -n open-cluster-management-policies
```

### Create/Update Application
```yaml
- name: Deploy RHACM Application
  run: |
    cat <<EOF | oc apply -f -
    apiVersion: app.k8s.io/v1beta1
    kind: Application
    metadata:
      name: myapp
      namespace: open-cluster-management
    spec:
      componentKinds:
        - group: apps.open-cluster-management.io
          kind: Subscription
      selector:
        matchLabels:
          app: myapp
    EOF
```

### Update Subscription
```yaml
- name: Update subscription to new version
  run: |
    oc patch subscription myapp-subscription \
      -n myapp-ns \
      --type merge \
      -p '{"spec":{"packageOverrides":[{"packageName":"myapp","packageAlias":"myapp","packageOverrides":[{"path":"spec.template.spec.containers[0].image","value":"myapp:${{ github.sha }}"}]}]}}'
```

### Trigger Policy Evaluation
```yaml
- name: Trigger policy evaluation
  run: |
    oc annotate policy deploy-policy \
      -n open-cluster-management-policies \
      policy.open-cluster-management.io/trigger-update="$(date +%s)" \
      --overwrite
```

### Target Specific Clusters
```yaml
- name: Apply to labeled clusters
  run: |
    cat <<EOF | oc apply -f -
    apiVersion: policy.open-cluster-management.io/v1
    kind: Placement
    metadata:
      name: deploy-placement
      namespace: open-cluster-management-policies
    spec:
      predicates:
        - requiredClusterSelector:
            labelSelector:
              matchLabels:
                environment: ${{ inputs.environment }}
    EOF
```
</rhacm>

<complete_examples>
## Complete Examples

### ArgoCD Deployment Pipeline
```yaml
name: Deploy via ArgoCD

on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [dev, staging, prod]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install ArgoCD CLI
        run: |
          curl -sSL -o /usr/local/bin/argocd \
            https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
          chmod +x /usr/local/bin/argocd
      
      - name: Sync application
        run: |
          argocd app sync myapp-${{ inputs.environment }} \
            --server ${{ secrets.ARGOCD_SERVER }} \
            --auth-token ${{ secrets.ARGOCD_TOKEN }} \
            --grpc-web
      
      - name: Wait for healthy
        run: |
          argocd app wait myapp-${{ inputs.environment }} \
            --server ${{ secrets.ARGOCD_SERVER }} \
            --auth-token ${{ secrets.ARGOCD_TOKEN }} \
            --grpc-web \
            --health \
            --timeout 300
```

### RHACM Multi-Cluster Deploy
```yaml
name: Deploy via RHACM

on:
  workflow_dispatch:
    inputs:
      cluster_label:
        description: 'Target cluster label'
        default: 'environment=prod'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install oc
        run: |
          curl -sSL https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/openshift-client-linux.tar.gz | tar xz
          sudo mv oc /usr/local/bin/
      
      - name: Login to RHACM hub
        run: oc login --token=${{ secrets.OCP_TOKEN }} --server=${{ secrets.OCP_SERVER }}
      
      - name: Apply deployment policy
        run: oc apply -f rhacm/policies/ -n open-cluster-management-policies
      
      - name: Verify policy compliance
        run: |
          sleep 30
          oc get policy -n open-cluster-management-policies -o wide
```
</complete_examples>
