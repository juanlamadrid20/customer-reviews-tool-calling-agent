# Databricks notebook source
import requests
import json
import time
from databricks.sdk.core import Config

# COMMAND ----------


cfg = Config()
host = cfg.host
headers = cfg.authenticate()

# COMMAND ----------

app_name = "amazon-customer-reviews-app"

# COMMAND ----------

app_description = "Product Reviews powered by Genie."
print("app_name: ", app_name, "\n", "app_description: ", app_description, sep="")

# COMMAND ----------

def get_app_info(app_name):
    response = requests.get(f"{host}/api/2.0/apps/get?name={app_name}", headers=headers)
    return response.json()

print(get_app_info(app_name))

# COMMAND ----------

def create_app(app_name, host, headers):
    url = host + "/api/2.0/apps"
    data = {
        "name": app_name,
        "description": app_description
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
  
create_app(app_name, host, headers)

# COMMAND ----------

# MAGIC %md
# MAGIC Checking the app identity creation
# MAGIC The create API is async, so we need to poll until it's ready.

# COMMAND ----------

def check_app_status(app_name, host, headers):
    url = host + f"/api/2.0/apps/{app_name}"

    for _ in range(20):
        time.sleep(5)
        response = requests.get(url, headers=headers)
        response_dict = json.loads(response.text)
        print(f"Status: ", response_dict)
        if response_dict.get("compute_status").get("state") == "ACTIVE":
            break
    return response_dict

check_app_status(app_name, host, headers)

# COMMAND ----------

# MAGIC %md
# MAGIC Now deploying the app using the created app identity
# MAGIC Deploy starts the pod, downloads the source code, install necessary dependencies, and starts the app.
# MAGIC
# MAGIC Once the app is created, we can deploy the app. This will create a deployment and a compute target for the app.
# MAGIC
# MAGIC The deployment will be in the "In Progress" state until the deployment is ready.
# MAGIC
# MAGIC This can take a few minutes if we have to provision a new container.
# MAGIC
# MAGIC After the container is provisioned, it should only take a few seconds to deploy the app again.

# COMMAND ----------

current_dir = !pwd
current_dir = current_dir[0]
app_dir = f"{current_dir}/src"
print("current_dir: ", current_dir, "\n", "app_dir: ", app_dir, sep="")

# COMMAND ----------

def deploy_app(app_name, host, headers, app_dir):
    url = host + f"/api/2.0/apps/{app_name}/deployments"
    data = {
      "source_code_path": app_dir,
      # "mode": "AUTO_SYNC" # SNAPSHOT is default and AUTO_SYNC is a private preview
    }
    response = requests.post(url, headers=headers, json=data)
    response_dict = json.loads(response.text)
    deployment_id = response_dict.get("deployment_id")
    return response_dict, deployment_id
  

response_dict, deployment_id = deploy_app(app_name, host, headers, app_dir)
print("response_dict: ", response_dict, "\n", "deployment_id: ", deployment_id, sep="")

# COMMAND ----------

# MAGIC %md
# MAGIC Checking the deployment status
# MAGIC The first time the app is deployed, it can take a couple of minutes to deploy the app.
# MAGIC
# MAGIC We will poll for the deployment to complete with the below code

# COMMAND ----------

def check_deployment_status(app_name, host, headers, deployment_id):
    url = host + f"/api/2.0/apps/{app_name}/deployments/{deployment_id}"

    for _ in range(60):
        time.sleep(5)
        response = requests.get(url, headers=headers)
        response_dict = json.loads(response.text)
        status = response_dict.get("status")
        if status and status.get("state") == "SUCCEEDED":
            print(f"Deployment of the app '{app_name}' completed. Status: ", status.get("state"))
            break
        else:
            print(f"Deployment of the app '{app_name}' in progress. Status: ", status.get("state") if status else "Unknown")

check_deployment_status(app_name, host, headers, deployment_id)

# COMMAND ----------


