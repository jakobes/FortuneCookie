from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import ContainerGroup, Container, ContainerPort, ImageRegistryCredential, ResourceRequests, ResourceRequirements, OperatingSystemTypes

# Azure subscription and resource details
subscription_id = 'YOUR_SUBSCRIPTION_ID'
resource_group_name = 'YOUR_RESOURCE_GROUP_NAME'
location = 'YOUR_RESOURCE_LOCATION'  # e.g., 'eastus'

# Container instance details
container_group_name = 'YOUR_CONTAINER_GROUP_NAME'
container_name = 'YOUR_CONTAINER_NAME'
image_name = 'YOUR_IMAGE_NAME'  # e.g., 'youracr.azurecr.io/your-image:latest'
cpu = 1.0  # Number of CPU cores
memory = 1.5  # GB of RAM
port = 80  # Port the container will listen on

# Optional: For images hosted in private registries like Azure Container Registry
registry_login_server = 'YOUR_ACR_LOGIN_SERVER'  # e.g., 'youracr.azurecr.io'
registry_username = 'YOUR_ACR_USERNAME'
registry_password = 'YOUR_ACR_PASSWORD'

# Authenticate with Azure
credential = DefaultAzureCredential()

# Initialize the Container Instance Management Client
container_instance_client = ContainerInstanceManagementClient(credential, subscription_id)

# Configure the container and registry credentials (if necessary)
container_resource_requirements = ResourceRequirements(
    requests=ResourceRequests(memory_in_gb=memory, cpu=cpu)
)
image_registry_credential = ImageRegistryCredential(
    server=registry_login_server,
    username=registry_username,
    password=registry_password
)

container = Container(
    name=container_name,
    image=image_name,
    resources=container_resource_requirements,
    ports=[ContainerPort(port=port)]
)

# Create or update the container group
container_group = ContainerGroup(
    location=location,
    containers=[container],
    os_type=OperatingSystemTypes.linux,  # Or OperatingSystemTypes.windows
    image_registry_credentials=[image_registry_credential] if registry_login_server else [],
    ip_address={'ports': [{'port': port, 'protocol': 'TCP'}], 'type': 'Public'}
)

# Deploy the container group
deployment_operation = container_instance_client.container_groups.begin_create_or_update(
    resource_group_name,
    container_group_name,
    container_group
)

# Wait for the deployment to complete
deployment_operation.result()

print(f"Container '{container_name}' deployed successfully to '{container_group_name}' in '{location}'.")
