from datetime import datetime
from enum import StrEnum
from typing import Dict, List, Optional, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AccountId = str
BaseModelIdentifier = str
BedrockModelId = str
Boolean = bool
BrandedName = str
BucketName = str
CustomModelArn = str
CustomModelName = str
ErrorMessage = str
EvaluationDatasetName = str
EvaluationJobArn = str
EvaluationJobDescription = str
EvaluationJobIdentifier = str
EvaluationJobName = str
EvaluationMetricDescription = str
EvaluationMetricName = str
EvaluationModelIdentifier = str
EvaluationModelInferenceParams = str
EvaluationRatingMethod = str
FoundationModelArn = str
GuardrailArn = str
GuardrailBlockedMessaging = str
GuardrailContextualGroundingFilterConfigThresholdDouble = float
GuardrailContextualGroundingFilterThresholdDouble = float
GuardrailDescription = str
GuardrailDraftVersion = str
GuardrailFailureRecommendation = str
GuardrailId = str
GuardrailIdentifier = str
GuardrailName = str
GuardrailNumericalVersion = str
GuardrailRegexConfigDescriptionString = str
GuardrailRegexConfigNameString = str
GuardrailRegexConfigPatternString = str
GuardrailRegexDescriptionString = str
GuardrailRegexNameString = str
GuardrailRegexPatternString = str
GuardrailStatusReason = str
GuardrailTopicDefinition = str
GuardrailTopicExample = str
GuardrailTopicName = str
GuardrailVersion = str
GuardrailWordConfigTextString = str
GuardrailWordTextString = str
HumanTaskInstructions = str
IdempotencyToken = str
ImportedModelArn = str
ImportedModelIdentifier = str
ImportedModelName = str
InferenceProfileArn = str
InferenceProfileDescription = str
InferenceProfileId = str
InferenceProfileIdentifier = str
InferenceProfileModelSourceArn = str
InferenceProfileName = str
InstructSupported = bool
JobName = str
KeyPrefix = str
KmsKeyArn = str
KmsKeyId = str
LogGroupName = str
MaxResults = int
Message = str
MetricFloat = float
ModelArchitecture = str
ModelArn = str
ModelCopyJobArn = str
ModelCustomizationJobArn = str
ModelCustomizationJobIdentifier = str
ModelId = str
ModelIdentifier = str
ModelImportJobArn = str
ModelImportJobIdentifier = str
ModelInvocationIdempotencyToken = str
ModelInvocationJobArn = str
ModelInvocationJobIdentifier = str
ModelInvocationJobName = str
ModelInvocationJobTimeoutDurationInHours = int
ModelName = str
NonBlankString = str
PaginationToken = str
PositiveInteger = int
Provider = str
ProvisionedModelArn = str
ProvisionedModelId = str
ProvisionedModelName = str
RoleArn = str
S3Uri = str
SageMakerFlowDefinitionArn = str
SecurityGroupId = str
String = str
SubnetId = str
TagKey = str
TagValue = str
TaggableResourcesArn = str


class CommitmentDuration(StrEnum):
    OneMonth = "OneMonth"
    SixMonths = "SixMonths"


class CustomizationType(StrEnum):
    FINE_TUNING = "FINE_TUNING"
    CONTINUED_PRE_TRAINING = "CONTINUED_PRE_TRAINING"


class EvaluationJobStatus(StrEnum):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"
    Deleting = "Deleting"


class EvaluationJobType(StrEnum):
    Human = "Human"
    Automated = "Automated"


class EvaluationTaskType(StrEnum):
    Summarization = "Summarization"
    Classification = "Classification"
    QuestionAndAnswer = "QuestionAndAnswer"
    Generation = "Generation"
    Custom = "Custom"


class FineTuningJobStatus(StrEnum):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class FoundationModelLifecycleStatus(StrEnum):
    ACTIVE = "ACTIVE"
    LEGACY = "LEGACY"


class GuardrailContentFilterType(StrEnum):
    SEXUAL = "SEXUAL"
    VIOLENCE = "VIOLENCE"
    HATE = "HATE"
    INSULTS = "INSULTS"
    MISCONDUCT = "MISCONDUCT"
    PROMPT_ATTACK = "PROMPT_ATTACK"


class GuardrailContextualGroundingFilterType(StrEnum):
    GROUNDING = "GROUNDING"
    RELEVANCE = "RELEVANCE"


