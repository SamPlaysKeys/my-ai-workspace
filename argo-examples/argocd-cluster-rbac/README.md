# ArgoCD Cluster-Wide RBAC

Grant ArgoCD instances read access to cluster resources for live state comparison.

## Overview

ArgoCD needs cluster-wide read access to compare live state against desired state in Git. There are two approaches:

| Approach | Pros | Cons |
|----------|------|------|
| `ARGOCD_CLUSTER_CONFIG_NAMESPACES` env var | Operator-managed, automatic | Less visible, operator dependency |
| Direct ClusterRole/ClusterRoleBinding | GitOps-friendly, explicit control | Manual maintenance |

This directory uses the direct RBAC approach.

## Files

- `clusterrole-live-state-reader.yaml` - ClusterRole and ClusterRoleBindings for ArgoCD namespaces

## Usage

### Apply the RBAC

```bash
oc apply -f clusterrole-live-state-reader.yaml
```

### Verify

```bash
# Check ClusterRole exists
oc get clusterrole argocd-application-controller-cluster-role

# Check bindings
oc get clusterrolebindings | grep argocd-application-controller

# Test permissions (as the service account)
oc auth can-i get pods --all-namespaces \
  --as=system:serviceaccount:openshift-gitops:openshift-gitops-argocd-application-controller
```

## Adding Additional Namespaces

To grant cluster read access to ArgoCD in another namespace:

1. Find the application controller service account:
   ```bash
   oc get sa -n <namespace> | grep application-controller
   ```

2. Add a new ClusterRoleBinding to the YAML:
   ```yaml
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRoleBinding
   metadata:
     name: argocd-application-controller-<namespace>
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: ClusterRole
     name: argocd-application-controller-cluster-role
   subjects:
   - kind: ServiceAccount
     name: <instance-name>-argocd-application-controller
     namespace: <namespace>
   ```

## Alternative: Operator Configuration

If you prefer the operator-managed approach, patch the subscription:

```bash
oc patch subscription openshift-gitops-operator -n openshift-operators --type=merge -p '
spec:
  config:
    env:
    - name: ARGOCD_CLUSTER_CONFIG_NAMESPACES
      value: "openshift-gitops,argocd-diff-preview"
'
```

## Permissions Granted

The ClusterRole grants:

| API Groups | Resources | Verbs |
|------------|-----------|-------|
| `*` (all) | `*` (all) | `get`, `list`, `watch` |
| `""` (core) | `events` | `create`, `patch` |

This is read-only access plus the ability to create events for status reporting.
