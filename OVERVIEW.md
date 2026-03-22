# Workspace Overview

A practical guide to using this AI-assisted DevOps workspace for creation, discovery, and learning.

## What This Workspace Is

This is an **AI collaboration workspace** for DevOps work. It contains:

- **Examples** - Runnable Ansible, ArgoCD, OpenShift, and CoreOS configurations
- **Troubleshooting guides** - Systematic investigation workflows for common issues
- **Scripts & tools** - Utilities created during AI sessions
- **Meta-development system** - Skills, commands, and agents for effective AI collaboration

The workspace is designed for **iterative development with an AI agent** - you describe what you need, the agent creates or discovers it, and you refine together.

## Quick Start

### Ask Directly

The simplest way to use this workspace:

```
Create an Ansible playbook that validates memory on Dell servers using Redfish API
```

```
Show me how to troubleshoot CSR issues in OpenShift
```

```
I need a script to extract targetRevision from nested ArgoCD apps
```

The agent will search existing content, create new content, or combine both.

### Use Slash Commands

For structured workflows, use slash commands (type `/` to see all):

| Command | When to Use |
|---------|-------------|
| `/create-plan [desc]` | Starting a new project or feature |
| `/debug` | Systematic troubleshooting |
| `/whats-next` | Ending a session, creating handoff |
| `/consider:first-principles` | Making architectural decisions |
| `/research:technical [topic]` | Deep-dive into a technology |

### Load Skills for Deep Guidance

When you need comprehensive methodology:

```
@.cursor/skills/debug-like-expert/SKILL.md

My OpenShift cluster operators are degraded after upgrade
```

```
@.cursor/skills/create-plans/SKILL.md

Plan a multi-cluster GitOps deployment with ArgoCD
```

## Interaction Patterns

### Pattern 1: Discovery

Find existing content that might help:

```
What examples do we have for RHACM secret management?
```

```
Show me the troubleshooting guide for namespace termination issues
```

```
Is there an Ansible pattern for retry with timeout?
```

### Pattern 2: Creation

Generate new content:

```
Create a troubleshooting guide for etcd performance issues
```

```
Write an Ansible playbook that validates NTP sync across all nodes
```

```
Add an example for ArgoCD ApplicationSet with cluster generators
```

### Pattern 3: Research + Creation

Combine external research with workspace creation:

```
/research:technical Kubernetes gateway API

Then create an example configuration for this workspace
```

### Pattern 4: Refinement

Iterate on existing content:

```
The retry pattern in ansible-examples/001 needs to handle connection timeouts differently
```

```
Update the CSR troubleshooting guide to include automatic approval scenarios
```

### Pattern 5: Planning

Structure complex work:

```
/create-plan

Migrate our existing Helm deployments to ArgoCD app-of-apps pattern
with support for multiple environments (dev, staging, prod)
```

### Pattern 6: Debugging

Systematic investigation:

```
/debug

My ArgoCD application shows "OutOfSync" but the diff looks empty.
The app uses Helm with values from a ConfigMap.
```

## Working with Agents and Subagents

### What Are Subagents?

Subagents are specialized AI workers that handle specific tasks autonomously. They run in parallel, have focused capabilities, and return results to the main conversation.

### When Subagents Are Used

The agent automatically spawns subagents for:

- **Parallel searches** - Searching multiple directories simultaneously
- **Code review** - Analyzing changes across multiple files
- **Research tasks** - Investigating topics while you continue working
- **Audit tasks** - Evaluating skills, commands, or configurations

### Requesting Subagent Work

You can explicitly request parallel work:

```
Search for all uses of "targetRevision" across the ArgoCD examples
and also check if we have any documentation about revision pinning
```

```
Audit all the skills in .cursor/skills/ for best practices compliance
```

### Audit Subagents

Three specialized auditors are available:

```
/audit-skill .cursor/skills/debug-like-expert/SKILL.md
```

```
/audit-slash-command .cursor/commands/create-plan.md
```

```
/audit-subagent .cursor/agents/skill-auditor.md
```

## Effective Usage Tips

### For Discovery

1. **Be specific about what you're looking for**
   - Good: "Ansible pattern for idempotent file creation with backup"
   - Less good: "Ansible file examples"

2. **Mention the technology stack**
   - "OpenShift 4.14 with OVN-Kubernetes networking"
   - "RHACM 2.9 policy for secret distribution"

3. **Reference existing content when relevant**
   - "Similar to the retry pattern in ansible-examples/001, but for HTTP calls"

### For Creation

1. **Provide context about the use case**
   - "For bare-metal clusters provisioned with the Assisted Installer"
   - "In an air-gapped environment without internet access"

