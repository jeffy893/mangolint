#!/usr/bin/env python3
"""
Generate AWS Architecture Diagram for Mangolint
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.network import ELB, CloudFront
from diagrams.aws.ml import Bedrock
from diagrams.aws.security import IAM, SecretsManager
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python

# Set diagram attributes
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
}

with Diagram("Mangolint AWS Architecture", 
             filename="architecture-diagram",
             show=False,
             direction="LR",
             graph_attr=graph_attr):
    
    users = Users("Users/Browsers")
    
    with Cluster("Application Layer"):
        with Cluster("Flask Web App"):
            flask_app = Flask("Mangolint\nFlask App")
            python_linter = Python("Linter Module\n(boto3)")
    
    with Cluster("AWS Cloud"):
        with Cluster("Security & Config"):
            iam = IAM("IAM Roles\n& Policies")
            credentials = SecretsManager("AWS Credentials\n~/.aws/credentials")
        
        with Cluster("AI/ML Services"):
            bedrock = Bedrock("Amazon Bedrock\nClaude 3 Sonnet")
        
        with Cluster("Optional: Static Assets"):
            s3 = S3("S3 Bucket\n(CSS/JS/Images)")
    
    # User flow
    users >> Edge(label="HTTP Request") >> flask_app
    flask_app >> Edge(label="Response\n(HTML/JSON)") >> users
    
    # Application to AWS
    flask_app >> python_linter
    python_linter >> Edge(label="boto3 SDK") >> iam
    iam >> Edge(label="Authenticate") >> credentials
    python_linter >> Edge(label="invoke_model()\nClaude 3 API", color="purple") >> bedrock
    bedrock >> Edge(label="AI Analysis\n(Indigenous Terms)", color="purple") >> python_linter
    
    # Static assets (optional)
    flask_app - Edge(label="Serve Static", style="dashed") - s3

print("Architecture diagram generated: architecture-diagram.png")
