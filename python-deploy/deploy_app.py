from azure.identity import DefaultAzureCredential, ClientSecretCredential, AzureCliCredential

from azure.mgmt.resource import ResourceManagementClient

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
from dotenv import load_dotenv
import os
name = 'fortunecookiev3'


resource_group_name = f"{name}-rg"
container_group_name = f"{name}-cgn"  # there may be no upper cases and no underscores in the names
container_name = f"{name}-cn"
container_image = ''    # TODO path to the container in the container registry

# this loads the credentials from the environment variables
credentials = DefaultAzureCredential()

# cli_credentials = AzureCliCredential()
# this is not necessary, we can instead just use the DefaultAzureCredential

# NOTE we need to create an Applictation manually first in the Azure Portal
# NOTE add a 'role assigment' for the Application in the Azure Portal.
# To do this, we set the application name as 'highly privileged' in the role assigment

load_dotenv("azure_credentials.env")

client_id = os.environ['AZURE_CLIENT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
tenant_id = os.environ['AZURE_TENANT_ID']  # os.environ['ATID']  # found under Microsoft Entra ID in Azure Portal
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]    # search for subscription_id in the azure portal

# check that the variables are all set:
assert all([client_id, client_secret, tenant_id, subscription_id])

# create a Resource Management client
resource_client = ResourceManagementClient(credential=credentials, subscription_id=subscription_id)
rg_result = resource_client.resource_groups.create_or_update(
    resource_group_name, {'location': 'northeurope'})  # type: ignore

# Define container service client
client = ContainerServiceClient(credentials, subscription_id)

# Initialize the Container Instance Management Client
container_instance_client = ContainerInstanceManagementClient(credentials, subscription_id)

container_resource_request = ResourceRequests(memory_in_gb=1, cpu=1)
container_resource_requirements = ResourceRequirements(requests=container_resource_request)
container_port = ContainerPort(port=80)
container = Container(name=container_name, image=container_image,
                      resources=container_resource_requirements, ports=[container_port])
container_group = ContainerGroup(
    location='northeurope', containers=[container],
    os_type=OperatingSystemTypes.linux)  # type: ignore


# create azure resource group from python SDK


response = container_instance_client.container_groups.begin_create_or_update(
    resource_group_name, container_group_name, container_group)

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
