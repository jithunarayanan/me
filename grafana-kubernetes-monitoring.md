
# Grafana Kubernetes Monitoring Setup Guide

## Getting Started

### Install Helm

```sh
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

### Helm Chart

We will use the `kube-prometheus-stack` Helm chart to install Grafana, Prometheus, and Alertmanager.

Check your Helm version:

```sh
helm version
# Example output:
# version.BuildInfo{Version:"v3.8.0", GitCommit:"d14138609b01886f544b2025f5000351c9eb092e", GitTreeState:"clean", GoVersion:"go1.17.5"}
```

### Add Helm Repository

```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### Create a Namespace

```sh
kubectl create namespace monitoring
```

### Create a Kubernetes Secret

```sh
kubectl create secret generic grafana-admin-credentials \
    --from-literal=username=admin \
    --from-literal=password=Admin@123 \
    -n monitoring
```

### Verify Your Secret

```sh
kubectl describe secret -n monitoring grafana-admin-credentials
```

You should see output similar to:

```
Name:         grafana-admin-credentials
Namespace:    monitoring
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
admin-password:  9 bytes
admin-user:      9 bytes
```

#### Verify the Username

```sh
kubectl get secret -n monitoring grafana-admin-credentials -o jsonpath="{.data.admin-user}" | base64 --decode
```

Expected output:

```
admin
```

#### Verify the Password

Use the same method as above, replacing `admin-user` with `admin-password`.

### Edit Values File

Create or edit your `values.yaml` file:

```sh
nano values.yaml
```

Paste in values from [`../values.yaml`](../values.yaml).

### Install kube-prometheus-stack

```sh
helm install -n monitoring prometheus prometheus-community/kube-prometheus-stack -f values.yaml
```

### Expose Grafana

To expose Grafana, you can patch the service or use port-forwarding:

**Option 1: Patch Service to LoadBalancer**

```sh
kubectl patch svc grafana-server -n monitoring -p '{"spec": {"type": "LoadBalancer"}}'
```

**Option 2: Port Forward**

```sh
kubectl port-forward -n monitoring <grafana-pod-name> 52222:3000
# Replace <grafana-pod-name> with your actual pod name
```

### Access Grafana

- Via LoadBalancer: `http://<loadbalancer_dns_name>`
- Via Port Forward: `http://localhost:52222`

### Upgrade the Stack

If you make changes to your `values.yaml`, deploy the updates with:

```sh
helm upgrade -n monitoring prometheus prometheus-community/kube-prometheus-stack -f values.yaml
```

---

## Useful Links

- [Helm Documentation](https://helm.sh/docs/)
- [kube-prometheus-stack Chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
