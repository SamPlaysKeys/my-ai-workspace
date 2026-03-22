# ArgoCD Utilities

Scripts for working with ArgoCD applications and GitOps workflows.

## Scripts

### app-of-apps-revisions.sh

Extracts `targetRevision` values from nested ArgoCD app-of-apps hierarchies (up to 3 levels deep).

**Use case:** When you have a root Application that deploys level-2 Applications, which in turn deploy level-3 (final) Applications, this script builds revision maps for each level.

**Requirements:**
- `yq` (mikefarah/yq)
- `argocd` CLI (authenticated)

**Environment variables:**
- `GITOPS_NAME` - ArgoCD project name
- `ROOT_APP_ID` - Full app identifier (project/app-name)
- `NEW_REV` - Revision to fetch (default: HEAD)
- `ARGOCD_OPTS` - Additional argocd CLI options (default: --grpc-web)

**Usage:**
```bash
export GITOPS_NAME=my-gitops
export ROOT_APP_ID=my-gitops/root-app
export NEW_REV=main

source app-of-apps-revisions.sh

# Access results
echo "${APP_REVISION_MAP[@]}"       # Level 2 apps
echo "${FINAL_APP_REVISION_MAP[@]}" # Level 3 apps
```

## Tests

Run tests to validate the revision parsing logic:

```bash
cd tests
./test-app-of-apps-revisions.sh
./test-app-revision-map.sh
```

Tests use local YAML fixtures (no ArgoCD connection required).
