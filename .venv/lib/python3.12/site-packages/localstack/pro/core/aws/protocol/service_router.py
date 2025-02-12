from localstack.aws.protocol import service_router as localstack_service_router
from localstack.aws.spec import ServiceModelIdentifier
from localstack.utils.patch import patch
def patch_service_router():
	B='appsync';import re;from typing import Callable,Optional;from localstack.http import Request
	@patch(localstack_service_router.custom_signing_name_rules)
	def A(fn,signing_name,path,**C):
		B='rds';A=signing_name
		if A in[B,'docdb','neptune']:return ServiceModelIdentifier(B)
		return fn(A,path,**C)
	@patch(localstack_service_router.custom_host_addressing_rules)
	def C(fn,host,**C):
		A=host
		if'.cloudfront.'in A:return ServiceModelIdentifier('cloudfront')
		if'mediastore-'in A:return ServiceModelIdentifier('mediastore-data')
		if'.appsync-api.'in A:return ServiceModelIdentifier(B)
		return fn(A,**C)
	@patch(localstack_service_router.legacy_rules)
	def D(fn,request,**D):
		A=request;C=A.path
		if re.match('/graphql/[a-zA-Z0-9-]+',C):return ServiceModelIdentifier(B)
		if'/2018-06-01/runtime'in C:return ServiceModelIdentifier('lambda')
		return fn(request=A,**D)