from enum import StrEnum
from typing import IO, Dict, Iterable, Iterator, List, Optional, TypedDict, Union

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

ConversationalModelId = str
ConverseRequestAdditionalModelResponseFieldPathsListMemberString = str
ConverseStreamRequestAdditionalModelResponseFieldPathsListMemberString = str
DocumentBlockNameString = str
GuardrailContentPolicyUnitsProcessed = int
GuardrailContextualGroundingFilterScoreDouble = float
GuardrailContextualGroundingFilterThresholdDouble = float
GuardrailContextualGroundingPolicyUnitsProcessed = int
GuardrailIdentifier = str
GuardrailOutputText = str
GuardrailSensitiveInformationPolicyFreeUnitsProcessed = int
GuardrailSensitiveInformationPolicyUnitsProcessed = int
GuardrailTopicPolicyUnitsProcessed = int
GuardrailVersion = str
GuardrailWordPolicyUnitsProcessed = int
InferenceConfigurationMaxTokensInteger = int
InferenceConfigurationTemperatureFloat = float
InferenceConfigurationTopPFloat = float
InvokeModelIdentifier = str
MimeType = str
NonBlankString = str
NonEmptyString = str
NonNegativeInteger = int
StatusCode = int
String = str
TextCharactersGuarded = int
TextCharactersTotal = int
TokenUsageInputTokensInteger = int
TokenUsageOutputTokensInteger = int
TokenUsageTotalTokensInteger = int
ToolName = str
ToolUseId = str


class ConversationRole(StrEnum):
    user = "user"
    assistant = "assistant"


class DocumentFormat(StrEnum):
    pdf = "pdf"
    csv = "csv"
    doc = "doc"
    docx = "docx"
    xls = "xls"
    xlsx = "xlsx"
    html = "html"
    txt = "txt"
    md = "md"


class GuardrailAction(StrEnum):
    NONE = "NONE"
    GUARDRAIL_INTERVENED = "GUARDRAIL_INTERVENED"


