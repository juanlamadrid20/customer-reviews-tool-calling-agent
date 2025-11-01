# About

Sample project using Databricks GenAI to build a agentic chatbot for Amazon reviews.

## Build and Deploy

This project uses Databricks Asset Bundles to deploy the Lakehouse App. 

### Prerequisites

- Databricks CLI installed and authenticated
- Access to the target Databricks workspace
- Serving endpoint `agents_juan_dev-genai-amazon_review_agent` must exist (created via agent deployment)

### Configuration

The app configuration is defined in `databricks.yml`. Key variables:
- `app_name`: App name (default: "amazon-customer-reviews-app")
- `model_endpoint_name`: Serving endpoint name (default: "agents_juan_dev-genai-amazon_review_agent")
- `user_name`: User with app permissions (default: "juan.lamadrid@databricks.com")

### Deployment Steps

1. **Deploy the bundle configuration:**
   ```bash
   databricks bundle deploy
   ```
   
   This uploads bundle files and deploys the app resource configuration.

2. **Run/Start the app:**
   ```bash
   databricks bundle run customer-reviews-app
   ```
   
   This command:
   - Checks app status
   - Prepares source code for deployment
   - Installs packages from `requirements.txt`
   - Starts the Streamlit app
   - Provides the app URL

3. **Access the app:**
   The app URL will be displayed after successful deployment. You can also find it in the Databricks workspace under Apps.

### Updating the App

After making changes to the app source code in `03-app/src/`:
1. Deploy the bundle: `databricks bundle deploy`
2. Run the app again: `databricks bundle run customer-reviews-app`

The app will redeploy with the latest source code.

# TODO

- [ ] remove hard coded 3 level namespace; use config notebook pattern
- [ ] add genie room agent
- [ ] examples (screenshots) showing playground (tool evaluation) showing review app.
- [ ] postman collection for testing the agentic chatbot
