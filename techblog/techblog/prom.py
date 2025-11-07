import requests
from django.http import JsonResponse
import os
from django.conf import settings 

PROMETHEUS_URL = settings.PROMETHEUS_URL

class PrometheusClient:
    """A client to fetch metrics from Prometheus API."""

    def __init__(self, base_url=PROMETHEUS_URL):
        self.base_url = base_url

    def query(self, metric_name):
        """Fetch metrics from Prometheus API."""
        query_url = f"{self.base_url}/api/v1/query"
        params = {"query": metric_name}

        try:
            response = requests.get(query_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data["status"] == "success":
                return data["data"]["result"]
            else:
                return {"error": data.get("error", "Unknown error")}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_cluster_metrics(self):
        """Fetch key cluster metrics."""
        return {
            "running_pods": self.query("count(kube_pod_container_status_running)"),
            "running_nodes": self.query("count(kube_node_info)"),
            "cpu_cores": self.query("sum(machine_cpu_cores)"),
            "memory_total": self.query("sum(node_memory_MemTotal_bytes/1024/1024/1024)"),
            "memory_free": self.query("sum(node_memory_MemFree_bytes/1024/1024/1024)"),
        }