class GuardrailContentFilterConfidence(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class GuardrailContentFilterStrength(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class GuardrailContentFilterType(StrEnum):
    INSULTS = "INSULTS"
    HATE = "HATE"
    SEXUAL = "SEXUAL"
    VIOLENCE = "VIOLENCE"
    MISCONDUCT = "MISCONDUCT"
    PROMPT_ATTACK = "PROMPT_ATTACK"


class GuardrailContentPolicyAction(StrEnum):
    BLOCKED = "BLOCKED"


class GuardrailContentQualifier(StrEnum):
    grounding_source = "grounding_source"
    query = "query"
    guard_content = "guard_content"


class GuardrailContentSource(StrEnum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


class GuardrailContextualGroundingFilterType(StrEnum):
    GROUNDING = "GROUNDING"
    RELEVANCE = "RELEVANCE"


class GuardrailContextualGroundingPolicyAction(StrEnum):
    BLOCKED = "BLOCKED"
    NONE = "NONE"


class GuardrailConverseContentQualifier(StrEnum):
    grounding_source = "grounding_source"
    query = "query"
    guard_content = "guard_content"


class GuardrailManagedWordType(StrEnum):
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


class GuardrailSensitiveInformationPolicyAction(StrEnum):
    ANONYMIZED = "ANONYMIZED"
    BLOCKED = "BLOCKED"


class GuardrailStreamProcessingMode(StrEnum):
    sync = "sync"
    async_ = "async"


class GuardrailTopicPolicyAction(StrEnum):
    BLOCKED = "BLOCKED"


class GuardrailTopicType(StrEnum):
    DENY = "DENY"


class GuardrailTrace(StrEnum):
    enabled = "enabled"
    disabled = "disabled"


class GuardrailWordPolicyAction(StrEnum):
    BLOCKED = "BLOCKED"


class ImageFormat(StrEnum):
    png = "png"
    jpeg = "jpeg"
    gif = "gif"
    webp = "webp"


class StopReason(StrEnum):
    end_turn = "end_turn"
    tool_use = "tool_use"
    max_tokens = "max_tokens"
    stop_sequence = "stop_sequence"
    guardrail_intervened = "guardrail_intervened"
    content_filtered = "content_filtered"


class ToolResultStatus(StrEnum):
    success = "success"
    error = "error"


class Trace(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class AccessDeniedException(ServiceException):
    """The request is denied because of missing access permissions."""

    code: str = "AccessDeniedException"
    sender_fault: bool = True
    status_code: int = 403


class InternalServerException(ServiceException):
    """An internal server error occurred. Retry your request."""

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 500


class ModelErrorException(ServiceException):
    """The request failed due to an error while processing the model."""

    code: str = "ModelErrorException"
    sender_fault: bool = True
    status_code: int = 424
    originalStatusCode: Optional[StatusCode]
    resourceName: Optional[NonBlankString]


class ModelNotReadyException(ServiceException):
    """The model specified in the request is not ready to serve inference
    requests. The AWS SDK will automatically retry the operation up to 5
    times. For information about configuring automatic retries, see `Retry
    behavior <https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html>`__
    in the *AWS SDKs and Tools* reference guide.
    """

    code: str = "ModelNotReadyException"
    sender_fault: bool = True
    status_code: int = 429


class ModelStreamErrorException(ServiceException):
    """An error occurred while streaming the response. Retry your request."""

    code: str = "ModelStreamErrorException"
    sender_fault: bool = True
    status_code: int = 424
    originalStatusCode: Optional[StatusCode]
    originalMessage: Optional[NonBlankString]


class ModelTimeoutException(ServiceException):
    """The request took too long to process. Processing time exceeded the model
    timeout length.
    """

    code: str = "ModelTimeoutException"
    sender_fault: bool = True
    status_code: int = 408


class ResourceNotFoundException(ServiceException):
    """The specified resource ARN was not found. Check the ARN and try your
    request again.
    """

    code: str = "ResourceNotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class ServiceQuotaExceededException(ServiceException):
    """Your request exceeds the service quota for your account. You can view
    your quotas at `Viewing service
    quotas <https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html>`__.
    You can resubmit your request later.
    """

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = True
    status_code: int = 400


class ServiceUnavailableException(ServiceException):
    """The service isn't currently available. Try again later."""

    code: str = "ServiceUnavailableException"
    sender_fault: bool = False
    status_code: int = 503


class ThrottlingException(ServiceException):
    """Your request was throttled because of service-wide limitations. Resubmit
    your request later or in a different region. You can also purchase
    `Provisioned
    Throughput <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>`__
    to increase the rate or number of tokens you can process.
    """

    code: str = "ThrottlingException"
    sender_fault: bool = True
    status_code: int = 429


class ValidationException(ServiceException):
    """Input validation failed. Check your request parameters and retry the
    request.
    """

    code: str = "ValidationException"
    sender_fault: bool = True
    status_code: int = 400


class AnyToolChoice(TypedDict, total=False):
    """The model must request at least one tool (no text is generated). For
    example, ``{"any" : {}}``.
    """

    pass


GuardrailContentQualifierList = List[GuardrailContentQualifier]


class GuardrailTextBlock(TypedDict, total=False):
    """The text block to be evaluated by the guardrail."""

    text: String
    qualifiers: Optional[GuardrailContentQualifierList]


class GuardrailContentBlock(TypedDict, total=False):
    """The content block to be evaluated by the guardrail."""

    text: Optional[GuardrailTextBlock]


GuardrailContentBlockList = List[GuardrailContentBlock]


class ApplyGuardrailRequest(ServiceRequest):
    guardrailIdentifier: GuardrailIdentifier
    guardrailVersion: GuardrailVersion
    source: GuardrailContentSource
    content: GuardrailContentBlockList


class GuardrailTextCharactersCoverage(TypedDict, total=False):
    """The guardrail coverage for the text characters."""

    guarded: Optional[TextCharactersGuarded]
    total: Optional[TextCharactersTotal]


class GuardrailCoverage(TypedDict, total=False):
    """The action of the guardrail coverage details."""

    textCharacters: Optional[GuardrailTextCharactersCoverage]


class GuardrailUsage(TypedDict, total=False):
    """The details on the use of the guardrail."""

    topicPolicyUnits: GuardrailTopicPolicyUnitsProcessed
    contentPolicyUnits: GuardrailContentPolicyUnitsProcessed
    wordPolicyUnits: GuardrailWordPolicyUnitsProcessed
    sensitiveInformationPolicyUnits: GuardrailSensitiveInformationPolicyUnitsProcessed
    sensitiveInformationPolicyFreeUnits: GuardrailSensitiveInformationPolicyFreeUnitsProcessed
    contextualGroundingPolicyUnits: GuardrailContextualGroundingPolicyUnitsProcessed


GuardrailProcessingLatency = int


class GuardrailInvocationMetrics(TypedDict, total=False):
    """The invocation metrics for the guardrail."""

    guardrailProcessingLatency: Optional[GuardrailProcessingLatency]
    usage: Optional[GuardrailUsage]
    guardrailCoverage: Optional[GuardrailCoverage]


GuardrailContextualGroundingFilter = TypedDict(
    "GuardrailContextualGroundingFilter",
    {
        "type": GuardrailContextualGroundingFilterType,
        "threshold": GuardrailContextualGroundingFilterThresholdDouble,
        "score": GuardrailContextualGroundingFilterScoreDouble,
        "action": GuardrailContextualGroundingPolicyAction,
    },
    total=False,
)
GuardrailContextualGroundingFilters = List[GuardrailContextualGroundingFilter]


class GuardrailContextualGroundingPolicyAssessment(TypedDict, total=False):
    """The policy assessment details for the guardrails contextual grounding
    filter.
    """

    filters: Optional[GuardrailContextualGroundingFilters]


class GuardrailRegexFilter(TypedDict, total=False):
    """A Regex filter configured in a guardrail."""

    name: Optional[String]
    match: Optional[String]
    regex: Optional[String]
    action: GuardrailSensitiveInformationPolicyAction


GuardrailRegexFilterList = List[GuardrailRegexFilter]
GuardrailPiiEntityFilter = TypedDict(
    "GuardrailPiiEntityFilter",
    {
        "match": String,
        "type": GuardrailPiiEntityType,
        "action": GuardrailSensitiveInformationPolicyAction,
    },
    total=False,
)
GuardrailPiiEntityFilterList = List[GuardrailPiiEntityFilter]


class GuardrailSensitiveInformationPolicyAssessment(TypedDict, total=False):
    """The assessment for aPersonally Identifiable Information (PII) policy."""

    piiEntities: GuardrailPiiEntityFilterList
    regexes: GuardrailRegexFilterList


GuardrailManagedWord = TypedDict(
    "GuardrailManagedWord",
    {
        "match": String,
        "type": GuardrailManagedWordType,
        "action": GuardrailWordPolicyAction,
    },
    total=False,
)
GuardrailManagedWordList = List[GuardrailManagedWord]


class GuardrailCustomWord(TypedDict, total=False):
    """A custom word configured in a guardrail."""

    match: String
    action: GuardrailWordPolicyAction


GuardrailCustomWordList = List[GuardrailCustomWord]


class GuardrailWordPolicyAssessment(TypedDict, total=False):
    """The word policy assessment."""

    customWords: GuardrailCustomWordList
    managedWordLists: GuardrailManagedWordList


GuardrailContentFilter = TypedDict(
    "GuardrailContentFilter",
    {
        "type": GuardrailContentFilterType,
        "confidence": GuardrailContentFilterConfidence,
        "filterStrength": Optional[GuardrailContentFilterStrength],
        "action": GuardrailContentPolicyAction,
    },
    total=False,
)
GuardrailContentFilterList = List[GuardrailContentFilter]


class GuardrailContentPolicyAssessment(TypedDict, total=False):
    """An assessment of a content policy for a guardrail."""

    filters: GuardrailContentFilterList


GuardrailTopic = TypedDict(
    "GuardrailTopic",
    {
        "name": String,
        "type": GuardrailTopicType,
        "action": GuardrailTopicPolicyAction,
    },
    total=False,
)
GuardrailTopicList = List[GuardrailTopic]


class GuardrailTopicPolicyAssessment(TypedDict, total=False):
    """A behavior assessment of a topic policy."""

    topics: GuardrailTopicList


class GuardrailAssessment(TypedDict, total=False):
    """A behavior assessment of the guardrail policies used in a call to the
    Converse API.
    """

    topicPolicy: Optional[GuardrailTopicPolicyAssessment]
    contentPolicy: Optional[GuardrailContentPolicyAssessment]
    wordPolicy: Optional[GuardrailWordPolicyAssessment]
    sensitiveInformationPolicy: Optional[GuardrailSensitiveInformationPolicyAssessment]
    contextualGroundingPolicy: Optional[GuardrailContextualGroundingPolicyAssessment]
    invocationMetrics: Optional[GuardrailInvocationMetrics]


GuardrailAssessmentList = List[GuardrailAssessment]


class GuardrailOutputContent(TypedDict, total=False):
    """The output content produced by the guardrail."""

    text: Optional[GuardrailOutputText]


GuardrailOutputContentList = List[GuardrailOutputContent]


class ApplyGuardrailResponse(TypedDict, total=False):
    usage: GuardrailUsage
    action: GuardrailAction
    outputs: GuardrailOutputContentList
    assessments: GuardrailAssessmentList
    guardrailCoverage: Optional[GuardrailCoverage]


class AutoToolChoice(TypedDict, total=False):
    """The Model automatically decides if a tool should be called or whether to
    generate text instead. For example, ``{"auto" : {}}``.
    """

    pass


Body = bytes
GuardrailConverseContentQualifierList = List[GuardrailConverseContentQualifier]


class GuardrailConverseTextBlock(TypedDict, total=False):
    """A text block that contains text that you want to assess with a
    guardrail. For more information, see GuardrailConverseContentBlock.
    """

    text: String
    qualifiers: Optional[GuardrailConverseContentQualifierList]


class GuardrailConverseContentBlock(TypedDict, total=False):
    """A content block for selective guarding with the
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    or
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__
    API operations.
    """

    text: Optional[GuardrailConverseTextBlock]


DocumentSourceBytesBlob = bytes


class DocumentSource(TypedDict, total=False):
    """Contains the content of a document."""

    bytes: Optional[DocumentSourceBytesBlob]


class DocumentBlock(TypedDict, total=False):
    """A document to include in a message."""

    format: DocumentFormat
    name: DocumentBlockNameString
    source: DocumentSource


ImageSourceBytesBlob = bytes


class ImageSource(TypedDict, total=False):
    """The source for an image."""

    bytes: Optional[ImageSourceBytesBlob]


class ImageBlock(TypedDict, total=False):
    """Image content for a message."""

    format: ImageFormat
    source: ImageSource


class Document(TypedDict, total=False):
    pass


class ToolResultContentBlock(TypedDict, total=False):
    """The tool result content block."""

    json: Optional[Document]
    text: Optional[String]
    image: Optional[ImageBlock]
    document: Optional[DocumentBlock]


ToolResultContentBlocks = List[ToolResultContentBlock]


class ToolResultBlock(TypedDict, total=False):
    """A tool result block that contains the results for a tool request that
    the model previously made.
    """

    toolUseId: ToolUseId
    content: ToolResultContentBlocks
    status: Optional[ToolResultStatus]


class ToolUseBlock(TypedDict, total=False):
    """A tool use content block. Contains information about a tool that the
    model is requesting be run., The model uses the result from the tool to
    generate a response.
    """

    toolUseId: ToolUseId
    name: ToolName
    input: Document


class ContentBlock(TypedDict, total=False):
    """A block of content for a message that you pass to, or receive from, a
    model with the
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    or
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__
    API operations.
    """

    text: Optional[String]
    image: Optional[ImageBlock]
    document: Optional[DocumentBlock]
    toolUse: Optional[ToolUseBlock]
    toolResult: Optional[ToolResultBlock]
    guardContent: Optional[GuardrailConverseContentBlock]


class ToolUseBlockDelta(TypedDict, total=False):
    """The delta for a tool use block."""

    input: String


class ContentBlockDelta(TypedDict, total=False):
    """A bock of content in a streaming response."""

    text: Optional[String]
    toolUse: Optional[ToolUseBlockDelta]


class ContentBlockDeltaEvent(TypedDict, total=False):
    """The content block delta event."""

    delta: ContentBlockDelta
    contentBlockIndex: NonNegativeInteger


class ToolUseBlockStart(TypedDict, total=False):
    """The start of a tool use block."""

    toolUseId: ToolUseId
    name: ToolName


class ContentBlockStart(TypedDict, total=False):
    """Content block start information."""

    toolUse: Optional[ToolUseBlockStart]


class ContentBlockStartEvent(TypedDict, total=False):
    """Content block start event."""

    start: ContentBlockStart
    contentBlockIndex: NonNegativeInteger


class ContentBlockStopEvent(TypedDict, total=False):
    """A content block stop event."""

    contentBlockIndex: NonNegativeInteger


ContentBlocks = List[ContentBlock]
Long = int


class ConverseMetrics(TypedDict, total=False):
    """Metrics for a call to
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__.
    """

    latencyMs: Long


class Message(TypedDict, total=False):
    """A message input, or returned from, a call to
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    or
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__.
    """

    role: ConversationRole
    content: ContentBlocks


class ConverseOutput(TypedDict, total=False):
    """The output from a call to
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__.
    """

    message: Optional[Message]


ConverseRequestAdditionalModelResponseFieldPathsList = List[
    ConverseRequestAdditionalModelResponseFieldPathsListMemberString
]


class PromptVariableValues(TypedDict, total=False):
    """Contains a map of variables in a prompt from Prompt management to an
    object containing the values to fill in for them when running model
    invocation. For more information, see `How Prompt management
    works <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-how.html>`__.
    """

    text: Optional[String]


PromptVariableMap = Dict[String, PromptVariableValues]


class GuardrailConfiguration(TypedDict, total=False):
    """Configuration information for a guardrail that you use with the
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    operation.
    """

    guardrailIdentifier: GuardrailIdentifier
    guardrailVersion: GuardrailVersion
    trace: Optional[GuardrailTrace]


class SpecificToolChoice(TypedDict, total=False):
    """The model must request a specific tool. For example,
    ``{"tool" : {"name" : "Your tool name"}}``.

    This field is only supported by Anthropic Claude 3 models.
    """

    name: ToolName


class ToolChoice(TypedDict, total=False):
    """Determines which tools the model should request in a call to
    ``Converse`` or ``ConverseStream``. ``ToolChoice`` is only supported by
    Anthropic Claude 3 models and by Mistral AI Mistral Large.
    """

    auto: Optional[AutoToolChoice]
    any: Optional[AnyToolChoice]
    tool: Optional[SpecificToolChoice]


class ToolInputSchema(TypedDict, total=False):
    """The schema for the tool. The top level schema type must be ``object``."""

    json: Optional[Document]


class ToolSpecification(TypedDict, total=False):
    """The specification for the tool."""

    name: ToolName
    description: Optional[NonEmptyString]
    inputSchema: ToolInputSchema


class Tool(TypedDict, total=False):
    """Information about a tool that you can use with the Converse API. For
    more information, see `Tool use (function
    calling) <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.
    """

    toolSpec: Optional[ToolSpecification]


ToolConfigurationToolsList = List[Tool]


class ToolConfiguration(TypedDict, total=False):
    """Configuration information for the tools that you pass to a model. For
    more information, see `Tool use (function
    calling) <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.

    This field is only supported by Anthropic Claude 3, Cohere Command R,
    Cohere Command R+, and Mistral Large models.
    """

    tools: ToolConfigurationToolsList
    toolChoice: Optional[ToolChoice]


InferenceConfigurationStopSequencesList = List[NonEmptyString]


class InferenceConfiguration(TypedDict, total=False):
    """Base inference parameters to pass to a model in a call to
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    or
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__.
    For more information, see `Inference parameters for foundation
    models <https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html>`__.

    If you need to pass additional parameters that the model supports, use
    the ``additionalModelRequestFields`` request field in the call to
    ``Converse`` or ``ConverseStream``. For more information, see `Model
    parameters <https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html>`__.
    """

    maxTokens: Optional[InferenceConfigurationMaxTokensInteger]
    temperature: Optional[InferenceConfigurationTemperatureFloat]
    topP: Optional[InferenceConfigurationTopPFloat]
    stopSequences: Optional[InferenceConfigurationStopSequencesList]


class SystemContentBlock(TypedDict, total=False):
    """A system content block."""

    text: Optional[NonEmptyString]
    guardContent: Optional[GuardrailConverseContentBlock]


SystemContentBlocks = List[SystemContentBlock]
Messages = List[Message]


class ConverseRequest(ServiceRequest):
    modelId: ConversationalModelId
    messages: Optional[Messages]
    system: Optional[SystemContentBlocks]
    inferenceConfig: Optional[InferenceConfiguration]
    toolConfig: Optional[ToolConfiguration]
    guardrailConfig: Optional[GuardrailConfiguration]
    additionalModelRequestFields: Optional[Document]
    promptVariables: Optional[PromptVariableMap]
    additionalModelResponseFieldPaths: Optional[
        ConverseRequestAdditionalModelResponseFieldPathsList
    ]


GuardrailAssessmentListMap = Dict[String, GuardrailAssessmentList]
GuardrailAssessmentMap = Dict[String, GuardrailAssessment]
ModelOutputs = List[GuardrailOutputText]


class GuardrailTraceAssessment(TypedDict, total=False):
    """A Top level guardrail trace object. For more information, see
    ConverseTrace.
    """

    modelOutput: Optional[ModelOutputs]
    inputAssessment: Optional[GuardrailAssessmentMap]
    outputAssessments: Optional[GuardrailAssessmentListMap]


class ConverseTrace(TypedDict, total=False):
    """The trace object in a response from
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__.
    Currently, you can only trace guardrails.
    """

    guardrail: Optional[GuardrailTraceAssessment]


class TokenUsage(TypedDict, total=False):
    """The tokens used in a message API inference call."""

    inputTokens: TokenUsageInputTokensInteger
    outputTokens: TokenUsageOutputTokensInteger
    totalTokens: TokenUsageTotalTokensInteger


class ConverseResponse(TypedDict, total=False):
    output: ConverseOutput
    stopReason: StopReason
    usage: TokenUsage
    metrics: ConverseMetrics
    additionalModelResponseFields: Optional[Document]
    trace: Optional[ConverseTrace]


class ConverseStreamTrace(TypedDict, total=False):
    """The trace object in a response from
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__.
    Currently, you can only trace guardrails.
    """

    guardrail: Optional[GuardrailTraceAssessment]


class ConverseStreamMetrics(TypedDict, total=False):
    """Metrics for the stream."""

    latencyMs: Long


class ConverseStreamMetadataEvent(TypedDict, total=False):
    """A conversation stream metadata event."""

    usage: TokenUsage
    metrics: ConverseStreamMetrics
    trace: Optional[ConverseStreamTrace]


class MessageStopEvent(TypedDict, total=False):
    """The stop event for a message."""

    stopReason: StopReason
    additionalModelResponseFields: Optional[Document]


class MessageStartEvent(TypedDict, total=False):
    """The start of a message."""

    role: ConversationRole


class ConverseStreamOutput(TypedDict, total=False):
    """The messages output stream"""

    messageStart: Optional[MessageStartEvent]
    contentBlockStart: Optional[ContentBlockStartEvent]
    contentBlockDelta: Optional[ContentBlockDeltaEvent]
    contentBlockStop: Optional[ContentBlockStopEvent]
    messageStop: Optional[MessageStopEvent]
    metadata: Optional[ConverseStreamMetadataEvent]
    internalServerException: Optional[InternalServerException]
    modelStreamErrorException: Optional[ModelStreamErrorException]
    validationException: Optional[ValidationException]
    throttlingException: Optional[ThrottlingException]
    serviceUnavailableException: Optional[ServiceUnavailableException]


ConverseStreamRequestAdditionalModelResponseFieldPathsList = List[
    ConverseStreamRequestAdditionalModelResponseFieldPathsListMemberString
]


class GuardrailStreamConfiguration(TypedDict, total=False):
    """Configuration information for a guardrail that you use with the
    ConverseStream action.
    """

    guardrailIdentifier: GuardrailIdentifier
    guardrailVersion: GuardrailVersion
    trace: Optional[GuardrailTrace]
    streamProcessingMode: Optional[GuardrailStreamProcessingMode]


class ConverseStreamRequest(ServiceRequest):
    modelId: ConversationalModelId
    messages: Optional[Messages]
    system: Optional[SystemContentBlocks]
    inferenceConfig: Optional[InferenceConfiguration]
    toolConfig: Optional[ToolConfiguration]
    guardrailConfig: Optional[GuardrailStreamConfiguration]
    additionalModelRequestFields: Optional[Document]
    promptVariables: Optional[PromptVariableMap]
    additionalModelResponseFieldPaths: Optional[
        ConverseStreamRequestAdditionalModelResponseFieldPathsList
    ]


class ConverseStreamResponse(TypedDict, total=False):
    stream: Iterator[ConverseStreamOutput]


class InvokeModelRequest(ServiceRequest):
    body: Optional[IO[Body]]
    contentType: Optional[MimeType]
    accept: Optional[MimeType]
    modelId: InvokeModelIdentifier
    trace: Optional[Trace]
    guardrailIdentifier: Optional[GuardrailIdentifier]
    guardrailVersion: Optional[GuardrailVersion]


class InvokeModelResponse(TypedDict, total=False):
    body: Union[Body, IO[Body], Iterable[Body]]
    contentType: MimeType


class InvokeModelWithResponseStreamRequest(ServiceRequest):
    body: Optional[IO[Body]]
    contentType: Optional[MimeType]
    accept: Optional[MimeType]
    modelId: InvokeModelIdentifier
    trace: Optional[Trace]
    guardrailIdentifier: Optional[GuardrailIdentifier]
    guardrailVersion: Optional[GuardrailVersion]


PartBody = bytes


class PayloadPart(TypedDict, total=False):
    """Payload content included in the response."""

    bytes: Optional[PartBody]


class ResponseStream(TypedDict, total=False):
    """Definition of content in the response stream."""

    chunk: Optional[PayloadPart]
    internalServerException: Optional[InternalServerException]
    modelStreamErrorException: Optional[ModelStreamErrorException]
    validationException: Optional[ValidationException]
    throttlingException: Optional[ThrottlingException]
    modelTimeoutException: Optional[ModelTimeoutException]
    serviceUnavailableException: Optional[ServiceUnavailableException]


class InvokeModelWithResponseStreamResponse(TypedDict, total=False):
    body: Iterator[ResponseStream]
    contentType: MimeType


class BedrockRuntimeApi:
    service = "bedrock-runtime"
    version = "2023-09-30"

    @handler("ApplyGuardrail")
    def apply_guardrail(
        self,
        context: RequestContext,
        guardrail_identifier: GuardrailIdentifier,
        guardrail_version: GuardrailVersion,
        source: GuardrailContentSource,
        content: GuardrailContentBlockList,
        **kwargs,
    ) -> ApplyGuardrailResponse:
        """The action to apply a guardrail.

        :param guardrail_identifier: The guardrail identifier used in the request to apply the guardrail.
        :param guardrail_version: The guardrail version used in the request to apply the guardrail.
        :param source: The source of data used in the request to apply the guardrail.
        :param content: The content details used in the request to apply the guardrail.
        :returns: ApplyGuardrailResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("Converse")
    def converse(
        self,
        context: RequestContext,
        model_id: ConversationalModelId,
        messages: Messages = None,
        system: SystemContentBlocks = None,
        inference_config: InferenceConfiguration = None,
        tool_config: ToolConfiguration = None,
        guardrail_config: GuardrailConfiguration = None,
        additional_model_request_fields: Document = None,
        prompt_variables: PromptVariableMap = None,
        additional_model_response_field_paths: ConverseRequestAdditionalModelResponseFieldPathsList = None,
        **kwargs,
    ) -> ConverseResponse:
        """Sends messages to the specified Amazon Bedrock model. ``Converse``
        provides a consistent interface that works with all models that support
        messages. This allows you to write code once and use it with different
        models. If a model has unique inference parameters, you can also pass
        those unique parameters to the model.

        Amazon Bedrock doesn't store any text, images, or documents that you
        provide as content. The data is only used to generate the response.

        You can submit a prompt by including it in the ``messages`` field,
        specifying the ``modelId`` of a foundation model or inference profile to
        run inference on it, and including any other fields that are relevant to
        your use case.

        You can also submit a prompt from Prompt management by specifying the
        ARN of the prompt version and including a map of variables to values in
        the ``promptVariables`` field. You can append more messages to the
        prompt by using the ``messages`` field. If you use a prompt from Prompt
        management, you can't include the following fields in the request:
        ``additionalModelRequestFields``, ``inferenceConfig``, ``system``, or
        ``toolConfig``. Instead, these fields must be defined through Prompt
        management. For more information, see `Use a prompt from Prompt
        management <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-use.html>`__.

        For information about the Converse API, see *Use the Converse API* in
        the *Amazon Bedrock User Guide*. To use a guardrail, see *Use a
        guardrail with the Converse API* in the *Amazon Bedrock User Guide*. To
        use a tool with a model, see *Tool use (Function calling)* in the
        *Amazon Bedrock User Guide*

        For example code, see *Converse API examples* in the *Amazon Bedrock
        User Guide*.

        This operation requires permission for the ``bedrock:InvokeModel``
        action.

        :param model_id: Specifies the model or throughput with which to run inference, or the
        prompt resource to use in inference.
        :param messages: The messages that you want to send to the model.
        :param system: A prompt that provides instructions or context to the model about the
        task it should perform, or the persona it should adopt during the
        conversation.
        :param inference_config: Inference parameters to pass to the model.
        :param tool_config: Configuration information for the tools that the model can use when
        generating a response.
        :param guardrail_config: Configuration information for a guardrail that you want to use in the
        request.
        :param additional_model_request_fields: Additional inference parameters that the model supports, beyond the base
        set of inference parameters that ``Converse`` and ``ConverseStream``
        support in the ``inferenceConfig`` field.
        :param prompt_variables: Contains a map of variables in a prompt from Prompt management to
        objects containing the values to fill in for them when running model
        invocation.
        :param additional_model_response_field_paths: Additional model parameters field paths to return in the response.
        :returns: ConverseResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        :raises ModelNotReadyException:
        :raises ModelErrorException:
        """
        raise NotImplementedError

    @handler("ConverseStream")
    def converse_stream(
        self,
        context: RequestContext,
        model_id: ConversationalModelId,
        messages: Messages = None,
        system: SystemContentBlocks = None,
        inference_config: InferenceConfiguration = None,
        tool_config: ToolConfiguration = None,
        guardrail_config: GuardrailStreamConfiguration = None,
        additional_model_request_fields: Document = None,
        prompt_variables: PromptVariableMap = None,
        additional_model_response_field_paths: ConverseStreamRequestAdditionalModelResponseFieldPathsList = None,
        **kwargs,
    ) -> ConverseStreamResponse:
        """Sends messages to the specified Amazon Bedrock model and returns the
        response in a stream. ``ConverseStream`` provides a consistent API that
        works with all Amazon Bedrock models that support messages. This allows
        you to write code once and use it with different models. Should a model
        have unique inference parameters, you can also pass those unique
        parameters to the model.

        To find out if a model supports streaming, call
        `GetFoundationModel <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetFoundationModel.html>`__
        and check the ``responseStreamingSupported`` field in the response.

        The CLI doesn't support streaming operations in Amazon Bedrock,
        including ``ConverseStream``.

        Amazon Bedrock doesn't store any text, images, or documents that you
        provide as content. The data is only used to generate the response.

        You can submit a prompt by including it in the ``messages`` field,
        specifying the ``modelId`` of a foundation model or inference profile to
        run inference on it, and including any other fields that are relevant to
        your use case.

        You can also submit a prompt from Prompt management by specifying the
        ARN of the prompt version and including a map of variables to values in
        the ``promptVariables`` field. You can append more messages to the
        prompt by using the ``messages`` field. If you use a prompt from Prompt
        management, you can't include the following fields in the request:
        ``additionalModelRequestFields``, ``inferenceConfig``, ``system``, or
        ``toolConfig``. Instead, these fields must be defined through Prompt
        management. For more information, see `Use a prompt from Prompt
        management <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-use.html>`__.

        For information about the Converse API, see *Use the Converse API* in
        the *Amazon Bedrock User Guide*. To use a guardrail, see *Use a
        guardrail with the Converse API* in the *Amazon Bedrock User Guide*. To
        use a tool with a model, see *Tool use (Function calling)* in the
        *Amazon Bedrock User Guide*

        For example code, see *Conversation streaming example* in the *Amazon
        Bedrock User Guide*.

        This operation requires permission for the
        ``bedrock:InvokeModelWithResponseStream`` action.

        :param model_id: Specifies the model or throughput with which to run inference, or the
        prompt resource to use in inference.
        :param messages: The messages that you want to send to the model.
        :param system: A prompt that provides instructions or context to the model about the
        task it should perform, or the persona it should adopt during the
        conversation.
        :param inference_config: Inference parameters to pass to the model.
        :param tool_config: Configuration information for the tools that the model can use when
        generating a response.
        :param guardrail_config: Configuration information for a guardrail that you want to use in the
        request.
        :param additional_model_request_fields: Additional inference parameters that the model supports, beyond the base
        set of inference parameters that ``Converse`` and ``ConverseStream``
        support in the ``inferenceConfig`` field.
        :param prompt_variables: Contains a map of variables in a prompt from Prompt management to
        objects containing the values to fill in for them when running model
        invocation.
        :param additional_model_response_field_paths: Additional model parameters field paths to return in the response.
        :returns: ConverseStreamResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        :raises ModelNotReadyException:
        :raises ModelErrorException:
        """
        raise NotImplementedError

    @handler("InvokeModel")
    def invoke_model(
        self,
        context: RequestContext,
        model_id: InvokeModelIdentifier,
        body: IO[Body] = None,
        content_type: MimeType = None,
        accept: MimeType = None,
        trace: Trace = None,
        guardrail_identifier: GuardrailIdentifier = None,
        guardrail_version: GuardrailVersion = None,
        **kwargs,
    ) -> InvokeModelResponse:
        """Invokes the specified Amazon Bedrock model to run inference using the
        prompt and inference parameters provided in the request body. You use
        model inference to generate text, images, and embeddings.

        For example code, see *Invoke model code examples* in the *Amazon
        Bedrock User Guide*.

        This operation requires permission for the ``bedrock:InvokeModel``
        action.

        :param model_id: The unique identifier of the model to invoke to run inference.
        :param body: The prompt and inference parameters in the format specified in the
        ``contentType`` in the header.
        :param content_type: The MIME type of the input data in the request.
        :param accept: The desired MIME type of the inference body in the response.
        :param trace: Specifies whether to enable or disable the Bedrock trace.
        :param guardrail_identifier: The unique identifier of the guardrail that you want to use.
        :param guardrail_version: The version number for the guardrail.
        :returns: InvokeModelResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        :raises ModelNotReadyException:
        :raises ServiceQuotaExceededException:
        :raises ModelErrorException:
        """
        raise NotImplementedError

    @handler("InvokeModelWithResponseStream")
    def invoke_model_with_response_stream(
        self,
        context: RequestContext,
        model_id: InvokeModelIdentifier,
        body: IO[Body] = None,
        content_type: MimeType = None,
        accept: MimeType = None,
        trace: Trace = None,
        guardrail_identifier: GuardrailIdentifier = None,
        guardrail_version: GuardrailVersion = None,
        **kwargs,
    ) -> InvokeModelWithResponseStreamResponse:
        """Invoke the specified Amazon Bedrock model to run inference using the
        prompt and inference parameters provided in the request body. The
        response is returned in a stream.

        To see if a model supports streaming, call
        `GetFoundationModel <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetFoundationModel.html>`__
        and check the ``responseStreamingSupported`` field in the response.

        The CLI doesn't support streaming operations in Amazon Bedrock,
        including ``InvokeModelWithResponseStream``.

        For example code, see *Invoke model with streaming code example* in the
        *Amazon Bedrock User Guide*.

        This operation requires permissions to perform the
        ``bedrock:InvokeModelWithResponseStream`` action.

        :param model_id: The unique identifier of the model to invoke to run inference.
        :param body: The prompt and inference parameters in the format specified in the
        ``contentType`` in the header.
        :param content_type: The MIME type of the input data in the request.
        :param accept: The desired MIME type of the inference body in the response.
        :param trace: Specifies whether to enable or disable the Bedrock trace.
        :param guardrail_identifier: The unique identifier of the guardrail that you want to use.
        :param guardrail_version: The version number for the guardrail.
        :returns: InvokeModelWithResponseStreamResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ModelStreamErrorException:
        :raises ValidationException:
        :raises ModelNotReadyException:
        :raises ServiceQuotaExceededException:
        :raises ModelErrorException:
        """
        raise NotImplementedError
