# Ansible Utilities

Scripts for working with Ansible projects and configurations.

## Scripts

### dedupe-requirements.py

Remove duplicate entries from Ansible `requirements.yml` files (collections and roles).

**Usage:**
```bash
# Preview duplicates (no changes)
./dedupe-requirements.py requirements.yml --dry-run

# Remove duplicates
./dedupe-requirements.py requirements.yml
```

**Features:**
- Handles both flat lists and sectioned formats (collections/roles)
- Identifies duplicates by name + version
- Supports dry-run mode for safe preview

**Requirements:**
- Python 3.6+
- PyYAML (`pip install pyyaml`)

---
AI-DISCLOSURE: This documentation was created with AI assistance.