2. **Specify output format if you have preferences**
   - "Create as a troubleshooting guide following our existing format"
   - "Add it to the ansible-examples directory with proper numbering"

3. **Include constraints and requirements**
   - "Must work with Ansible 2.14+"
   - "Should not require cluster-admin privileges"

### For Complex Tasks

1. **Use `/create-plan` first**
   - Breaks down work into phases
   - Creates verification criteria
   - Produces trackable deliverables

2. **Use `/whats-next` when switching context**
   - Captures current state
   - Documents next steps
   - Enables clean handoffs

3. **Load relevant skills for methodology**
   - `/debug` for troubleshooting
   - `@.cursor/skills/create-plans/SKILL.md` for planning

### For Iteration

1. **Reference specific files or sections**
   - "In `ocp-troubleshooting/api-slowness/README.md`, the investigation steps need..."

2. **Explain what's not working**
   - "The playbook fails when the host is unreachable - need better error handling"

3. **Ask for alternatives**
   - "Show me a different approach to this that doesn't require jq"

## Repository Structure

```
ai/
├── ansible-examples/      # Ansible patterns and playbooks
├── argo-examples/         # ArgoCD and GitOps configurations
├── ocp-examples/          # OpenShift cluster configurations
├── ocp-troubleshooting/   # Systematic troubleshooting guides
├── rhacm-examples/        # RHACM multi-cluster management
├── coreos-examples/       # CoreOS/Ignition configurations
├── scripts/               # AI-created utility scripts
│   ├── ansible/           # Ansible utilities
│   └── argocd/            # ArgoCD utilities
├── tools/                 # Standalone utilities
├── external/              # Git submodules (external repos)
│   └── code-for-msps/     # PowerShell scripts for MSPs
├── prompts/               # Saved prompts for reuse
├── analyses/              # Research and analysis outputs
├── labs/                  # Experimental work
├── notes/                 # Reference documentation
├── docs/                  # Additional documentation
└── .cursor/               # Meta-development system
    ├── commands/          # Slash commands
    ├── skills/            # Deep methodology guides
    └── agents/            # Specialized auditors
```

### External Repositories

The `external/` directory contains git submodules. After cloning, initialize them:

```bash
git submodule update --init --recursive
```

See `external/README.md` for usage details.

## Example Sessions

### Session 1: Adding a New Troubleshooting Guide

```
User: Create a troubleshooting guide for worker nodes that won't join the cluster

Agent: [Creates ocp-troubleshooting/worker-node-join-failure/]
       - README.md with symptoms, investigation, resolution
       - diagnostic-commands.sh
       - common-causes.md

User: Add a section about certificate issues - that's usually the cause

Agent: [Updates README.md with certificate-specific section]
       [Adds certificate validation commands]

User: /whats-next

Agent: [Creates handoff document with current state and suggested improvements]
```

### Session 2: Research and Implementation

```
User: /research:technical Kubernetes external secrets operator

Agent: [Researches ESO, returns summary of capabilities and patterns]

User: Now create RHACM policies to deploy ESO across managed clusters

Agent: [Creates rhacm-examples/external-secrets-operator/]
       - install-eso-operator-policy.yaml
       - vault-secretstore-policy.yaml
       - README.md with usage instructions

User: /audit-skill on the new content to check quality

Agent: [Runs audit, suggests improvements]
```

### Session 3: Debugging with Methodology

```
User: /debug

My ArgoCD applications are stuck in "Progressing" state after
upgrading ArgoCD from 2.8 to 2.10. The apps worked fine before.

Agent: [Activates systematic debugging]
       - Gathers evidence (version info, app status, events)
       - Forms hypotheses (sync waves, finalizers, resource hooks)
       - Tests each hypothesis
       - Identifies root cause
       - Documents resolution

User: Can you add this to our troubleshooting guides?

Agent: [Creates ocp-troubleshooting/argocd-stuck-progressing/]
```

## Key Principles

1. **Everything is searchable** - The agent can find and reference any content in the workspace

2. **Creation follows patterns** - New content follows existing conventions (README format, directory structure, naming)

3. **AI disclosure is standard** - All AI-created content includes disclosure notices

4. **Iteration is expected** - First drafts are starting points; refine through conversation

5. **Context matters** - More context leads to better results

## Getting Help

- **Commands reference**: Type `/` in chat to see all slash commands
- **Skills reference**: `@.cursor/README.md` for full documentation
- **Quick start**: `@.cursor/QUICK-START.md` for common patterns
- **Workspace rules**: `.cursorrules` defines workspace conventions

---

AI-DISCLOSURE: This document was created with AI assistance.
