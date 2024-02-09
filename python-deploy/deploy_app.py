from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (
        ContainerGroup,
        Container,
        ContainerPort,
        ImageRegistryCredential,
        ResourceRequests,
        ResourceRequirements,
        OperatingSystemTypes
)

import os

name = 'DailyFortuneV2'
resource_group_name = f"{name}_RGN"
container_group_name = f"{name}_CGN"
container_name = f"{name}_CN"
container_image = ''    # TODO path to the container in the container registry

credentials = DefaultAzureCredential()
subscription_id = "4c9e9e55-06ef-4fed-8a11-9a545431049c"    # TODO: Look up on the internet

# Define container service client
client = ContainerServiceClient(credentials, subscription_id)

# Initialize the Container Instance Management Client
container_instance_client = ContainerInstanceManagementClient(credentials, subscription_id)

container_resource_request = ResourceRequests(memory_in_gb=1, cpu=1)
container_resource_requirements = ResourceRequirements(requests=container_resource_request)
container_port = ContainerPort(port=80)
container = Container(name=container_name, image=container_image, resources=container_resource_requirements, ports=[container_port])
container_group = ContainerGroup(location='northeurope', containers=[container], os_type=OperatingSystemTypes.linux)

tenant_id = os.environ['ATID']
client_id = os.environ['ACID']
client_secret = os.environ['ACS']

response = container_instance_client.container_groups.begin_create_or_update(resource_group_name, container_group_name, container_group)
# from IPython import embd; embed()
print(response.result)


"""
RES_GROUP=$ACR_NAME # Resource Group name

az group create --resource-group $RES_GROUP --location eastus
az acr create --resource-group $RES_GROUP --name $ACR_NAME --sku Standard --location eastus
"""


"""
az acr build --registry $ACR_NAME --image helloacrtasks:v1 --file /path/to/Dockerfile /path/to/build/context.
"""

"""
AKV_NAME=$ACR_NAME-vault

az keyvault create --resource-group $RES_GROUP --name $AKV_NAME
"""


"""
# Create service principal, store its password in AKV (the registry *password*)
az keyvault secret set \
  --vault-name $AKV_NAME \
  --name $ACR_NAME-pull-pwd \
  --value $(az ad sp create-for-rbac \
                --name $ACR_NAME-pull \
                --scopes $(az acr show --name $ACR_NAME --query id --output tsv) \
                --role acrpull \
                --query password \
                --output tsv)
"""

"""
# Store service principal ID in AKV (the registry *username*)
az keyvault secret set \
    --vault-name $AKV_NAME \
    --name $ACR_NAME-pull-usr \
    --value $(az ad sp list --display-name $ACR_NAME-pull --query [].appId --output tsv)
"""