class GuardrailFilterStrength(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class GuardrailManagedWordsType(StrEnum):
    PROFANITY = "PROFANITY"


class GuardrailPiiEntityType(StrEnum):
    ADDRESS = "ADDRESS"
    AGE = "AGE"
    AWS_ACCESS_KEY = "AWS_ACCESS_KEY"
    AWS_SECRET_KEY = "AWS_SECRET_KEY"
    CA_HEALTH_NUMBER = "CA_HEALTH_NUMBER"
    CA_SOCIAL_INSURANCE_NUMBER = "CA_SOCIAL_INSURANCE_NUMBER"
    CREDIT_DEBIT_CARD_CVV = "CREDIT_DEBIT_CARD_CVV"
    CREDIT_DEBIT_CARD_EXPIRY = "CREDIT_DEBIT_CARD_EXPIRY"
    CREDIT_DEBIT_CARD_NUMBER = "CREDIT_DEBIT_CARD_NUMBER"
    DRIVER_ID = "DRIVER_ID"
    EMAIL = "EMAIL"
    INTERNATIONAL_BANK_ACCOUNT_NUMBER = "INTERNATIONAL_BANK_ACCOUNT_NUMBER"
    IP_ADDRESS = "IP_ADDRESS"
    LICENSE_PLATE = "LICENSE_PLATE"
    MAC_ADDRESS = "MAC_ADDRESS"
    NAME = "NAME"
    PASSWORD = "PASSWORD"
    PHONE = "PHONE"
    PIN = "PIN"
    SWIFT_CODE = "SWIFT_CODE"
    UK_NATIONAL_HEALTH_SERVICE_NUMBER = "UK_NATIONAL_HEALTH_SERVICE_NUMBER"
    UK_NATIONAL_INSURANCE_NUMBER = "UK_NATIONAL_INSURANCE_NUMBER"
    UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER = "UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER"
    URL = "URL"
    USERNAME = "USERNAME"
    US_BANK_ACCOUNT_NUMBER = "US_BANK_ACCOUNT_NUMBER"
    US_BANK_ROUTING_NUMBER = "US_BANK_ROUTING_NUMBER"
    US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER = "US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER"
    US_PASSPORT_NUMBER = "US_PASSPORT_NUMBER"
    US_SOCIAL_SECURITY_NUMBER = "US_SOCIAL_SECURITY_NUMBER"
    VEHICLE_IDENTIFICATION_NUMBER = "VEHICLE_IDENTIFICATION_NUMBER"


class GuardrailSensitiveInformationAction(StrEnum):
    BLOCK = "BLOCK"
    ANONYMIZE = "ANONYMIZE"


class GuardrailStatus(StrEnum):
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    VERSIONING = "VERSIONING"
    READY = "READY"
    FAILED = "FAILED"
    DELETING = "DELETING"


class GuardrailTopicType(StrEnum):
    DENY = "DENY"


class InferenceProfileStatus(StrEnum):
    ACTIVE = "ACTIVE"


class InferenceProfileType(StrEnum):
    SYSTEM_DEFINED = "SYSTEM_DEFINED"
    APPLICATION = "APPLICATION"


class InferenceType(StrEnum):
    ON_DEMAND = "ON_DEMAND"
    PROVISIONED = "PROVISIONED"


class ModelCopyJobStatus(StrEnum):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"


class ModelCustomization(StrEnum):
    FINE_TUNING = "FINE_TUNING"
    CONTINUED_PRE_TRAINING = "CONTINUED_PRE_TRAINING"


class ModelCustomizationJobStatus(StrEnum):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"


class ModelImportJobStatus(StrEnum):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"


class ModelInvocationJobStatus(StrEnum):
    Submitted = "Submitted"
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"
    PartiallyCompleted = "PartiallyCompleted"
    Expired = "Expired"
    Validating = "Validating"
    Scheduled = "Scheduled"


class ModelModality(StrEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    EMBEDDING = "EMBEDDING"


class ProvisionedModelStatus(StrEnum):
    Creating = "Creating"
    InService = "InService"
    Updating = "Updating"
    Failed = "Failed"


class S3InputFormat(StrEnum):
    JSONL = "JSONL"


class SortByProvisionedModels(StrEnum):
    CreationTime = "CreationTime"


class SortJobsBy(StrEnum):
    CreationTime = "CreationTime"


class SortModelsBy(StrEnum):
    CreationTime = "CreationTime"


class SortOrder(StrEnum):
    Ascending = "Ascending"
    Descending = "Descending"


class AccessDeniedException(ServiceException):
    """The request is denied because of missing access permissions."""

    code: str = "AccessDeniedException"
    sender_fault: bool = True
    status_code: int = 403


class ConflictException(ServiceException):
    """Error occurred because of a conflict while performing an operation."""

    code: str = "ConflictException"
    sender_fault: bool = True
    status_code: int = 400


class InternalServerException(ServiceException):
    """An internal server error occurred. Retry your request."""

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 500


class ResourceNotFoundException(ServiceException):
    """The specified resource Amazon Resource Name (ARN) was not found. Check
    the Amazon Resource Name (ARN) and try your request again.
    """

    code: str = "ResourceNotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class ServiceQuotaExceededException(ServiceException):
    """The number of requests exceeds the service quota. Resubmit your request
    later.
    """

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = True
    status_code: int = 400


class ThrottlingException(ServiceException):
    """The number of requests exceeds the limit. Resubmit your request later."""

    code: str = "ThrottlingException"
    sender_fault: bool = True
    status_code: int = 429


class TooManyTagsException(ServiceException):
    """The request contains more tags than can be associated with a resource
    (50 tags per resource). The maximum number of tags includes both
    existing tags and those included in your current request.
    """

    code: str = "TooManyTagsException"
    sender_fault: bool = True
    status_code: int = 400
    resourceName: Optional[TaggableResourcesArn]


class ValidationException(ServiceException):
    """Input validation failed. Check your request parameters and retry the
    request.
    """

    code: str = "ValidationException"
    sender_fault: bool = True
    status_code: int = 400


EvaluationMetricNames = List[EvaluationMetricName]


class EvaluationDatasetLocation(TypedDict, total=False):
    """The location in Amazon S3 where your prompt dataset is stored."""

    s3Uri: Optional[S3Uri]


class EvaluationDataset(TypedDict, total=False):
    """Used to specify the name of a built-in prompt dataset and optionally,
    the Amazon S3 bucket where a custom prompt dataset is saved.
    """

    name: EvaluationDatasetName
    datasetLocation: Optional[EvaluationDatasetLocation]


class EvaluationDatasetMetricConfig(TypedDict, total=False):
    """Defines the built-in prompt datasets, built-in metric names and custom
    metric names, and the task type.
    """

    taskType: EvaluationTaskType
    dataset: EvaluationDataset
    metricNames: EvaluationMetricNames


EvaluationDatasetMetricConfigs = List[EvaluationDatasetMetricConfig]


class AutomatedEvaluationConfig(TypedDict, total=False):
    """Use to specify a automatic model evaluation job. The
    ``EvaluationDatasetMetricConfig`` object is used to specify the prompt
    datasets, task type, and metric names.
    """

    datasetMetricConfigs: EvaluationDatasetMetricConfigs


class BatchDeleteEvaluationJobError(TypedDict, total=False):
    """A JSON array that provides the status of the model evaluation jobs being
    deleted.
    """

    jobIdentifier: EvaluationJobIdentifier
    code: String
    message: Optional[String]


BatchDeleteEvaluationJobErrors = List[BatchDeleteEvaluationJobError]


class BatchDeleteEvaluationJobItem(TypedDict, total=False):
    """An array of model evaluation jobs to be deleted, and their associated
    statuses.
    """

    jobIdentifier: EvaluationJobIdentifier
    jobStatus: EvaluationJobStatus


BatchDeleteEvaluationJobItems = List[BatchDeleteEvaluationJobItem]
EvaluationJobIdentifiers = List[EvaluationJobIdentifier]


class BatchDeleteEvaluationJobRequest(ServiceRequest):
    jobIdentifiers: EvaluationJobIdentifiers


class BatchDeleteEvaluationJobResponse(TypedDict, total=False):
    errors: BatchDeleteEvaluationJobErrors
    evaluationJobs: BatchDeleteEvaluationJobItems


class S3Config(TypedDict, total=False):
    """S3 configuration for storing log data."""

    bucketName: BucketName
    keyPrefix: Optional[KeyPrefix]


class CloudWatchConfig(TypedDict, total=False):
    """CloudWatch logging configuration."""

    logGroupName: LogGroupName
    roleArn: RoleArn
    largeDataDeliveryS3Config: Optional[S3Config]


class EvaluationOutputDataConfig(TypedDict, total=False):
    """The Amazon S3 location where the results of your model evaluation job
    are saved.
    """

    s3Uri: S3Uri


class EvaluationBedrockModel(TypedDict, total=False):
    """Contains the ARN of the Amazon Bedrock model or `inference
    profile <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>`__
    specified in your model evaluation job. Each Amazon Bedrock model
    supports different ``inferenceParams``. To learn more about supported
    inference parameters for Amazon Bedrock models, see `Inference
    parameters for foundation
    models <https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html>`__.

    The ``inferenceParams`` are specified using JSON. To successfully insert
    JSON as string make sure that all quotations are properly escaped. For
    example, ``"temperature":"0.25"`` key value pair would need to be
    formatted as ``\\"temperature\\":\\"0.25\\"`` to successfully accepted in
    the request.
    """

    modelIdentifier: EvaluationModelIdentifier
    inferenceParams: EvaluationModelInferenceParams


class EvaluationModelConfig(TypedDict, total=False):
    """Defines the models used in the model evaluation job."""

    bedrockModel: Optional[EvaluationBedrockModel]


EvaluationModelConfigs = List[EvaluationModelConfig]


class EvaluationInferenceConfig(TypedDict, total=False):
    """Used to define the models you want used in your model evaluation job.
    Automated model evaluation jobs support only a single model. In a
    human-based model evaluation job, your annotator can compare the
    responses for up to two different models.
    """

    models: Optional[EvaluationModelConfigs]


class HumanEvaluationCustomMetric(TypedDict, total=False):
    """In a model evaluation job that uses human workers you must define the
    name of the metric, and how you want that metric rated ``ratingMethod``,
    and an optional description of the metric.
    """

    name: EvaluationMetricName
    description: Optional[EvaluationMetricDescription]
    ratingMethod: EvaluationRatingMethod


HumanEvaluationCustomMetrics = List[HumanEvaluationCustomMetric]


class HumanWorkflowConfig(TypedDict, total=False):
    """Contains ``SageMakerFlowDefinition`` object. The object is used to
    specify the prompt dataset, task type, rating method and metric names.
    """

    flowDefinitionArn: SageMakerFlowDefinitionArn
    instructions: Optional[HumanTaskInstructions]


class HumanEvaluationConfig(TypedDict, total=False):
    """Specifies the custom metrics, how tasks will be rated, the flow
    definition ARN, and your custom prompt datasets. Model evaluation jobs
    use human workers *only* support the use of custom prompt datasets. To
    learn more about custom prompt datasets and the required format, see
    `Custom prompt
    datasets <https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-prompt-datasets-custom.html>`__.

    When you create custom metrics in ``HumanEvaluationCustomMetric`` you
    must specify the metric's ``name``. The list of ``names`` specified in
    the ``HumanEvaluationCustomMetric`` array, must match the
    ``metricNames`` array of strings specified in
    ``EvaluationDatasetMetricConfig``. For example, if in the
    ``HumanEvaluationCustomMetric`` array your specified the names
    ``"accuracy", "toxicity", "readability"`` as custom metrics *then* the
    ``metricNames`` array would need to look like the following
    ``["accuracy", "toxicity", "readability"]`` in
    ``EvaluationDatasetMetricConfig``.
    """

    humanWorkflowConfig: Optional[HumanWorkflowConfig]
    customMetrics: Optional[HumanEvaluationCustomMetrics]
    datasetMetricConfigs: EvaluationDatasetMetricConfigs


class EvaluationConfig(TypedDict, total=False):
    """Used to specify either a ``AutomatedEvaluationConfig`` or
    ``HumanEvaluationConfig`` object.
    """

    automated: Optional[AutomatedEvaluationConfig]
    human: Optional[HumanEvaluationConfig]


class Tag(TypedDict, total=False):
    """Definition of the key/value pair for a tag."""

    key: TagKey
    value: TagValue


TagList = List[Tag]


class CreateEvaluationJobRequest(ServiceRequest):
    jobName: EvaluationJobName
    jobDescription: Optional[EvaluationJobDescription]
    clientRequestToken: Optional[IdempotencyToken]
    roleArn: RoleArn
    customerEncryptionKeyId: Optional[KmsKeyId]
    jobTags: Optional[TagList]
    evaluationConfig: EvaluationConfig
    inferenceConfig: EvaluationInferenceConfig
    outputDataConfig: EvaluationOutputDataConfig


class CreateEvaluationJobResponse(TypedDict, total=False):
    jobArn: EvaluationJobArn


GuardrailContextualGroundingFilterConfig = TypedDict(
    "GuardrailContextualGroundingFilterConfig",
    {
        "type": GuardrailContextualGroundingFilterType,
        "threshold": GuardrailContextualGroundingFilterConfigThresholdDouble,
    },
    total=False,
)
GuardrailContextualGroundingFiltersConfig = List[GuardrailContextualGroundingFilterConfig]


class GuardrailContextualGroundingPolicyConfig(TypedDict, total=False):
    """The policy configuration details for the guardrails contextual grounding
    policy.
    """

    filtersConfig: GuardrailContextualGroundingFiltersConfig


class GuardrailRegexConfig(TypedDict, total=False):
    """The regular expression to configure for the guardrail."""

    name: GuardrailRegexConfigNameString
    description: Optional[GuardrailRegexConfigDescriptionString]
    pattern: GuardrailRegexConfigPatternString
    action: GuardrailSensitiveInformationAction


GuardrailRegexesConfig = List[GuardrailRegexConfig]
GuardrailPiiEntityConfig = TypedDict(
    "GuardrailPiiEntityConfig",
    {
        "type": GuardrailPiiEntityType,
        "action": GuardrailSensitiveInformationAction,
    },
    total=False,
)
GuardrailPiiEntitiesConfig = List[GuardrailPiiEntityConfig]


class GuardrailSensitiveInformationPolicyConfig(TypedDict, total=False):
    """Contains details about PII entities and regular expressions to configure
    for the guardrail.
    """

    piiEntitiesConfig: Optional[GuardrailPiiEntitiesConfig]
    regexesConfig: Optional[GuardrailRegexesConfig]


GuardrailManagedWordsConfig = TypedDict(
    "GuardrailManagedWordsConfig",
    {
        "type": GuardrailManagedWordsType,
    },
    total=False,
)
GuardrailManagedWordListsConfig = List[GuardrailManagedWordsConfig]


class GuardrailWordConfig(TypedDict, total=False):
    """A word to configure for the guardrail."""

    text: GuardrailWordConfigTextString


GuardrailWordsConfig = List[GuardrailWordConfig]


class GuardrailWordPolicyConfig(TypedDict, total=False):
    """Contains details about the word policy to configured for the guardrail."""

    wordsConfig: Optional[GuardrailWordsConfig]
    managedWordListsConfig: Optional[GuardrailManagedWordListsConfig]


GuardrailContentFilterConfig = TypedDict(
    "GuardrailContentFilterConfig",
    {
        "type": GuardrailContentFilterType,
        "inputStrength": GuardrailFilterStrength,
        "outputStrength": GuardrailFilterStrength,
    },
    total=False,
)
GuardrailContentFiltersConfig = List[GuardrailContentFilterConfig]


class GuardrailContentPolicyConfig(TypedDict, total=False):
    """Contains details about how to handle harmful content."""

    filtersConfig: GuardrailContentFiltersConfig


GuardrailTopicExamples = List[GuardrailTopicExample]
GuardrailTopicConfig = TypedDict(
    "GuardrailTopicConfig",
    {
        "name": GuardrailTopicName,
        "definition": GuardrailTopicDefinition,
        "examples": Optional[GuardrailTopicExamples],
        "type": GuardrailTopicType,
    },
    total=False,
)
GuardrailTopicsConfig = List[GuardrailTopicConfig]


class GuardrailTopicPolicyConfig(TypedDict, total=False):
    """Contains details about topics that the guardrail should identify and
    deny.
    """

    topicsConfig: GuardrailTopicsConfig


class CreateGuardrailRequest(ServiceRequest):
    name: GuardrailName
    description: Optional[GuardrailDescription]
    topicPolicyConfig: Optional[GuardrailTopicPolicyConfig]
    contentPolicyConfig: Optional[GuardrailContentPolicyConfig]
    wordPolicyConfig: Optional[GuardrailWordPolicyConfig]
    sensitiveInformationPolicyConfig: Optional[GuardrailSensitiveInformationPolicyConfig]
    contextualGroundingPolicyConfig: Optional[GuardrailContextualGroundingPolicyConfig]
    blockedInputMessaging: GuardrailBlockedMessaging
    blockedOutputsMessaging: GuardrailBlockedMessaging
    kmsKeyId: Optional[KmsKeyId]
    tags: Optional[TagList]
    clientRequestToken: Optional[IdempotencyToken]


Timestamp = datetime


class CreateGuardrailResponse(TypedDict, total=False):
    guardrailId: GuardrailId
    guardrailArn: GuardrailArn
    version: GuardrailDraftVersion
    createdAt: Timestamp


class CreateGuardrailVersionRequest(ServiceRequest):
    guardrailIdentifier: GuardrailIdentifier
    description: Optional[GuardrailDescription]
    clientRequestToken: Optional[IdempotencyToken]


class CreateGuardrailVersionResponse(TypedDict, total=False):
    guardrailId: GuardrailId
    version: GuardrailNumericalVersion


class InferenceProfileModelSource(TypedDict, total=False):
    """Contains information about the model or system-defined inference profile
    that is the source for an inference profile..
    """

    copyFrom: Optional[InferenceProfileModelSourceArn]


class CreateInferenceProfileRequest(ServiceRequest):
    inferenceProfileName: InferenceProfileName
    description: Optional[InferenceProfileDescription]
    clientRequestToken: Optional[IdempotencyToken]
    modelSource: InferenceProfileModelSource
    tags: Optional[TagList]


class CreateInferenceProfileResponse(TypedDict, total=False):
    inferenceProfileArn: InferenceProfileArn
    status: Optional[InferenceProfileStatus]


class CreateModelCopyJobRequest(ServiceRequest):
    sourceModelArn: ModelArn
    targetModelName: CustomModelName
    modelKmsKeyId: Optional[KmsKeyId]
    targetModelTags: Optional[TagList]
    clientRequestToken: Optional[IdempotencyToken]


class CreateModelCopyJobResponse(TypedDict, total=False):
    jobArn: ModelCopyJobArn


SecurityGroupIds = List[SecurityGroupId]
SubnetIds = List[SubnetId]


class VpcConfig(TypedDict, total=False):
    """The configuration of a virtual private cloud (VPC). For more
    information, see `Protect your data using Amazon Virtual Private Cloud
    and Amazon Web Services
    PrivateLink <https://docs.aws.amazon.com/bedrock/latest/userguide/usingVPC.html>`__.
    """

    subnetIds: SubnetIds
    securityGroupIds: SecurityGroupIds


ModelCustomizationHyperParameters = Dict[String, String]


class OutputDataConfig(TypedDict, total=False):
    """S3 Location of the output data."""

    s3Uri: S3Uri


class Validator(TypedDict, total=False):
    """Information about a validator."""

    s3Uri: S3Uri


Validators = List[Validator]


class ValidationDataConfig(TypedDict, total=False):
    """Array of up to 10 validators."""

    validators: Validators


class TrainingDataConfig(TypedDict, total=False):
    """S3 Location of the training data."""

    s3Uri: S3Uri


class CreateModelCustomizationJobRequest(ServiceRequest):
    jobName: JobName
    customModelName: CustomModelName
    roleArn: RoleArn
    clientRequestToken: Optional[IdempotencyToken]
    baseModelIdentifier: BaseModelIdentifier
    customizationType: Optional[CustomizationType]
    customModelKmsKeyId: Optional[KmsKeyId]
    jobTags: Optional[TagList]
    customModelTags: Optional[TagList]
    trainingDataConfig: TrainingDataConfig
    validationDataConfig: Optional[ValidationDataConfig]
    outputDataConfig: OutputDataConfig
    hyperParameters: ModelCustomizationHyperParameters
    vpcConfig: Optional[VpcConfig]


class CreateModelCustomizationJobResponse(TypedDict, total=False):
    jobArn: ModelCustomizationJobArn


class S3DataSource(TypedDict, total=False):
    """The Amazon S3 data source of the imported job."""

    s3Uri: S3Uri


class ModelDataSource(TypedDict, total=False):
    """Data source for the imported model."""

    s3DataSource: Optional[S3DataSource]


class CreateModelImportJobRequest(ServiceRequest):
    jobName: JobName
    importedModelName: ImportedModelName
    roleArn: RoleArn
    modelDataSource: ModelDataSource
    jobTags: Optional[TagList]
    importedModelTags: Optional[TagList]
    clientRequestToken: Optional[IdempotencyToken]
    vpcConfig: Optional[VpcConfig]
    importedModelKmsKeyId: Optional[KmsKeyId]


class CreateModelImportJobResponse(TypedDict, total=False):
    jobArn: ModelImportJobArn


class ModelInvocationJobS3OutputDataConfig(TypedDict, total=False):
    """Contains the configuration of the S3 location of the output data."""

    s3Uri: S3Uri
    s3EncryptionKeyId: Optional[KmsKeyId]
    s3BucketOwner: Optional[AccountId]


class ModelInvocationJobOutputDataConfig(TypedDict, total=False):
    """Contains the configuration of the S3 location of the output data."""

    s3OutputDataConfig: Optional[ModelInvocationJobS3OutputDataConfig]


class ModelInvocationJobS3InputDataConfig(TypedDict, total=False):
    """Contains the configuration of the S3 location of the input data."""

    s3InputFormat: Optional[S3InputFormat]
    s3Uri: S3Uri
    s3BucketOwner: Optional[AccountId]


class ModelInvocationJobInputDataConfig(TypedDict, total=False):
    """Details about the location of the input to the batch inference job."""

    s3InputDataConfig: Optional[ModelInvocationJobS3InputDataConfig]


class CreateModelInvocationJobRequest(ServiceRequest):
    jobName: ModelInvocationJobName
    roleArn: RoleArn
    clientRequestToken: Optional[ModelInvocationIdempotencyToken]
    modelId: ModelId
    inputDataConfig: ModelInvocationJobInputDataConfig
    outputDataConfig: ModelInvocationJobOutputDataConfig
    vpcConfig: Optional[VpcConfig]
    timeoutDurationInHours: Optional[ModelInvocationJobTimeoutDurationInHours]
    tags: Optional[TagList]


class CreateModelInvocationJobResponse(TypedDict, total=False):
    jobArn: ModelInvocationJobArn


class CreateProvisionedModelThroughputRequest(ServiceRequest):
    clientRequestToken: Optional[IdempotencyToken]
    modelUnits: PositiveInteger
    provisionedModelName: ProvisionedModelName
    modelId: ModelIdentifier
    commitmentDuration: Optional[CommitmentDuration]
    tags: Optional[TagList]


class CreateProvisionedModelThroughputResponse(TypedDict, total=False):
    provisionedModelArn: ProvisionedModelArn


class CustomModelSummary(TypedDict, total=False):
    """Summary information for a custom model."""

    modelArn: CustomModelArn
    modelName: CustomModelName
    creationTime: Timestamp
    baseModelArn: ModelArn
    baseModelName: ModelName
    customizationType: Optional[CustomizationType]
    ownerAccountId: Optional[AccountId]


CustomModelSummaryList = List[CustomModelSummary]


class DeleteCustomModelRequest(ServiceRequest):
    modelIdentifier: ModelIdentifier


class DeleteCustomModelResponse(TypedDict, total=False):
    pass


class DeleteGuardrailRequest(ServiceRequest):
    guardrailIdentifier: GuardrailIdentifier
    guardrailVersion: Optional[GuardrailNumericalVersion]


class DeleteGuardrailResponse(TypedDict, total=False):
    pass


class DeleteImportedModelRequest(ServiceRequest):
    modelIdentifier: ImportedModelIdentifier


class DeleteImportedModelResponse(TypedDict, total=False):
    pass


class DeleteInferenceProfileRequest(ServiceRequest):
    inferenceProfileIdentifier: InferenceProfileIdentifier


class DeleteInferenceProfileResponse(TypedDict, total=False):
    pass


class DeleteModelInvocationLoggingConfigurationRequest(ServiceRequest):
    pass


class DeleteModelInvocationLoggingConfigurationResponse(TypedDict, total=False):
    pass


class DeleteProvisionedModelThroughputRequest(ServiceRequest):
    provisionedModelId: ProvisionedModelId


class DeleteProvisionedModelThroughputResponse(TypedDict, total=False):
    pass


ErrorMessages = List[ErrorMessage]
EvaluationModelIdentifiers = List[EvaluationModelIdentifier]
EvaluationTaskTypes = List[EvaluationTaskType]


class EvaluationSummary(TypedDict, total=False):
    """A summary of the model evaluation job."""

    jobArn: EvaluationJobArn
    jobName: EvaluationJobName
    status: EvaluationJobStatus
    creationTime: Timestamp
    jobType: EvaluationJobType
    evaluationTaskTypes: EvaluationTaskTypes
    modelIdentifiers: EvaluationModelIdentifiers


EvaluationSummaries = List[EvaluationSummary]


class FoundationModelLifecycle(TypedDict, total=False):
    """Details about whether a model version is available or deprecated."""

    status: FoundationModelLifecycleStatus


InferenceTypeList = List[InferenceType]
ModelCustomizationList = List[ModelCustomization]
ModelModalityList = List[ModelModality]


class FoundationModelDetails(TypedDict, total=False):
    """Information about a foundation model."""

    modelArn: FoundationModelArn
    modelId: BedrockModelId
    modelName: Optional[BrandedName]
    providerName: Optional[BrandedName]
    inputModalities: Optional[ModelModalityList]
    outputModalities: Optional[ModelModalityList]
    responseStreamingSupported: Optional[Boolean]
    customizationsSupported: Optional[ModelCustomizationList]
    inferenceTypesSupported: Optional[InferenceTypeList]
    modelLifecycle: Optional[FoundationModelLifecycle]


class FoundationModelSummary(TypedDict, total=False):
    """Summary information for a foundation model."""

    modelArn: FoundationModelArn
    modelId: BedrockModelId
    modelName: Optional[BrandedName]
    providerName: Optional[BrandedName]
    inputModalities: Optional[ModelModalityList]
    outputModalities: Optional[ModelModalityList]
    responseStreamingSupported: Optional[Boolean]
    customizationsSupported: Optional[ModelCustomizationList]
    inferenceTypesSupported: Optional[InferenceTypeList]
    modelLifecycle: Optional[FoundationModelLifecycle]


FoundationModelSummaryList = List[FoundationModelSummary]


class GetCustomModelRequest(ServiceRequest):
    modelIdentifier: ModelIdentifier


class ValidatorMetric(TypedDict, total=False):
    """The metric for the validator."""

    validationLoss: Optional[MetricFloat]


ValidationMetrics = List[ValidatorMetric]


class TrainingMetrics(TypedDict, total=False):
    """Metrics associated with the custom job."""

    trainingLoss: Optional[MetricFloat]


class GetCustomModelResponse(TypedDict, total=False):
    modelArn: ModelArn
    modelName: CustomModelName
    jobName: Optional[JobName]
    jobArn: ModelCustomizationJobArn
    baseModelArn: ModelArn
    customizationType: Optional[CustomizationType]
    modelKmsKeyArn: Optional[KmsKeyArn]
    hyperParameters: Optional[ModelCustomizationHyperParameters]
    trainingDataConfig: TrainingDataConfig
    validationDataConfig: Optional[ValidationDataConfig]
    outputDataConfig: OutputDataConfig
    trainingMetrics: Optional[TrainingMetrics]
    validationMetrics: Optional[ValidationMetrics]
    creationTime: Timestamp


class GetEvaluationJobRequest(ServiceRequest):
    jobIdentifier: EvaluationJobIdentifier


class GetEvaluationJobResponse(TypedDict, total=False):
    jobName: EvaluationJobName
    status: EvaluationJobStatus
    jobArn: EvaluationJobArn
    jobDescription: Optional[EvaluationJobDescription]
    roleArn: RoleArn
    customerEncryptionKeyId: Optional[KmsKeyId]
    jobType: EvaluationJobType
    evaluationConfig: EvaluationConfig
    inferenceConfig: EvaluationInferenceConfig
    outputDataConfig: EvaluationOutputDataConfig
    creationTime: Timestamp
    lastModifiedTime: Optional[Timestamp]
    failureMessages: Optional[ErrorMessages]


class GetFoundationModelRequest(ServiceRequest):
    modelIdentifier: ModelIdentifier


class GetFoundationModelResponse(TypedDict, total=False):
    modelDetails: Optional[FoundationModelDetails]


class GetGuardrailRequest(ServiceRequest):
    guardrailIdentifier: GuardrailIdentifier
    guardrailVersion: Optional[GuardrailVersion]


GuardrailFailureRecommendations = List[GuardrailFailureRecommendation]
GuardrailStatusReasons = List[GuardrailStatusReason]
GuardrailContextualGroundingFilter = TypedDict(
    "GuardrailContextualGroundingFilter",
    {
        "type": GuardrailContextualGroundingFilterType,
        "threshold": GuardrailContextualGroundingFilterThresholdDouble,
    },
    total=False,
)
GuardrailContextualGroundingFilters = List[GuardrailContextualGroundingFilter]


class GuardrailContextualGroundingPolicy(TypedDict, total=False):
    """The details for the guardrails contextual grounding policy."""

    filters: GuardrailContextualGroundingFilters


class GuardrailRegex(TypedDict, total=False):
    """The regular expression configured for the guardrail."""

    name: GuardrailRegexNameString
    description: Optional[GuardrailRegexDescriptionString]
    pattern: GuardrailRegexPatternString
    action: GuardrailSensitiveInformationAction


GuardrailRegexes = List[GuardrailRegex]
GuardrailPiiEntity = TypedDict(
    "GuardrailPiiEntity",
    {
        "type": GuardrailPiiEntityType,
        "action": GuardrailSensitiveInformationAction,
    },
    total=False,
)
GuardrailPiiEntities = List[GuardrailPiiEntity]


class GuardrailSensitiveInformationPolicy(TypedDict, total=False):
    """Contains details about PII entities and regular expressions configured
    for the guardrail.
    """

    piiEntities: Optional[GuardrailPiiEntities]
    regexes: Optional[GuardrailRegexes]


GuardrailManagedWords = TypedDict(
    "GuardrailManagedWords",
    {
        "type": GuardrailManagedWordsType,
    },
    total=False,
)
GuardrailManagedWordLists = List[GuardrailManagedWords]


class GuardrailWord(TypedDict, total=False):
    """A word configured for the guardrail."""

    text: GuardrailWordTextString


GuardrailWords = List[GuardrailWord]


class GuardrailWordPolicy(TypedDict, total=False):
    """Contains details about the word policy configured for the guardrail."""

    words: Optional[GuardrailWords]
    managedWordLists: Optional[GuardrailManagedWordLists]


GuardrailContentFilter = TypedDict(
    "GuardrailContentFilter",
    {
        "type": GuardrailContentFilterType,
        "inputStrength": GuardrailFilterStrength,
        "outputStrength": GuardrailFilterStrength,
    },
    total=False,
)
GuardrailContentFilters = List[GuardrailContentFilter]


class GuardrailContentPolicy(TypedDict, total=False):
    """Contains details about how to handle harmful content.

    This data type is used in the following API operations:

    -  `GetGuardrail response
       body <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetGuardrail.html#API_GetGuardrail_ResponseSyntax>`__
    """

    filters: Optional[GuardrailContentFilters]


GuardrailTopic = TypedDict(
    "GuardrailTopic",
    {
        "name": GuardrailTopicName,
        "definition": GuardrailTopicDefinition,
        "examples": Optional[GuardrailTopicExamples],
        "type": Optional[GuardrailTopicType],
    },
    total=False,
)
GuardrailTopics = List[GuardrailTopic]


class GuardrailTopicPolicy(TypedDict, total=False):
    """Contains details about topics that the guardrail should identify and
    deny.

    This data type is used in the following API operations:

    -  `GetGuardrail response
       body <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetGuardrail.html#API_GetGuardrail_ResponseSyntax>`__
    """

    topics: GuardrailTopics


class GetGuardrailResponse(TypedDict, total=False):
    name: GuardrailName
    description: Optional[GuardrailDescription]
    guardrailId: GuardrailId
    guardrailArn: GuardrailArn
    version: GuardrailVersion
    status: GuardrailStatus
    topicPolicy: Optional[GuardrailTopicPolicy]
    contentPolicy: Optional[GuardrailContentPolicy]
    wordPolicy: Optional[GuardrailWordPolicy]
    sensitiveInformationPolicy: Optional[GuardrailSensitiveInformationPolicy]
    contextualGroundingPolicy: Optional[GuardrailContextualGroundingPolicy]
    createdAt: Timestamp
    updatedAt: Timestamp
    statusReasons: Optional[GuardrailStatusReasons]
    failureRecommendations: Optional[GuardrailFailureRecommendations]
    blockedInputMessaging: GuardrailBlockedMessaging
    blockedOutputsMessaging: GuardrailBlockedMessaging
    kmsKeyArn: Optional[KmsKeyArn]


class GetImportedModelRequest(ServiceRequest):
    modelIdentifier: ImportedModelIdentifier


class GetImportedModelResponse(TypedDict, total=False):
    modelArn: Optional[ImportedModelArn]
    modelName: Optional[ImportedModelName]
    jobName: Optional[JobName]
    jobArn: Optional[ModelImportJobArn]
    modelDataSource: Optional[ModelDataSource]
    creationTime: Optional[Timestamp]
    modelArchitecture: Optional[String]
    modelKmsKeyArn: Optional[KmsKeyArn]
    instructSupported: Optional[InstructSupported]


class GetInferenceProfileRequest(ServiceRequest):
    inferenceProfileIdentifier: InferenceProfileIdentifier


class InferenceProfileModel(TypedDict, total=False):
    """Contains information about a model."""

    modelArn: Optional[FoundationModelArn]


InferenceProfileModels = List[InferenceProfileModel]
GetInferenceProfileResponse = TypedDict(
    "GetInferenceProfileResponse",
    {
        "inferenceProfileName": InferenceProfileName,
        "description": Optional[InferenceProfileDescription],
        "createdAt": Optional[Timestamp],
        "updatedAt": Optional[Timestamp],
        "inferenceProfileArn": InferenceProfileArn,
        "models": InferenceProfileModels,
        "inferenceProfileId": InferenceProfileId,
        "status": InferenceProfileStatus,
        "type": InferenceProfileType,
    },
    total=False,
)


class GetModelCopyJobRequest(ServiceRequest):
    jobArn: ModelCopyJobArn


class GetModelCopyJobResponse(TypedDict, total=False):
    jobArn: ModelCopyJobArn
    status: ModelCopyJobStatus
    creationTime: Timestamp
    targetModelArn: CustomModelArn
    targetModelName: Optional[CustomModelName]
    sourceAccountId: AccountId
    sourceModelArn: ModelArn
    targetModelKmsKeyArn: Optional[KmsKeyArn]
    targetModelTags: Optional[TagList]
    failureMessage: Optional[ErrorMessage]
    sourceModelName: Optional[CustomModelName]


class GetModelCustomizationJobRequest(ServiceRequest):
    jobIdentifier: ModelCustomizationJobIdentifier


class GetModelCustomizationJobResponse(TypedDict, total=False):
    jobArn: ModelCustomizationJobArn
    jobName: JobName
    outputModelName: CustomModelName
    outputModelArn: Optional[CustomModelArn]
    clientRequestToken: Optional[IdempotencyToken]
    roleArn: RoleArn
    status: Optional[ModelCustomizationJobStatus]
    failureMessage: Optional[ErrorMessage]
    creationTime: Timestamp
    lastModifiedTime: Optional[Timestamp]
    endTime: Optional[Timestamp]
    baseModelArn: FoundationModelArn
    hyperParameters: ModelCustomizationHyperParameters
    trainingDataConfig: TrainingDataConfig
    validationDataConfig: ValidationDataConfig
    outputDataConfig: OutputDataConfig
    customizationType: Optional[CustomizationType]
    outputModelKmsKeyArn: Optional[KmsKeyArn]
    trainingMetrics: Optional[TrainingMetrics]
    validationMetrics: Optional[ValidationMetrics]
    vpcConfig: Optional[VpcConfig]


class GetModelImportJobRequest(ServiceRequest):
    jobIdentifier: ModelImportJobIdentifier


class GetModelImportJobResponse(TypedDict, total=False):
    jobArn: Optional[ModelImportJobArn]
    jobName: Optional[JobName]
    importedModelName: Optional[ImportedModelName]
    importedModelArn: Optional[ImportedModelArn]
    roleArn: Optional[RoleArn]
    modelDataSource: Optional[ModelDataSource]
    status: Optional[ModelImportJobStatus]
    failureMessage: Optional[ErrorMessage]
    creationTime: Optional[Timestamp]
    lastModifiedTime: Optional[Timestamp]
    endTime: Optional[Timestamp]
    vpcConfig: Optional[VpcConfig]
    importedModelKmsKeyArn: Optional[KmsKeyArn]


class GetModelInvocationJobRequest(ServiceRequest):
    jobIdentifier: ModelInvocationJobIdentifier


class GetModelInvocationJobResponse(TypedDict, total=False):
    jobArn: ModelInvocationJobArn
    jobName: Optional[ModelInvocationJobName]
    modelId: ModelId
    clientRequestToken: Optional[ModelInvocationIdempotencyToken]
    roleArn: RoleArn
    status: Optional[ModelInvocationJobStatus]
    message: Optional[Message]
    submitTime: Timestamp
    lastModifiedTime: Optional[Timestamp]
    endTime: Optional[Timestamp]
    inputDataConfig: ModelInvocationJobInputDataConfig
    outputDataConfig: ModelInvocationJobOutputDataConfig
    vpcConfig: Optional[VpcConfig]
    timeoutDurationInHours: Optional[ModelInvocationJobTimeoutDurationInHours]
    jobExpirationTime: Optional[Timestamp]


class GetModelInvocationLoggingConfigurationRequest(ServiceRequest):
    pass


class LoggingConfig(TypedDict, total=False):
    """Configuration fields for invocation logging."""

    cloudWatchConfig: Optional[CloudWatchConfig]
    s3Config: Optional[S3Config]
    textDataDeliveryEnabled: Optional[Boolean]
    imageDataDeliveryEnabled: Optional[Boolean]
    embeddingDataDeliveryEnabled: Optional[Boolean]


class GetModelInvocationLoggingConfigurationResponse(TypedDict, total=False):
    loggingConfig: Optional[LoggingConfig]


class GetProvisionedModelThroughputRequest(ServiceRequest):
    provisionedModelId: ProvisionedModelId


class GetProvisionedModelThroughputResponse(TypedDict, total=False):
    modelUnits: PositiveInteger
    desiredModelUnits: PositiveInteger
    provisionedModelName: ProvisionedModelName
    provisionedModelArn: ProvisionedModelArn
    modelArn: ModelArn
    desiredModelArn: ModelArn
    foundationModelArn: FoundationModelArn
    status: ProvisionedModelStatus
    creationTime: Timestamp
    lastModifiedTime: Timestamp
    failureMessage: Optional[ErrorMessage]
    commitmentDuration: Optional[CommitmentDuration]
    commitmentExpirationTime: Optional[Timestamp]


class GuardrailSummary(TypedDict, total=False):
    """Contains details about a guardrail.

    This data type is used in the following API operations:

    -  `ListGuardrails response
       body <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListGuardrails.html#API_ListGuardrails_ResponseSyntax>`__
    """

    id: GuardrailId
    arn: GuardrailArn
    status: GuardrailStatus
    name: GuardrailName
    description: Optional[GuardrailDescription]
    version: GuardrailVersion
    createdAt: Timestamp
    updatedAt: Timestamp


GuardrailSummaries = List[GuardrailSummary]


class ImportedModelSummary(TypedDict, total=False):
    """Information about the imported model."""

    modelArn: ImportedModelArn
    modelName: ImportedModelName
    creationTime: Timestamp
    instructSupported: Optional[InstructSupported]
    modelArchitecture: Optional[ModelArchitecture]


ImportedModelSummaryList = List[ImportedModelSummary]
InferenceProfileSummary = TypedDict(
    "InferenceProfileSummary",
    {
        "inferenceProfileName": InferenceProfileName,
        "description": Optional[InferenceProfileDescription],
        "createdAt": Optional[Timestamp],
        "updatedAt": Optional[Timestamp],
        "inferenceProfileArn": InferenceProfileArn,
        "models": InferenceProfileModels,
        "inferenceProfileId": InferenceProfileId,
        "status": InferenceProfileStatus,
        "type": InferenceProfileType,
    },
    total=False,
)
InferenceProfileSummaries = List[InferenceProfileSummary]


class ListCustomModelsRequest(ServiceRequest):
    creationTimeBefore: Optional[Timestamp]
    creationTimeAfter: Optional[Timestamp]
    nameContains: Optional[CustomModelName]
    baseModelArnEquals: Optional[ModelArn]
    foundationModelArnEquals: Optional[FoundationModelArn]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    sortBy: Optional[SortModelsBy]
    sortOrder: Optional[SortOrder]
    isOwned: Optional[Boolean]


class ListCustomModelsResponse(TypedDict, total=False):
    nextToken: Optional[PaginationToken]
    modelSummaries: Optional[CustomModelSummaryList]


class ListEvaluationJobsRequest(ServiceRequest):
    creationTimeAfter: Optional[Timestamp]
    creationTimeBefore: Optional[Timestamp]
    statusEquals: Optional[EvaluationJobStatus]
    nameContains: Optional[EvaluationJobName]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    sortBy: Optional[SortJobsBy]
    sortOrder: Optional[SortOrder]


class ListEvaluationJobsResponse(TypedDict, total=False):
    nextToken: Optional[PaginationToken]
    jobSummaries: Optional[EvaluationSummaries]


class ListFoundationModelsRequest(ServiceRequest):
    byProvider: Optional[Provider]
    byCustomizationType: Optional[ModelCustomization]
    byOutputModality: Optional[ModelModality]
    byInferenceType: Optional[InferenceType]


class ListFoundationModelsResponse(TypedDict, total=False):
    modelSummaries: Optional[FoundationModelSummaryList]


class ListGuardrailsRequest(ServiceRequest):
    guardrailIdentifier: Optional[GuardrailIdentifier]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]


class ListGuardrailsResponse(TypedDict, total=False):
    guardrails: GuardrailSummaries
    nextToken: Optional[PaginationToken]


class ListImportedModelsRequest(ServiceRequest):
    creationTimeBefore: Optional[Timestamp]
    creationTimeAfter: Optional[Timestamp]
    nameContains: Optional[ImportedModelName]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    sortBy: Optional[SortModelsBy]
    sortOrder: Optional[SortOrder]


class ListImportedModelsResponse(TypedDict, total=False):
    nextToken: Optional[PaginationToken]
    modelSummaries: Optional[ImportedModelSummaryList]


class ListInferenceProfilesRequest(ServiceRequest):
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    typeEquals: Optional[InferenceProfileType]


class ListInferenceProfilesResponse(TypedDict, total=False):
    inferenceProfileSummaries: Optional[InferenceProfileSummaries]
    nextToken: Optional[PaginationToken]


class ListModelCopyJobsRequest(ServiceRequest):
    creationTimeAfter: Optional[Timestamp]
    creationTimeBefore: Optional[Timestamp]
    statusEquals: Optional[ModelCopyJobStatus]
    sourceAccountEquals: Optional[AccountId]
    sourceModelArnEquals: Optional[ModelArn]
    targetModelNameContains: Optional[CustomModelName]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    sortBy: Optional[SortJobsBy]
    sortOrder: Optional[SortOrder]


class ModelCopyJobSummary(TypedDict, total=False):
    """Contains details about each model copy job.

    This data type is used in the following API operations:

    -  `ListModelCopyJobs
       response <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListModelCopyJobs.html#API_ListModelCopyJobs_ResponseSyntax>`__
    """

    jobArn: ModelCopyJobArn
    status: ModelCopyJobStatus
    creationTime: Timestamp
    targetModelArn: CustomModelArn
    targetModelName: Optional[CustomModelName]
    sourceAccountId: AccountId
    sourceModelArn: ModelArn
    targetModelKmsKeyArn: Optional[KmsKeyArn]
    targetModelTags: Optional[TagList]
    failureMessage: Optional[ErrorMessage]
    sourceModelName: Optional[CustomModelName]


ModelCopyJobSummaries = List[ModelCopyJobSummary]


class ListModelCopyJobsResponse(TypedDict, total=False):
    nextToken: Optional[PaginationToken]
    modelCopyJobSummaries: Optional[ModelCopyJobSummaries]


class ListModelCustomizationJobsRequest(ServiceRequest):
    creationTimeAfter: Optional[Timestamp]
    creationTimeBefore: Optional[Timestamp]
    statusEquals: Optional[FineTuningJobStatus]
    nameContains: Optional[JobName]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    sortBy: Optional[SortJobsBy]
    sortOrder: Optional[SortOrder]


class ModelCustomizationJobSummary(TypedDict, total=False):
    """Information about one customization job"""

    jobArn: ModelCustomizationJobArn
    baseModelArn: ModelArn
    jobName: JobName
    status: ModelCustomizationJobStatus
    lastModifiedTime: Optional[Timestamp]
    creationTime: Timestamp
    endTime: Optional[Timestamp]
    customModelArn: Optional[CustomModelArn]
    customModelName: Optional[CustomModelName]
    customizationType: Optional[CustomizationType]


ModelCustomizationJobSummaries = List[ModelCustomizationJobSummary]


class ListModelCustomizationJobsResponse(TypedDict, total=False):
    nextToken: Optional[PaginationToken]
    modelCustomizationJobSummaries: Optional[ModelCustomizationJobSummaries]


class ListModelImportJobsRequest(ServiceRequest):
    creationTimeAfter: Optional[Timestamp]
    creationTimeBefore: Optional[Timestamp]
    statusEquals: Optional[ModelImportJobStatus]
    nameContains: Optional[JobName]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    sortBy: Optional[SortJobsBy]
    sortOrder: Optional[SortOrder]


class ModelImportJobSummary(TypedDict, total=False):
    """Information about the import job."""

    jobArn: ModelImportJobArn
    jobName: JobName
    status: ModelImportJobStatus
    lastModifiedTime: Optional[Timestamp]
    creationTime: Timestamp
    endTime: Optional[Timestamp]
    importedModelArn: Optional[ImportedModelArn]
    importedModelName: Optional[ImportedModelName]


ModelImportJobSummaries = List[ModelImportJobSummary]


class ListModelImportJobsResponse(TypedDict, total=False):
    nextToken: Optional[PaginationToken]
    modelImportJobSummaries: Optional[ModelImportJobSummaries]


class ListModelInvocationJobsRequest(ServiceRequest):
    submitTimeAfter: Optional[Timestamp]
    submitTimeBefore: Optional[Timestamp]
    statusEquals: Optional[ModelInvocationJobStatus]
    nameContains: Optional[ModelInvocationJobName]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    sortBy: Optional[SortJobsBy]
    sortOrder: Optional[SortOrder]


class ModelInvocationJobSummary(TypedDict, total=False):
    """A summary of a batch inference job."""

    jobArn: ModelInvocationJobArn
    jobName: ModelInvocationJobName
    modelId: ModelId
    clientRequestToken: Optional[ModelInvocationIdempotencyToken]
    roleArn: RoleArn
    status: Optional[ModelInvocationJobStatus]
    message: Optional[Message]
    submitTime: Timestamp
    lastModifiedTime: Optional[Timestamp]
    endTime: Optional[Timestamp]
    inputDataConfig: ModelInvocationJobInputDataConfig
    outputDataConfig: ModelInvocationJobOutputDataConfig
    vpcConfig: Optional[VpcConfig]
    timeoutDurationInHours: Optional[ModelInvocationJobTimeoutDurationInHours]
    jobExpirationTime: Optional[Timestamp]


ModelInvocationJobSummaries = List[ModelInvocationJobSummary]


class ListModelInvocationJobsResponse(TypedDict, total=False):
    nextToken: Optional[PaginationToken]
    invocationJobSummaries: Optional[ModelInvocationJobSummaries]


class ListProvisionedModelThroughputsRequest(ServiceRequest):
    creationTimeAfter: Optional[Timestamp]
    creationTimeBefore: Optional[Timestamp]
    statusEquals: Optional[ProvisionedModelStatus]
    modelArnEquals: Optional[ModelArn]
    nameContains: Optional[ProvisionedModelName]
    maxResults: Optional[MaxResults]
    nextToken: Optional[PaginationToken]
    sortBy: Optional[SortByProvisionedModels]
    sortOrder: Optional[SortOrder]


class ProvisionedModelSummary(TypedDict, total=False):
    """A summary of information about a Provisioned Throughput.

    This data type is used in the following API operations:

    -  `ListProvisionedThroughputs
       response <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_ListProvisionedModelThroughputs.html#API_ListProvisionedModelThroughputs_ResponseSyntax>`__
    """

    provisionedModelName: ProvisionedModelName
    provisionedModelArn: ProvisionedModelArn
    modelArn: ModelArn
    desiredModelArn: ModelArn
    foundationModelArn: FoundationModelArn
    modelUnits: PositiveInteger
    desiredModelUnits: PositiveInteger
    status: ProvisionedModelStatus
    commitmentDuration: Optional[CommitmentDuration]
    commitmentExpirationTime: Optional[Timestamp]
    creationTime: Timestamp
    lastModifiedTime: Timestamp


ProvisionedModelSummaries = List[ProvisionedModelSummary]


class ListProvisionedModelThroughputsResponse(TypedDict, total=False):
    nextToken: Optional[PaginationToken]
    provisionedModelSummaries: Optional[ProvisionedModelSummaries]


class ListTagsForResourceRequest(ServiceRequest):
    resourceARN: TaggableResourcesArn


class ListTagsForResourceResponse(TypedDict, total=False):
    tags: Optional[TagList]


class PutModelInvocationLoggingConfigurationRequest(ServiceRequest):
    loggingConfig: LoggingConfig


class PutModelInvocationLoggingConfigurationResponse(TypedDict, total=False):
    pass


class StopEvaluationJobRequest(ServiceRequest):
    jobIdentifier: EvaluationJobIdentifier


class StopEvaluationJobResponse(TypedDict, total=False):
    pass


class StopModelCustomizationJobRequest(ServiceRequest):
    jobIdentifier: ModelCustomizationJobIdentifier


class StopModelCustomizationJobResponse(TypedDict, total=False):
    pass


class StopModelInvocationJobRequest(ServiceRequest):
    jobIdentifier: ModelInvocationJobIdentifier


class StopModelInvocationJobResponse(TypedDict, total=False):
    pass


TagKeyList = List[TagKey]


class TagResourceRequest(ServiceRequest):
    resourceARN: TaggableResourcesArn
    tags: TagList


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    resourceARN: TaggableResourcesArn
    tagKeys: TagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateGuardrailRequest(ServiceRequest):
    guardrailIdentifier: GuardrailIdentifier
    name: GuardrailName
    description: Optional[GuardrailDescription]
    topicPolicyConfig: Optional[GuardrailTopicPolicyConfig]
    contentPolicyConfig: Optional[GuardrailContentPolicyConfig]
    wordPolicyConfig: Optional[GuardrailWordPolicyConfig]
    sensitiveInformationPolicyConfig: Optional[GuardrailSensitiveInformationPolicyConfig]
    contextualGroundingPolicyConfig: Optional[GuardrailContextualGroundingPolicyConfig]
    blockedInputMessaging: GuardrailBlockedMessaging
    blockedOutputsMessaging: GuardrailBlockedMessaging
    kmsKeyId: Optional[KmsKeyId]


class UpdateGuardrailResponse(TypedDict, total=False):
    guardrailId: GuardrailId
    guardrailArn: GuardrailArn
    version: GuardrailDraftVersion
    updatedAt: Timestamp


class UpdateProvisionedModelThroughputRequest(ServiceRequest):
    provisionedModelId: ProvisionedModelId
    desiredProvisionedModelName: Optional[ProvisionedModelName]
    desiredModelId: Optional[ModelIdentifier]


class UpdateProvisionedModelThroughputResponse(TypedDict, total=False):
    pass


class BedrockApi:
    service = "bedrock"
    version = "2023-04-20"

    @handler("BatchDeleteEvaluationJob")
    def batch_delete_evaluation_job(
        self, context: RequestContext, job_identifiers: EvaluationJobIdentifiers, **kwargs
    ) -> BatchDeleteEvaluationJobResponse:
        """Creates a batch deletion job. A model evaluation job can only be deleted
        if it has following status ``FAILED``, ``COMPLETED``, and ``STOPPED``.
        You can request up to 25 model evaluation jobs be deleted in a single
        request.

        :param job_identifiers: An array of model evaluation job ARNs to be deleted.
        :returns: BatchDeleteEvaluationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateEvaluationJob")
    def create_evaluation_job(
        self,
        context: RequestContext,
        job_name: EvaluationJobName,
        role_arn: RoleArn,
        evaluation_config: EvaluationConfig,
        inference_config: EvaluationInferenceConfig,
        output_data_config: EvaluationOutputDataConfig,
        job_description: EvaluationJobDescription = None,
        client_request_token: IdempotencyToken = None,
        customer_encryption_key_id: KmsKeyId = None,
        job_tags: TagList = None,
        **kwargs,
    ) -> CreateEvaluationJobResponse:
        """API operation for creating and managing Amazon Bedrock automatic model
        evaluation jobs and model evaluation jobs that use human workers. To
        learn more about the requirements for creating a model evaluation job
        see, `Model
        evaluation <https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html>`__.

        :param job_name: The name of the model evaluation job.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM service role that Amazon
        Bedrock can assume to perform tasks on your behalf.
        :param evaluation_config: Specifies whether the model evaluation job is automatic or uses human
        worker.
        :param inference_config: Specify the models you want to use in your model evaluation job.
        :param output_data_config: An object that defines where the results of model evaluation job will be
        saved in Amazon S3.
        :param job_description: A description of the model evaluation job.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than one time.
        :param customer_encryption_key_id: Specify your customer managed key ARN that will be used to encrypt your
        model evaluation job.
        :param job_tags: Tags to attach to the model evaluation job.
        :returns: CreateEvaluationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateGuardrail")
    def create_guardrail(
        self,
        context: RequestContext,
        name: GuardrailName,
        blocked_input_messaging: GuardrailBlockedMessaging,
        blocked_outputs_messaging: GuardrailBlockedMessaging,
        description: GuardrailDescription = None,
        topic_policy_config: GuardrailTopicPolicyConfig = None,
        content_policy_config: GuardrailContentPolicyConfig = None,
        word_policy_config: GuardrailWordPolicyConfig = None,
        sensitive_information_policy_config: GuardrailSensitiveInformationPolicyConfig = None,
        contextual_grounding_policy_config: GuardrailContextualGroundingPolicyConfig = None,
        kms_key_id: KmsKeyId = None,
        tags: TagList = None,
        client_request_token: IdempotencyToken = None,
        **kwargs,
    ) -> CreateGuardrailResponse:
        """Creates a guardrail to block topics and to implement safeguards for your
        generative AI applications.

        You can configure the following policies in a guardrail to avoid
        undesirable and harmful content, filter out denied topics and words, and
        remove sensitive information for privacy protection.

        -  **Content filters** - Adjust filter strengths to block input prompts
           or model responses containing harmful content.

        -  **Denied topics** - Define a set of topics that are undesirable in
           the context of your application. These topics will be blocked if
           detected in user queries or model responses.

        -  **Word filters** - Configure filters to block undesirable words,
           phrases, and profanity. Such words can include offensive terms,
           competitor names etc.

        -  **Sensitive information filters** - Block or mask sensitive
           information such as personally identifiable information (PII) or
           custom regex in user inputs and model responses.

        In addition to the above policies, you can also configure the messages
        to be returned to the user if a user input or model response is in
        violation of the policies defined in the guardrail.

        For more information, see `Guardrails for Amazon
        Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html>`__
        in the *Amazon Bedrock User Guide*.

        :param name: The name to give the guardrail.
        :param blocked_input_messaging: The message to return when the guardrail blocks a prompt.
        :param blocked_outputs_messaging: The message to return when the guardrail blocks a model response.
        :param description: A description of the guardrail.
        :param topic_policy_config: The topic policies to configure for the guardrail.
        :param content_policy_config: The content filter policies to configure for the guardrail.
        :param word_policy_config: The word policy you configure for the guardrail.
        :param sensitive_information_policy_config: The sensitive information policy to configure for the guardrail.
        :param contextual_grounding_policy_config: The contextual grounding policy configuration used to create a
        guardrail.
        :param kms_key_id: The ARN of the KMS key that you use to encrypt the guardrail.
        :param tags: The tags that you want to attach to the guardrail.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than once.
        :returns: CreateGuardrailResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises TooManyTagsException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateGuardrailVersion")
    def create_guardrail_version(
        self,
        context: RequestContext,
        guardrail_identifier: GuardrailIdentifier,
        description: GuardrailDescription = None,
        client_request_token: IdempotencyToken = None,
        **kwargs,
    ) -> CreateGuardrailVersionResponse:
        """Creates a version of the guardrail. Use this API to create a snapshot of
        the guardrail when you are satisfied with a configuration, or to compare
        the configuration with another version.

        :param guardrail_identifier: The unique identifier of the guardrail.
        :param description: A description of the guardrail version.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than once.
        :returns: CreateGuardrailVersionResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateInferenceProfile")
    def create_inference_profile(
        self,
        context: RequestContext,
        inference_profile_name: InferenceProfileName,
        model_source: InferenceProfileModelSource,
        description: InferenceProfileDescription = None,
        client_request_token: IdempotencyToken = None,
        tags: TagList = None,
        **kwargs,
    ) -> CreateInferenceProfileResponse:
        """Creates an application inference profile to track metrics and costs when
        invoking a model. To create an application inference profile for a
        foundation model in one region, specify the ARN of the model in that
        region. To create an application inference profile for a foundation
        model across multiple regions, specify the ARN of the system-defined
        inference profile that contains the regions that you want to route
        requests to. For more information, see `Increase throughput and
        resilience with cross-region inference in Amazon
        Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>`__.
        in the Amazon Bedrock User Guide.

        :param inference_profile_name: A name for the inference profile.
        :param model_source: The foundation model or system-defined inference profile that the
        inference profile will track metrics and costs for.
        :param description: A description for the inference profile.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than one time.
        :param tags: An array of objects, each of which contains a tag and its value.
        :returns: CreateInferenceProfileResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises TooManyTagsException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateModelCopyJob")
    def create_model_copy_job(
        self,
        context: RequestContext,
        source_model_arn: ModelArn,
        target_model_name: CustomModelName,
        model_kms_key_id: KmsKeyId = None,
        target_model_tags: TagList = None,
        client_request_token: IdempotencyToken = None,
        **kwargs,
    ) -> CreateModelCopyJobResponse:
        """Copies a model to another region so that it can be used there. For more
        information, see `Copy models to be used in other
        regions <https://docs.aws.amazon.com/bedrock/latest/userguide/copy-model.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param source_model_arn: The Amazon Resource Name (ARN) of the model to be copied.
        :param target_model_name: A name for the copied model.
        :param model_kms_key_id: The ARN of the KMS key that you use to encrypt the model copy.
        :param target_model_tags: Tags to associate with the target model.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than one time.
        :returns: CreateModelCopyJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises TooManyTagsException:
        """
        raise NotImplementedError

    @handler("CreateModelCustomizationJob")
    def create_model_customization_job(
        self,
        context: RequestContext,
        job_name: JobName,
        custom_model_name: CustomModelName,
        role_arn: RoleArn,
        base_model_identifier: BaseModelIdentifier,
        training_data_config: TrainingDataConfig,
        output_data_config: OutputDataConfig,
        hyper_parameters: ModelCustomizationHyperParameters,
        client_request_token: IdempotencyToken = None,
        customization_type: CustomizationType = None,
        custom_model_kms_key_id: KmsKeyId = None,
        job_tags: TagList = None,
        custom_model_tags: TagList = None,
        validation_data_config: ValidationDataConfig = None,
        vpc_config: VpcConfig = None,
        **kwargs,
    ) -> CreateModelCustomizationJobResponse:
        """Creates a fine-tuning job to customize a base model.

        You specify the base foundation model and the location of the training
        data. After the model-customization job completes successfully, your
        custom model resource will be ready to use. Amazon Bedrock returns
        validation loss metrics and output generations after the job completes.

        For information on the format of training and validation data, see
        `Prepare the
        datasets <https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-prepare.html>`__.

        Model-customization jobs are asynchronous and the completion time
        depends on the base model and the training/validation data size. To
        monitor a job, use the ``GetModelCustomizationJob`` operation to
        retrieve the job status.

        For more information, see `Custom
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param job_name: A name for the fine-tuning job.
        :param custom_model_name: A name for the resulting custom model.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM service role that Amazon
        Bedrock can assume to perform tasks on your behalf.
        :param base_model_identifier: Name of the base model.
        :param training_data_config: Information about the training dataset.
        :param output_data_config: S3 location for the output data.
        :param hyper_parameters: Parameters related to tuning the model.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than one time.
        :param customization_type: The customization type.
        :param custom_model_kms_key_id: The custom model is encrypted at rest using this key.
        :param job_tags: Tags to attach to the job.
        :param custom_model_tags: Tags to attach to the resulting custom model.
        :param validation_data_config: Information about the validation dataset.
        :param vpc_config: The configuration of the Virtual Private Cloud (VPC) that contains the
        resources that you're using for this job.
        :returns: CreateModelCustomizationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises TooManyTagsException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateModelImportJob")
    def create_model_import_job(
        self,
        context: RequestContext,
        job_name: JobName,
        imported_model_name: ImportedModelName,
        role_arn: RoleArn,
        model_data_source: ModelDataSource,
        job_tags: TagList = None,
        imported_model_tags: TagList = None,
        client_request_token: IdempotencyToken = None,
        vpc_config: VpcConfig = None,
        imported_model_kms_key_id: KmsKeyId = None,
        **kwargs,
    ) -> CreateModelImportJobResponse:
        """Creates a model import job to import model that you have customized in
        other environments, such as Amazon SageMaker. For more information, see
        `Import a customized
        model <https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html>`__

        :param job_name: The name of the import job.
        :param imported_model_name: The name of the imported model.
        :param role_arn: The Amazon Resource Name (ARN) of the model import job.
        :param model_data_source: The data source for the imported model.
        :param job_tags: Tags to attach to this import job.
        :param imported_model_tags: Tags to attach to the imported model.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than one time.
        :param vpc_config: VPC configuration parameters for the private Virtual Private Cloud (VPC)
        that contains the resources you are using for the import job.
        :param imported_model_kms_key_id: The imported model is encrypted at rest using this key.
        :returns: CreateModelImportJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises TooManyTagsException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateModelInvocationJob")
    def create_model_invocation_job(
        self,
        context: RequestContext,
        job_name: ModelInvocationJobName,
        role_arn: RoleArn,
        model_id: ModelId,
        input_data_config: ModelInvocationJobInputDataConfig,
        output_data_config: ModelInvocationJobOutputDataConfig,
        client_request_token: ModelInvocationIdempotencyToken = None,
        vpc_config: VpcConfig = None,
        timeout_duration_in_hours: ModelInvocationJobTimeoutDurationInHours = None,
        tags: TagList = None,
        **kwargs,
    ) -> CreateModelInvocationJobResponse:
        """Creates a batch inference job to invoke a model on multiple prompts.
        Format your data according to `Format your inference
        data <https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-data>`__
        and upload it to an Amazon S3 bucket. For more information, see `Process
        multiple prompts with batch
        inference <https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html>`__.

        The response returns a ``jobArn`` that you can use to stop or get
        details about the job.

        :param job_name: A name to give the batch inference job.
        :param role_arn: The Amazon Resource Name (ARN) of the service role with permissions to
        carry out and manage batch inference.
        :param model_id: The unique identifier of the foundation model to use for the batch
        inference job.
        :param input_data_config: Details about the location of the input to the batch inference job.
        :param output_data_config: Details about the location of the output of the batch inference job.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than one time.
        :param vpc_config: The configuration of the Virtual Private Cloud (VPC) for the data in the
        batch inference job.
        :param timeout_duration_in_hours: The number of hours after which to force the batch inference job to time
        out.
        :param tags: Any tags to associate with the batch inference job.
        :returns: CreateModelInvocationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateProvisionedModelThroughput")
    def create_provisioned_model_throughput(
        self,
        context: RequestContext,
        model_units: PositiveInteger,
        provisioned_model_name: ProvisionedModelName,
        model_id: ModelIdentifier,
        client_request_token: IdempotencyToken = None,
        commitment_duration: CommitmentDuration = None,
        tags: TagList = None,
        **kwargs,
    ) -> CreateProvisionedModelThroughputResponse:
        """Creates dedicated throughput for a base or custom model with the model
        units and for the duration that you specify. For pricing details, see
        `Amazon Bedrock Pricing <http://aws.amazon.com/bedrock/pricing/>`__. For
        more information, see `Provisioned
        Throughput <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param model_units: Number of model units to allocate.
        :param provisioned_model_name: The name for this Provisioned Throughput.
        :param model_id: The Amazon Resource Name (ARN) or name of the model to associate with
        this Provisioned Throughput.
        :param client_request_token: A unique, case-sensitive identifier to ensure that the API request
        completes no more than one time.
        :param commitment_duration: The commitment duration requested for the Provisioned Throughput.
        :param tags: Tags to associate with this Provisioned Throughput.
        :returns: CreateProvisionedModelThroughputResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises TooManyTagsException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteCustomModel")
    def delete_custom_model(
        self, context: RequestContext, model_identifier: ModelIdentifier, **kwargs
    ) -> DeleteCustomModelResponse:
        """Deletes a custom model that you created earlier. For more information,
        see `Custom
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param model_identifier: Name of the model to delete.
        :returns: DeleteCustomModelResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteGuardrail")
    def delete_guardrail(
        self,
        context: RequestContext,
        guardrail_identifier: GuardrailIdentifier,
        guardrail_version: GuardrailNumericalVersion = None,
        **kwargs,
    ) -> DeleteGuardrailResponse:
        """Deletes a guardrail.

        -  To delete a guardrail, only specify the ARN of the guardrail in the
           ``guardrailIdentifier`` field. If you delete a guardrail, all of its
           versions will be deleted.

        -  To delete a version of a guardrail, specify the ARN of the guardrail
           in the ``guardrailIdentifier`` field and the version in the
           ``guardrailVersion`` field.

        :param guardrail_identifier: The unique identifier of the guardrail.
        :param guardrail_version: The version of the guardrail.
        :returns: DeleteGuardrailResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteImportedModel")
    def delete_imported_model(
        self, context: RequestContext, model_identifier: ImportedModelIdentifier, **kwargs
    ) -> DeleteImportedModelResponse:
        """Deletes a custom model that you imported earlier. For more information,
        see `Import a customized
        model <https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param model_identifier: Name of the imported model to delete.
        :returns: DeleteImportedModelResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteInferenceProfile")
    def delete_inference_profile(
        self,
        context: RequestContext,
        inference_profile_identifier: InferenceProfileIdentifier,
        **kwargs,
    ) -> DeleteInferenceProfileResponse:
        """Deletes an application inference profile. For more information, see
        `Increase throughput and resilience with cross-region inference in
        Amazon
        Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>`__.
        in the Amazon Bedrock User Guide.

        :param inference_profile_identifier: The Amazon Resource Name (ARN) or ID of the application inference
        profile to delete.
        :returns: DeleteInferenceProfileResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteModelInvocationLoggingConfiguration")
    def delete_model_invocation_logging_configuration(
        self, context: RequestContext, **kwargs
    ) -> DeleteModelInvocationLoggingConfigurationResponse:
        """Delete the invocation logging.

        :returns: DeleteModelInvocationLoggingConfigurationResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteProvisionedModelThroughput")
    def delete_provisioned_model_throughput(
        self, context: RequestContext, provisioned_model_id: ProvisionedModelId, **kwargs
    ) -> DeleteProvisionedModelThroughputResponse:
        """Deletes a Provisioned Throughput. You can't delete a Provisioned
        Throughput before the commitment term is over. For more information, see
        `Provisioned
        Throughput <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param provisioned_model_id: The Amazon Resource Name (ARN) or name of the Provisioned Throughput.
        :returns: DeleteProvisionedModelThroughputResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetCustomModel")
    def get_custom_model(
        self, context: RequestContext, model_identifier: ModelIdentifier, **kwargs
    ) -> GetCustomModelResponse:
        """Get the properties associated with a Amazon Bedrock custom model that
        you have created.For more information, see `Custom
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param model_identifier: Name or Amazon Resource Name (ARN) of the custom model.
        :returns: GetCustomModelResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetEvaluationJob")
    def get_evaluation_job(
        self, context: RequestContext, job_identifier: EvaluationJobIdentifier, **kwargs
    ) -> GetEvaluationJobResponse:
        """Retrieves the properties associated with a model evaluation job,
        including the status of the job. For more information, see `Model
        evaluation <https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html>`__.

        :param job_identifier: The Amazon Resource Name (ARN) of the model evaluation job.
        :returns: GetEvaluationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetFoundationModel")
    def get_foundation_model(
        self, context: RequestContext, model_identifier: ModelIdentifier, **kwargs
    ) -> GetFoundationModelResponse:
        """Get details about a Amazon Bedrock foundation model.

        :param model_identifier: The model identifier.
        :returns: GetFoundationModelResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetGuardrail")
    def get_guardrail(
        self,
        context: RequestContext,
        guardrail_identifier: GuardrailIdentifier,
        guardrail_version: GuardrailVersion = None,
        **kwargs,
    ) -> GetGuardrailResponse:
        """Gets details about a guardrail. If you don't specify a version, the
        response returns details for the ``DRAFT`` version.

        :param guardrail_identifier: The unique identifier of the guardrail for which to get details.
        :param guardrail_version: The version of the guardrail for which to get details.
        :returns: GetGuardrailResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetImportedModel")
    def get_imported_model(
        self, context: RequestContext, model_identifier: ImportedModelIdentifier, **kwargs
    ) -> GetImportedModelResponse:
        """Gets properties associated with a customized model you imported.

        :param model_identifier: Name or Amazon Resource Name (ARN) of the imported model.
        :returns: GetImportedModelResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetInferenceProfile")
    def get_inference_profile(
        self,
        context: RequestContext,
        inference_profile_identifier: InferenceProfileIdentifier,
        **kwargs,
    ) -> GetInferenceProfileResponse:
        """Gets information about an inference profile. For more information, see
        `Increase throughput and resilience with cross-region inference in
        Amazon
        Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>`__.
        in the Amazon Bedrock User Guide.

        :param inference_profile_identifier: The ID or Amazon Resource Name (ARN) of the inference profile.
        :returns: GetInferenceProfileResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetModelCopyJob")
    def get_model_copy_job(
        self, context: RequestContext, job_arn: ModelCopyJobArn, **kwargs
    ) -> GetModelCopyJobResponse:
        """Retrieves information about a model copy job. For more information, see
        `Copy models to be used in other
        regions <https://docs.aws.amazon.com/bedrock/latest/userguide/copy-model.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param job_arn: The Amazon Resource Name (ARN) of the model copy job.
        :returns: GetModelCopyJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetModelCustomizationJob")
    def get_model_customization_job(
        self, context: RequestContext, job_identifier: ModelCustomizationJobIdentifier, **kwargs
    ) -> GetModelCustomizationJobResponse:
        """Retrieves the properties associated with a model-customization job,
        including the status of the job. For more information, see `Custom
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param job_identifier: Identifier for the customization job.
        :returns: GetModelCustomizationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetModelImportJob")
    def get_model_import_job(
        self, context: RequestContext, job_identifier: ModelImportJobIdentifier, **kwargs
    ) -> GetModelImportJobResponse:
        """Retrieves the properties associated with import model job, including the
        status of the job. For more information, see `Import a customized
        model <https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param job_identifier: The identifier of the import job.
        :returns: GetModelImportJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetModelInvocationJob")
    def get_model_invocation_job(
        self, context: RequestContext, job_identifier: ModelInvocationJobIdentifier, **kwargs
    ) -> GetModelInvocationJobResponse:
        """Gets details about a batch inference job. For more information, see
        `View details about a batch inference
        job <https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-manage.html#batch-inference-view>`__

        :param job_identifier: The Amazon Resource Name (ARN) of the batch inference job.
        :returns: GetModelInvocationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetModelInvocationLoggingConfiguration")
    def get_model_invocation_logging_configuration(
        self, context: RequestContext, **kwargs
    ) -> GetModelInvocationLoggingConfigurationResponse:
        """Get the current configuration values for model invocation logging.

        :returns: GetModelInvocationLoggingConfigurationResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetProvisionedModelThroughput")
    def get_provisioned_model_throughput(
        self, context: RequestContext, provisioned_model_id: ProvisionedModelId, **kwargs
    ) -> GetProvisionedModelThroughputResponse:
        """Returns details for a Provisioned Throughput. For more information, see
        `Provisioned
        Throughput <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param provisioned_model_id: The Amazon Resource Name (ARN) or name of the Provisioned Throughput.
        :returns: GetProvisionedModelThroughputResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListCustomModels")
    def list_custom_models(
        self,
        context: RequestContext,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
        name_contains: CustomModelName = None,
        base_model_arn_equals: ModelArn = None,
        foundation_model_arn_equals: FoundationModelArn = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        sort_by: SortModelsBy = None,
        sort_order: SortOrder = None,
        is_owned: Boolean = None,
        **kwargs,
    ) -> ListCustomModelsResponse:
        """Returns a list of the custom models that you have created with the
        ``CreateModelCustomizationJob`` operation.

        For more information, see `Custom
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param creation_time_before: Return custom models created before the specified time.
        :param creation_time_after: Return custom models created after the specified time.
        :param name_contains: Return custom models only if the job name contains these characters.
        :param base_model_arn_equals: Return custom models only if the base model Amazon Resource Name (ARN)
        matches this parameter.
        :param foundation_model_arn_equals: Return custom models only if the foundation model Amazon Resource Name
        (ARN) matches this parameter.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: If the total number of results is greater than the ``maxResults`` value
        provided in the request, enter the token returned in the ``nextToken``
        field in the response in this field to return the next batch of results.
        :param sort_by: The field to sort by in the returned list of models.
        :param sort_order: The sort order of the results.
        :param is_owned: Return custom models depending on if the current account owns them
        (``true``) or if they were shared with the current account (``false``).
        :returns: ListCustomModelsResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListEvaluationJobs")
    def list_evaluation_jobs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        status_equals: EvaluationJobStatus = None,
        name_contains: EvaluationJobName = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        sort_by: SortJobsBy = None,
        sort_order: SortOrder = None,
        **kwargs,
    ) -> ListEvaluationJobsResponse:
        """Lists model evaluation jobs.

        :param creation_time_after: A filter that includes model evaluation jobs created after the time
        specified.
        :param creation_time_before: A filter that includes model evaluation jobs created prior to the time
        specified.
        :param status_equals: Only return jobs where the status condition is met.
        :param name_contains: Query parameter string for model evaluation job names.
        :param max_results: The maximum number of results to return.
        :param next_token: Continuation token from the previous response, for Amazon Bedrock to
        list the next set of results.
        :param sort_by: Allows you to sort model evaluation jobs by when they were created.
        :param sort_order: How you want the order of jobs sorted.
        :returns: ListEvaluationJobsResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListFoundationModels")
    def list_foundation_models(
        self,
        context: RequestContext,
        by_provider: Provider = None,
        by_customization_type: ModelCustomization = None,
        by_output_modality: ModelModality = None,
        by_inference_type: InferenceType = None,
        **kwargs,
    ) -> ListFoundationModelsResponse:
        """Lists Amazon Bedrock foundation models that you can use. You can filter
        the results with the request parameters. For more information, see
        `Foundation
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/foundation-models.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param by_provider: Return models belonging to the model provider that you specify.
        :param by_customization_type: Return models that support the customization type that you specify.
        :param by_output_modality: Return models that support the output modality that you specify.
        :param by_inference_type: Return models that support the inference type that you specify.
        :returns: ListFoundationModelsResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListGuardrails")
    def list_guardrails(
        self,
        context: RequestContext,
        guardrail_identifier: GuardrailIdentifier = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        **kwargs,
    ) -> ListGuardrailsResponse:
        """Lists details about all the guardrails in an account. To list the
        ``DRAFT`` version of all your guardrails, don't specify the
        ``guardrailIdentifier`` field. To list all versions of a guardrail,
        specify the ARN of the guardrail in the ``guardrailIdentifier`` field.

        You can set the maximum number of results to return in a response in the
        ``maxResults`` field. If there are more results than the number you set,
        the response returns a ``nextToken`` that you can send in another
        ``ListGuardrails`` request to see the next batch of results.

        :param guardrail_identifier: The unique identifier of the guardrail.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: If there are more results than were returned in the response, the
        response returns a ``nextToken`` that you can send in another
        ``ListGuardrails`` request to see the next batch of results.
        :returns: ListGuardrailsResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListImportedModels")
    def list_imported_models(
        self,
        context: RequestContext,
        creation_time_before: Timestamp = None,
        creation_time_after: Timestamp = None,
        name_contains: ImportedModelName = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        sort_by: SortModelsBy = None,
        sort_order: SortOrder = None,
        **kwargs,
    ) -> ListImportedModelsResponse:
        """Returns a list of models you've imported. You can filter the results to
        return based on one or more criteria. For more information, see `Import
        a customized
        model <https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param creation_time_before: Return imported models that created before the specified time.
        :param creation_time_after: Return imported models that were created after the specified time.
        :param name_contains: Return imported models only if the model name contains these characters.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: If the total number of results is greater than the ``maxResults`` value
        provided in the request, enter the token returned in the ``nextToken``
        field in the response in this field to return the next batch of results.
        :param sort_by: The field to sort by in the returned list of imported models.
        :param sort_order: Specifies whetehr to sort the results in ascending or descending order.
        :returns: ListImportedModelsResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListInferenceProfiles")
    def list_inference_profiles(
        self,
        context: RequestContext,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        type_equals: InferenceProfileType = None,
        **kwargs,
    ) -> ListInferenceProfilesResponse:
        """Returns a list of inference profiles that you can use. For more
        information, see `Increase throughput and resilience with cross-region
        inference in Amazon
        Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>`__.
        in the Amazon Bedrock User Guide.

        :param max_results: The maximum number of results to return in the response.
        :param next_token: If the total number of results is greater than the ``maxResults`` value
        provided in the request, enter the token returned in the ``nextToken``
        field in the response in this field to return the next batch of results.
        :param type_equals: Filters for inference profiles that match the type you specify.
        :returns: ListInferenceProfilesResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListModelCopyJobs")
    def list_model_copy_jobs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        status_equals: ModelCopyJobStatus = None,
        source_account_equals: AccountId = None,
        source_model_arn_equals: ModelArn = None,
        target_model_name_contains: CustomModelName = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        sort_by: SortJobsBy = None,
        sort_order: SortOrder = None,
        **kwargs,
    ) -> ListModelCopyJobsResponse:
        """Returns a list of model copy jobs that you have submitted. You can
        filter the jobs to return based on one or more criteria. For more
        information, see `Copy models to be used in other
        regions <https://docs.aws.amazon.com/bedrock/latest/userguide/copy-model.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param creation_time_after: Filters for model copy jobs created after the specified time.
        :param creation_time_before: Filters for model copy jobs created before the specified time.
        :param status_equals: Filters for model copy jobs whose status matches the value that you
        specify.
        :param source_account_equals: Filters for model copy jobs in which the account that the source model
        belongs to is equal to the value that you specify.
        :param source_model_arn_equals: Filters for model copy jobs in which the Amazon Resource Name (ARN) of
        the source model to is equal to the value that you specify.
        :param target_model_name_contains: Filters for model copy jobs in which the name of the copied model
        contains the string that you specify.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: If the total number of results is greater than the ``maxResults`` value
        provided in the request, enter the token returned in the ``nextToken``
        field in the response in this field to return the next batch of results.
        :param sort_by: The field to sort by in the returned list of model copy jobs.
        :param sort_order: Specifies whether to sort the results in ascending or descending order.
        :returns: ListModelCopyJobsResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListModelCustomizationJobs")
    def list_model_customization_jobs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        status_equals: FineTuningJobStatus = None,
        name_contains: JobName = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        sort_by: SortJobsBy = None,
        sort_order: SortOrder = None,
        **kwargs,
    ) -> ListModelCustomizationJobsResponse:
        """Returns a list of model customization jobs that you have submitted. You
        can filter the jobs to return based on one or more criteria.

        For more information, see `Custom
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param creation_time_after: Return customization jobs created after the specified time.
        :param creation_time_before: Return customization jobs created before the specified time.
        :param status_equals: Return customization jobs with the specified status.
        :param name_contains: Return customization jobs only if the job name contains these
        characters.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: If the total number of results is greater than the ``maxResults`` value
        provided in the request, enter the token returned in the ``nextToken``
        field in the response in this field to return the next batch of results.
        :param sort_by: The field to sort by in the returned list of jobs.
        :param sort_order: The sort order of the results.
        :returns: ListModelCustomizationJobsResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListModelImportJobs")
    def list_model_import_jobs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        status_equals: ModelImportJobStatus = None,
        name_contains: JobName = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        sort_by: SortJobsBy = None,
        sort_order: SortOrder = None,
        **kwargs,
    ) -> ListModelImportJobsResponse:
        """Returns a list of import jobs you've submitted. You can filter the
        results to return based on one or more criteria. For more information,
        see `Import a customized
        model <https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param creation_time_after: Return import jobs that were created after the specified time.
        :param creation_time_before: Return import jobs that were created before the specified time.
        :param status_equals: Return imported jobs with the specified status.
        :param name_contains: Return imported jobs only if the job name contains these characters.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: If the total number of results is greater than the ``maxResults`` value
        provided in the request, enter the token returned in the ``nextToken``
        field in the response in this field to return the next batch of results.
        :param sort_by: The field to sort by in the returned list of imported jobs.
        :param sort_order: Specifies whether to sort the results in ascending or descending order.
        :returns: ListModelImportJobsResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListModelInvocationJobs")
    def list_model_invocation_jobs(
        self,
        context: RequestContext,
        submit_time_after: Timestamp = None,
        submit_time_before: Timestamp = None,
        status_equals: ModelInvocationJobStatus = None,
        name_contains: ModelInvocationJobName = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        sort_by: SortJobsBy = None,
        sort_order: SortOrder = None,
        **kwargs,
    ) -> ListModelInvocationJobsResponse:
        """Lists all batch inference jobs in the account. For more information, see
        `View details about a batch inference
        job <https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-manage.html#batch-inference-view>`__.

        :param submit_time_after: Specify a time to filter for batch inference jobs that were submitted
        after the time you specify.
        :param submit_time_before: Specify a time to filter for batch inference jobs that were submitted
        before the time you specify.
        :param status_equals: Specify a status to filter for batch inference jobs whose statuses match
        the string you specify.
        :param name_contains: Specify a string to filter for batch inference jobs whose names contain
        the string.
        :param max_results: The maximum number of results to return.
        :param next_token: If there were more results than the value you specified in the
        ``maxResults`` field in a previous ``ListModelInvocationJobs`` request,
        the response would have returned a ``nextToken`` value.
        :param sort_by: An attribute by which to sort the results.
        :param sort_order: Specifies whether to sort the results by ascending or descending order.
        :returns: ListModelInvocationJobsResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListProvisionedModelThroughputs")
    def list_provisioned_model_throughputs(
        self,
        context: RequestContext,
        creation_time_after: Timestamp = None,
        creation_time_before: Timestamp = None,
        status_equals: ProvisionedModelStatus = None,
        model_arn_equals: ModelArn = None,
        name_contains: ProvisionedModelName = None,
        max_results: MaxResults = None,
        next_token: PaginationToken = None,
        sort_by: SortByProvisionedModels = None,
        sort_order: SortOrder = None,
        **kwargs,
    ) -> ListProvisionedModelThroughputsResponse:
        """Lists the Provisioned Throughputs in the account. For more information,
        see `Provisioned
        Throughput <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param creation_time_after: A filter that returns Provisioned Throughputs created after the
        specified time.
        :param creation_time_before: A filter that returns Provisioned Throughputs created before the
        specified time.
        :param status_equals: A filter that returns Provisioned Throughputs if their statuses matches
        the value that you specify.
        :param model_arn_equals: A filter that returns Provisioned Throughputs whose model Amazon
        Resource Name (ARN) is equal to the value that you specify.
        :param name_contains: A filter that returns Provisioned Throughputs if their name contains the
        expression that you specify.
        :param max_results: THe maximum number of results to return in the response.
        :param next_token: If there are more results than the number you specified in the
        ``maxResults`` field, the response returns a ``nextToken`` value.
        :param sort_by: The field by which to sort the returned list of Provisioned Throughputs.
        :param sort_order: The sort order of the results.
        :returns: ListProvisionedModelThroughputsResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: TaggableResourcesArn, **kwargs
    ) -> ListTagsForResourceResponse:
        """List the tags associated with the specified resource.

        For more information, see `Tagging
        resources <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :returns: ListTagsForResourceResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("PutModelInvocationLoggingConfiguration")
    def put_model_invocation_logging_configuration(
        self, context: RequestContext, logging_config: LoggingConfig, **kwargs
    ) -> PutModelInvocationLoggingConfigurationResponse:
        """Set the configuration values for model invocation logging.

        :param logging_config: The logging configuration values to set.
        :returns: PutModelInvocationLoggingConfigurationResponse
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("StopEvaluationJob")
    def stop_evaluation_job(
        self, context: RequestContext, job_identifier: EvaluationJobIdentifier, **kwargs
    ) -> StopEvaluationJobResponse:
        """Stops an in progress model evaluation job.

        :param job_identifier: The ARN of the model evaluation job you want to stop.
        :returns: StopEvaluationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("StopModelCustomizationJob")
    def stop_model_customization_job(
        self, context: RequestContext, job_identifier: ModelCustomizationJobIdentifier, **kwargs
    ) -> StopModelCustomizationJobResponse:
        """Stops an active model customization job. For more information, see
        `Custom
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param job_identifier: Job identifier of the job to stop.
        :returns: StopModelCustomizationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("StopModelInvocationJob")
    def stop_model_invocation_job(
        self, context: RequestContext, job_identifier: ModelInvocationJobIdentifier, **kwargs
    ) -> StopModelInvocationJobResponse:
        """Stops a batch inference job. You're only charged for tokens that were
        already processed. For more information, see `Stop a batch inference
        job <https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-manage.html#batch-inference-stop>`__.

        :param job_identifier: The Amazon Resource Name (ARN) of the batch inference job to stop.
        :returns: StopModelInvocationJobResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: TaggableResourcesArn, tags: TagList, **kwargs
    ) -> TagResourceResponse:
        """Associate tags with a resource. For more information, see `Tagging
        resources <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource to tag.
        :param tags: Tags to associate with the resource.
        :returns: TagResourceResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises TooManyTagsException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self,
        context: RequestContext,
        resource_arn: TaggableResourcesArn,
        tag_keys: TagKeyList,
        **kwargs,
    ) -> UntagResourceResponse:
        """Remove one or more tags from a resource. For more information, see
        `Tagging
        resources <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource to untag.
        :param tag_keys: Tag keys of the tags to remove from the resource.
        :returns: UntagResourceResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateGuardrail")
    def update_guardrail(
        self,
        context: RequestContext,
        guardrail_identifier: GuardrailIdentifier,
        name: GuardrailName,
        blocked_input_messaging: GuardrailBlockedMessaging,
        blocked_outputs_messaging: GuardrailBlockedMessaging,
        description: GuardrailDescription = None,
        topic_policy_config: GuardrailTopicPolicyConfig = None,
        content_policy_config: GuardrailContentPolicyConfig = None,
        word_policy_config: GuardrailWordPolicyConfig = None,
        sensitive_information_policy_config: GuardrailSensitiveInformationPolicyConfig = None,
        contextual_grounding_policy_config: GuardrailContextualGroundingPolicyConfig = None,
        kms_key_id: KmsKeyId = None,
        **kwargs,
    ) -> UpdateGuardrailResponse:
        """Updates a guardrail with the values you specify.

        -  Specify a ``name`` and optional ``description``.

        -  Specify messages for when the guardrail successfully blocks a prompt
           or a model response in the ``blockedInputMessaging`` and
           ``blockedOutputsMessaging`` fields.

        -  Specify topics for the guardrail to deny in the ``topicPolicyConfig``
           object. Each
           `GuardrailTopicConfig <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GuardrailTopicConfig.html>`__
           object in the ``topicsConfig`` list pertains to one topic.

           -  Give a ``name`` and ``description`` so that the guardrail can
              properly identify the topic.

           -  Specify ``DENY`` in the ``type`` field.

           -  (Optional) Provide up to five prompts that you would categorize as
              belonging to the topic in the ``examples`` list.

        -  Specify filter strengths for the harmful categories defined in Amazon
           Bedrock in the ``contentPolicyConfig`` object. Each
           `GuardrailContentFilterConfig <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GuardrailContentFilterConfig.html>`__
           object in the ``filtersConfig`` list pertains to a harmful category.
           For more information, see `Content
           filters <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filters>`__.
           For more information about the fields in a content filter, see
           `GuardrailContentFilterConfig <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GuardrailContentFilterConfig.html>`__.

           -  Specify the category in the ``type`` field.

           -  Specify the strength of the filter for prompts in the
              ``inputStrength`` field and for model responses in the
              ``strength`` field of the
              `GuardrailContentFilterConfig <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GuardrailContentFilterConfig.html>`__.

        -  (Optional) For security, include the ARN of a KMS key in the
           ``kmsKeyId`` field.

        :param guardrail_identifier: The unique identifier of the guardrail.
        :param name: A name for the guardrail.
        :param blocked_input_messaging: The message to return when the guardrail blocks a prompt.
        :param blocked_outputs_messaging: The message to return when the guardrail blocks a model response.
        :param description: A description of the guardrail.
        :param topic_policy_config: The topic policy to configure for the guardrail.
        :param content_policy_config: The content policy to configure for the guardrail.
        :param word_policy_config: The word policy to configure for the guardrail.
        :param sensitive_information_policy_config: The sensitive information policy to configure for the guardrail.
        :param contextual_grounding_policy_config: The contextual grounding policy configuration used to update a
        guardrail.
        :param kms_key_id: The ARN of the KMS key with which to encrypt the guardrail.
        :returns: UpdateGuardrailResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateProvisionedModelThroughput")
    def update_provisioned_model_throughput(
        self,
        context: RequestContext,
        provisioned_model_id: ProvisionedModelId,
        desired_provisioned_model_name: ProvisionedModelName = None,
        desired_model_id: ModelIdentifier = None,
        **kwargs,
    ) -> UpdateProvisionedModelThroughputResponse:
        """Updates the name or associated model for a Provisioned Throughput. For
        more information, see `Provisioned
        Throughput <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>`__
        in the `Amazon Bedrock User
        Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-service.html>`__.

        :param provisioned_model_id: The Amazon Resource Name (ARN) or name of the Provisioned Throughput to
        update.
        :param desired_provisioned_model_name: The new name for this Provisioned Throughput.
        :param desired_model_id: The Amazon Resource Name (ARN) of the new model to associate with this
        Provisioned Throughput.
        :returns: UpdateProvisionedModelThroughputResponse
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError
