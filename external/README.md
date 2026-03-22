# External Repositories

This directory contains git submodules - external repositories integrated into this workspace for reference and use.

## Working with Submodules

### Initial Clone

When cloning this repository, submodules are not automatically fetched. Initialize them with:

```bash
git submodule update --init --recursive
```

### Updating Submodules

Pull the latest changes from upstream:

```bash
# Update all submodules
git submodule update --remote --merge

# Update a specific submodule
git submodule update --remote --merge external/code-for-msps
```

### Adding New Submodules

```bash
git submodule add <repository-url> external/<name>
```

## Available Submodules

### code-for-msps

**Source:** [SamPlaysKeys/Code-for-MSPs](https://github.com/SamPlaysKeys/Code-for-MSPs)

PowerShell scripts and utilities for Managed Service Providers (MSPs) covering:

| Category | Examples |
|----------|----------|
| **Azure/M365** | Azure AD migration, Autopilot, ATP policies, Intune scripts |
| **System Admin** | BitLocker, power settings, Windows upgrades, bloatware removal |
| **User Management** | Profile migration, admin user creation, password generation |
| **Network** | DNS settings, printers, mapped drives, IPv6 management |
| **Utilities** | UI dialogs, file downloads, text-to-speech |

**Quick reference:**

```powershell
# Get Windows license key
.\external\code-for-msps\Get-WindowsKey.ps1

# Check BitLocker status
.\external\code-for-msps\BitlockerChecking.ps1

# Generate secure password
.\external\code-for-msps\PasswordGenerate.ps1

# Azure AD migration prep
.\external\code-for-msps\Azure AD Migration Prep.ps1
```

See `external/code-for-msps/README.md` for complete documentation.

## Referencing External Content

When using scripts from external repositories:

1. **Don't modify directly** - Changes in submodules require separate commits
2. **Copy and adapt** - For customization, copy to `scripts/` and modify there
3. **Reference the source** - Document which external script inspired your work

Example workflow:

```bash
# Copy a script for customization
cp "external/code-for-msps/PasswordGenerate.ps1" scripts/windows/

# Modify your copy as needed
# The original stays pristine for updates
```

---
AI-DISCLOSURE: This documentation was created with AI assistance.
