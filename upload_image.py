# copied from https://learn.microsoft.com/en-us/python/api/overview/azure/containerregistry-readme?view=azure-python#upload-images
# probably not working as is

# Create a ContainerRegistryClient that will authenticate through Active Directory
from azure.containerregistry import ContainerRegistryClient
from azure.identity import DefaultAzureCredential

endpoint = "https://mycontainerregistry.azurecr.io"
audience = "https://management.azure.com"
client = ContainerRegistryClient(endpoint, DefaultAzureCredential(), audience=audience)

repository_name = "sample-oci-image"
layer = BytesIO(b"Sample layer")
config = BytesIO(json.dumps(
    {
        "sample config": "content",
    }).encode())
with ContainerRegistryClient(endpoint, credential) as client:
    # Upload a layer
    layer_digest, layer_size = client.upload_blob(repository_name, layer)
    print(f"Uploaded layer: digest - {layer_digest}, size - {layer_size}")
    # Upload a config
    config_digest, config_size = client.upload_blob(repository_name, config)
    print(f"Uploaded config: digest - {config_digest}, size - {config_size}")
    # Create an oci image with config and layer info
    oci_manifest = {
        "config": {
            "mediaType": "application/vnd.oci.image.config.v1+json",
            "digest": config_digest,
            "sizeInBytes": config_size,
        },
        "schemaVersion": 2,
        "layers": [
            {
                "mediaType": "application/vnd.oci.image.layer.v1.tar",
                "digest": layer_digest,
                "size": layer_size,
                "annotations": {
                    "org.opencontainers.image.ref.name": "artifact.txt",
                },
            },
        ],
    }
    # Set the image with tag "latest"
    manifest_digest = client.set_manifest(repository_name, oci_manifest, tag="latest")
    print(f"Uploaded manifest: digest - {manifest_digest}")
