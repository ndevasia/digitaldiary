from .ec2 import Ec2SubnetReplicator, Ec2VPCReplicator
from .secrets_manager import SecretmanagerSecretReplicator
from .ssm import SsmParameterReplicator

RESOURCE_REPLICATORS = {
    resource_replicator.type: resource_replicator
    for resource_replicator in [
        SsmParameterReplicator,
        SecretmanagerSecretReplicator,
        Ec2VPCReplicator,
        Ec2SubnetReplicator,
    ]
}

__all__ = ["RESOURCE_REPLICATORS"]
