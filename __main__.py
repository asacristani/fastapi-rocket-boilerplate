"""A Google Cloud Python Pulumi program"""

import pulumi
import pulumi_gcp as gcp
import pulumi_kubernetes as k8s
from pulumi_gcp import storage

# SET YOUR VARIABLES
db_instance_name = "instance"
region = "us-central1"
db_tier = "db-f1-micro"
db_user = "myuser"
db_password = "mypassword"


# See versions at https://registry.terraform.io
# /providers/hashicorp/google/latest/docs/resources
# /sql_database_instance#database_version
instance = gcp.sql.DatabaseInstance(
    db_instance_name,
    region=region,
    database_version="POSTGRES_15",
    settings=gcp.sql.DatabaseInstanceSettingsArgs(
        tier=db_tier,
    ),
    deletion_protection=True,
)

database_user = gcp.sql.User(
    db_user, instance=instance.name, password=db_password
)

database = gcp.sql.Database("database", instance=instance.name)

# Create a GCP resource (Storage Bucket)
bucket = storage.Bucket("my-bucket", location="US")

# Export the DNS name of the bucket
pulumi.export("bucket_name", bucket.url)


# Define your Google Cloud project
project = "your-gcp-project"
gcp_config = pulumi.Config("gcp")
project = gcp_config.get("project") or project

# Configure the GKE cluster
cluster_name = "my-gke-cluster"
cluster = gcp.container.Cluster(
    cluster_name,
    initial_node_count=1,
    min_master_version="latest",
    node_version="latest",
    project=project,
    location="us-central1",
)

# Use gcp.container.getClusterCredentials to get Kubernetes config
kubeconfig = pulumi.Output.all(cluster.name, project).apply(
    lambda args: gcp.container.get_cluster_credentials(
        cluster_name=args[0], project=args[1]
    )
)

# Define the configuration for your Kubernetes services

# App Deployment
app_deployment = k8s.apps.v1.Deployment(
    "app-deployment",
    metadata={
        "name": "app-deployment",
    },
    spec={
        "replicas": 2,
        "selector": {
            "matchLabels": {"app": "app"},
        },
        "template": {
            "metadata": {"labels": {"app": "app"}},
            "spec": {
                "containers": [
                    {
                        "name": "app-container",
                        "image": "your-app-image:latest",
                        "ports": [{"containerPort": 8000}],
                        # You can add additional
                        # configurations and resources here
                    }
                ]
            },
        },
    },
)

# Celery Deployment
celery_deployment = k8s.apps.v1.Deployment(
    "celery-deployment",
    metadata={
        "name": "celery-deployment",
    },
    spec={
        "replicas": 2,  # Adjust as needed
        "selector": {
            "matchLabels": {"app": "celery"},
        },
        "template": {
            "metadata": {"labels": {"app": "celery"}},
            "spec": {
                "containers": [
                    {
                        "name": "celery-container",
                        "image": "your-celery-image:latest",
                        # Add any necessary command and args here
                        # You can add additional configurations
                        # and resources here
                    }
                ]
            },
        },
    },
)

# Redis Deployment
redis_deployment = k8s.apps.v1.Deployment(
    "redis-deployment",
    metadata={
        "name": "redis-deployment",
    },
    spec={
        "replicas": 1,  # Redis is typically deployed with a single node
        "selector": {
            "matchLabels": {"app": "redis"},
        },
        "template": {
            "metadata": {"labels": {"app": "redis"}},
            "spec": {
                "containers": [
                    {
                        "name": "redis-container",
                        "image": "redis:latest",
                        "ports": [{"containerPort": 6379}],
                        # You can add additional configurations
                        # and resources here
                    }
                ]
            },
        },
    },
)

# RabbitMQ Deployment
rabbitmq_deployment = k8s.apps.v1.Deployment(
    "rabbitmq-deployment",
    metadata={
        "name": "rabbitmq-deployment",
    },
    spec={
        "replicas": 1,  # RabbitMQ is typically deployed with a single node
        "selector": {
            "matchLabels": {"app": "rabbitmq"},
        },
        "template": {
            "metadata": {"labels": {"app": "rabbitmq"}},
            "spec": {
                "containers": [
                    {
                        "name": "rabbitmq-container",
                        "image": "rabbitmq:3.6-management",
                        "ports": [
                            {"containerPort": 5672},
                            {"containerPort": 15672},
                        ],  # RabbitMQ ports
                        # You can add additional configurations
                        # and resources here
                    }
                ]
            },
        },
    },
)

# Export useful information
pulumi.export("cluster_name", cluster.name)
pulumi.export("kubeconfig", cluster.kube_config)

# Deploy the infrastructure
pulumi.export("app_deployment", app_deployment.metadata)
pulumi.export("celery_deployment", celery_deployment.metadata)
pulumi.export("redis_deployment", redis_deployment.metadata)
pulumi.export("rabbitmq_deployment", rabbitmq_deployment.metadata)
