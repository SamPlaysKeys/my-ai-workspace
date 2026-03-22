# Scripts

AI-created utility scripts organized by technology domain.

## Structure

```
scripts/
├── argocd/           # ArgoCD utilities
│   ├── *.sh          # Production scripts
│   └── tests/        # Test harnesses and fixtures
├── openshift/        # OpenShift utilities (future)
├── ansible/          # Ansible utilities (future)
└── README.md
```

## Guidelines

**Organization:**
- Group scripts by technology/tool (argocd, openshift, ansible, etc.)
- Keep test scripts in `tests/` subdirectory
- Keep test fixtures in `tests/fixtures/`

**Naming:**
- Use descriptive, hyphenated names: `app-of-apps-revisions.sh`
- Prefix test scripts with `test-`: `test-app-revision-map.sh`

**Documentation:**
- Each directory should have a README explaining its contents
- Scripts should include usage comments at the top

## Current Contents

### argocd/
- `app-of-apps-revisions.sh` - Extract targetRevision from nested ArgoCD app-of-apps hierarchies
