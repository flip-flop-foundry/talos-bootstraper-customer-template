# PLACEHOLDER_APP

Your application is hosted on a Kubernetes cluster managed by GitOps.
This repository is the single source of truth for both your application code and its deployment configuration.

- **Live URL:** `https://PLACEHOLDER_INGRESS_HOST`
- **Gitea org:** `PLACEHOLDER_ORG`
- **Kubernetes namespace:** `PLACEHOLDER_NAMESPACE`
- **ArgoCD project:** `customer-PLACEHOLDER_CUSTOMER_NAME`

---

## How it works

```
You push to main
      │
      ▼
Gitea Actions CI pipeline (this repo, .gitea/workflows/)
  1. Builds a Docker image
  2. Pushes to the Gitea container registry (PLACEHOLDER_GITEA_DOMAIN/PLACEHOLDER_ORG/PLACEHOLDER_APP)
  3. Triggers kubectl rollout restart → new pod picks up the fresh image
      │
      ▼
ArgoCD watches deploy/ in this repo
  → Applies any manifest changes automatically
  → Your app is live at https://PLACEHOLDER_INGRESS_HOST
```

---

## Repository structure

```
PLACEHOLDER_APP/
├── src/                        Application source code
├── Dockerfile                  Builds the container image
├── deploy/                     Kubernetes manifests (synced by ArgoCD)
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingressroute.yaml
└── .gitea/workflows/
    └── build-and-deploy.yaml   CI/CD pipeline
```

**ArgoCD deploys everything in `deploy/` automatically.** Adding or modifying a manifest file and pushing to `main` is all it takes.

---

## Adding a new application repository

Any repository you create in the `PLACEHOLDER_ORG` Gitea organisation that contains a `deploy/` directory will be **automatically discovered and deployed** by ArgoCD — no extra configuration required.

The namespace will be `PLACEHOLDER_ORG-<repoName>`. Contact the cluster operator to:
- Have the namespace and RBAC created
- Have the repo-level CI variables (`REGISTRY_DOMAIN`, `CUSTOMER_ORG`, `APP_NAME`, `NAMESPACE`) set for the new repo
- Have the `gitea-registry-pull` imagePullSecret created in the new namespace

---

## CI pipeline — secrets and variables

These are already configured on this repository. You should not need to change them unless you are setting up a **new** repo from scratch.

### Org-level secrets (inherited by every repo in `PLACEHOLDER_ORG`)

| Secret | Description |
|--------|-------------|
| `CI_REGISTRY_TOKEN` | Token for `docker push` to the Gitea container registry |
| `CI_REGISTRY_USER` | Username for the CI service account |

### Repo-level variables (this repo)

| Variable | Value |
|----------|-------|
| `REGISTRY_DOMAIN` | `PLACEHOLDER_GITEA_DOMAIN` |
| `CUSTOMER_ORG` | `PLACEHOLDER_ORG` |
| `APP_NAME` | `PLACEHOLDER_APP` |
| `NAMESPACE` | `PLACEHOLDER_NAMESPACE` |

---

## Kubernetes manifests (`deploy/`)

Your manifests are applied as-is by ArgoCD. They must target the `PLACEHOLDER_NAMESPACE` namespace.

The container image reference in `deploy/deployment.yaml` is:
```
PLACEHOLDER_GITEA_DOMAIN/PLACEHOLDER_ORG/PLACEHOLDER_APP:latest
```

**Image pull auth is handled automatically** — no `imagePullSecrets` block is needed in your Deployment.

### ArgoCD project restrictions

Your Applications run under the `customer-PLACEHOLDER_CUSTOMER_NAME` ArgoCD project, which enforces:
- Source repos must be in `https://PLACEHOLDER_GITEA_DOMAIN/PLACEHOLDER_ORG/*`
- Deployments may only target `PLACEHOLDER_ORG-*` namespaces
- Cluster-scoped resources are not permitted

You do not need to reference the project in your manifests.

---

## Ingress

The app is exposed via a standard Kubernetes `Ingress` in `deploy/ingress.yaml` at:

```
https://PLACEHOLDER_INGRESS_HOST
```

The hostname format is `<org>-<repo>.<clusterDomain>` (e.g. `PLACEHOLDER_NAMESPACE.PLACEHOLDER_CLUSTER_DOMAIN`), which is unique across all customer orgs and repos on the cluster. cert-manager and external-dns are configured via annotations on the Ingress resource.

To add a second hostname or path, edit `deploy/ingress.yaml` and push. ArgoCD will apply the change within a few minutes.

---

## CI/CD — how the runner authenticates with Kubernetes

The Gitea Actions runner runs as a pod inside the cluster using the `gitea-runner-service-account`. This service account has the following permissions in the `PLACEHOLDER_NAMESPACE` namespace:

| Resource | Verbs |
|----------|-------|
| `apps/deployments` | `get`, `list`, `patch` |

The runner's init container injects the service account token into the job environment as `KUBE_SA_TOKEN`, along with `KUBERNETES_SERVICE_HOST` and `KUBERNETES_SERVICE_PORT`. The CI workflow uses these to call `kubectl rollout restart` without any additional kubeconfig setup.

---

## Local development

```bash
cd src
pip install -r requirements.txt
APP_NAME=PLACEHOLDER_APP APP_VERSION=dev python app.py
```

Then open <http://localhost:8080>.
