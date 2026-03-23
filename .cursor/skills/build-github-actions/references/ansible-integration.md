# Ansible Integration

<setup>
## Setup Options

### Option 1: Direct Installation
```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'

- name: Install Ansible
  run: pip install ansible ansible-lint
```

### Option 2: Use Action
```yaml
- name: Run playbook
  uses: dawidd6/action-ansible-playbook@v2
  with:
    playbook: site.yml
    inventory: inventory/production
    key: ${{ secrets.SSH_PRIVATE_KEY }}
```
</setup>

<ssh_authentication>
## SSH Authentication

### SSH Key from Secret
```yaml
- name: Setup SSH key
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    ssh-keyscan -H ${{ secrets.TARGET_HOST }} >> ~/.ssh/known_hosts

- name: Run playbook
  run: ansible-playbook -i inventory site.yml
```

### SSH Agent
```yaml
- name: Setup SSH agent
  uses: webfactory/ssh-agent@v0.9.0
  with:
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

- name: Run playbook
  run: ansible-playbook -i inventory site.yml
```

### Disable Host Key Checking (dev only)
```yaml
env:
  ANSIBLE_HOST_KEY_CHECKING: 'false'
```
</ssh_authentication>

<vault_integration>
## Ansible Vault

### Vault Password from Secret
```yaml
- name: Create vault password file
  run: echo "${{ secrets.ANSIBLE_VAULT_PASSWORD }}" > .vault_pass

- name: Run playbook
  run: ansible-playbook --vault-password-file .vault_pass site.yml

- name: Cleanup
  if: always()
  run: rm -f .vault_pass
```

### Vault with Environment Variable
```yaml
- name: Run playbook
  env:
    ANSIBLE_VAULT_PASSWORD: ${{ secrets.ANSIBLE_VAULT_PASSWORD }}
  run: ansible-playbook --vault-password-file <(echo "$ANSIBLE_VAULT_PASSWORD") site.yml
```
</vault_integration>

<inventory_patterns>
## Inventory Patterns

### Static Inventory per Environment
```
inventory/
├── dev
├── staging
└── production
```

```yaml
- name: Run playbook
  run: ansible-playbook -i inventory/${{ inputs.environment }} site.yml
```

### Dynamic Inventory from Secret
```yaml
- name: Create inventory
  run: echo "${{ secrets.ANSIBLE_INVENTORY }}" > inventory.yml

- name: Run playbook
  run: ansible-playbook -i inventory.yml site.yml
```

### AWS Dynamic Inventory
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: us-east-1

- name: Run with AWS inventory
  run: ansible-playbook -i aws_ec2.yml site.yml
```
</inventory_patterns>

<extra_vars>
## Extra Variables

### From Workflow Inputs
```yaml
- name: Run playbook
  run: |
    ansible-playbook site.yml \
      --extra-vars "env=${{ inputs.environment }}" \
      --extra-vars "version=${{ github.sha }}" \
      --extra-vars "deployed_by=github-actions"
```

### From JSON
```yaml
- name: Run playbook
  run: |
    ansible-playbook site.yml \
      --extra-vars '${{ toJson(inputs) }}'
```
</extra_vars>

<complete_example>
## Complete Deployment Example

```yaml
name: Ansible Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options: [dev, staging, prod]
      playbook:
        description: 'Playbook to run'
        required: true
        default: 'deploy.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install Ansible
        run: pip install ansible
      
      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          echo "${{ secrets.SSH_KNOWN_HOSTS }}" >> ~/.ssh/known_hosts
      
      - name: Create vault password file
        run: echo "${{ secrets.ANSIBLE_VAULT_PASSWORD }}" > .vault_pass
      
      - name: Run playbook
        run: |
          ansible-playbook \
            -i inventory/${{ inputs.environment }} \
            --vault-password-file .vault_pass \
            --extra-vars "version=${{ github.sha }}" \
            ${{ inputs.playbook }}
      
      - name: Cleanup secrets
        if: always()
        run: |
          rm -f ~/.ssh/id_rsa .vault_pass
```
</complete_example>

<linting>
## Ansible Lint in CI

```yaml
- name: Install ansible-lint
  run: pip install ansible-lint

- name: Lint playbooks
  run: ansible-lint site.yml roles/
```
</linting>
