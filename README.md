# Homepage Deployment on Kubernetes

Setup and deployment of the Homepage service in Rancher (CESNET).

## Components

- **Deployment**: `homepage-deployment.yaml`
  - Image: `ghcr.io/gethomepage/homepage:latest`
  - Container port: `3000`
  - Security context:
    - `runAsNonRoot: true`
    - `allowPrivilegeEscalation: false`
    - `capabilities.drop: ["ALL"]`
    - `seccompProfile: RuntimeDefault`
  - Volumes:
    - `homepage-config` (ConfigMap) mounted at `/app/config`
      - Read-only configuration files, populated by ConfigMap
    - `homepage-logs` (PVC) mounted at `/app/config/logs`
      - Writable logs directory
    - homepage-icons (PVC) mounted at `/app/public/icons`
      - Custom icons added manually
  - InitContainer: copies required config files from `/app/src/skeleton` to `/app/config` if missing

- **ConfigMap**: `homepage-configmap.yaml`
  - Contains homepage configuration files:
    - `bookmarks.yaml`
    - `services.yaml`
    - `settings.yaml`
    - `widgets.yaml`
  - Updates to ConfigMap require pod restart to take effect.

    ```sh
    kubectl rollout restart deployment homepage
    ```

- **PersistentVolumeClaim**:
  - `homepage-logs-pvc.yaml`
    - Stores logs and writable configuration files.
    - Mounted at `/app/config/logs` in the container.
  - `homepage-icons-pvc.yaml`
    - Stores manually added icons.

- **Service**: `homepage-service.yaml`
  - Exposes the container on port `3000` internally in the cluster.

- **ServiceAccount** and **Secret**
  - Provide required permissions for accessing the cluster.

## Deployment

Apply all resources in the correct order:

```bash
kubectl apply -f homepage-logs-pvc.yaml
kubectl apply -f homepage-icons-pvc.yaml
kubectl apply -f homepage-configmap.yaml
kubectl apply -f homepage-deployment.yaml
kubectl apply -f homepage-service.yaml
kubectl apply -f homepage-serviceaccount.yaml
```

## Accessing the service
Since the service is internal, you can port-forward to localhost:

```bash
kubectl port-forward service/homepage 3000:3000 -n namespace
```

Then access Homepage at http://localhost:3000.

## Modifying Homepage Configuration
1. Edit the ConfigMap:

```bash
kubectl edit configmap homepage-config -n namespace
```
1. After saving changes, restart the pod to pick up the new configuration:

```bash
kubectl delete pod -l app=homepage -n namespace
```
The pod will recreate with the updated configuration.

## Adding Custom Icons

1. Copy your icons into the PVC mounted at /app/public/icons using a temporary pod:

    ```bash
    kubectl run -i --tty temp-copy --rm --image=busybox --restart=Never -n namespace -- /bin/sh
    # Mount the PVC at /icons inside this pod
    # Copy your icon files to /icons
    ```

1. Restart the Homepage pod if needed. The new icons will be available in the UI.
