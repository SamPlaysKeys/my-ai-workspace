# Container Operations

<docker_build>
## Docker Build and Push

### Basic Build and Push
```yaml
- name: Login to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### With Caching
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Multi-Architecture
```yaml
- name: Set up QEMU
  uses: docker/setup-qemu-action@v3

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### Multiple Tags
```yaml
- name: Docker metadata
  id: meta
  uses: docker/metadata-action@v5
  with:
    images: ghcr.io/${{ github.repository }}
    tags: |
      type=sha
      type=ref,event=branch
      type=semver,pattern={{version}}
      type=raw,value=latest,enable={{is_default_branch}}

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
```
</docker_build>

<registry_auth>
## Registry Authentication

### GitHub Container Registry (GHCR)
```yaml
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

### Docker Hub
```yaml
- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

### Quay.io
```yaml
- uses: docker/login-action@v3
  with:
    registry: quay.io
    username: ${{ secrets.QUAY_USERNAME }}
    password: ${{ secrets.QUAY_PASSWORD }}
```

### AWS ECR
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: us-east-1

- name: Login to ECR
  uses: aws-actions/amazon-ecr-login@v2
```

### Azure ACR
```yaml
- uses: docker/login-action@v3
  with:
    registry: ${{ secrets.ACR_REGISTRY }}
    username: ${{ secrets.ACR_USERNAME }}
    password: ${{ secrets.ACR_PASSWORD }}
```
</registry_auth>

<image_scanning>
## Image Scanning

### Trivy
```yaml
- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload scan results
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results.sarif'
```

### Grype
```yaml
- name: Scan image
  uses: anchore/scan-action@v3
  with:
    image: ghcr.io/${{ github.repository }}:${{ github.sha }}
    fail-build: true
    severity-cutoff: high
```
</image_scanning>

<host_operations>
## Docker Host Operations

### Rebuild Docker Host via SSH
```yaml
- name: Rebuild Docker host
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.DOCKER_HOST }}
    username: ${{ secrets.DOCKER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      docker pull ghcr.io/${{ github.repository }}:${{ github.sha }}
      docker stop myapp || true
      docker rm myapp || true
      docker run -d --name myapp \
        -p 80:8080 \
        --restart unless-stopped \
        ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### Docker Compose Deploy
```yaml
- name: Deploy with docker-compose
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.DOCKER_HOST }}
    username: ${{ secrets.DOCKER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /opt/myapp
      export IMAGE_TAG=${{ github.sha }}
      docker-compose pull
      docker-compose up -d
```

### Prune Old Images
```yaml
- name: Cleanup old images
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.DOCKER_HOST }}
    username: ${{ secrets.DOCKER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      docker image prune -af --filter "until=168h"
```
</host_operations>

<complete_example>
## Complete Build and Deploy Example

```yaml
name: Build and Deploy Container

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image: ${{ steps.meta.outputs.tags }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha
            type=raw,value=latest
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Scan image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
          exit-code: '1'
          severity: 'CRITICAL,HIGH'

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Deploy to Docker host
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.DOCKER_HOST }}
          username: ${{ secrets.DOCKER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            docker pull ghcr.io/${{ github.repository }}:${{ github.sha }}
            docker stop myapp || true
            docker rm myapp || true
            docker run -d --name myapp \
              -p 80:8080 \
              --restart unless-stopped \
              ghcr.io/${{ github.repository }}:${{ github.sha }}
```
</complete_example>
