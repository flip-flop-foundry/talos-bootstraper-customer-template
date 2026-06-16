# Example GitOps Customer

This repository is an example of a GitOps-managed application running on a
Talos Kubernetes cluster. It demonstrates the full end-to-end flow:

1. **Code** lives in this Gitea repository
2. **CI** (Gitea Actions) builds a Docker image and pushes it to the Gitea container registry
3. **CD** (ArgoCD via ApplicationSet) picks up the `deploy/` manifests and keeps the cluster in sync
4. **Rollout** — after each image push the runner's Kubernetes service account triggers a rolling restart

## Repository Variables (set by `bootstrap-customer.sh`)

| Variable | Description |
|---|---|
| `GITEA_DOMAIN` | Gitea instance hostname |
| `CUSTOMER_ORG` | Gitea org that owns this repo |
| `APP_NAME` | Application / Deployment name |
| `NAMESPACE` | Kubernetes namespace |

## How the CI workflow uses Kubernetes

The `gitea-runner-service-account` runs the act_runner pod inside the cluster.
The runner's `saveEnvs` initContainer writes the service account token to the
job container's `.env` file, making these variables available to every workflow step:

| Variable | Value |
|---|---|
| `KUBERNETES_SERVICE_HOST` | Cluster API server address |
| `KUBERNETES_SERVICE_PORT` | Cluster API server port |
| `KUBE_SA_TOKEN` | Bearer token for `gitea-runner-service-account` |

`bootstrap-customer.sh` creates a `Role` + `RoleBinding` in the customer namespace
so the runner SA can `patch` / `get` the Deployment (enough for `kubectl rollout restart`).

## ArgoCD Integration

This repo is discovered automatically by the `customer-apps` ApplicationSet, which
polls the Gitea customer org for repositories that contain a `deploy/` directory.
The ApplicationSet creates an ArgoCD `Application` pointing at `deploy/` for each
matching repo.

## Local development

```bash
cd src
pip install -r requirements.txt
APP_NAME=hello-world APP_VERSION=dev python app.py
```

Then open <http://localhost:8080>.
