# Homepage Dashboard - EGI Cloud

This repository contains the configuration and Helm chart for the EGI Cloud Homepage dashboard.

**Production URLs**: 
- [https://home.cloud.egi.eu](https://home.cloud.egi.eu) (Primary)
- [https://homepage.dyn.cloud.e-infra.cz](https://homepage.dyn.cloud.e-infra.cz) (Legacy/Alternative)

## Project Structure

- `chart/`: A simplified, local Helm chart for migrating and managing Homepage.
  - `values.yaml`: The primary configuration file where you define all services, widgets, and settings.
  - `templates/configmap.yaml`: Dynamically generates the ConfigMap from `values.yaml`.
  - `templates/deployment.yaml`: Deploys the application with optimized persistent storage (initContainer + emptyDir) and security settings.

## Getting Started

### Prerequisites

- A Kubernetes cluster.
- Helm installed.
- Proper namespace context (e.g., `torre-ns`).

### Configuration

All configuration is managed within the `chart/values.yaml` file. You can customize:
- **Services**: Define the links and icons for the dashboard.
- **Widgets**: Configure cluster info, search, and resources.
- **Ingress**: Set your hostname and TLS settings.
- **Security**: Pod security contexts are pre-configured to follow cluster `restricted` policies.

### Installation / Upgrade

To deploy or update the dashboard, run the following command from the repository root:

```bash
helm upgrade --install homepage ./chart -f ./chart/values.yaml -n torre-ns
```

## Troubleshooting

If the service doesn't respond or shows a 503 error:

```bash
# Check pod status and restarts
kubectl get pods -n torre-ns -l app.kubernetes.io/name=homepage

# View pod logs (check for EACCES or EROFS errors)
kubectl logs deployment/homepage -n torre-ns

# Check Ingress and Certificate status
kubectl get ingress,certificate -n torre-ns
```

### Manual Configuration Refresh
If changes in `values.yaml` are applied but not reflected, you can force a restart:
```bash
kubectl rollout restart deployment homepage -n torre-ns
```

---
*Maintained by the EGI Cloud Team.*

## Development & Automation

### Automated Workflow (Recommended)
This project uses GitHub Actions ([update-helm-chart.yml](.github/workflows/update-helm-chart.yml)) for a full CI/CD pipeline:
1.  **Version Bump**: Automatically increments the chart version on every push to `main`.
2.  **Linting**: Validates the Helm chart before any action.
3.  **Deployment**: Automatically deploys the update to the `torre-ns` namespace.
4.  **Automatic Rollback**: The deployment uses the `--atomic` flag. If the new version fails to start correctly (e.g., a crash loop), Helm will automatically roll back to the previous stable version.

> [!IMPORTANT]
> To enable automation, ensure you have added a `KUBECONFIG` secret (base64 encoded) to your GitHub repository settings.

### Manual Operations

#### Deploy / Update
If you need to deploy manually from your local machine:
```bash
helm upgrade --install homepage ./chart -f ./chart/values.yaml -n torre-ns --atomic --wait
```

#### Monitoring & History
To see the deployment history and find revision numbers:
```bash
helm history homepage -n torre-ns
```

#### Manual Rollback
If you need to revert to a specific previous version manually:
```bash
# Rollback to the immediate previous version
helm rollback homepage -n torre-ns

# Rollback to a specific revision (e.g., revision 5)
helm rollback homepage 5 -n torre-ns
```
