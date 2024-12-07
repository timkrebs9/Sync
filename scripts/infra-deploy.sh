# Login to Azure
az login

# Create a resource group
az group create --name sync-rg --location eastus

# Create Azure Container Registry
az acr create --resource-group sync-rg --name syncregistry --sku Basic

# Enable admin access
az acr update -n syncregistry --admin-enabled true

# Build and push to ACR
az acr build --registry syncregistry --image sync-api:v1 .

# Create App Service plan
az appservice plan create --name sync-plan --resource-group sync-rg --is-linux --sku B1

# Create Web App
az webapp create --resource-group sync-rg --plan sync-plan --name sync-api --deployment-container-image-name syncregistry.azurecr.io sync-api:v1