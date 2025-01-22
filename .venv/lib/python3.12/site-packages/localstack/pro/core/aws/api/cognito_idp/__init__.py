from datetime import datetime
from enum import StrEnum
from typing import Dict, List, Optional, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AWSAccountIdType = str
AccessTokenValidityType = int
AccountTakeoverActionNotifyType = bool
AdminCreateUserUnusedAccountValidityDaysType = int
ArnType = str
AttributeMappingKeyType = str
AttributeNameType = str
AttributeValueType = str
AuthSessionValidityType = int
BooleanType = bool
CSSType = str
CSSVersionType = str
ClientIdType = str
ClientNameType = str
ClientPermissionType = str
ClientSecretType = str
CompletionMessageType = str
ConfirmationCodeType = str
CustomAttributeNameType = str
DescriptionType = str
DeviceKeyType = str
DeviceNameType = str
DomainType = str
DomainVersionType = str
EmailAddressType = str
EmailInviteMessageType = str
EmailMfaMessageType = str
EmailMfaSubjectType = str
EmailNotificationBodyType = str
EmailNotificationSubjectType = str
EmailVerificationMessageByLinkType = str
EmailVerificationMessageType = str
EmailVerificationSubjectByLinkType = str
EmailVerificationSubjectType = str
EventIdType = str
ForceAliasCreation = bool
GenerateSecret = bool
GroupNameType = str
HexStringType = str
IdTokenValidityType = int
IdpIdentifierType = str
ImageUrlType = str
IntegerType = int
InvalidParameterExceptionReasonCodeType = str
ListProvidersLimitType = int
ListResourceServersLimitType = int
ManagedLoginBrandingIdType = str
MessageType = str
PaginationKey = str
PaginationKeyType = str
PasswordHistorySizeType = int
PasswordPolicyMinLengthType = int
PasswordType = str
PoolQueryLimitType = int
PreSignedUrlType = str
PrecedenceType = int
PriorityType = int
ProviderNameType = str
ProviderNameTypeV2 = str
QueryLimit = int
QueryLimitType = int
RedirectUrlType = str
RefreshTokenValidityType = int
RegionCodeType = str
RelyingPartyIdType = str
ResourceIdType = str
ResourceServerIdentifierType = str
ResourceServerNameType = str
ResourceServerScopeDescriptionType = str
ResourceServerScopeNameType = str
S3ArnType = str
S3BucketType = str
SESConfigurationSet = str
ScopeType = str
SearchPaginationTokenType = str
SecretCodeType = str
SecretHashType = str
SessionType = str
SmsInviteMessageType = str
SmsVerificationMessageType = str
SoftwareTokenMFAUserCodeType = str
StringType = str
TagKeysType = str
TagValueType = str
TemporaryPasswordValidityDaysType = int
TokenModelType = str
UserFilterType = str
UserImportJobIdType = str
UserImportJobNameType = str
UserPoolIdType = str
UserPoolNameType = str
UsernameType = str
WebAuthnAuthenticatorAttachmentType = str
WebAuthnAuthenticatorTransportType = str
WebAuthnCredentialsQueryLimitType = int
WrappedBooleanType = bool
WrappedIntegerType = int


class AccountTakeoverEventActionType(StrEnum):
    BLOCK = "BLOCK"
    MFA_IF_CONFIGURED = "MFA_IF_CONFIGURED"
    MFA_REQUIRED = "MFA_REQUIRED"
    NO_ACTION = "NO_ACTION"


class AdvancedSecurityEnabledModeType(StrEnum):
    AUDIT = "AUDIT"
    ENFORCED = "ENFORCED"


class AdvancedSecurityModeType(StrEnum):
    OFF = "OFF"
    AUDIT = "AUDIT"
    ENFORCED = "ENFORCED"


class AliasAttributeType(StrEnum):
    phone_number = "phone_number"
    email = "email"
    preferred_username = "preferred_username"


class AssetCategoryType(StrEnum):
    FAVICON_ICO = "FAVICON_ICO"
    FAVICON_SVG = "FAVICON_SVG"
    EMAIL_GRAPHIC = "EMAIL_GRAPHIC"
    SMS_GRAPHIC = "SMS_GRAPHIC"
    AUTH_APP_GRAPHIC = "AUTH_APP_GRAPHIC"
    PASSWORD_GRAPHIC = "PASSWORD_GRAPHIC"
    PASSKEY_GRAPHIC = "PASSKEY_GRAPHIC"
    PAGE_HEADER_LOGO = "PAGE_HEADER_LOGO"
    PAGE_HEADER_BACKGROUND = "PAGE_HEADER_BACKGROUND"
    PAGE_FOOTER_LOGO = "PAGE_FOOTER_LOGO"
    PAGE_FOOTER_BACKGROUND = "PAGE_FOOTER_BACKGROUND"
    PAGE_BACKGROUND = "PAGE_BACKGROUND"
    FORM_BACKGROUND = "FORM_BACKGROUND"
    FORM_LOGO = "FORM_LOGO"
    IDP_BUTTON_ICON = "IDP_BUTTON_ICON"


class AssetExtensionType(StrEnum):
    ICO = "ICO"
    JPEG = "JPEG"
    PNG = "PNG"
    SVG = "SVG"
    WEBP = "WEBP"


class AttributeDataType(StrEnum):
    String = "String"
    Number = "Number"
    DateTime = "DateTime"
    Boolean = "Boolean"


class AuthFactorType(StrEnum):
    PASSWORD = "PASSWORD"
    EMAIL_OTP = "EMAIL_OTP"
    SMS_OTP = "SMS_OTP"
    WEB_AUTHN = "WEB_AUTHN"


class AuthFlowType(StrEnum):
    USER_SRP_AUTH = "USER_SRP_AUTH"
    REFRESH_TOKEN_AUTH = "REFRESH_TOKEN_AUTH"
    REFRESH_TOKEN = "REFRESH_TOKEN"
    CUSTOM_AUTH = "CUSTOM_AUTH"
    ADMIN_NO_SRP_AUTH = "ADMIN_NO_SRP_AUTH"
    USER_PASSWORD_AUTH = "USER_PASSWORD_AUTH"
    ADMIN_USER_PASSWORD_AUTH = "ADMIN_USER_PASSWORD_AUTH"
    USER_AUTH = "USER_AUTH"


class ChallengeName(StrEnum):
    Password = "Password"
    Mfa = "Mfa"


class ChallengeNameType(StrEnum):
    SMS_MFA = "SMS_MFA"
    EMAIL_OTP = "EMAIL_OTP"
    SOFTWARE_TOKEN_MFA = "SOFTWARE_TOKEN_MFA"
    SELECT_MFA_TYPE = "SELECT_MFA_TYPE"
    MFA_SETUP = "MFA_SETUP"
    PASSWORD_VERIFIER = "PASSWORD_VERIFIER"
    CUSTOM_CHALLENGE = "CUSTOM_CHALLENGE"
    SELECT_CHALLENGE = "SELECT_CHALLENGE"
    DEVICE_SRP_AUTH = "DEVICE_SRP_AUTH"
    DEVICE_PASSWORD_VERIFIER = "DEVICE_PASSWORD_VERIFIER"
    ADMIN_NO_SRP_AUTH = "ADMIN_NO_SRP_AUTH"
    NEW_PASSWORD_REQUIRED = "NEW_PASSWORD_REQUIRED"
    SMS_OTP = "SMS_OTP"
    PASSWORD = "PASSWORD"
    WEB_AUTHN = "WEB_AUTHN"
    PASSWORD_SRP = "PASSWORD_SRP"


class ChallengeResponse(StrEnum):
    Success = "Success"
    Failure = "Failure"


class ColorSchemeModeType(StrEnum):
    LIGHT = "LIGHT"
    DARK = "DARK"
    DYNAMIC = "DYNAMIC"


class CompromisedCredentialsEventActionType(StrEnum):
    BLOCK = "BLOCK"
    NO_ACTION = "NO_ACTION"


class CustomEmailSenderLambdaVersionType(StrEnum):
    V1_0 = "V1_0"


class CustomSMSSenderLambdaVersionType(StrEnum):
    V1_0 = "V1_0"


class DefaultEmailOptionType(StrEnum):
    CONFIRM_WITH_LINK = "CONFIRM_WITH_LINK"
    CONFIRM_WITH_CODE = "CONFIRM_WITH_CODE"


class DeletionProtectionType(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class DeliveryMediumType(StrEnum):
    SMS = "SMS"
    EMAIL = "EMAIL"


class DeviceRememberedStatusType(StrEnum):
    remembered = "remembered"
    not_remembered = "not_remembered"


class DomainStatusType(StrEnum):
    CREATING = "CREATING"
    DELETING = "DELETING"
    UPDATING = "UPDATING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"


class EmailSendingAccountType(StrEnum):
    COGNITO_DEFAULT = "COGNITO_DEFAULT"
    DEVELOPER = "DEVELOPER"


class EventFilterType(StrEnum):
    SIGN_IN = "SIGN_IN"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    SIGN_UP = "SIGN_UP"


class EventResponseType(StrEnum):
    Pass = "Pass"
    Fail = "Fail"
    InProgress = "InProgress"


class EventSourceName(StrEnum):
    userNotification = "userNotification"
    userAuthEvents = "userAuthEvents"


class EventType(StrEnum):
    SignIn = "SignIn"
    SignUp = "SignUp"
    ForgotPassword = "ForgotPassword"
    PasswordChange = "PasswordChange"
    ResendCode = "ResendCode"


class ExplicitAuthFlowsType(StrEnum):
    ADMIN_NO_SRP_AUTH = "ADMIN_NO_SRP_AUTH"
    CUSTOM_AUTH_FLOW_ONLY = "CUSTOM_AUTH_FLOW_ONLY"
    USER_PASSWORD_AUTH = "USER_PASSWORD_AUTH"
    ALLOW_ADMIN_USER_PASSWORD_AUTH = "ALLOW_ADMIN_USER_PASSWORD_AUTH"
    ALLOW_CUSTOM_AUTH = "ALLOW_CUSTOM_AUTH"
    ALLOW_USER_PASSWORD_AUTH = "ALLOW_USER_PASSWORD_AUTH"
    ALLOW_USER_SRP_AUTH = "ALLOW_USER_SRP_AUTH"
    ALLOW_REFRESH_TOKEN_AUTH = "ALLOW_REFRESH_TOKEN_AUTH"
    ALLOW_USER_AUTH = "ALLOW_USER_AUTH"


class FeedbackValueType(StrEnum):
    Valid = "Valid"
    Invalid = "Invalid"


class IdentityProviderTypeType(StrEnum):
    SAML = "SAML"
    Facebook = "Facebook"
    Google = "Google"
    LoginWithAmazon = "LoginWithAmazon"
    SignInWithApple = "SignInWithApple"
    OIDC = "OIDC"


class LogLevel(StrEnum):
    ERROR = "ERROR"
    INFO = "INFO"


class MessageActionType(StrEnum):
    RESEND = "RESEND"
    SUPPRESS = "SUPPRESS"


class OAuthFlowType(StrEnum):
    code = "code"
    implicit = "implicit"
    client_credentials = "client_credentials"


class PreTokenGenerationLambdaVersionType(StrEnum):
    V1_0 = "V1_0"
    V2_0 = "V2_0"


class PreventUserExistenceErrorTypes(StrEnum):
    LEGACY = "LEGACY"
    ENABLED = "ENABLED"


class RecoveryOptionNameType(StrEnum):
    verified_email = "verified_email"
    verified_phone_number = "verified_phone_number"
    admin_only = "admin_only"


class RiskDecisionType(StrEnum):
    NoRisk = "NoRisk"
    AccountTakeover = "AccountTakeover"
    Block = "Block"


class RiskLevelType(StrEnum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class StatusType(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class TimeUnitsType(StrEnum):
    seconds = "seconds"
    minutes = "minutes"
    hours = "hours"
    days = "days"


class UserImportJobStatusType(StrEnum):
    Created = "Created"
    Pending = "Pending"
    InProgress = "InProgress"
    Stopping = "Stopping"
    Expired = "Expired"
    Stopped = "Stopped"
    Failed = "Failed"
    Succeeded = "Succeeded"


class UserPoolMfaType(StrEnum):
    OFF = "OFF"
    ON = "ON"
    OPTIONAL = "OPTIONAL"


class UserPoolTierType(StrEnum):
    LITE = "LITE"
    ESSENTIALS = "ESSENTIALS"
    PLUS = "PLUS"


class UserStatusType(StrEnum):
    UNCONFIRMED = "UNCONFIRMED"
    CONFIRMED = "CONFIRMED"
    ARCHIVED = "ARCHIVED"
    COMPROMISED = "COMPROMISED"
    UNKNOWN = "UNKNOWN"
    RESET_REQUIRED = "RESET_REQUIRED"
    FORCE_CHANGE_PASSWORD = "FORCE_CHANGE_PASSWORD"
    EXTERNAL_PROVIDER = "EXTERNAL_PROVIDER"


class UserVerificationType(StrEnum):
    required = "required"
    preferred = "preferred"


class UsernameAttributeType(StrEnum):
    phone_number = "phone_number"
    email = "email"


class VerifiedAttributeType(StrEnum):
    phone_number = "phone_number"
    email = "email"


class VerifySoftwareTokenResponseType(StrEnum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class AliasExistsException(ServiceException):
    """This exception is thrown when a user tries to confirm the account with
    an email address or phone number that has already been supplied as an
    alias for a different user profile. This exception indicates that an
    account with this email address or phone already exists in a user pool
    that you've configured to use email address or phone number as a sign-in
    alias.
    """

    code: str = "AliasExistsException"
    sender_fault: bool = False
    status_code: int = 400


class CodeDeliveryFailureException(ServiceException):
    """This exception is thrown when a verification code fails to deliver
    successfully.
    """

    code: str = "CodeDeliveryFailureException"
    sender_fault: bool = False
    status_code: int = 400


class CodeMismatchException(ServiceException):
    """This exception is thrown if the provided code doesn't match what the
    server was expecting.
    """

    code: str = "CodeMismatchException"
    sender_fault: bool = False
    status_code: int = 400


class ConcurrentModificationException(ServiceException):
    """This exception is thrown if two or more modifications are happening
    concurrently.
    """

    code: str = "ConcurrentModificationException"
    sender_fault: bool = False
    status_code: int = 400


class DuplicateProviderException(ServiceException):
    """This exception is thrown when the provider is already supported by the
    user pool.
    """

    code: str = "DuplicateProviderException"
    sender_fault: bool = False
    status_code: int = 400


class EnableSoftwareTokenMFAException(ServiceException):
    """This exception is thrown when there is a code mismatch and the service
    fails to configure the software token TOTP multi-factor authentication
    (MFA).
    """

    code: str = "EnableSoftwareTokenMFAException"
    sender_fault: bool = False
    status_code: int = 400


class ExpiredCodeException(ServiceException):
    """This exception is thrown if a code has expired."""

    code: str = "ExpiredCodeException"
    sender_fault: bool = False
    status_code: int = 400


class FeatureUnavailableInTierException(ServiceException):
    """This exception is thrown when a feature you attempted to configure isn't
    available in your current feature plan.
    """

    code: str = "FeatureUnavailableInTierException"
    sender_fault: bool = False
    status_code: int = 400


class ForbiddenException(ServiceException):
    """This exception is thrown when WAF doesn't allow your request based on a
    web ACL that's associated with your user pool.
    """

    code: str = "ForbiddenException"
    sender_fault: bool = False
    status_code: int = 400


class GroupExistsException(ServiceException):
    """This exception is thrown when Amazon Cognito encounters a group that
    already exists in the user pool.
    """

    code: str = "GroupExistsException"
    sender_fault: bool = False
    status_code: int = 400


class InternalErrorException(ServiceException):
    """This exception is thrown when Amazon Cognito encounters an internal
    error.
    """

    code: str = "InternalErrorException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidEmailRoleAccessPolicyException(ServiceException):
    """This exception is thrown when Amazon Cognito isn't allowed to use your
    email identity. HTTP status code: 400.
    """

    code: str = "InvalidEmailRoleAccessPolicyException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidLambdaResponseException(ServiceException):
    """This exception is thrown when Amazon Cognito encounters an invalid
    Lambda response.
    """

    code: str = "InvalidLambdaResponseException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidOAuthFlowException(ServiceException):
    """This exception is thrown when the specified OAuth flow is not valid."""

    code: str = "InvalidOAuthFlowException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidParameterException(ServiceException):
    """This exception is thrown when the Amazon Cognito service encounters an
    invalid parameter.
    """

    code: str = "InvalidParameterException"
    sender_fault: bool = False
    status_code: int = 400
    reasonCode: Optional[InvalidParameterExceptionReasonCodeType]


class InvalidPasswordException(ServiceException):
    """This exception is thrown when Amazon Cognito encounters an invalid
    password.
    """

    code: str = "InvalidPasswordException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidSmsRoleAccessPolicyException(ServiceException):
    """This exception is returned when the role provided for SMS configuration
    doesn't have permission to publish using Amazon SNS.
    """

    code: str = "InvalidSmsRoleAccessPolicyException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidSmsRoleTrustRelationshipException(ServiceException):
    """This exception is thrown when the trust relationship is not valid for
    the role provided for SMS configuration. This can happen if you don't
    trust ``cognito-idp.amazonaws.com`` or the external ID provided in the
    role does not match what is provided in the SMS configuration for the
    user pool.
    """

    code: str = "InvalidSmsRoleTrustRelationshipException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidUserPoolConfigurationException(ServiceException):
    """This exception is thrown when the user pool configuration is not valid."""

    code: str = "InvalidUserPoolConfigurationException"
    sender_fault: bool = False
    status_code: int = 400


class LimitExceededException(ServiceException):
    """This exception is thrown when a user exceeds the limit for a requested
    Amazon Web Services resource.
    """

    code: str = "LimitExceededException"
    sender_fault: bool = False
    status_code: int = 400


class MFAMethodNotFoundException(ServiceException):
    """This exception is thrown when Amazon Cognito can't find a multi-factor
    authentication (MFA) method.
    """

    code: str = "MFAMethodNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ManagedLoginBrandingExistsException(ServiceException):
    """This exception is thrown when you attempt to apply a managed login
    branding style to an app client that already has an assigned style.
    """

    code: str = "ManagedLoginBrandingExistsException"
    sender_fault: bool = False
    status_code: int = 400


class NotAuthorizedException(ServiceException):
    """This exception is thrown when a user isn't authorized."""

    code: str = "NotAuthorizedException"
    sender_fault: bool = False
    status_code: int = 400


class PasswordHistoryPolicyViolationException(ServiceException):
    """The message returned when a user's new password matches a previous
    password and doesn't comply with the password-history policy.
    """

    code: str = "PasswordHistoryPolicyViolationException"
    sender_fault: bool = False
    status_code: int = 400


class PasswordResetRequiredException(ServiceException):
    """This exception is thrown when a password reset is required."""

    code: str = "PasswordResetRequiredException"
    sender_fault: bool = False
    status_code: int = 400


class PreconditionNotMetException(ServiceException):
    """This exception is thrown when a precondition is not met."""

    code: str = "PreconditionNotMetException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceNotFoundException(ServiceException):
    """This exception is thrown when the Amazon Cognito service can't find the
    requested resource.
    """

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ScopeDoesNotExistException(ServiceException):
    """This exception is thrown when the specified scope doesn't exist."""

    code: str = "ScopeDoesNotExistException"
    sender_fault: bool = False
    status_code: int = 400


class SoftwareTokenMFANotFoundException(ServiceException):
    """This exception is thrown when the software token time-based one-time
    password (TOTP) multi-factor authentication (MFA) isn't activated for
    the user pool.
    """

    code: str = "SoftwareTokenMFANotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class TierChangeNotAllowedException(ServiceException):
    """This exception is thrown when you've attempted to change your feature
    plan but the operation isn't permitted.
    """

    code: str = "TierChangeNotAllowedException"
    sender_fault: bool = False
    status_code: int = 400


class TooManyFailedAttemptsException(ServiceException):
    """This exception is thrown when the user has made too many failed attempts
    for a given action, such as sign-in.
    """

    code: str = "TooManyFailedAttemptsException"
    sender_fault: bool = False
    status_code: int = 400


class TooManyRequestsException(ServiceException):
    """This exception is thrown when the user has made too many requests for a
    given operation.
    """

    code: str = "TooManyRequestsException"
    sender_fault: bool = False
    status_code: int = 400


class UnauthorizedException(ServiceException):
    """Exception that is thrown when the request isn't authorized. This can
    happen due to an invalid access token in the request.
    """

    code: str = "UnauthorizedException"
    sender_fault: bool = False
    status_code: int = 400


class UnexpectedLambdaException(ServiceException):
    """This exception is thrown when Amazon Cognito encounters an unexpected
    exception with Lambda.
    """

    code: str = "UnexpectedLambdaException"
    sender_fault: bool = False
    status_code: int = 400


class UnsupportedIdentityProviderException(ServiceException):
    """This exception is thrown when the specified identifier isn't supported."""

    code: str = "UnsupportedIdentityProviderException"
    sender_fault: bool = False
    status_code: int = 400


class UnsupportedOperationException(ServiceException):
    """Exception that is thrown when you attempt to perform an operation that
    isn't enabled for the user pool client.
    """

    code: str = "UnsupportedOperationException"
    sender_fault: bool = False
    status_code: int = 400


class UnsupportedTokenTypeException(ServiceException):
    """Exception that is thrown when an unsupported token is passed to an
    operation.
    """

    code: str = "UnsupportedTokenTypeException"
    sender_fault: bool = False
    status_code: int = 400


class UnsupportedUserStateException(ServiceException):
    """The request failed because the user is in an unsupported state."""

    code: str = "UnsupportedUserStateException"
    sender_fault: bool = False
    status_code: int = 400


class UserImportInProgressException(ServiceException):
    """This exception is thrown when you're trying to modify a user pool while
    a user import job is in progress for that pool.
    """

    code: str = "UserImportInProgressException"
    sender_fault: bool = False
    status_code: int = 400


class UserLambdaValidationException(ServiceException):
    """This exception is thrown when the Amazon Cognito service encounters a
    user validation exception with the Lambda service.
    """

    code: str = "UserLambdaValidationException"
    sender_fault: bool = False
    status_code: int = 400


class UserNotConfirmedException(ServiceException):
    """This exception is thrown when a user isn't confirmed successfully."""

    code: str = "UserNotConfirmedException"
    sender_fault: bool = False
    status_code: int = 400


class UserNotFoundException(ServiceException):
    """This exception is thrown when a user isn't found."""

    code: str = "UserNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class UserPoolAddOnNotEnabledException(ServiceException):
    """This exception is thrown when user pool add-ons aren't enabled."""

    code: str = "UserPoolAddOnNotEnabledException"
    sender_fault: bool = False
    status_code: int = 400


class UserPoolTaggingException(ServiceException):
    """This exception is thrown when a user pool tag can't be set or updated."""

    code: str = "UserPoolTaggingException"
    sender_fault: bool = False
    status_code: int = 400


class UsernameExistsException(ServiceException):
    """This exception is thrown when Amazon Cognito encounters a user name that
    already exists in the user pool.
    """

    code: str = "UsernameExistsException"
    sender_fault: bool = False
    status_code: int = 400


class WebAuthnChallengeNotFoundException(ServiceException):
    """This exception is thrown when the challenge from ``StartWebAuthn``
    registration has expired.
    """

    code: str = "WebAuthnChallengeNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class WebAuthnClientMismatchException(ServiceException):
    """This exception is thrown when the access token is for a different client
    than the one in the original ``StartWebAuthnRegistration`` request.
    """

    code: str = "WebAuthnClientMismatchException"
    sender_fault: bool = False
    status_code: int = 400


class WebAuthnConfigurationMissingException(ServiceException):
    """This exception is thrown when a user pool doesn't have a configured
    relying party id or a user pool domain.
    """

    code: str = "WebAuthnConfigurationMissingException"
    sender_fault: bool = False
    status_code: int = 400


class WebAuthnCredentialNotSupportedException(ServiceException):
    """This exception is thrown when a user presents passkey credentials from
    an unsupported device or provider.
    """

    code: str = "WebAuthnCredentialNotSupportedException"
    sender_fault: bool = False
    status_code: int = 400


class WebAuthnNotEnabledException(ServiceException):
    """This exception is thrown when the passkey feature isn't enabled for the
    user pool.
    """

    code: str = "WebAuthnNotEnabledException"
    sender_fault: bool = False
    status_code: int = 400


class WebAuthnOriginNotAllowedException(ServiceException):
    """This exception is thrown when the passkey credential's registration
    origin does not align with the user pool relying party id.
    """

    code: str = "WebAuthnOriginNotAllowedException"
    sender_fault: bool = False
    status_code: int = 400


class WebAuthnRelyingPartyMismatchException(ServiceException):
    """This exception is thrown when the given passkey credential is associated
    with a different relying party ID than the user pool relying party ID.
    """

    code: str = "WebAuthnRelyingPartyMismatchException"
    sender_fault: bool = False
    status_code: int = 400


class RecoveryOptionType(TypedDict, total=False):
    """A recovery option for a user. The ``AccountRecoverySettingType`` data
    type is an array of this object. Each ``RecoveryOptionType`` has a
    priority property that determines whether it is a primary or secondary
    option.

    For example, if ``verified_email`` has a priority of ``1`` and
    ``verified_phone_number`` has a priority of ``2``, your user pool sends
    account-recovery messages to a verified email address but falls back to
    an SMS message if the user has a verified phone number. The
    ``admin_only`` option prevents self-service account recovery.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    Priority: PriorityType
    Name: RecoveryOptionNameType


RecoveryMechanismsType = List[RecoveryOptionType]


class AccountRecoverySettingType(TypedDict, total=False):
    """The settings for user message delivery in forgot-password operations.
    Contains preference for email or SMS message delivery of password reset
    codes, or for admin-only password reset.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    RecoveryMechanisms: Optional[RecoveryMechanismsType]


class AccountTakeoverActionType(TypedDict, total=False):
    """The automated response to a risk level for adaptive authentication in
    full-function, or ``ENFORCED``, mode. You can assign an action to each
    risk level that advanced security features evaluates.

    This data type is a request parameter of
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__
    and a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__.
    """

    Notify: AccountTakeoverActionNotifyType
    EventAction: AccountTakeoverEventActionType


class AccountTakeoverActionsType(TypedDict, total=False):
    """A list of account-takeover actions for each level of risk that Amazon
    Cognito might assess with advanced security features.

    This data type is a request parameter of
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__
    and a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__.
    """

    LowAction: Optional[AccountTakeoverActionType]
    MediumAction: Optional[AccountTakeoverActionType]
    HighAction: Optional[AccountTakeoverActionType]


class NotifyEmailType(TypedDict, total=False):
    """The template for email messages that advanced security features sends to
    a user when your threat protection automated response has a *Notify*
    action.

    This data type is a request parameter of
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__
    and a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__.
    """

    Subject: EmailNotificationSubjectType
    HtmlBody: Optional[EmailNotificationBodyType]
    TextBody: Optional[EmailNotificationBodyType]


class NotifyConfigurationType(TypedDict, total=False):
    """The configuration for Amazon SES email messages that advanced security
    features sends to a user when your adaptive authentication automated
    response has a *Notify* action.

    This data type is a request parameter of
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__
    and a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__.
    """

    From: Optional[StringType]
    ReplyTo: Optional[StringType]
    SourceArn: ArnType
    BlockEmail: Optional[NotifyEmailType]
    NoActionEmail: Optional[NotifyEmailType]
    MfaEmail: Optional[NotifyEmailType]


class AccountTakeoverRiskConfigurationType(TypedDict, total=False):
    """The settings for automated responses and notification templates for
    adaptive authentication with advanced security features.

    This data type is a request parameter of
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__
    and a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__.
    """

    NotifyConfiguration: Optional[NotifyConfigurationType]
    Actions: AccountTakeoverActionsType


class StringAttributeConstraintsType(TypedDict, total=False):
    """The minimum and maximum length values of an attribute that is of the
    string type, for example ``custom:department``.

    This data type is part of
    `SchemaAttributeType <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SchemaAttributeType.html>`__.
    It defines the length constraints on string-type attributes that you
    configure in
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and displays the length constraints of all string-type attributes in the
    response to
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__
    """

    MinLength: Optional[StringType]
    MaxLength: Optional[StringType]


class NumberAttributeConstraintsType(TypedDict, total=False):
    """The minimum and maximum values of an attribute that is of the number
    type, for example ``custom:age``.

    This data type is part of
    `SchemaAttributeType <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SchemaAttributeType.html>`__.
    It defines the length constraints on number-type attributes that you
    configure in
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and displays the length constraints of all number-type attributes in the
    response to
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__
    """

    MinValue: Optional[StringType]
    MaxValue: Optional[StringType]


class SchemaAttributeType(TypedDict, total=False):
    """A list of the user attributes and their properties in your user pool.
    The attribute schema contains standard attributes, custom attributes
    with a ``custom:`` prefix, and developer attributes with a ``dev:``
    prefix. For more information, see `User pool
    attributes <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html>`__.

    Developer-only ``dev:`` attributes are a legacy feature of user pools,
    and are read-only to all app clients. You can create and update
    developer-only attributes only with IAM-authenticated API operations.
    Use app client read/write permissions instead.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    Name: Optional[CustomAttributeNameType]
    AttributeDataType: Optional[AttributeDataType]
    DeveloperOnlyAttribute: Optional[BooleanType]
    Mutable: Optional[BooleanType]
    Required: Optional[BooleanType]
    NumberAttributeConstraints: Optional[NumberAttributeConstraintsType]
    StringAttributeConstraints: Optional[StringAttributeConstraintsType]


CustomAttributesListType = List[SchemaAttributeType]


class AddCustomAttributesRequest(ServiceRequest):
    """Represents the request to add custom attributes."""

    UserPoolId: UserPoolIdType
    CustomAttributes: CustomAttributesListType


class AddCustomAttributesResponse(TypedDict, total=False):
    """Represents the response from the server for the request to add custom
    attributes.
    """

    pass


class AdminAddUserToGroupRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Username: UsernameType
    GroupName: GroupNameType


ClientMetadataType = Dict[StringType, StringType]


class AdminConfirmSignUpRequest(ServiceRequest):
    """Confirm a user's registration as a user pool administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType
    ClientMetadata: Optional[ClientMetadataType]


class AdminConfirmSignUpResponse(TypedDict, total=False):
    """Represents the response from the server for the request to confirm
    registration.
    """

    pass


class MessageTemplateType(TypedDict, total=False):
    """The message template structure."""

    SMSMessage: Optional[SmsInviteMessageType]
    EmailMessage: Optional[EmailInviteMessageType]
    EmailSubject: Optional[EmailVerificationSubjectType]


class AdminCreateUserConfigType(TypedDict, total=False):
    """The settings for administrator creation of users in a user pool.
    Contains settings for allowing user sign-up, customizing invitation
    messages to new users, and the amount of time before temporary passwords
    expire.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    AllowAdminCreateUserOnly: Optional[BooleanType]
    UnusedAccountValidityDays: Optional[AdminCreateUserUnusedAccountValidityDaysType]
    InviteMessageTemplate: Optional[MessageTemplateType]


DeliveryMediumListType = List[DeliveryMediumType]


class AttributeType(TypedDict, total=False):
    """The name and value of a user attribute.

    This data type is a request parameter of
    `AdminUpdateUserAttributes <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminUpdateUserAttributes.html>`__
    and
    `UpdateUserAttributes <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserAttributes.html>`__.
    """

    Name: AttributeNameType
    Value: Optional[AttributeValueType]


AttributeListType = List[AttributeType]


class AdminCreateUserRequest(ServiceRequest):
    """Creates a new user in the specified user pool."""

    UserPoolId: UserPoolIdType
    Username: UsernameType
    UserAttributes: Optional[AttributeListType]
    ValidationData: Optional[AttributeListType]
    TemporaryPassword: Optional[PasswordType]
    ForceAliasCreation: Optional[ForceAliasCreation]
    MessageAction: Optional[MessageActionType]
    DesiredDeliveryMediums: Optional[DeliveryMediumListType]
    ClientMetadata: Optional[ClientMetadataType]


class MFAOptionType(TypedDict, total=False):
    """*This data type is no longer supported.* Applies only to SMS
    multi-factor authentication (MFA) configurations. Does not apply to
    time-based one-time password (TOTP) software token MFA configurations.
    """

    DeliveryMedium: Optional[DeliveryMediumType]
    AttributeName: Optional[AttributeNameType]


MFAOptionListType = List[MFAOptionType]
DateType = datetime


class UserType(TypedDict, total=False):
    """A user profile in a Amazon Cognito user pool.

    This data type is a response parameter to
    `AdminCreateUser <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminCreateUser.html>`__
    and
    `ListUsers <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ListUsers.html>`__.
    """

    Username: Optional[UsernameType]
    Attributes: Optional[AttributeListType]
    UserCreateDate: Optional[DateType]
    UserLastModifiedDate: Optional[DateType]
    Enabled: Optional[BooleanType]
    UserStatus: Optional[UserStatusType]
    MFAOptions: Optional[MFAOptionListType]


class AdminCreateUserResponse(TypedDict, total=False):
    """Represents the response from the server to the request to create the
    user.
    """

    User: Optional[UserType]


AttributeNameListType = List[AttributeNameType]


class AdminDeleteUserAttributesRequest(ServiceRequest):
    """Represents the request to delete user attributes as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType
    UserAttributeNames: AttributeNameListType


class AdminDeleteUserAttributesResponse(TypedDict, total=False):
    """Represents the response received from the server for a request to delete
    user attributes.
    """

    pass


class AdminDeleteUserRequest(ServiceRequest):
    """Represents the request to delete a user as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType


class ProviderUserIdentifierType(TypedDict, total=False):
    """The characteristics of a source or destination user for linking a
    federated user profile to a local user profile.

    This data type is a request parameter of
    `AdminLinkProviderForUser <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminLinkProviderForUser.html>`__
    and
    `AdminDisableProviderForUser <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminDisableProviderForUser.html>`__.
    """

    ProviderName: Optional[ProviderNameType]
    ProviderAttributeName: Optional[StringType]
    ProviderAttributeValue: Optional[StringType]


class AdminDisableProviderForUserRequest(ServiceRequest):
    UserPoolId: StringType
    User: ProviderUserIdentifierType


class AdminDisableProviderForUserResponse(TypedDict, total=False):
    pass


class AdminDisableUserRequest(ServiceRequest):
    """Represents the request to disable the user as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType


class AdminDisableUserResponse(TypedDict, total=False):
    """Represents the response received from the server to disable the user as
    an administrator.
    """

    pass


class AdminEnableUserRequest(ServiceRequest):
    """Represents the request that enables the user as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType


class AdminEnableUserResponse(TypedDict, total=False):
    """Represents the response from the server for the request to enable a user
    as an administrator.
    """

    pass


class AdminForgetDeviceRequest(ServiceRequest):
    """Sends the forgot device request, as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType
    DeviceKey: DeviceKeyType


class AdminGetDeviceRequest(ServiceRequest):
    """Represents the request to get the device, as an administrator."""

    DeviceKey: DeviceKeyType
    UserPoolId: UserPoolIdType
    Username: UsernameType


class DeviceType(TypedDict, total=False):
    """Information about a user's device that they've registered for device SRP
    authentication in your application. For more information, see `Working
    with user devices in your user
    pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`__.

    The data type is a response parameter of
    `AdminGetDevice <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminGetDevice.html>`__,
    `AdminListDevices <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminListDevices.html>`__,
    and
    `GetDevice <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetDevice.html>`__.
    """

    DeviceKey: Optional[DeviceKeyType]
    DeviceAttributes: Optional[AttributeListType]
    DeviceCreateDate: Optional[DateType]
    DeviceLastModifiedDate: Optional[DateType]
    DeviceLastAuthenticatedDate: Optional[DateType]


class AdminGetDeviceResponse(TypedDict, total=False):
    """Gets the device response, as an administrator."""

    Device: DeviceType


class AdminGetUserRequest(ServiceRequest):
    """Represents the request to get the specified user as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType


UserMFASettingListType = List[StringType]


class AdminGetUserResponse(TypedDict, total=False):
    """Represents the response from the server from the request to get the
    specified user as an administrator.
    """

    Username: UsernameType
    UserAttributes: Optional[AttributeListType]
    UserCreateDate: Optional[DateType]
    UserLastModifiedDate: Optional[DateType]
    Enabled: Optional[BooleanType]
    UserStatus: Optional[UserStatusType]
    MFAOptions: Optional[MFAOptionListType]
    PreferredMfaSetting: Optional[StringType]
    UserMFASettingList: Optional[UserMFASettingListType]


class HttpHeader(TypedDict, total=False):
    """The HTTP header in the ``ContextData`` parameter.

    This data type is a request parameter of server-side authentication
    operations like
    `AdminInitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminInitiateAuth.html>`__
    and
    `AdminRespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminRespondToAuthChallenge.html>`__.
    """

    headerName: Optional[StringType]
    headerValue: Optional[StringType]


HttpHeaderList = List[HttpHeader]


class ContextDataType(TypedDict, total=False):
    """Contextual user data used for evaluating the risk of an authentication
    event by user pool threat protection.

    This data type is a request parameter of server-side authentication
    operations like
    `AdminInitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminInitiateAuth.html>`__
    and
    `AdminRespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminRespondToAuthChallenge.html>`__.
    """

    IpAddress: StringType
    ServerName: StringType
    ServerPath: StringType
    HttpHeaders: HttpHeaderList
    EncodedData: Optional[StringType]


class AnalyticsMetadataType(TypedDict, total=False):
    """Information that your application adds to authentication requests.
    Applies an endpoint ID to the analytics data that your user pool sends
    to Amazon Pinpoint.

    An endpoint ID uniquely identifies a mobile device, email address or
    phone number that can receive messages from Amazon Pinpoint analytics.
    For more information about Amazon Web Services Regions that can contain
    Amazon Pinpoint resources for use with Amazon Cognito user pools, see
    `Using Amazon Pinpoint analytics with Amazon Cognito user
    pools <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-pinpoint-integration.html>`__.

    This data type is a request parameter of authentication operations like
    `InitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_InitiateAuth.html>`__,
    `AdminInitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminInitiateAuth.html>`__,
    `RespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RespondToAuthChallenge.html>`__,
    and
    `AdminRespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminRespondToAuthChallenge.html>`__.
    """

    AnalyticsEndpointId: Optional[StringType]


AuthParametersType = Dict[StringType, StringType]


class AdminInitiateAuthRequest(ServiceRequest):
    """Initiates the authorization request, as an administrator."""

    UserPoolId: UserPoolIdType
    ClientId: ClientIdType
    AuthFlow: AuthFlowType
    AuthParameters: Optional[AuthParametersType]
    ClientMetadata: Optional[ClientMetadataType]
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    ContextData: Optional[ContextDataType]
    Session: Optional[SessionType]


class NewDeviceMetadataType(TypedDict, total=False):
    """Information that your user pool responds with in
    ``AuthenticationResult`` when you configure it to remember devices and
    a user signs in with an unrecognized device. Amazon Cognito presents a
    new device key that you can use to set up `device
    authentication <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`__
    in a "Remember me on this device" authentication model.

    This data type is a response parameter of authentication operations like
    `InitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_InitiateAuth.html>`__,
    `AdminInitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminInitiateAuth.html>`__,
    `RespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RespondToAuthChallenge.html>`__,
    and
    `AdminRespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminRespondToAuthChallenge.html>`__.
    """

    DeviceKey: Optional[DeviceKeyType]
    DeviceGroupKey: Optional[StringType]


class AuthenticationResultType(TypedDict, total=False):
    """The object that your application receives after authentication. Contains
    tokens and information for device authentication.

    This data type is a response parameter of authentication operations like
    `InitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_InitiateAuth.html>`__,
    `AdminInitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminInitiateAuth.html>`__,
    `RespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RespondToAuthChallenge.html>`__,
    and
    `AdminRespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminRespondToAuthChallenge.html>`__.
    """

    AccessToken: Optional[TokenModelType]
    ExpiresIn: Optional[IntegerType]
    TokenType: Optional[StringType]
    RefreshToken: Optional[TokenModelType]
    IdToken: Optional[TokenModelType]
    NewDeviceMetadata: Optional[NewDeviceMetadataType]


ChallengeParametersType = Dict[StringType, StringType]


class AdminInitiateAuthResponse(TypedDict, total=False):
    """Initiates the authentication response, as an administrator."""

    ChallengeName: Optional[ChallengeNameType]
    Session: Optional[SessionType]
    ChallengeParameters: Optional[ChallengeParametersType]
    AuthenticationResult: Optional[AuthenticationResultType]


class AdminLinkProviderForUserRequest(ServiceRequest):
    UserPoolId: StringType
    DestinationUser: ProviderUserIdentifierType
    SourceUser: ProviderUserIdentifierType


class AdminLinkProviderForUserResponse(TypedDict, total=False):
    pass


class AdminListDevicesRequest(ServiceRequest):
    """Represents the request to list devices, as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType
    Limit: Optional[QueryLimitType]
    PaginationToken: Optional[SearchPaginationTokenType]


DeviceListType = List[DeviceType]


class AdminListDevicesResponse(TypedDict, total=False):
    """Lists the device's response, as an administrator."""

    Devices: Optional[DeviceListType]
    PaginationToken: Optional[SearchPaginationTokenType]


class AdminListGroupsForUserRequest(ServiceRequest):
    Username: UsernameType
    UserPoolId: UserPoolIdType
    Limit: Optional[QueryLimitType]
    NextToken: Optional[PaginationKey]


class GroupType(TypedDict, total=False):
    """A user pool group. Contains details about the group and the way that it
    contributes to IAM role decisions with identity pools. Identity pools
    can make decisions about the IAM role to assign based on groups: users
    get credentials for the role associated with their highest-priority
    group.

    This data type is a response parameter of
    `AdminListGroupsForUser <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminListGroupsForUser.html>`__,
    `CreateGroup <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateGroup.html>`__,
    `GetGroup <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetGroup.html>`__,
    `ListGroups <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ListGroups.html>`__,
    and
    `UpdateGroup <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateGroup.html>`__.
    """

    GroupName: Optional[GroupNameType]
    UserPoolId: Optional[UserPoolIdType]
    Description: Optional[DescriptionType]
    RoleArn: Optional[ArnType]
    Precedence: Optional[PrecedenceType]
    LastModifiedDate: Optional[DateType]
    CreationDate: Optional[DateType]


GroupListType = List[GroupType]


class AdminListGroupsForUserResponse(TypedDict, total=False):
    Groups: Optional[GroupListType]
    NextToken: Optional[PaginationKey]


class AdminListUserAuthEventsRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Username: UsernameType
    MaxResults: Optional[QueryLimitType]
    NextToken: Optional[PaginationKey]


class EventFeedbackType(TypedDict, total=False):
    """The feedback that your application submitted to an advanced security
    features event log, as displayed in an
    `AdminListUserAuthEvents <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminListUserAuthEvents.html>`__
    response.
    """

    FeedbackValue: FeedbackValueType
    Provider: StringType
    FeedbackDate: Optional[DateType]


class EventContextDataType(TypedDict, total=False):
    """The context data that your application submitted in an authentication
    request with advanced security features, as displayed in an
    `AdminListUserAuthEvents <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminListUserAuthEvents.html>`__
    response.
    """

    IpAddress: Optional[StringType]
    DeviceName: Optional[StringType]
    Timezone: Optional[StringType]
    City: Optional[StringType]
    Country: Optional[StringType]


class ChallengeResponseType(TypedDict, total=False):
    """The responses to the challenge that you received in the previous
    request. Each challenge has its own required response parameters. The
    following examples are partial JSON request bodies that highlight
    challenge-response parameters.

    You must provide a SECRET_HASH parameter in all challenge responses to
    an app client that has a client secret. Include a ``DEVICE_KEY`` for
    device authentication.

    SELECT_CHALLENGE
       ``"ChallengeName": "SELECT_CHALLENGE", "ChallengeResponses": { "USERNAME": "[username]", "ANSWER": "[Challenge name]"}``

       Available challenges are ``PASSWORD``, ``PASSWORD_SRP``,
       ``EMAIL_OTP``, ``SMS_OTP``, and ``WEB_AUTHN``.

       Complete authentication in the ``SELECT_CHALLENGE`` response for
       ``PASSWORD``, ``PASSWORD_SRP``, and ``WEB_AUTHN``:

       -  ``"ChallengeName": "SELECT_CHALLENGE", "ChallengeResponses": { "ANSWER": "WEB_AUTHN", "USERNAME": "[username]", "CREDENTIAL": "[AuthenticationResponseJSON]"}``

          See
          `AuthenticationResponseJSON <https://www.w3.org/TR/webauthn-3/#dictdef-authenticationresponsejson>`__.

       -  ``"ChallengeName": "SELECT_CHALLENGE", "ChallengeResponses": { "ANSWER": "PASSWORD", "USERNAME": "[username]", "PASSWORD": "[password]"}``

       -  ``"ChallengeName": "SELECT_CHALLENGE", "ChallengeResponses": { "ANSWER": "PASSWORD_SRP", "USERNAME": "[username]", "SRP_A": "[SRP_A]"}``

       For ``SMS_OTP`` and ``EMAIL_OTP``, respond with the username and
       answer. Your user pool will send a code for the user to submit in the
       next challenge response.

       -  ``"ChallengeName": "SELECT_CHALLENGE", "ChallengeResponses": { "ANSWER": "SMS_OTP", "USERNAME": "[username]"}``

       -  ``"ChallengeName": "SELECT_CHALLENGE", "ChallengeResponses": { "ANSWER": "EMAIL_OTP", "USERNAME": "[username]"}``

    SMS_OTP
       ``"ChallengeName": "SMS_OTP", "ChallengeResponses": {"SMS_OTP_CODE": "[code]", "USERNAME": "[username]"}``

    EMAIL_OTP
       ``"ChallengeName": "EMAIL_OTP", "ChallengeResponses": {"EMAIL_OTP_CODE": "[code]", "USERNAME": "[username]"}``

    SMS_MFA
       ``"ChallengeName": "SMS_MFA", "ChallengeResponses": {"SMS_MFA_CODE": "[code]", "USERNAME": "[username]"}``

    PASSWORD_VERIFIER
       This challenge response is part of the SRP flow. Amazon Cognito
       requires that your application respond to this challenge within a few
       seconds. When the response time exceeds this period, your user pool
       returns a ``NotAuthorizedException`` error.

       ``"ChallengeName": "PASSWORD_VERIFIER", "ChallengeResponses": {"PASSWORD_CLAIM_SIGNATURE": "[claim_signature]", "PASSWORD_CLAIM_SECRET_BLOCK": "[secret_block]", "TIMESTAMP": [timestamp], "USERNAME": "[username]"}``

       Add ``"DEVICE_KEY"`` when you sign in with a remembered device.

    CUSTOM_CHALLENGE
       ``"ChallengeName": "CUSTOM_CHALLENGE", "ChallengeResponses": {"USERNAME": "[username]", "ANSWER": "[challenge_answer]"}``

       Add ``"DEVICE_KEY"`` when you sign in with a remembered device.

    NEW_PASSWORD_REQUIRED
       ``"ChallengeName": "NEW_PASSWORD_REQUIRED", "ChallengeResponses": {"NEW_PASSWORD": "[new_password]", "USERNAME": "[username]"}``

       To set any required attributes that ``InitiateAuth`` returned in an
       ``requiredAttributes`` parameter, add
       ``"userAttributes.[attribute_name]": "[attribute_value]"``. This
       parameter can also set values for writable attributes that aren't
       required by your user pool.

       In a ``NEW_PASSWORD_REQUIRED`` challenge response, you can't modify a
       required attribute that already has a value. In
       ``RespondToAuthChallenge``, set a value for any keys that Amazon
       Cognito returned in the ``requiredAttributes`` parameter, then use
       the ``UpdateUserAttributes`` API operation to modify the value of any
       additional attributes.

    SOFTWARE_TOKEN_MFA
       ``"ChallengeName": "SOFTWARE_TOKEN_MFA", "ChallengeResponses": {"USERNAME": "[username]", "SOFTWARE_TOKEN_MFA_CODE": [authenticator_code]}``

    DEVICE_SRP_AUTH
       ``"ChallengeName": "DEVICE_SRP_AUTH", "ChallengeResponses": {"USERNAME": "[username]", "DEVICE_KEY": "[device_key]", "SRP_A": "[srp_a]"}``

    DEVICE_PASSWORD_VERIFIER
       ``"ChallengeName": "DEVICE_PASSWORD_VERIFIER", "ChallengeResponses": {"DEVICE_KEY": "[device_key]", "PASSWORD_CLAIM_SIGNATURE": "[claim_signature]", "PASSWORD_CLAIM_SECRET_BLOCK": "[secret_block]", "TIMESTAMP": [timestamp], "USERNAME": "[username]"}``

    MFA_SETUP
       ``"ChallengeName": "MFA_SETUP", "ChallengeResponses": {"USERNAME": "[username]"}, "SESSION": "[Session ID from VerifySoftwareToken]"``

    SELECT_MFA_TYPE
       ``"ChallengeName": "SELECT_MFA_TYPE", "ChallengeResponses": {"USERNAME": "[username]", "ANSWER": "[SMS_MFA or SOFTWARE_TOKEN_MFA]"}``

    For more information about ``SECRET_HASH``, see `Computing secret hash
    values <https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html#cognito-user-pools-computing-secret-hash>`__.
    For information about ``DEVICE_KEY``, see `Working with user devices in
    your user
    pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`__.

    This data type is a request parameter of
    `RespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RespondToAuthChallenge.html>`__
    and
    `AdminRespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminRespondToAuthChallenge.html>`__.
    """

    ChallengeName: Optional[ChallengeName]
    ChallengeResponse: Optional[ChallengeResponse]


ChallengeResponseListType = List[ChallengeResponseType]


class EventRiskType(TypedDict, total=False):
    """The risk evaluation by adaptive authentication, as displayed in an
    `AdminListUserAuthEvents <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminListUserAuthEvents.html>`__
    response. Contains evaluations of compromised-credentials detection and
    assessed risk level and action taken by adaptive authentication.
    """

    RiskDecision: Optional[RiskDecisionType]
    RiskLevel: Optional[RiskLevelType]
    CompromisedCredentialsDetected: Optional[WrappedBooleanType]


class AuthEventType(TypedDict, total=False):
    """One authentication event that Amazon Cognito logged in a user pool with
    advanced security features active. Contains user and device metadata and
    a risk assessment from your user pool.

    This data type is a request parameter of
    `AdminListUserAuthEvents <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminListUserAuthEvents.html>`__.
    """

    EventId: Optional[StringType]
    EventType: Optional[EventType]
    CreationDate: Optional[DateType]
    EventResponse: Optional[EventResponseType]
    EventRisk: Optional[EventRiskType]
    ChallengeResponses: Optional[ChallengeResponseListType]
    EventContextData: Optional[EventContextDataType]
    EventFeedback: Optional[EventFeedbackType]


AuthEventsType = List[AuthEventType]


class AdminListUserAuthEventsResponse(TypedDict, total=False):
    AuthEvents: Optional[AuthEventsType]
    NextToken: Optional[PaginationKey]


class AdminRemoveUserFromGroupRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Username: UsernameType
    GroupName: GroupNameType


class AdminResetUserPasswordRequest(ServiceRequest):
    """Represents the request to reset a user's password as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType
    ClientMetadata: Optional[ClientMetadataType]


class AdminResetUserPasswordResponse(TypedDict, total=False):
    """Represents the response from the server to reset a user password as an
    administrator.
    """

    pass


ChallengeResponsesType = Dict[StringType, StringType]


class AdminRespondToAuthChallengeRequest(ServiceRequest):
    """The request to respond to the authentication challenge, as an
    administrator.
    """

    UserPoolId: UserPoolIdType
    ClientId: ClientIdType
    ChallengeName: ChallengeNameType
    ChallengeResponses: Optional[ChallengeResponsesType]
    Session: Optional[SessionType]
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    ContextData: Optional[ContextDataType]
    ClientMetadata: Optional[ClientMetadataType]


class AdminRespondToAuthChallengeResponse(TypedDict, total=False):
    """Responds to the authentication challenge, as an administrator."""

    ChallengeName: Optional[ChallengeNameType]
    Session: Optional[SessionType]
    ChallengeParameters: Optional[ChallengeParametersType]
    AuthenticationResult: Optional[AuthenticationResultType]


class EmailMfaSettingsType(TypedDict, total=False):
    """User preferences for multi-factor authentication with email messages.
    Activates or deactivates email MFA and sets it as the preferred MFA
    method when multiple methods are available. To activate this setting,
    `advanced security
    features <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-advanced-security.html>`__
    must be active in your user pool.

    This data type is a request parameter of
    `SetUserMFAPreference <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserMFAPreference.html>`__
    and
    `AdminSetUserMFAPreference <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminSetUserMFAPreference.html>`__.
    """

    Enabled: Optional[BooleanType]
    PreferredMfa: Optional[BooleanType]


class SoftwareTokenMfaSettingsType(TypedDict, total=False):
    """A user's preference for using time-based one-time password (TOTP)
    multi-factor authentication (MFA). Turns TOTP MFA on and off, and can
    set TOTP as preferred when other MFA options are available. You can't
    turn off TOTP MFA for any of your users when MFA is required in your
    user pool; you can only set the type that your user prefers.

    This data type is a request parameter of
    `SetUserMFAPreference <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserMFAPreference.html>`__
    and
    `AdminSetUserMFAPreference <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminSetUserMFAPreference.html>`__.
    """

    Enabled: Optional[BooleanType]
    PreferredMfa: Optional[BooleanType]


class SMSMfaSettingsType(TypedDict, total=False):
    """A user's preference for using SMS message multi-factor authentication
    (MFA). Turns SMS MFA on and off, and can set SMS as preferred when other
    MFA options are available. You can't turn off SMS MFA for any of your
    users when MFA is required in your user pool; you can only set the type
    that your user prefers.

    This data type is a request parameter of
    `SetUserMFAPreference <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserMFAPreference.html>`__
    and
    `AdminSetUserMFAPreference <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminSetUserMFAPreference.html>`__.
    """

    Enabled: Optional[BooleanType]
    PreferredMfa: Optional[BooleanType]


class AdminSetUserMFAPreferenceRequest(ServiceRequest):
    SMSMfaSettings: Optional[SMSMfaSettingsType]
    SoftwareTokenMfaSettings: Optional[SoftwareTokenMfaSettingsType]
    EmailMfaSettings: Optional[EmailMfaSettingsType]
    Username: UsernameType
    UserPoolId: UserPoolIdType


class AdminSetUserMFAPreferenceResponse(TypedDict, total=False):
    pass


class AdminSetUserPasswordRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Username: UsernameType
    Password: PasswordType
    Permanent: Optional[BooleanType]


class AdminSetUserPasswordResponse(TypedDict, total=False):
    pass


class AdminSetUserSettingsRequest(ServiceRequest):
    """You can use this parameter to set an MFA configuration that uses the SMS
    delivery medium.
    """

    UserPoolId: UserPoolIdType
    Username: UsernameType
    MFAOptions: MFAOptionListType


class AdminSetUserSettingsResponse(TypedDict, total=False):
    """Represents the response from the server to set user settings as an
    administrator.
    """

    pass


class AdminUpdateAuthEventFeedbackRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Username: UsernameType
    EventId: EventIdType
    FeedbackValue: FeedbackValueType


class AdminUpdateAuthEventFeedbackResponse(TypedDict, total=False):
    pass


class AdminUpdateDeviceStatusRequest(ServiceRequest):
    """The request to update the device status, as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType
    DeviceKey: DeviceKeyType
    DeviceRememberedStatus: Optional[DeviceRememberedStatusType]


class AdminUpdateDeviceStatusResponse(TypedDict, total=False):
    """The status response to the request to update the device, as an
    administrator.
    """

    pass


class AdminUpdateUserAttributesRequest(ServiceRequest):
    """Represents the request to update the user's attributes as an
    administrator.
    """

    UserPoolId: UserPoolIdType
    Username: UsernameType
    UserAttributes: AttributeListType
    ClientMetadata: Optional[ClientMetadataType]


class AdminUpdateUserAttributesResponse(TypedDict, total=False):
    """Represents the response from the server for the request to update user
    attributes as an administrator.
    """

    pass


class AdminUserGlobalSignOutRequest(ServiceRequest):
    """The request to sign out of all devices, as an administrator."""

    UserPoolId: UserPoolIdType
    Username: UsernameType


class AdminUserGlobalSignOutResponse(TypedDict, total=False):
    """The global sign-out response, as an administrator."""

    pass


class AdvancedSecurityAdditionalFlowsType(TypedDict, total=False):
    """Advanced security configuration options for additional authentication
    types in your user pool, including custom authentication.
    """

    CustomAuthMode: Optional[AdvancedSecurityEnabledModeType]


AliasAttributesListType = List[AliasAttributeType]
AllowedFirstAuthFactorsListType = List[AuthFactorType]


class AnalyticsConfigurationType(TypedDict, total=False):
    """The settings for Amazon Pinpoint analytics configuration. With an
    analytics configuration, your application can collect user-activity
    metrics for user notifications with a Amazon Pinpoint campaign.

    Amazon Pinpoint isn't available in all Amazon Web Services Regions. For
    a list of available Regions, see `Amazon Cognito and Amazon Pinpoint
    Region
    availability <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-pinpoint-integration.html#cognito-user-pools-find-region-mappings>`__.

    This data type is a request parameter of
    `CreateUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPoolClient.html>`__
    and
    `UpdateUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPoolClient.html>`__,
    and a response parameter of
    `DescribeUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPoolClient.html>`__.
    """

    ApplicationId: Optional[HexStringType]
    ApplicationArn: Optional[ArnType]
    RoleArn: Optional[ArnType]
    ExternalId: Optional[StringType]
    UserDataShared: Optional[BooleanType]


AssetBytesType = bytes


class AssetType(TypedDict, total=False):
    """An image file from a managed login branding style in a user pool.

    This data type is a request parameter of
    `CreateManagedLoginBranding <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateManagedLoginBranding.html>`__
    and
    `UpdateManagedLoginBranding <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateManagedLoginBranding.html>`__,
    and a response parameter of
    `DescribeManagedLoginBranding <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeManagedLoginBranding.html>`__.
    """

    Category: AssetCategoryType
    ColorMode: ColorSchemeModeType
    Extension: AssetExtensionType
    Bytes: Optional[AssetBytesType]
    ResourceId: Optional[ResourceIdType]


AssetListType = List[AssetType]


class AssociateSoftwareTokenRequest(ServiceRequest):
    AccessToken: Optional[TokenModelType]
    Session: Optional[SessionType]


class AssociateSoftwareTokenResponse(TypedDict, total=False):
    SecretCode: Optional[SecretCodeType]
    Session: Optional[SessionType]


AttributeMappingType = Dict[AttributeMappingKeyType, StringType]
AttributesRequireVerificationBeforeUpdateType = List[VerifiedAttributeType]
AvailableChallengeListType = List[ChallengeNameType]
BlockedIPRangeListType = List[StringType]
CallbackURLsListType = List[RedirectUrlType]


class ChangePasswordRequest(ServiceRequest):
    """Represents the request to change a user password."""

    PreviousPassword: Optional[PasswordType]
    ProposedPassword: PasswordType
    AccessToken: TokenModelType


class ChangePasswordResponse(TypedDict, total=False):
    """The response from the server to the change password request."""

    pass


ClientPermissionListType = List[ClientPermissionType]


class CloudWatchLogsConfigurationType(TypedDict, total=False):
    """Configuration for the CloudWatch log group destination of user pool
    detailed activity logging, or of user activity log export with advanced
    security features.

    This data type is a request parameter of
    `SetLogDeliveryConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetLogDeliveryConfiguration.html>`__
    and a response parameter of
    `GetLogDeliveryConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetLogDeliveryConfiguration.html>`__.
    """

    LogGroupArn: Optional[ArnType]


class CodeDeliveryDetailsType(TypedDict, total=False):
    """The delivery details for an email or SMS message that Amazon Cognito
    sent for authentication or verification.

    This data type is a response parameter of operations that send a code
    for user profile confirmation, verification, or management, for example
    `ForgotPassword <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ForgotPassword.html>`__
    and
    `SignUp <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SignUp.html>`__.
    """

    Destination: Optional[StringType]
    DeliveryMedium: Optional[DeliveryMediumType]
    AttributeName: Optional[AttributeNameType]


CodeDeliveryDetailsListType = List[CodeDeliveryDetailsType]


class Document(TypedDict, total=False):
    pass


class CompleteWebAuthnRegistrationRequest(ServiceRequest):
    AccessToken: TokenModelType
    Credential: Document


class CompleteWebAuthnRegistrationResponse(TypedDict, total=False):
    pass


class CompromisedCredentialsActionsType(TypedDict, total=False):
    """Settings for user pool actions when Amazon Cognito detects compromised
    credentials with advanced security features in full-function
    ``ENFORCED`` mode.

    This data type is a request parameter of
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__
    and a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__.
    """

    EventAction: CompromisedCredentialsEventActionType


EventFiltersType = List[EventFilterType]


class CompromisedCredentialsRiskConfigurationType(TypedDict, total=False):
    """Settings for compromised-credentials actions and authentication-event
    sources with advanced security features in full-function ``ENFORCED``
    mode.

    This data type is a request parameter of
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__
    and a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__.
    """

    EventFilter: Optional[EventFiltersType]
    Actions: CompromisedCredentialsActionsType


ConfiguredUserAuthFactorsListType = List[AuthFactorType]


class DeviceSecretVerifierConfigType(TypedDict, total=False):
    """A Secure Remote Password (SRP) value that your application generates
    when you register a user's device. For more information, see `Getting a
    device
    key <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html#user-pools-remembered-devices-getting-a-device-key>`__.

    This data type is a request parameter of
    `ConfirmDevice <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ConfirmDevice.html>`__.
    """

    PasswordVerifier: Optional[StringType]
    Salt: Optional[StringType]


class ConfirmDeviceRequest(ServiceRequest):
    """Confirms the device request."""

    AccessToken: TokenModelType
    DeviceKey: DeviceKeyType
    DeviceSecretVerifierConfig: Optional[DeviceSecretVerifierConfigType]
    DeviceName: Optional[DeviceNameType]


class ConfirmDeviceResponse(TypedDict, total=False):
    """Confirms the device response."""

    UserConfirmationNecessary: Optional[BooleanType]


class UserContextDataType(TypedDict, total=False):
    """Contextual data, such as the user's device fingerprint, IP address, or
    location, used for evaluating the risk of an unexpected event by Amazon
    Cognito advanced security.

    This data type is a request parameter of public-client authentication
    operations like
    `InitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_InitiateAuth.html>`__
    and
    `RespondToAuthChallenge <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RespondToAuthChallenge.html>`__.
    """

    IpAddress: Optional[StringType]
    EncodedData: Optional[StringType]


class ConfirmForgotPasswordRequest(ServiceRequest):
    """The request representing the confirmation for a password reset."""

    ClientId: ClientIdType
    SecretHash: Optional[SecretHashType]
    Username: UsernameType
    ConfirmationCode: ConfirmationCodeType
    Password: PasswordType
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    UserContextData: Optional[UserContextDataType]
    ClientMetadata: Optional[ClientMetadataType]


class ConfirmForgotPasswordResponse(TypedDict, total=False):
    """The response from the server that results from a user's request to
    retrieve a forgotten password.
    """

    pass


class ConfirmSignUpRequest(ServiceRequest):
    """Represents the request to confirm registration of a user."""

    ClientId: ClientIdType
    SecretHash: Optional[SecretHashType]
    Username: UsernameType
    ConfirmationCode: ConfirmationCodeType
    ForceAliasCreation: Optional[ForceAliasCreation]
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    UserContextData: Optional[UserContextDataType]
    ClientMetadata: Optional[ClientMetadataType]
    Session: Optional[SessionType]


class ConfirmSignUpResponse(TypedDict, total=False):
    """Represents the response from the server for the registration
    confirmation.
    """

    Session: Optional[SessionType]


class CreateGroupRequest(ServiceRequest):
    GroupName: GroupNameType
    UserPoolId: UserPoolIdType
    Description: Optional[DescriptionType]
    RoleArn: Optional[ArnType]
    Precedence: Optional[PrecedenceType]


class CreateGroupResponse(TypedDict, total=False):
    Group: Optional[GroupType]


IdpIdentifiersListType = List[IdpIdentifierType]
ProviderDetailsType = Dict[StringType, StringType]


class CreateIdentityProviderRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ProviderName: ProviderNameTypeV2
    ProviderType: IdentityProviderTypeType
    ProviderDetails: ProviderDetailsType
    AttributeMapping: Optional[AttributeMappingType]
    IdpIdentifiers: Optional[IdpIdentifiersListType]


class IdentityProviderType(TypedDict, total=False):
    """A user pool identity provider (IdP). Contains information about a
    third-party IdP to a user pool, the attributes that it populates to user
    profiles, and the trust relationship between the IdP and your user pool.

    This data type is a response parameter of
    `CreateIdentityProvider <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateIdentityProvider.html>`__,
    `DescribeIdentityProvider <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeIdentityProvider.html>`__,
    `GetIdentityProviderByIdentifier <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetIdentityProviderByIdentifier.html>`__,
    and
    `UpdateIdentityProvider <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateIdentityProvider.html>`__.
    """

    UserPoolId: Optional[UserPoolIdType]
    ProviderName: Optional[ProviderNameType]
    ProviderType: Optional[IdentityProviderTypeType]
    ProviderDetails: Optional[ProviderDetailsType]
    AttributeMapping: Optional[AttributeMappingType]
    IdpIdentifiers: Optional[IdpIdentifiersListType]
    LastModifiedDate: Optional[DateType]
    CreationDate: Optional[DateType]


class CreateIdentityProviderResponse(TypedDict, total=False):
    IdentityProvider: IdentityProviderType


class CreateManagedLoginBrandingRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ClientId: ClientIdType
    UseCognitoProvidedValues: Optional[BooleanType]
    Settings: Optional[Document]
    Assets: Optional[AssetListType]


class ManagedLoginBrandingType(TypedDict, total=False):
    """A managed login branding style that's assigned to a user pool app
    client.

    This data type is a response parameter of
    `CreateManagedLoginBranding <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateManagedLoginBranding.html>`__,
    `UpdateManagedLoginBranding <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateManagedLoginBranding.html>`__,
    `DescribeManagedLoginBranding <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeManagedLoginBranding.html>`__,
    and
    `DescribeManagedLoginBrandingByClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeManagedLoginBrandingByClient.html>`__.
    """

    ManagedLoginBrandingId: Optional[ManagedLoginBrandingIdType]
    UserPoolId: Optional[UserPoolIdType]
    UseCognitoProvidedValues: Optional[BooleanType]
    Settings: Optional[Document]
    Assets: Optional[AssetListType]
    CreationDate: Optional[DateType]
    LastModifiedDate: Optional[DateType]


class CreateManagedLoginBrandingResponse(TypedDict, total=False):
    ManagedLoginBranding: Optional[ManagedLoginBrandingType]


class ResourceServerScopeType(TypedDict, total=False):
    """One custom scope associated with a user pool resource server. This data
    type is a member of ``ResourceServerScopeType``. For more information,
    see `Scopes, M2M, and API authorization with resource
    servers <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-define-resource-servers.html>`__.

    This data type is a request parameter of
    `CreateResourceServer <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateResourceServer.html>`__
    and a response parameter of
    `DescribeResourceServer <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeResourceServer.html>`__.
    """

    ScopeName: ResourceServerScopeNameType
    ScopeDescription: ResourceServerScopeDescriptionType


ResourceServerScopeListType = List[ResourceServerScopeType]


class CreateResourceServerRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Identifier: ResourceServerIdentifierType
    Name: ResourceServerNameType
    Scopes: Optional[ResourceServerScopeListType]


class ResourceServerType(TypedDict, total=False):
    """The details of a resource server configuration and associated custom
    scopes in a user pool.

    This data type is a request parameter of
    `CreateResourceServer <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateResourceServer.html>`__
    and a response parameter of
    `DescribeResourceServer <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeResourceServer.html>`__.
    """

    UserPoolId: Optional[UserPoolIdType]
    Identifier: Optional[ResourceServerIdentifierType]
    Name: Optional[ResourceServerNameType]
    Scopes: Optional[ResourceServerScopeListType]


class CreateResourceServerResponse(TypedDict, total=False):
    ResourceServer: ResourceServerType


class CreateUserImportJobRequest(ServiceRequest):
    """Represents the request to create the user import job."""

    JobName: UserImportJobNameType
    UserPoolId: UserPoolIdType
    CloudWatchLogsRoleArn: ArnType


LongType = int


class UserImportJobType(TypedDict, total=False):
    """A user import job in a user pool. Describes the status of user import
    with a CSV file. For more information, see `Importing users into user
    pools from a CSV
    file <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-using-import-tool.html>`__.

    This data type is a request parameter of
    `CreateUserImportJob <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserImportJob.html>`__,
    `DescribeUserImportJob <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserImportJob.html>`__,
    `ListUserImportJobs <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ListUserImportJobs.html>`__,
    `StartUserImportJob <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_StartUserImportJob.html>`__,
    and
    `StopUserImportJob <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_StopUserImportJob.html>`__.
    """

    JobName: Optional[UserImportJobNameType]
    JobId: Optional[UserImportJobIdType]
    UserPoolId: Optional[UserPoolIdType]
    PreSignedUrl: Optional[PreSignedUrlType]
    CreationDate: Optional[DateType]
    StartDate: Optional[DateType]
    CompletionDate: Optional[DateType]
    Status: Optional[UserImportJobStatusType]
    CloudWatchLogsRoleArn: Optional[ArnType]
    ImportedUsers: Optional[LongType]
    SkippedUsers: Optional[LongType]
    FailedUsers: Optional[LongType]
    CompletionMessage: Optional[CompletionMessageType]


class CreateUserImportJobResponse(TypedDict, total=False):
    """Represents the response from the server to the request to create the
    user import job.
    """

    UserImportJob: Optional[UserImportJobType]


ScopeListType = List[ScopeType]
OAuthFlowsType = List[OAuthFlowType]
LogoutURLsListType = List[RedirectUrlType]
SupportedIdentityProvidersListType = List[ProviderNameType]
ExplicitAuthFlowsListType = List[ExplicitAuthFlowsType]


class TokenValidityUnitsType(TypedDict, total=False):
    """The time units that, with ``IdTokenValidity``, ``AccessTokenValidity``,
    and ``RefreshTokenValidity``, set and display the duration of ID,
    access, and refresh tokens for an app client. You can assign a separate
    token validity unit to each type of token.

    This data type is a request parameter of
    `CreateUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPoolClient.html>`__
    and
    `UpdateUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPoolClient.html>`__,
    and a response parameter of
    `DescribeUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPoolClient.html>`__.
    """

    AccessToken: Optional[TimeUnitsType]
    IdToken: Optional[TimeUnitsType]
    RefreshToken: Optional[TimeUnitsType]


class CreateUserPoolClientRequest(ServiceRequest):
    """Represents the request to create a user pool client."""

    UserPoolId: UserPoolIdType
    ClientName: ClientNameType
    GenerateSecret: Optional[GenerateSecret]
    RefreshTokenValidity: Optional[RefreshTokenValidityType]
    AccessTokenValidity: Optional[AccessTokenValidityType]
    IdTokenValidity: Optional[IdTokenValidityType]
    TokenValidityUnits: Optional[TokenValidityUnitsType]
    ReadAttributes: Optional[ClientPermissionListType]
    WriteAttributes: Optional[ClientPermissionListType]
    ExplicitAuthFlows: Optional[ExplicitAuthFlowsListType]
    SupportedIdentityProviders: Optional[SupportedIdentityProvidersListType]
    CallbackURLs: Optional[CallbackURLsListType]
    LogoutURLs: Optional[LogoutURLsListType]
    DefaultRedirectURI: Optional[RedirectUrlType]
    AllowedOAuthFlows: Optional[OAuthFlowsType]
    AllowedOAuthScopes: Optional[ScopeListType]
    AllowedOAuthFlowsUserPoolClient: Optional[BooleanType]
    AnalyticsConfiguration: Optional[AnalyticsConfigurationType]
    PreventUserExistenceErrors: Optional[PreventUserExistenceErrorTypes]
    EnableTokenRevocation: Optional[WrappedBooleanType]
    EnablePropagateAdditionalUserContextData: Optional[WrappedBooleanType]
    AuthSessionValidity: Optional[AuthSessionValidityType]


class UserPoolClientType(TypedDict, total=False):
    """The configuration of a user pool client.

    This data type is a request parameter of
    `CreateUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPoolClient.html>`__
    and
    `UpdateUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPoolClient.html>`__,
    and a response parameter of
    `DescribeUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPoolClient.html>`__.
    """

    UserPoolId: Optional[UserPoolIdType]
    ClientName: Optional[ClientNameType]
    ClientId: Optional[ClientIdType]
    ClientSecret: Optional[ClientSecretType]
    LastModifiedDate: Optional[DateType]
    CreationDate: Optional[DateType]
    RefreshTokenValidity: Optional[RefreshTokenValidityType]
    AccessTokenValidity: Optional[AccessTokenValidityType]
    IdTokenValidity: Optional[IdTokenValidityType]
    TokenValidityUnits: Optional[TokenValidityUnitsType]
    ReadAttributes: Optional[ClientPermissionListType]
    WriteAttributes: Optional[ClientPermissionListType]
    ExplicitAuthFlows: Optional[ExplicitAuthFlowsListType]
    SupportedIdentityProviders: Optional[SupportedIdentityProvidersListType]
    CallbackURLs: Optional[CallbackURLsListType]
    LogoutURLs: Optional[LogoutURLsListType]
    DefaultRedirectURI: Optional[RedirectUrlType]
    AllowedOAuthFlows: Optional[OAuthFlowsType]
    AllowedOAuthScopes: Optional[ScopeListType]
    AllowedOAuthFlowsUserPoolClient: Optional[BooleanType]
    AnalyticsConfiguration: Optional[AnalyticsConfigurationType]
    PreventUserExistenceErrors: Optional[PreventUserExistenceErrorTypes]
    EnableTokenRevocation: Optional[WrappedBooleanType]
    EnablePropagateAdditionalUserContextData: Optional[WrappedBooleanType]
    AuthSessionValidity: Optional[AuthSessionValidityType]


class CreateUserPoolClientResponse(TypedDict, total=False):
    """Represents the response from the server to create a user pool client."""

    UserPoolClient: Optional[UserPoolClientType]


class CustomDomainConfigType(TypedDict, total=False):
    """The configuration for a hosted UI custom domain.

    This data type is a request parameter of
    `CreateUserPoolDomain <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPoolDomain.html>`__
    and
    `UpdateUserPoolDomain <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPoolDomain.html>`__.
    """

    CertificateArn: ArnType


class CreateUserPoolDomainRequest(ServiceRequest):
    Domain: DomainType
    UserPoolId: UserPoolIdType
    ManagedLoginVersion: Optional[WrappedIntegerType]
    CustomDomainConfig: Optional[CustomDomainConfigType]


class CreateUserPoolDomainResponse(TypedDict, total=False):
    ManagedLoginVersion: Optional[WrappedIntegerType]
    CloudFrontDomain: Optional[DomainType]


class UsernameConfigurationType(TypedDict, total=False):
    """The configuration of a user pool for username case sensitivity.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    CaseSensitive: WrappedBooleanType


class UserPoolAddOnsType(TypedDict, total=False):
    """User pool add-ons. Contains settings for activation of advanced security
    features. To log user security information but take no action, set to
    ``AUDIT``. To configure automatic security responses to risky traffic to
    your user pool, set to ``ENFORCED``.

    For more information, see `Adding advanced security to a user
    pool <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-advanced-security.html>`__.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    AdvancedSecurityMode: AdvancedSecurityModeType
    AdvancedSecurityAdditionalFlows: Optional[AdvancedSecurityAdditionalFlowsType]


SchemaAttributesListType = List[SchemaAttributeType]
UserPoolTagsType = Dict[TagKeysType, TagValueType]


class SmsConfigurationType(TypedDict, total=False):
    """User pool configuration for delivery of SMS messages with Amazon Simple
    Notification Service. To send SMS messages with Amazon SNS in the Amazon
    Web Services Region that you want, the Amazon Cognito user pool uses an
    Identity and Access Management (IAM) role in your Amazon Web Services
    account.

    This data type is a request parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__,
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and
    `SetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserPoolMfaConfig.html>`__,
    and a response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__,
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and
    `GetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetUserPoolMfaConfig.html>`__.
    """

    SnsCallerArn: ArnType
    ExternalId: Optional[StringType]
    SnsRegion: Optional[RegionCodeType]


class EmailConfigurationType(TypedDict, total=False):
    """The email configuration of your user pool. The email configuration type
    sets your preferred sending method, Amazon Web Services Region, and
    sender for messages from your user pool.

    Amazon Cognito can send email messages with Amazon Simple Email Service
    resources in the Amazon Web Services Region where you created your user
    pool, and in alternate Regions in some cases. For more information on
    the supported Regions, see `Email settings for Amazon Cognito user
    pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-email.html>`__.

    This data type is a request parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__,
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and
    `SetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserPoolMfaConfig.html>`__,
    and a response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__,
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and
    `GetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetUserPoolMfaConfig.html>`__.
    """

    SourceArn: Optional[ArnType]
    ReplyToEmailAddress: Optional[EmailAddressType]
    EmailSendingAccount: Optional[EmailSendingAccountType]
    From: Optional[StringType]
    ConfigurationSet: Optional[SESConfigurationSet]


class DeviceConfigurationType(TypedDict, total=False):
    """The device-remembering configuration for a user pool. A
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__
    request returns a null value for this object when the user pool isn't
    configured to remember devices. When device remembering is active, you
    can remember a user's device with a
    `ConfirmDevice <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ConfirmDevice.html>`__
    API request. Additionally. when the property
    ``DeviceOnlyRememberedOnUserPrompt`` is ``true``, you must follow
    ``ConfirmDevice`` with an
    `UpdateDeviceStatus <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateDeviceStatus.html>`__
    API request that sets the user's device to ``remembered`` or
    ``not_remembered``.

    To sign in with a remembered device, include ``DEVICE_KEY`` in the
    authentication parameters in your user's
    `InitiateAuth <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_InitiateAuth.html>`__
    request. If your app doesn't include a ``DEVICE_KEY`` parameter, the
    `response <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_InitiateAuth.html#API_InitiateAuth_ResponseSyntax>`__
    from Amazon Cognito includes newly-generated ``DEVICE_KEY`` and
    ``DEVICE_GROUP_KEY`` values under ``NewDeviceMetadata``. Store these
    values to use in future device-authentication requests.

    When you provide a value for any property of ``DeviceConfiguration``,
    you activate the device remembering for the user pool.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    ChallengeRequiredOnNewDevice: Optional[BooleanType]
    DeviceOnlyRememberedOnUserPrompt: Optional[BooleanType]


class UserAttributeUpdateSettingsType(TypedDict, total=False):
    """The settings for updates to user attributes. These settings include the
    property ``AttributesRequireVerificationBeforeUpdate``, a user-pool
    setting that tells Amazon Cognito how to handle changes to the value of
    your users' email address and phone number attributes. For more
    information, see `Verifying updates to email addresses and phone
    numbers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-email-phone-verification.html#user-pool-settings-verifications-verify-attribute-updates>`__.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    AttributesRequireVerificationBeforeUpdate: Optional[
        AttributesRequireVerificationBeforeUpdateType
    ]


class VerificationMessageTemplateType(TypedDict, total=False):
    """The template for the verification message that your user pool delivers
    to users who set an email address or phone number attribute.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    SmsMessage: Optional[SmsVerificationMessageType]
    EmailMessage: Optional[EmailVerificationMessageType]
    EmailSubject: Optional[EmailVerificationSubjectType]
    EmailMessageByLink: Optional[EmailVerificationMessageByLinkType]
    EmailSubjectByLink: Optional[EmailVerificationSubjectByLinkType]
    DefaultEmailOption: Optional[DefaultEmailOptionType]


UsernameAttributesListType = List[UsernameAttributeType]
VerifiedAttributesListType = List[VerifiedAttributeType]


class CustomEmailLambdaVersionConfigType(TypedDict, total=False):
    """The properties of a custom email sender Lambda trigger.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    LambdaVersion: CustomEmailSenderLambdaVersionType
    LambdaArn: ArnType


class CustomSMSLambdaVersionConfigType(TypedDict, total=False):
    """The properties of a custom SMS sender Lambda trigger.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    LambdaVersion: CustomSMSSenderLambdaVersionType
    LambdaArn: ArnType


class PreTokenGenerationVersionConfigType(TypedDict, total=False):
    """The properties of a pre token generation Lambda trigger.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    LambdaVersion: PreTokenGenerationLambdaVersionType
    LambdaArn: ArnType


class LambdaConfigType(TypedDict, total=False):
    """A collection of user pool Lambda triggers. Amazon Cognito invokes
    triggers at several possible stages of user pool operations. Triggers
    can modify the outcome of the operations that invoked them.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    PreSignUp: Optional[ArnType]
    CustomMessage: Optional[ArnType]
    PostConfirmation: Optional[ArnType]
    PreAuthentication: Optional[ArnType]
    PostAuthentication: Optional[ArnType]
    DefineAuthChallenge: Optional[ArnType]
    CreateAuthChallenge: Optional[ArnType]
    VerifyAuthChallengeResponse: Optional[ArnType]
    PreTokenGeneration: Optional[ArnType]
    UserMigration: Optional[ArnType]
    PreTokenGenerationConfig: Optional[PreTokenGenerationVersionConfigType]
    CustomSMSSender: Optional[CustomSMSLambdaVersionConfigType]
    CustomEmailSender: Optional[CustomEmailLambdaVersionConfigType]
    KMSKeyID: Optional[ArnType]


class SignInPolicyType(TypedDict, total=False):
    """The policy for allowed types of authentication in a user pool.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    AllowedFirstAuthFactors: Optional[AllowedFirstAuthFactorsListType]


class PasswordPolicyType(TypedDict, total=False):
    """The password policy settings for a user pool, including complexity,
    history, and length requirements.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    MinimumLength: Optional[PasswordPolicyMinLengthType]
    RequireUppercase: Optional[BooleanType]
    RequireLowercase: Optional[BooleanType]
    RequireNumbers: Optional[BooleanType]
    RequireSymbols: Optional[BooleanType]
    PasswordHistorySize: Optional[PasswordHistorySizeType]
    TemporaryPasswordValidityDays: Optional[TemporaryPasswordValidityDaysType]


class UserPoolPolicyType(TypedDict, total=False):
    """A list of user pool policies. Contains the policy that sets
    password-complexity requirements.

    This data type is a request and response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__
    and
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and a response parameter of
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    PasswordPolicy: Optional[PasswordPolicyType]
    SignInPolicy: Optional[SignInPolicyType]


class CreateUserPoolRequest(ServiceRequest):
    """Represents the request to create a user pool."""

    PoolName: UserPoolNameType
    Policies: Optional[UserPoolPolicyType]
    DeletionProtection: Optional[DeletionProtectionType]
    LambdaConfig: Optional[LambdaConfigType]
    AutoVerifiedAttributes: Optional[VerifiedAttributesListType]
    AliasAttributes: Optional[AliasAttributesListType]
    UsernameAttributes: Optional[UsernameAttributesListType]
    SmsVerificationMessage: Optional[SmsVerificationMessageType]
    EmailVerificationMessage: Optional[EmailVerificationMessageType]
    EmailVerificationSubject: Optional[EmailVerificationSubjectType]
    VerificationMessageTemplate: Optional[VerificationMessageTemplateType]
    SmsAuthenticationMessage: Optional[SmsVerificationMessageType]
    MfaConfiguration: Optional[UserPoolMfaType]
    UserAttributeUpdateSettings: Optional[UserAttributeUpdateSettingsType]
    DeviceConfiguration: Optional[DeviceConfigurationType]
    EmailConfiguration: Optional[EmailConfigurationType]
    SmsConfiguration: Optional[SmsConfigurationType]
    UserPoolTags: Optional[UserPoolTagsType]
    AdminCreateUserConfig: Optional[AdminCreateUserConfigType]
    Schema: Optional[SchemaAttributesListType]
    UserPoolAddOns: Optional[UserPoolAddOnsType]
    UsernameConfiguration: Optional[UsernameConfigurationType]
    AccountRecoverySetting: Optional[AccountRecoverySettingType]
    UserPoolTier: Optional[UserPoolTierType]


class UserPoolType(TypedDict, total=False):
    """The configuration of a user pool.

    This data type is a response parameter of
    `CreateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CreateUserPool.html>`__,
    `UpdateUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html>`__,
    and
    `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.
    """

    Id: Optional[UserPoolIdType]
    Name: Optional[UserPoolNameType]
    Policies: Optional[UserPoolPolicyType]
    DeletionProtection: Optional[DeletionProtectionType]
    LambdaConfig: Optional[LambdaConfigType]
    Status: Optional[StatusType]
    LastModifiedDate: Optional[DateType]
    CreationDate: Optional[DateType]
    SchemaAttributes: Optional[SchemaAttributesListType]
    AutoVerifiedAttributes: Optional[VerifiedAttributesListType]
    AliasAttributes: Optional[AliasAttributesListType]
    UsernameAttributes: Optional[UsernameAttributesListType]
    SmsVerificationMessage: Optional[SmsVerificationMessageType]
    EmailVerificationMessage: Optional[EmailVerificationMessageType]
    EmailVerificationSubject: Optional[EmailVerificationSubjectType]
    VerificationMessageTemplate: Optional[VerificationMessageTemplateType]
    SmsAuthenticationMessage: Optional[SmsVerificationMessageType]
    UserAttributeUpdateSettings: Optional[UserAttributeUpdateSettingsType]
    MfaConfiguration: Optional[UserPoolMfaType]
    DeviceConfiguration: Optional[DeviceConfigurationType]
    EstimatedNumberOfUsers: Optional[IntegerType]
    EmailConfiguration: Optional[EmailConfigurationType]
    SmsConfiguration: Optional[SmsConfigurationType]
    UserPoolTags: Optional[UserPoolTagsType]
    SmsConfigurationFailure: Optional[StringType]
    EmailConfigurationFailure: Optional[StringType]
    Domain: Optional[DomainType]
    CustomDomain: Optional[DomainType]
    AdminCreateUserConfig: Optional[AdminCreateUserConfigType]
    UserPoolAddOns: Optional[UserPoolAddOnsType]
    UsernameConfiguration: Optional[UsernameConfigurationType]
    Arn: Optional[ArnType]
    AccountRecoverySetting: Optional[AccountRecoverySettingType]
    UserPoolTier: Optional[UserPoolTierType]


class CreateUserPoolResponse(TypedDict, total=False):
    """Represents the response from the server for the request to create a user
    pool.
    """

    UserPool: Optional[UserPoolType]


class DeleteGroupRequest(ServiceRequest):
    GroupName: GroupNameType
    UserPoolId: UserPoolIdType


class DeleteIdentityProviderRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ProviderName: ProviderNameType


class DeleteManagedLoginBrandingRequest(ServiceRequest):
    ManagedLoginBrandingId: ManagedLoginBrandingIdType
    UserPoolId: UserPoolIdType


class DeleteResourceServerRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Identifier: ResourceServerIdentifierType


class DeleteUserAttributesRequest(ServiceRequest):
    """Represents the request to delete user attributes."""

    UserAttributeNames: AttributeNameListType
    AccessToken: TokenModelType


class DeleteUserAttributesResponse(TypedDict, total=False):
    """Represents the response from the server to delete user attributes."""

    pass


class DeleteUserPoolClientRequest(ServiceRequest):
    """Represents the request to delete a user pool client."""

    UserPoolId: UserPoolIdType
    ClientId: ClientIdType


class DeleteUserPoolDomainRequest(ServiceRequest):
    Domain: DomainType
    UserPoolId: UserPoolIdType


class DeleteUserPoolDomainResponse(TypedDict, total=False):
    pass


class DeleteUserPoolRequest(ServiceRequest):
    """Represents the request to delete a user pool."""

    UserPoolId: UserPoolIdType


class DeleteUserRequest(ServiceRequest):
    """Represents the request to delete a user."""

    AccessToken: TokenModelType


class DeleteWebAuthnCredentialRequest(ServiceRequest):
    AccessToken: TokenModelType
    CredentialId: StringType


class DeleteWebAuthnCredentialResponse(TypedDict, total=False):
    pass


class DescribeIdentityProviderRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ProviderName: ProviderNameType


class DescribeIdentityProviderResponse(TypedDict, total=False):
    IdentityProvider: IdentityProviderType


class DescribeManagedLoginBrandingByClientRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ClientId: ClientIdType
    ReturnMergedResources: Optional[BooleanType]


class DescribeManagedLoginBrandingByClientResponse(TypedDict, total=False):
    ManagedLoginBranding: Optional[ManagedLoginBrandingType]


class DescribeManagedLoginBrandingRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ManagedLoginBrandingId: ManagedLoginBrandingIdType
    ReturnMergedResources: Optional[BooleanType]


class DescribeManagedLoginBrandingResponse(TypedDict, total=False):
    ManagedLoginBranding: Optional[ManagedLoginBrandingType]


class DescribeResourceServerRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Identifier: ResourceServerIdentifierType


class DescribeResourceServerResponse(TypedDict, total=False):
    ResourceServer: ResourceServerType


class DescribeRiskConfigurationRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ClientId: Optional[ClientIdType]


SkippedIPRangeListType = List[StringType]


class RiskExceptionConfigurationType(TypedDict, total=False):
    """Exceptions to the risk evaluation configuration, including always-allow
    and always-block IP address ranges.

    This data type is a request parameter of
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__
    and a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__.
    """

    BlockedIPRangeList: Optional[BlockedIPRangeListType]
    SkippedIPRangeList: Optional[SkippedIPRangeListType]


class RiskConfigurationType(TypedDict, total=False):
    """The settings of risk configuration for threat protection with advanced
    security features in a user pool.

    This data type is a response parameter of
    `DescribeRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeRiskConfiguration.html>`__
    and
    `SetRiskConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetRiskConfiguration.html>`__.
    """

    UserPoolId: Optional[UserPoolIdType]
    ClientId: Optional[ClientIdType]
    CompromisedCredentialsRiskConfiguration: Optional[CompromisedCredentialsRiskConfigurationType]
    AccountTakeoverRiskConfiguration: Optional[AccountTakeoverRiskConfigurationType]
    RiskExceptionConfiguration: Optional[RiskExceptionConfigurationType]
    LastModifiedDate: Optional[DateType]


class DescribeRiskConfigurationResponse(TypedDict, total=False):
    RiskConfiguration: RiskConfigurationType


class DescribeUserImportJobRequest(ServiceRequest):
    """Represents the request to describe the user import job."""

    UserPoolId: UserPoolIdType
    JobId: UserImportJobIdType


class DescribeUserImportJobResponse(TypedDict, total=False):
    """Represents the response from the server to the request to describe the
    user import job.
    """

    UserImportJob: Optional[UserImportJobType]


class DescribeUserPoolClientRequest(ServiceRequest):
    """Represents the request to describe a user pool client."""

    UserPoolId: UserPoolIdType
    ClientId: ClientIdType


class DescribeUserPoolClientResponse(TypedDict, total=False):
    """Represents the response from the server from a request to describe the
    user pool client.
    """

    UserPoolClient: Optional[UserPoolClientType]


class DescribeUserPoolDomainRequest(ServiceRequest):
    Domain: DomainType


class DomainDescriptionType(TypedDict, total=False):
    """A container for information about the user pool domain associated with
    the hosted UI and OAuth endpoints.

    This data type is a response parameter of
    `DescribeUserPoolDomain <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPoolDomain.html>`__.
    """

    UserPoolId: Optional[UserPoolIdType]
    AWSAccountId: Optional[AWSAccountIdType]
    Domain: Optional[DomainType]
    S3Bucket: Optional[S3BucketType]
    CloudFrontDistribution: Optional[StringType]
    Version: Optional[DomainVersionType]
    Status: Optional[DomainStatusType]
    CustomDomainConfig: Optional[CustomDomainConfigType]
    ManagedLoginVersion: Optional[WrappedIntegerType]


class DescribeUserPoolDomainResponse(TypedDict, total=False):
    DomainDescription: Optional[DomainDescriptionType]


class DescribeUserPoolRequest(ServiceRequest):
    """Represents the request to describe the user pool."""

    UserPoolId: UserPoolIdType


class DescribeUserPoolResponse(TypedDict, total=False):
    """Represents the response to describe the user pool."""

    UserPool: Optional[UserPoolType]


class EmailMfaConfigType(TypedDict, total=False):
    """Sets or shows user pool email message configuration for MFA. Includes
    the subject and body of the email message template for MFA messages. To
    activate this setting, `advanced security
    features <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-advanced-security.html>`__
    must be active in your user pool.

    This data type is a request parameter of
    `SetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserPoolMfaConfig.html>`__
    and a response parameter of
    `GetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetUserPoolMfaConfig.html>`__.
    """

    Message: Optional[EmailMfaMessageType]
    Subject: Optional[EmailMfaSubjectType]


class FirehoseConfigurationType(TypedDict, total=False):
    """Configuration for the Amazon Data Firehose stream destination of user
    activity log export with advanced security features.
    """

    StreamArn: Optional[ArnType]


class ForgetDeviceRequest(ServiceRequest):
    """Represents the request to forget the device."""

    AccessToken: Optional[TokenModelType]
    DeviceKey: DeviceKeyType


class ForgotPasswordRequest(ServiceRequest):
    """Represents the request to reset a user's password."""

    ClientId: ClientIdType
    SecretHash: Optional[SecretHashType]
    UserContextData: Optional[UserContextDataType]
    Username: UsernameType
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    ClientMetadata: Optional[ClientMetadataType]


class ForgotPasswordResponse(TypedDict, total=False):
    """The response from Amazon Cognito to a request to reset a password."""

    CodeDeliveryDetails: Optional[CodeDeliveryDetailsType]


class GetCSVHeaderRequest(ServiceRequest):
    """Represents the request to get the header information of the CSV file for
    the user import job.
    """

    UserPoolId: UserPoolIdType


ListOfStringTypes = List[StringType]


class GetCSVHeaderResponse(TypedDict, total=False):
    """Represents the response from the server to the request to get the header
    information of the CSV file for the user import job.
    """

    UserPoolId: Optional[UserPoolIdType]
    CSVHeader: Optional[ListOfStringTypes]


class GetDeviceRequest(ServiceRequest):
    """Represents the request to get the device."""

    DeviceKey: DeviceKeyType
    AccessToken: Optional[TokenModelType]


class GetDeviceResponse(TypedDict, total=False):
    """Gets the device response."""

    Device: DeviceType


class GetGroupRequest(ServiceRequest):
    GroupName: GroupNameType
    UserPoolId: UserPoolIdType


class GetGroupResponse(TypedDict, total=False):
    Group: Optional[GroupType]


class GetIdentityProviderByIdentifierRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    IdpIdentifier: IdpIdentifierType


class GetIdentityProviderByIdentifierResponse(TypedDict, total=False):
    IdentityProvider: IdentityProviderType


class GetLogDeliveryConfigurationRequest(ServiceRequest):
    UserPoolId: UserPoolIdType


class S3ConfigurationType(TypedDict, total=False):
    """Configuration for the Amazon S3 bucket destination of user activity log
    export with advanced security features.
    """

    BucketArn: Optional[S3ArnType]


class LogConfigurationType(TypedDict, total=False):
    """The configuration of user event logs to an external Amazon Web Services
    service like Amazon Data Firehose, Amazon S3, or Amazon CloudWatch Logs.

    This data type is a request parameter of
    `SetLogDeliveryConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetLogDeliveryConfiguration.html>`__
    and a response parameter of
    `GetLogDeliveryConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetLogDeliveryConfiguration.html>`__.
    """

    LogLevel: LogLevel
    EventSource: EventSourceName
    CloudWatchLogsConfiguration: Optional[CloudWatchLogsConfigurationType]
    S3Configuration: Optional[S3ConfigurationType]
    FirehoseConfiguration: Optional[FirehoseConfigurationType]


LogConfigurationListType = List[LogConfigurationType]


class LogDeliveryConfigurationType(TypedDict, total=False):
    """The logging parameters of a user pool, as returned in the response to a
    `GetLogDeliveryConfiguration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetLogDeliveryConfiguration.html>`__
    request.
    """

    UserPoolId: UserPoolIdType
    LogConfigurations: LogConfigurationListType


class GetLogDeliveryConfigurationResponse(TypedDict, total=False):
    LogDeliveryConfiguration: Optional[LogDeliveryConfigurationType]


class GetSigningCertificateRequest(ServiceRequest):
    """Request to get a signing certificate from Amazon Cognito."""

    UserPoolId: UserPoolIdType


class GetSigningCertificateResponse(TypedDict, total=False):
    """Response from Amazon Cognito for a signing certificate request."""

    Certificate: Optional[StringType]


class GetUICustomizationRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ClientId: Optional[ClientIdType]


class UICustomizationType(TypedDict, total=False):
    """A container for the UI customization information for the hosted UI in a
    user pool.

    This data type is a response parameter of
    `GetUICustomization <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPoolClient.html>`__.
    """

    UserPoolId: Optional[UserPoolIdType]
    ClientId: Optional[ClientIdType]
    ImageUrl: Optional[ImageUrlType]
    CSS: Optional[CSSType]
    CSSVersion: Optional[CSSVersionType]
    LastModifiedDate: Optional[DateType]
    CreationDate: Optional[DateType]


class GetUICustomizationResponse(TypedDict, total=False):
    UICustomization: UICustomizationType


class GetUserAttributeVerificationCodeRequest(ServiceRequest):
    """Represents the request to get user attribute verification."""

    AccessToken: TokenModelType
    AttributeName: AttributeNameType
    ClientMetadata: Optional[ClientMetadataType]


class GetUserAttributeVerificationCodeResponse(TypedDict, total=False):
    """The verification code response returned by the server response to get
    the user attribute verification code.
    """

    CodeDeliveryDetails: Optional[CodeDeliveryDetailsType]


class GetUserAuthFactorsRequest(ServiceRequest):
    AccessToken: TokenModelType


class GetUserAuthFactorsResponse(TypedDict, total=False):
    Username: UsernameType
    PreferredMfaSetting: Optional[StringType]
    UserMFASettingList: Optional[UserMFASettingListType]
    ConfiguredUserAuthFactors: Optional[ConfiguredUserAuthFactorsListType]


class GetUserPoolMfaConfigRequest(ServiceRequest):
    UserPoolId: UserPoolIdType


class WebAuthnConfigurationType(TypedDict, total=False):
    """Settings for multi-factor authentication (MFA) with passkey, or
    webauthN, biometric and security-key devices in a user pool. Configures
    the following:

    -  Configuration at the user-pool level for whether you want to require
       passkey configuration as an MFA factor, or include it as a choice.

    -  The user pool relying-party ID. This is the user pool domain that
       user's passkey providers should trust as a receiver of passkey
       authentication.

    -  The providers that you want to allow as origins for passkey
       authentication.

    This data type is a request parameter of
    `SetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserPoolMfaConfig.html>`__
    and a response parameter of
    `GetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetUserPoolMfaConfig.html>`__.
    """

    RelyingPartyId: Optional[RelyingPartyIdType]
    UserVerification: Optional[UserVerificationType]


class SoftwareTokenMfaConfigType(TypedDict, total=False):
    """Settings for time-based one-time password (TOTP) multi-factor
    authentication (MFA) in a user pool. Enables and disables availability
    of this feature.

    This data type is a request parameter of
    `SetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserPoolMfaConfig.html>`__
    and a response parameter of
    `GetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetUserPoolMfaConfig.html>`__.
    """

    Enabled: Optional[BooleanType]


class SmsMfaConfigType(TypedDict, total=False):
    """The configuration of multi-factor authentication (MFA) with SMS messages
    in a user pool.

    This data type is a request parameter of
    `SetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserPoolMfaConfig.html>`__
    and a response parameter of
    `GetUserPoolMfaConfig <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetUserPoolMfaConfig.html>`__.
    """

    SmsAuthenticationMessage: Optional[SmsVerificationMessageType]
    SmsConfiguration: Optional[SmsConfigurationType]


class GetUserPoolMfaConfigResponse(TypedDict, total=False):
    SmsMfaConfiguration: Optional[SmsMfaConfigType]
    SoftwareTokenMfaConfiguration: Optional[SoftwareTokenMfaConfigType]
    EmailMfaConfiguration: Optional[EmailMfaConfigType]
    MfaConfiguration: Optional[UserPoolMfaType]
    WebAuthnConfiguration: Optional[WebAuthnConfigurationType]


class GetUserRequest(ServiceRequest):
    """Represents the request to get information about the user."""

    AccessToken: TokenModelType


class GetUserResponse(TypedDict, total=False):
    """Represents the response from the server from the request to get
    information about the user.
    """

    Username: UsernameType
    UserAttributes: AttributeListType
    MFAOptions: Optional[MFAOptionListType]
    PreferredMfaSetting: Optional[StringType]
    UserMFASettingList: Optional[UserMFASettingListType]


class GlobalSignOutRequest(ServiceRequest):
    """Represents the request to sign out all devices."""

    AccessToken: TokenModelType


class GlobalSignOutResponse(TypedDict, total=False):
    """The response to the request to sign out all devices."""

    pass


ImageFileType = bytes


class InitiateAuthRequest(ServiceRequest):
    """Initiates the authentication request."""

    AuthFlow: AuthFlowType
    AuthParameters: Optional[AuthParametersType]
    ClientMetadata: Optional[ClientMetadataType]
    ClientId: ClientIdType
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    UserContextData: Optional[UserContextDataType]
    Session: Optional[SessionType]


class InitiateAuthResponse(TypedDict, total=False):
    """Initiates the authentication response."""

    ChallengeName: Optional[ChallengeNameType]
    Session: Optional[SessionType]
    ChallengeParameters: Optional[ChallengeParametersType]
    AuthenticationResult: Optional[AuthenticationResultType]
    AvailableChallenges: Optional[AvailableChallengeListType]


class ListDevicesRequest(ServiceRequest):
    """Represents the request to list the devices."""

    AccessToken: TokenModelType
    Limit: Optional[QueryLimitType]
    PaginationToken: Optional[SearchPaginationTokenType]


class ListDevicesResponse(TypedDict, total=False):
    """Represents the response to list devices."""

    Devices: Optional[DeviceListType]
    PaginationToken: Optional[SearchPaginationTokenType]


class ListGroupsRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Limit: Optional[QueryLimitType]
    NextToken: Optional[PaginationKey]


class ListGroupsResponse(TypedDict, total=False):
    Groups: Optional[GroupListType]
    NextToken: Optional[PaginationKey]


class ListIdentityProvidersRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    MaxResults: Optional[ListProvidersLimitType]
    NextToken: Optional[PaginationKeyType]


class ProviderDescription(TypedDict, total=False):
    """The details of a user pool identity provider (IdP), including name and
    type.

    This data type is a response parameter of
    `ListIdentityProviders <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ListIdentityProviders.html>`__.
    """

    ProviderName: Optional[ProviderNameType]
    ProviderType: Optional[IdentityProviderTypeType]
    LastModifiedDate: Optional[DateType]
    CreationDate: Optional[DateType]


ProvidersListType = List[ProviderDescription]


class ListIdentityProvidersResponse(TypedDict, total=False):
    Providers: ProvidersListType
    NextToken: Optional[PaginationKeyType]


class ListResourceServersRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    MaxResults: Optional[ListResourceServersLimitType]
    NextToken: Optional[PaginationKeyType]


ResourceServersListType = List[ResourceServerType]


class ListResourceServersResponse(TypedDict, total=False):
    ResourceServers: ResourceServersListType
    NextToken: Optional[PaginationKeyType]


class ListTagsForResourceRequest(ServiceRequest):
    ResourceArn: ArnType


class ListTagsForResourceResponse(TypedDict, total=False):
    Tags: Optional[UserPoolTagsType]


class ListUserImportJobsRequest(ServiceRequest):
    """Represents the request to list the user import jobs."""

    UserPoolId: UserPoolIdType
    MaxResults: PoolQueryLimitType
    PaginationToken: Optional[PaginationKeyType]


UserImportJobsListType = List[UserImportJobType]


class ListUserImportJobsResponse(TypedDict, total=False):
    """Represents the response from the server to the request to list the user
    import jobs.
    """

    UserImportJobs: Optional[UserImportJobsListType]
    PaginationToken: Optional[PaginationKeyType]


class ListUserPoolClientsRequest(ServiceRequest):
    """Represents the request to list the user pool clients."""

    UserPoolId: UserPoolIdType
    MaxResults: Optional[QueryLimit]
    NextToken: Optional[PaginationKey]


class UserPoolClientDescription(TypedDict, total=False):
    """A short description of a user pool app client.

    This data type is a response parameter of
    `ListUserPoolClients <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ListUserPoolClients.html>`__.
    """

    ClientId: Optional[ClientIdType]
    UserPoolId: Optional[UserPoolIdType]
    ClientName: Optional[ClientNameType]


UserPoolClientListType = List[UserPoolClientDescription]


class ListUserPoolClientsResponse(TypedDict, total=False):
    """Represents the response from the server that lists user pool clients."""

    UserPoolClients: Optional[UserPoolClientListType]
    NextToken: Optional[PaginationKey]


class ListUserPoolsRequest(ServiceRequest):
    """Represents the request to list user pools."""

    NextToken: Optional[PaginationKeyType]
    MaxResults: PoolQueryLimitType


class UserPoolDescriptionType(TypedDict, total=False):
    """A short description of a user pool.

    This data type is a response parameter of
    `ListUserPools <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ListUserPools.html>`__.
    """

    Id: Optional[UserPoolIdType]
    Name: Optional[UserPoolNameType]
    LambdaConfig: Optional[LambdaConfigType]
    Status: Optional[StatusType]
    LastModifiedDate: Optional[DateType]
    CreationDate: Optional[DateType]


UserPoolListType = List[UserPoolDescriptionType]


class ListUserPoolsResponse(TypedDict, total=False):
    """Represents the response to list user pools."""

    UserPools: Optional[UserPoolListType]
    NextToken: Optional[PaginationKeyType]


class ListUsersInGroupRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    GroupName: GroupNameType
    Limit: Optional[QueryLimitType]
    NextToken: Optional[PaginationKey]


UsersListType = List[UserType]


class ListUsersInGroupResponse(TypedDict, total=False):
    Users: Optional[UsersListType]
    NextToken: Optional[PaginationKey]


SearchedAttributeNamesListType = List[AttributeNameType]


class ListUsersRequest(ServiceRequest):
    """Represents the request to list users."""

    UserPoolId: UserPoolIdType
    AttributesToGet: Optional[SearchedAttributeNamesListType]
    Limit: Optional[QueryLimitType]
    PaginationToken: Optional[SearchPaginationTokenType]
    Filter: Optional[UserFilterType]


class ListUsersResponse(TypedDict, total=False):
    """The response from the request to list users."""

    Users: Optional[UsersListType]
    PaginationToken: Optional[SearchPaginationTokenType]


class ListWebAuthnCredentialsRequest(ServiceRequest):
    AccessToken: TokenModelType
    NextToken: Optional[PaginationKey]
    MaxResults: Optional[WebAuthnCredentialsQueryLimitType]


WebAuthnAuthenticatorTransportsList = List[WebAuthnAuthenticatorTransportType]


class WebAuthnCredentialDescription(TypedDict, total=False):
    """The details of a passkey, or webauthN, biometric or security-key
    authentication factor for a user.

    This data type is a response parameter of
    `ListWebAuthnCredentials <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ListWebAuthnCredentials.html>`__.
    """

    CredentialId: StringType
    FriendlyCredentialName: StringType
    RelyingPartyId: StringType
    AuthenticatorAttachment: Optional[WebAuthnAuthenticatorAttachmentType]
    AuthenticatorTransports: WebAuthnAuthenticatorTransportsList
    CreatedAt: DateType


WebAuthnCredentialDescriptionListType = List[WebAuthnCredentialDescription]


class ListWebAuthnCredentialsResponse(TypedDict, total=False):
    Credentials: WebAuthnCredentialDescriptionListType
    NextToken: Optional[PaginationKey]


class ResendConfirmationCodeRequest(ServiceRequest):
    """Represents the request to resend the confirmation code."""

    ClientId: ClientIdType
    SecretHash: Optional[SecretHashType]
    UserContextData: Optional[UserContextDataType]
    Username: UsernameType
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    ClientMetadata: Optional[ClientMetadataType]


class ResendConfirmationCodeResponse(TypedDict, total=False):
    """The response from the server when Amazon Cognito makes the request to
    resend a confirmation code.
    """

    CodeDeliveryDetails: Optional[CodeDeliveryDetailsType]


class RespondToAuthChallengeRequest(ServiceRequest):
    """The request to respond to an authentication challenge."""

    ClientId: ClientIdType
    ChallengeName: ChallengeNameType
    Session: Optional[SessionType]
    ChallengeResponses: Optional[ChallengeResponsesType]
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    UserContextData: Optional[UserContextDataType]
    ClientMetadata: Optional[ClientMetadataType]


class RespondToAuthChallengeResponse(TypedDict, total=False):
    """The response to respond to the authentication challenge."""

    ChallengeName: Optional[ChallengeNameType]
    Session: Optional[SessionType]
    ChallengeParameters: Optional[ChallengeParametersType]
    AuthenticationResult: Optional[AuthenticationResultType]


class RevokeTokenRequest(ServiceRequest):
    Token: TokenModelType
    ClientId: ClientIdType
    ClientSecret: Optional[ClientSecretType]


class RevokeTokenResponse(TypedDict, total=False):
    pass


class SetLogDeliveryConfigurationRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    LogConfigurations: LogConfigurationListType


class SetLogDeliveryConfigurationResponse(TypedDict, total=False):
    LogDeliveryConfiguration: Optional[LogDeliveryConfigurationType]


class SetRiskConfigurationRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ClientId: Optional[ClientIdType]
    CompromisedCredentialsRiskConfiguration: Optional[CompromisedCredentialsRiskConfigurationType]
    AccountTakeoverRiskConfiguration: Optional[AccountTakeoverRiskConfigurationType]
    RiskExceptionConfiguration: Optional[RiskExceptionConfigurationType]


class SetRiskConfigurationResponse(TypedDict, total=False):
    RiskConfiguration: RiskConfigurationType


class SetUICustomizationRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ClientId: Optional[ClientIdType]
    CSS: Optional[CSSType]
    ImageFile: Optional[ImageFileType]


class SetUICustomizationResponse(TypedDict, total=False):
    UICustomization: UICustomizationType


class SetUserMFAPreferenceRequest(ServiceRequest):
    SMSMfaSettings: Optional[SMSMfaSettingsType]
    SoftwareTokenMfaSettings: Optional[SoftwareTokenMfaSettingsType]
    EmailMfaSettings: Optional[EmailMfaSettingsType]
    AccessToken: TokenModelType


class SetUserMFAPreferenceResponse(TypedDict, total=False):
    pass


class SetUserPoolMfaConfigRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    SmsMfaConfiguration: Optional[SmsMfaConfigType]
    SoftwareTokenMfaConfiguration: Optional[SoftwareTokenMfaConfigType]
    EmailMfaConfiguration: Optional[EmailMfaConfigType]
    MfaConfiguration: Optional[UserPoolMfaType]
    WebAuthnConfiguration: Optional[WebAuthnConfigurationType]


class SetUserPoolMfaConfigResponse(TypedDict, total=False):
    SmsMfaConfiguration: Optional[SmsMfaConfigType]
    SoftwareTokenMfaConfiguration: Optional[SoftwareTokenMfaConfigType]
    EmailMfaConfiguration: Optional[EmailMfaConfigType]
    MfaConfiguration: Optional[UserPoolMfaType]
    WebAuthnConfiguration: Optional[WebAuthnConfigurationType]


class SetUserSettingsRequest(ServiceRequest):
    """Represents the request to set user settings."""

    AccessToken: TokenModelType
    MFAOptions: MFAOptionListType


class SetUserSettingsResponse(TypedDict, total=False):
    """The response from the server for a set user settings request."""

    pass


class SignUpRequest(ServiceRequest):
    """Represents the request to register a user."""

    ClientId: ClientIdType
    SecretHash: Optional[SecretHashType]
    Username: UsernameType
    Password: Optional[PasswordType]
    UserAttributes: Optional[AttributeListType]
    ValidationData: Optional[AttributeListType]
    AnalyticsMetadata: Optional[AnalyticsMetadataType]
    UserContextData: Optional[UserContextDataType]
    ClientMetadata: Optional[ClientMetadataType]


class SignUpResponse(TypedDict, total=False):
    """The response from the server for a registration request."""

    UserConfirmed: BooleanType
    CodeDeliveryDetails: Optional[CodeDeliveryDetailsType]
    UserSub: StringType
    Session: Optional[SessionType]


class StartUserImportJobRequest(ServiceRequest):
    """Represents the request to start the user import job."""

    UserPoolId: UserPoolIdType
    JobId: UserImportJobIdType


class StartUserImportJobResponse(TypedDict, total=False):
    """Represents the response from the server to the request to start the user
    import job.
    """

    UserImportJob: Optional[UserImportJobType]


class StartWebAuthnRegistrationRequest(ServiceRequest):
    AccessToken: TokenModelType


class StartWebAuthnRegistrationResponse(TypedDict, total=False):
    CredentialCreationOptions: Document


class StopUserImportJobRequest(ServiceRequest):
    """Represents the request to stop the user import job."""

    UserPoolId: UserPoolIdType
    JobId: UserImportJobIdType


class StopUserImportJobResponse(TypedDict, total=False):
    """Represents the response from the server to the request to stop the user
    import job.
    """

    UserImportJob: Optional[UserImportJobType]


class TagResourceRequest(ServiceRequest):
    ResourceArn: ArnType
    Tags: UserPoolTagsType


class TagResourceResponse(TypedDict, total=False):
    pass


UserPoolTagsListType = List[TagKeysType]


class UntagResourceRequest(ServiceRequest):
    ResourceArn: ArnType
    TagKeys: UserPoolTagsListType


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateAuthEventFeedbackRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Username: UsernameType
    EventId: EventIdType
    FeedbackToken: TokenModelType
    FeedbackValue: FeedbackValueType


class UpdateAuthEventFeedbackResponse(TypedDict, total=False):
    pass


class UpdateDeviceStatusRequest(ServiceRequest):
    """Represents the request to update the device status."""

    AccessToken: TokenModelType
    DeviceKey: DeviceKeyType
    DeviceRememberedStatus: Optional[DeviceRememberedStatusType]


class UpdateDeviceStatusResponse(TypedDict, total=False):
    """The response to the request to update the device status."""

    pass


class UpdateGroupRequest(ServiceRequest):
    GroupName: GroupNameType
    UserPoolId: UserPoolIdType
    Description: Optional[DescriptionType]
    RoleArn: Optional[ArnType]
    Precedence: Optional[PrecedenceType]


class UpdateGroupResponse(TypedDict, total=False):
    Group: Optional[GroupType]


class UpdateIdentityProviderRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    ProviderName: ProviderNameType
    ProviderDetails: Optional[ProviderDetailsType]
    AttributeMapping: Optional[AttributeMappingType]
    IdpIdentifiers: Optional[IdpIdentifiersListType]


class UpdateIdentityProviderResponse(TypedDict, total=False):
    IdentityProvider: IdentityProviderType


class UpdateManagedLoginBrandingRequest(ServiceRequest):
    UserPoolId: Optional[UserPoolIdType]
    ManagedLoginBrandingId: Optional[ManagedLoginBrandingIdType]
    UseCognitoProvidedValues: Optional[BooleanType]
    Settings: Optional[Document]
    Assets: Optional[AssetListType]


class UpdateManagedLoginBrandingResponse(TypedDict, total=False):
    ManagedLoginBranding: Optional[ManagedLoginBrandingType]


class UpdateResourceServerRequest(ServiceRequest):
    UserPoolId: UserPoolIdType
    Identifier: ResourceServerIdentifierType
    Name: ResourceServerNameType
    Scopes: Optional[ResourceServerScopeListType]


class UpdateResourceServerResponse(TypedDict, total=False):
    ResourceServer: ResourceServerType


class UpdateUserAttributesRequest(ServiceRequest):
    """Represents the request to update user attributes."""

    UserAttributes: AttributeListType
    AccessToken: TokenModelType
    ClientMetadata: Optional[ClientMetadataType]


class UpdateUserAttributesResponse(TypedDict, total=False):
    """Represents the response from the server for the request to update user
    attributes.
    """

    CodeDeliveryDetailsList: Optional[CodeDeliveryDetailsListType]


class UpdateUserPoolClientRequest(ServiceRequest):
    """Represents the request to update the user pool client."""

    UserPoolId: UserPoolIdType
    ClientId: ClientIdType
    ClientName: Optional[ClientNameType]
    RefreshTokenValidity: Optional[RefreshTokenValidityType]
    AccessTokenValidity: Optional[AccessTokenValidityType]
    IdTokenValidity: Optional[IdTokenValidityType]
    TokenValidityUnits: Optional[TokenValidityUnitsType]
    ReadAttributes: Optional[ClientPermissionListType]
    WriteAttributes: Optional[ClientPermissionListType]
    ExplicitAuthFlows: Optional[ExplicitAuthFlowsListType]
    SupportedIdentityProviders: Optional[SupportedIdentityProvidersListType]
    CallbackURLs: Optional[CallbackURLsListType]
    LogoutURLs: Optional[LogoutURLsListType]
    DefaultRedirectURI: Optional[RedirectUrlType]
    AllowedOAuthFlows: Optional[OAuthFlowsType]
    AllowedOAuthScopes: Optional[ScopeListType]
    AllowedOAuthFlowsUserPoolClient: Optional[BooleanType]
    AnalyticsConfiguration: Optional[AnalyticsConfigurationType]
    PreventUserExistenceErrors: Optional[PreventUserExistenceErrorTypes]
    EnableTokenRevocation: Optional[WrappedBooleanType]
    EnablePropagateAdditionalUserContextData: Optional[WrappedBooleanType]
    AuthSessionValidity: Optional[AuthSessionValidityType]


class UpdateUserPoolClientResponse(TypedDict, total=False):
    """Represents the response from the server to the request to update the
    user pool client.
    """

    UserPoolClient: Optional[UserPoolClientType]


class UpdateUserPoolDomainRequest(ServiceRequest):
    """The UpdateUserPoolDomain request input."""

    Domain: DomainType
    UserPoolId: UserPoolIdType
    ManagedLoginVersion: Optional[WrappedIntegerType]
    CustomDomainConfig: CustomDomainConfigType


class UpdateUserPoolDomainResponse(TypedDict, total=False):
    """The UpdateUserPoolDomain response output."""

    ManagedLoginVersion: Optional[WrappedIntegerType]
    CloudFrontDomain: Optional[DomainType]


class UpdateUserPoolRequest(ServiceRequest):
    """Represents the request to update the user pool."""

    UserPoolId: UserPoolIdType
    Policies: Optional[UserPoolPolicyType]
    DeletionProtection: Optional[DeletionProtectionType]
    LambdaConfig: Optional[LambdaConfigType]
    AutoVerifiedAttributes: Optional[VerifiedAttributesListType]
    SmsVerificationMessage: Optional[SmsVerificationMessageType]
    EmailVerificationMessage: Optional[EmailVerificationMessageType]
    EmailVerificationSubject: Optional[EmailVerificationSubjectType]
    VerificationMessageTemplate: Optional[VerificationMessageTemplateType]
    SmsAuthenticationMessage: Optional[SmsVerificationMessageType]
    UserAttributeUpdateSettings: Optional[UserAttributeUpdateSettingsType]
    MfaConfiguration: Optional[UserPoolMfaType]
    DeviceConfiguration: Optional[DeviceConfigurationType]
    EmailConfiguration: Optional[EmailConfigurationType]
    SmsConfiguration: Optional[SmsConfigurationType]
    UserPoolTags: Optional[UserPoolTagsType]
    AdminCreateUserConfig: Optional[AdminCreateUserConfigType]
    UserPoolAddOns: Optional[UserPoolAddOnsType]
    AccountRecoverySetting: Optional[AccountRecoverySettingType]
    PoolName: Optional[UserPoolNameType]
    UserPoolTier: Optional[UserPoolTierType]


class UpdateUserPoolResponse(TypedDict, total=False):
    """Represents the response from the server when you make a request to
    update the user pool.
    """

    pass


class VerifySoftwareTokenRequest(ServiceRequest):
    AccessToken: Optional[TokenModelType]
    Session: Optional[SessionType]
    UserCode: SoftwareTokenMFAUserCodeType
    FriendlyDeviceName: Optional[StringType]


class VerifySoftwareTokenResponse(TypedDict, total=False):
    Status: Optional[VerifySoftwareTokenResponseType]
    Session: Optional[SessionType]


class VerifyUserAttributeRequest(ServiceRequest):
    """Represents the request to verify user attributes."""

    AccessToken: TokenModelType
    AttributeName: AttributeNameType
    Code: ConfirmationCodeType


class VerifyUserAttributeResponse(TypedDict, total=False):
    """A container representing the response from the server from the request
    to verify user attributes.
    """

    pass


class CognitoIdpApi:
    service = "cognito-idp"
    version = "2016-04-18"

    @handler("AddCustomAttributes")
    def add_custom_attributes(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        custom_attributes: CustomAttributesListType,
        **kwargs,
    ) -> AddCustomAttributesResponse:
        """Adds additional user attributes to the user pool schema.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to add custom
        attributes.
        :param custom_attributes: An array of custom attributes, such as Mutable and Name.
        :returns: AddCustomAttributesResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserImportInProgressException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminAddUserToGroup")
    def admin_add_user_to_group(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        group_name: GroupNameType,
        **kwargs,
    ) -> None:
        """Adds a user to a group. A user who is in a group can present a
        preferred-role claim to an identity pool, and populates a
        ``cognito:groups`` claim to their access and identity tokens.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param username: The username of the user that you want to query or modify.
        :param group_name: The name of the group that you want to add your user to.
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminConfirmSignUp")
    def admin_confirm_sign_up(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> AdminConfirmSignUpResponse:
        """This IAM-authenticated API operation confirms user sign-up as an
        administrator. Unlike
        `ConfirmSignUp <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ConfirmSignUp.html>`__,
        your IAM credentials authorize user account confirmation. No
        confirmation code is required.

        This request sets a user account active in a user pool that `requires
        confirmation of new user
        accounts <https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html#signing-up-users-in-your-app-and-confirming-them-as-admin>`__
        before they can sign in. You can configure your user pool to not send
        confirmation codes to new users and instead confirm them with this API
        operation on the back end.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for which you want to confirm user registration.
        :param username: The username of the user that you want to query or modify.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: AdminConfirmSignUpResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises NotAuthorizedException:
        :raises TooManyFailedAttemptsException:
        :raises InvalidLambdaResponseException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminCreateUser")
    def admin_create_user(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        user_attributes: AttributeListType = None,
        validation_data: AttributeListType = None,
        temporary_password: PasswordType = None,
        force_alias_creation: ForceAliasCreation = None,
        message_action: MessageActionType = None,
        desired_delivery_mediums: DeliveryMediumListType = None,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> AdminCreateUserResponse:
        """Creates a new user in the specified user pool.

        If ``MessageAction`` isn't set, the default is to send a welcome message
        via email or phone (SMS).

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        This message is based on a template that you configured in your call to
        create or update a user pool. This template includes your custom sign-up
        instructions and placeholders for user name and temporary password.

        Alternatively, you can call ``AdminCreateUser`` with ``SUPPRESS`` for
        the ``MessageAction`` parameter, and Amazon Cognito won't send any
        email.

        In either case, if the user has a password, they will be in the
        ``FORCE_CHANGE_PASSWORD`` state until they sign in and set their
        password. Your invitation message template must have the ``{####}``
        password placeholder if your users have passwords. If your template
        doesn't have this placeholder, Amazon Cognito doesn't deliver the
        invitation message. In this case, you must update your message template
        and resend the password with a new ``AdminCreateUser`` request with a
        ``MessageAction`` value of ``RESEND``.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where the user will be created.
        :param username: The value that you want to set as the username sign-in attribute.
        :param user_attributes: An array of name-value pairs that contain user attributes and attribute
        values to be set for the user to be created.
        :param validation_data: Temporary user attributes that contribute to the outcomes of your pre
        sign-up Lambda trigger.
        :param temporary_password: The user's temporary password.
        :param force_alias_creation: This parameter is used only if the ``phone_number_verified`` or
        ``email_verified`` attribute is set to ``True``.
        :param message_action: Set to ``RESEND`` to resend the invitation message to a user that
        already exists and reset the expiration limit on the user's account.
        :param desired_delivery_mediums: Specify ``"EMAIL"`` if email will be used to send the welcome message.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: AdminCreateUserResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises UserNotFoundException:
        :raises UsernameExistsException:
        :raises InvalidPasswordException:
        :raises CodeDeliveryFailureException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises InvalidLambdaResponseException:
        :raises PreconditionNotMetException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UnsupportedUserStateException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminDeleteUser")
    def admin_delete_user(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        **kwargs,
    ) -> None:
        """Deletes a user as an administrator. Works on any user.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to delete the user.
        :param username: The username of the user that you want to query or modify.
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminDeleteUserAttributes")
    def admin_delete_user_attributes(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        user_attribute_names: AttributeNameListType,
        **kwargs,
    ) -> AdminDeleteUserAttributesResponse:
        """Deletes the user attributes in a user pool as an administrator. Works on
        any user.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to delete user
        attributes.
        :param username: The username of the user that you want to query or modify.
        :param user_attribute_names: An array of strings representing the user attribute names you want to
        delete.
        :returns: AdminDeleteUserAttributesResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminDisableProviderForUser")
    def admin_disable_provider_for_user(
        self,
        context: RequestContext,
        user_pool_id: StringType,
        user: ProviderUserIdentifierType,
        **kwargs,
    ) -> AdminDisableProviderForUserResponse:
        """Prevents the user from signing in with the specified external (SAML or
        social) identity provider (IdP). If the user that you want to deactivate
        is a Amazon Cognito user pools native username + password user, they
        can't use their password to sign in. If the user to deactivate is a
        linked external IdP user, any link between that user and an existing
        user is removed. When the external user signs in again, and the user is
        no longer attached to the previously linked ``DestinationUser``, the
        user must create a new user account. See
        `AdminLinkProviderForUser <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminLinkProviderForUser.html>`__.

        The ``ProviderName`` must match the value specified when creating an IdP
        for the pool.

        To deactivate a native username + password user, the ``ProviderName``
        value must be ``Cognito`` and the ``ProviderAttributeName`` must be
        ``Cognito_Subject``. The ``ProviderAttributeValue`` must be the name
        that is used in the user pool for the user.

        The ``ProviderAttributeName`` must always be ``Cognito_Subject`` for
        social IdPs. The ``ProviderAttributeValue`` must always be the exact
        subject that was used when the user was originally linked as a source
        user.

        For de-linking a SAML identity, there are two scenarios. If the linked
        identity has not yet been used to sign in, the ``ProviderAttributeName``
        and ``ProviderAttributeValue`` must be the same values that were used
        for the ``SourceUser`` when the identities were originally linked using
        ``AdminLinkProviderForUser`` call. (If the linking was done with
        ``ProviderAttributeName`` set to ``Cognito_Subject``, the same applies
        here). However, if the user has already signed in, the
        ``ProviderAttributeName`` must be ``Cognito_Subject`` and
        ``ProviderAttributeValue`` must be the subject of the SAML assertion.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param user: The user to be disabled.
        :returns: AdminDisableProviderForUserResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises AliasExistsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminDisableUser")
    def admin_disable_user(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        **kwargs,
    ) -> AdminDisableUserResponse:
        """Deactivates a user and revokes all access tokens for the user. A
        deactivated user can't sign in, but still appears in the responses to
        ``GetUser`` and ``ListUsers`` API requests.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to disable the user.
        :param username: The username of the user that you want to query or modify.
        :returns: AdminDisableUserResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminEnableUser")
    def admin_enable_user(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        **kwargs,
    ) -> AdminEnableUserResponse:
        """Enables the specified user as an administrator. Works on any user.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to enable the user.
        :param username: The username of the user that you want to query or modify.
        :returns: AdminEnableUserResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminForgetDevice")
    def admin_forget_device(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        device_key: DeviceKeyType,
        **kwargs,
    ) -> None:
        """Forgets the device, as an administrator.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param username: The username of the user that you want to query or modify.
        :param device_key: The device key.
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises InvalidUserPoolConfigurationException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminGetDevice")
    def admin_get_device(
        self,
        context: RequestContext,
        device_key: DeviceKeyType,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        **kwargs,
    ) -> AdminGetDeviceResponse:
        """Gets the device, as an administrator.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param device_key: The device key.
        :param user_pool_id: The user pool ID.
        :param username: The username of the user that you want to query or modify.
        :returns: AdminGetDeviceResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises InvalidUserPoolConfigurationException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        :raises NotAuthorizedException:
        """
        raise NotImplementedError

    @handler("AdminGetUser")
    def admin_get_user(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        **kwargs,
    ) -> AdminGetUserResponse:
        """Gets the specified user by user name in a user pool as an administrator.
        Works on any user. This operation contributes to your monthly active
        user (MAU) count for the purpose of billing.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to get information
        about the user.
        :param username: The username of the user that you want to query or modify.
        :returns: AdminGetUserResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminInitiateAuth")
    def admin_initiate_auth(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType,
        auth_flow: AuthFlowType,
        auth_parameters: AuthParametersType = None,
        client_metadata: ClientMetadataType = None,
        analytics_metadata: AnalyticsMetadataType = None,
        context_data: ContextDataType = None,
        session: SessionType = None,
        **kwargs,
    ) -> AdminInitiateAuthResponse:
        """Initiates the authentication flow, as an administrator.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The ID of the Amazon Cognito user pool.
        :param client_id: The app client ID.
        :param auth_flow: The authentication flow that you want to initiate.
        :param auth_parameters: The authentication parameters.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for
        certain custom workflows that this action triggers.
        :param analytics_metadata: The analytics metadata for collecting Amazon Pinpoint metrics for
        ``AdminInitiateAuth`` calls.
        :param context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param session: The optional session ID from a ``ConfirmSignUp`` API request.
        :returns: AdminInitiateAuthResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        :raises UnexpectedLambdaException:
        :raises InvalidUserPoolConfigurationException:
        :raises UserLambdaValidationException:
        :raises InvalidLambdaResponseException:
        :raises MFAMethodNotFoundException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        """
        raise NotImplementedError

    @handler("AdminLinkProviderForUser")
    def admin_link_provider_for_user(
        self,
        context: RequestContext,
        user_pool_id: StringType,
        destination_user: ProviderUserIdentifierType,
        source_user: ProviderUserIdentifierType,
        **kwargs,
    ) -> AdminLinkProviderForUserResponse:
        """Links an existing user account in a user pool (``DestinationUser``) to
        an identity from an external IdP (``SourceUser``) based on a specified
        attribute name and value from the external IdP. This allows you to
        create a link from the existing user account to an external federated
        user identity that has not yet been used to sign in. You can then use
        the federated user identity to sign in as the existing user account.

        For example, if there is an existing user with a username and password,
        this API links that user to a federated user identity. When the user
        signs in with a federated user identity, they sign in as the existing
        user account.

        The maximum number of federated identities linked to a user is five.

        Because this API allows a user with an external federated identity to
        sign in as an existing user in the user pool, it is critical that it
        only be used with external IdPs and provider attributes that have been
        trusted by the application owner.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param destination_user: The existing user in the user pool that you want to assign to the
        external IdP user account.
        :param source_user: An external IdP account for a user who doesn't exist yet in the user
        pool.
        :returns: AdminLinkProviderForUserResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises AliasExistsException:
        :raises LimitExceededException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminListDevices")
    def admin_list_devices(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        limit: QueryLimitType = None,
        pagination_token: SearchPaginationTokenType = None,
        **kwargs,
    ) -> AdminListDevicesResponse:
        """Lists a user's registered devices.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param username: The username of the user that you want to query or modify.
        :param limit: The limit of the devices request.
        :param pagination_token: This API operation returns a limited number of results.
        :returns: AdminListDevicesResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises InvalidUserPoolConfigurationException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        :raises NotAuthorizedException:
        """
        raise NotImplementedError

    @handler("AdminListGroupsForUser")
    def admin_list_groups_for_user(
        self,
        context: RequestContext,
        username: UsernameType,
        user_pool_id: UserPoolIdType,
        limit: QueryLimitType = None,
        next_token: PaginationKey = None,
        **kwargs,
    ) -> AdminListGroupsForUserResponse:
        """Lists the groups that a user belongs to.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param username: The username of the user that you want to query or modify.
        :param user_pool_id: The user pool ID for the user pool.
        :param limit: The limit of the request to list groups.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :returns: AdminListGroupsForUserResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminListUserAuthEvents")
    def admin_list_user_auth_events(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        max_results: QueryLimitType = None,
        next_token: PaginationKey = None,
        **kwargs,
    ) -> AdminListUserAuthEventsResponse:
        """A history of user activity and any risks detected as part of Amazon
        Cognito advanced security.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param username: The username of the user that you want to query or modify.
        :param max_results: The maximum number of authentication events to return.
        :param next_token: A pagination token.
        :returns: AdminListUserAuthEventsResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises UserPoolAddOnNotEnabledException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminRemoveUserFromGroup")
    def admin_remove_user_from_group(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        group_name: GroupNameType,
        **kwargs,
    ) -> None:
        """Removes the specified user from the specified group.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param username: The username of the user that you want to query or modify.
        :param group_name: The group name.
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminResetUserPassword")
    def admin_reset_user_password(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> AdminResetUserPasswordResponse:
        """Resets the specified user's password in a user pool as an administrator.
        Works on any user.

        To use this API operation, your user pool must have self-service account
        recovery configured. Use
        `AdminSetUserPassword <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminSetUserPassword.html>`__
        if you manage passwords as an administrator.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        Deactivates a user's password, requiring them to change it. If a user
        tries to sign in after the API is called, Amazon Cognito responds with a
        ``PasswordResetRequiredException`` error. Your app must then perform the
        actions that reset your user's password: the forgot-password flow. In
        addition, if the user pool has phone verification selected and a
        verified phone number exists for the user, or if email verification is
        selected and a verified email exists for the user, calling this API will
        also result in sending a message to the end user with the code to change
        their password.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to reset the user's
        password.
        :param username: The username of the user that you want to query or modify.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: AdminResetUserPasswordResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises NotAuthorizedException:
        :raises InvalidLambdaResponseException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises UserNotFoundException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminRespondToAuthChallenge")
    def admin_respond_to_auth_challenge(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType,
        challenge_name: ChallengeNameType,
        challenge_responses: ChallengeResponsesType = None,
        session: SessionType = None,
        analytics_metadata: AnalyticsMetadataType = None,
        context_data: ContextDataType = None,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> AdminRespondToAuthChallengeResponse:
        """Some API operations in a user pool generate a challenge, like a prompt
        for an MFA code, for device authentication that bypasses MFA, or for a
        custom authentication challenge. An ``AdminRespondToAuthChallenge`` API
        request provides the answer to that challenge, like a code or a secure
        remote password (SRP). The parameters of a response to an authentication
        challenge vary with the type of challenge.

        For more information about custom authentication challenges, see `Custom
        authentication challenge Lambda
        triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`__.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The ID of the Amazon Cognito user pool.
        :param client_id: The app client ID.
        :param challenge_name: The challenge name.
        :param challenge_responses: The responses to the challenge that you received in the previous
        request.
        :param session: The session that should be passed both ways in challenge-response calls
        to the service.
        :param analytics_metadata: The analytics metadata for collecting Amazon Pinpoint metrics for
        ``AdminRespondToAuthChallenge`` calls.
        :param context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: AdminRespondToAuthChallengeResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises CodeMismatchException:
        :raises ExpiredCodeException:
        :raises UnexpectedLambdaException:
        :raises InvalidPasswordException:
        :raises PasswordHistoryPolicyViolationException:
        :raises UserLambdaValidationException:
        :raises InvalidLambdaResponseException:
        :raises TooManyRequestsException:
        :raises InvalidUserPoolConfigurationException:
        :raises InternalErrorException:
        :raises MFAMethodNotFoundException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises AliasExistsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises SoftwareTokenMFANotFoundException:
        """
        raise NotImplementedError

    @handler("AdminSetUserMFAPreference")
    def admin_set_user_mfa_preference(
        self,
        context: RequestContext,
        username: UsernameType,
        user_pool_id: UserPoolIdType,
        sms_mfa_settings: SMSMfaSettingsType = None,
        software_token_mfa_settings: SoftwareTokenMfaSettingsType = None,
        email_mfa_settings: EmailMfaSettingsType = None,
        **kwargs,
    ) -> AdminSetUserMFAPreferenceResponse:
        """Sets the user's multi-factor authentication (MFA) preference, including
        which MFA options are activated, and if any are preferred. Only one
        factor can be set as preferred. The preferred MFA factor will be used to
        authenticate a user if multiple factors are activated. If multiple
        options are activated and no preference is set, a challenge to choose an
        MFA option will be returned during sign-in.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param username: The username of the user that you want to query or modify.
        :param user_pool_id: The ID of the user pool where you want to set a user's MFA preferences.
        :param sms_mfa_settings: User preferences for SMS message MFA.
        :param software_token_mfa_settings: User preferences for time-based one-time password (TOTP) MFA.
        :param email_mfa_settings: User preferences for email message MFA.
        :returns: AdminSetUserMFAPreferenceResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminSetUserPassword")
    def admin_set_user_password(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        password: PasswordType,
        permanent: BooleanType = None,
        **kwargs,
    ) -> AdminSetUserPasswordResponse:
        """Sets the specified user's password in a user pool as an administrator.
        Works on any user.

        The password can be temporary or permanent. If it is temporary, the user
        status enters the ``FORCE_CHANGE_PASSWORD`` state. When the user next
        tries to sign in, the InitiateAuth/AdminInitiateAuth response will
        contain the ``NEW_PASSWORD_REQUIRED`` challenge. If the user doesn't
        sign in before it expires, the user won't be able to sign in, and an
        administrator must reset their password.

        Once the user has set a new password, or the password is permanent, the
        user status is set to ``Confirmed``.

        ``AdminSetUserPassword`` can set a password for the user profile that
        Amazon Cognito creates for third-party federated users. When you set a
        password, the federated user's status changes from ``EXTERNAL_PROVIDER``
        to ``CONFIRMED``. A user in this state can sign in as a federated user,
        and initiate authentication flows in the API like a linked native user.
        They can also modify their password and attributes in
        token-authenticated API requests like ``ChangePassword`` and
        ``UpdateUserAttributes``. As a best security practice and to keep users
        in sync with your external IdP, don't set passwords on federated user
        profiles. To set up a federated user for native sign-in with a linked
        native user, refer to `Linking federated users to an existing user
        profile <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-federation-consolidate-users.html>`__.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to set the user's
        password.
        :param username: The username of the user that you want to query or modify.
        :param password: The password for the user.
        :param permanent: ``True`` if the password is permanent, ``False`` if it is temporary.
        :returns: AdminSetUserPasswordResponse
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        :raises TooManyRequestsException:
        :raises InvalidParameterException:
        :raises InvalidPasswordException:
        :raises PasswordHistoryPolicyViolationException:
        """
        raise NotImplementedError

    @handler("AdminSetUserSettings")
    def admin_set_user_settings(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        mfa_options: MFAOptionListType,
        **kwargs,
    ) -> AdminSetUserSettingsResponse:
        """*This action is no longer supported.* You can use it to configure only
        SMS MFA. You can't use it to configure time-based one-time password
        (TOTP) software token MFA. To configure either type of MFA, use
        `AdminSetUserMFAPreference <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminSetUserMFAPreference.html>`__
        instead.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The ID of the user pool that contains the user whose options you're
        setting.
        :param username: The username of the user that you want to query or modify.
        :param mfa_options: You can use this parameter only to set an SMS configuration that uses
        SMS for delivery.
        :returns: AdminSetUserSettingsResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminUpdateAuthEventFeedback")
    def admin_update_auth_event_feedback(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        event_id: EventIdType,
        feedback_value: FeedbackValueType,
        **kwargs,
    ) -> AdminUpdateAuthEventFeedbackResponse:
        """Provides feedback for an authentication event indicating if it was from
        a valid user. This feedback is used for improving the risk evaluation
        decision for the user pool as part of Amazon Cognito advanced security.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param username: The username of the user that you want to query or modify.
        :param event_id: The authentication event ID.
        :param feedback_value: The authentication event feedback value.
        :returns: AdminUpdateAuthEventFeedbackResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises UserPoolAddOnNotEnabledException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminUpdateDeviceStatus")
    def admin_update_device_status(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        device_key: DeviceKeyType,
        device_remembered_status: DeviceRememberedStatusType = None,
        **kwargs,
    ) -> AdminUpdateDeviceStatusResponse:
        """Updates the device status as an administrator.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param username: The username of the user that you want to query or modify.
        :param device_key: The device key.
        :param device_remembered_status: The status indicating whether a device has been remembered or not.
        :returns: AdminUpdateDeviceStatusResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises InvalidUserPoolConfigurationException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AdminUpdateUserAttributes")
    def admin_update_user_attributes(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        user_attributes: AttributeListType,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> AdminUpdateUserAttributesResponse:
        """This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        Updates the specified user's attributes, including developer attributes,
        as an administrator. Works on any user. To delete an attribute from your
        user, submit the attribute in your API request with a blank value.

        For custom attributes, you must prepend the ``custom:`` prefix to the
        attribute name.

        In addition to updating user attributes, this API can also be used to
        mark phone and email as verified.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to update user
        attributes.
        :param username: The username of the user that you want to query or modify.
        :param user_attributes: An array of name-value pairs representing user attributes.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: AdminUpdateUserAttributesResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises InvalidLambdaResponseException:
        :raises AliasExistsException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        """
        raise NotImplementedError

    @handler("AdminUserGlobalSignOut")
    def admin_user_global_sign_out(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        **kwargs,
    ) -> AdminUserGlobalSignOutResponse:
        """Invalidates the identity, access, and refresh tokens that Amazon Cognito
        issued to a user. Call this operation with your administrative
        credentials when your user signs out of your app. This results in the
        following behavior.

        -  Amazon Cognito no longer accepts *token-authorized* user operations
           that you authorize with a signed-out user's access tokens. For more
           information, see `Using the Amazon Cognito user pools API and user
           pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

           Amazon Cognito returns an ``Access Token has been revoked`` error
           when your app attempts to authorize a user pools API request with a
           revoked access token that contains the scope
           ``aws.cognito.signin.user.admin``.

        -  Amazon Cognito no longer accepts a signed-out user's ID token in a
           `GetId <https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_GetId.html>`__
           request to an identity pool with ``ServerSideTokenCheck`` enabled for
           its user pool IdP configuration in
           `CognitoIdentityProvider <https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_CognitoIdentityProvider.html>`__.

        -  Amazon Cognito no longer accepts a signed-out user's refresh tokens
           in refresh requests.

        Other requests might be valid until your user's token expires.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param username: The username of the user that you want to query or modify.
        :returns: AdminUserGlobalSignOutResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("AssociateSoftwareToken")
    def associate_software_token(
        self,
        context: RequestContext,
        access_token: TokenModelType = None,
        session: SessionType = None,
        **kwargs,
    ) -> AssociateSoftwareTokenResponse:
        """Begins setup of time-based one-time password (TOTP) multi-factor
        authentication (MFA) for a user, with a unique private key that Amazon
        Cognito generates and returns in the API response. You can authorize an
        ``AssociateSoftwareToken`` request with either the user's access token,
        or a session string from a challenge response that you received from
        Amazon Cognito.

        Amazon Cognito disassociates an existing software token when you verify
        the new token in a
        `VerifySoftwareToken <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_VerifySoftwareToken.html>`__
        API request. If you don't verify the software token and your user pool
        doesn't require MFA, the user can then authenticate with user name and
        password credentials alone. If your user pool requires TOTP MFA, Amazon
        Cognito generates an ``MFA_SETUP`` or ``SOFTWARE_TOKEN_SETUP`` challenge
        each time your user signs in. Complete setup with
        ``AssociateSoftwareToken`` and ``VerifySoftwareToken``.

        After you set up software token MFA for your user, Amazon Cognito
        generates a ``SOFTWARE_TOKEN_MFA`` challenge when they authenticate.
        Respond to this challenge with your user's TOTP.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        software token you want to generate.
        :param session: The session that should be passed both ways in challenge-response calls
        to the service.
        :returns: AssociateSoftwareTokenResponse
        :raises ConcurrentModificationException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises ResourceNotFoundException:
        :raises InternalErrorException:
        :raises SoftwareTokenMFANotFoundException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ChangePassword")
    def change_password(
        self,
        context: RequestContext,
        proposed_password: PasswordType,
        access_token: TokenModelType,
        previous_password: PasswordType = None,
        **kwargs,
    ) -> ChangePasswordResponse:
        """Changes the password for a specified user in a user pool.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param proposed_password: The new password.
        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        password you want to change.
        :param previous_password: The user's previous password.
        :returns: ChangePasswordResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises InvalidPasswordException:
        :raises PasswordHistoryPolicyViolationException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CompleteWebAuthnRegistration")
    def complete_web_authn_registration(
        self, context: RequestContext, access_token: TokenModelType, credential: Document, **kwargs
    ) -> CompleteWebAuthnRegistrationResponse:
        """Completes registration of a passkey authenticator for the current user.
        Your application provides data from a successful registration request
        with the data from the output of a
        `StartWebAuthnRegistration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_StartWebAuthnRegistration.html>`__.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        passkey registration you want to verify.
        :param credential: A
        `RegistrationResponseJSON <https://www.
        :returns: CompleteWebAuthnRegistrationResponse
        :raises ForbiddenException:
        :raises InternalErrorException:
        :raises InvalidParameterException:
        :raises LimitExceededException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises WebAuthnNotEnabledException:
        :raises WebAuthnChallengeNotFoundException:
        :raises WebAuthnRelyingPartyMismatchException:
        :raises WebAuthnClientMismatchException:
        :raises WebAuthnOriginNotAllowedException:
        :raises WebAuthnCredentialNotSupportedException:
        """
        raise NotImplementedError

    @handler("ConfirmDevice")
    def confirm_device(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        device_key: DeviceKeyType,
        device_secret_verifier_config: DeviceSecretVerifierConfigType = None,
        device_name: DeviceNameType = None,
        **kwargs,
    ) -> ConfirmDeviceResponse:
        """Confirms tracking of the device. This API call is the call that begins
        device tracking. For more information about device authentication, see
        `Working with user devices in your user
        pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`__.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose device
        you want to confirm.
        :param device_key: The device key.
        :param device_secret_verifier_config: The configuration of the device secret verifier.
        :param device_name: The device name.
        :returns: ConfirmDeviceResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises InvalidPasswordException:
        :raises InvalidLambdaResponseException:
        :raises UsernameExistsException:
        :raises InvalidUserPoolConfigurationException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ConfirmForgotPassword")
    def confirm_forgot_password(
        self,
        context: RequestContext,
        client_id: ClientIdType,
        username: UsernameType,
        confirmation_code: ConfirmationCodeType,
        password: PasswordType,
        secret_hash: SecretHashType = None,
        analytics_metadata: AnalyticsMetadataType = None,
        user_context_data: UserContextDataType = None,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> ConfirmForgotPasswordResponse:
        """Allows a user to enter a confirmation code to reset a forgotten
        password.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param client_id: The app client ID of the app associated with the user pool.
        :param username: The username of the user that you want to query or modify.
        :param confirmation_code: The confirmation code from your user's request to reset their password.
        :param password: The new password that your user wants to set.
        :param secret_hash: A keyed-hash message authentication code (HMAC) calculated using the
        secret key of a user pool client and username plus the client ID in the
        message.
        :param analytics_metadata: The Amazon Pinpoint analytics metadata for collecting metrics for
        ``ConfirmForgotPassword`` calls.
        :param user_context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: ConfirmForgotPasswordResponse
        :raises ResourceNotFoundException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises InvalidParameterException:
        :raises InvalidPasswordException:
        :raises PasswordHistoryPolicyViolationException:
        :raises NotAuthorizedException:
        :raises CodeMismatchException:
        :raises ExpiredCodeException:
        :raises TooManyFailedAttemptsException:
        :raises InvalidLambdaResponseException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ConfirmSignUp")
    def confirm_sign_up(
        self,
        context: RequestContext,
        client_id: ClientIdType,
        username: UsernameType,
        confirmation_code: ConfirmationCodeType,
        secret_hash: SecretHashType = None,
        force_alias_creation: ForceAliasCreation = None,
        analytics_metadata: AnalyticsMetadataType = None,
        user_context_data: UserContextDataType = None,
        client_metadata: ClientMetadataType = None,
        session: SessionType = None,
        **kwargs,
    ) -> ConfirmSignUpResponse:
        """This public API operation provides a code that Amazon Cognito sent to
        your user when they signed up in your user pool via the
        `SignUp <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SignUp.html>`__
        API operation. After your user enters their code, they confirm ownership
        of the email address or phone number that they provided, and their user
        account becomes active. Depending on your user pool configuration, your
        users will receive their confirmation code in an email or SMS message.

        Local users who signed up in your user pool are the only type of user
        who can confirm sign-up with a code. Users who federate through an
        external identity provider (IdP) have already been confirmed by their
        IdP. Administrator-created users, users created with the
        `AdminCreateUser <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminCreateUser.html>`__
        API operation, confirm their accounts when they respond to their
        invitation email message and choose a password. They do not receive a
        confirmation code. Instead, they receive a temporary password.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param client_id: The ID of the app client associated with the user pool.
        :param username: The username of the user that you want to query or modify.
        :param confirmation_code: The confirmation code sent by a user's request to confirm registration.
        :param secret_hash: A keyed-hash message authentication code (HMAC) calculated using the
        secret key of a user pool client and username plus the client ID in the
        message.
        :param force_alias_creation: Boolean to be specified to force user confirmation irrespective of
        existing alias.
        :param analytics_metadata: The Amazon Pinpoint analytics metadata for collecting metrics for
        ``ConfirmSignUp`` calls.
        :param user_context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :param session: The optional session ID from a ``SignUp`` API request.
        :returns: ConfirmSignUpResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises NotAuthorizedException:
        :raises TooManyFailedAttemptsException:
        :raises CodeMismatchException:
        :raises ExpiredCodeException:
        :raises InvalidLambdaResponseException:
        :raises AliasExistsException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateGroup")
    def create_group(
        self,
        context: RequestContext,
        group_name: GroupNameType,
        user_pool_id: UserPoolIdType,
        description: DescriptionType = None,
        role_arn: ArnType = None,
        precedence: PrecedenceType = None,
        **kwargs,
    ) -> CreateGroupResponse:
        """Creates a new group in the specified user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param group_name: The name of the group.
        :param user_pool_id: The user pool ID for the user pool.
        :param description: A string containing the description of the group.
        :param role_arn: The role Amazon Resource Name (ARN) for the group.
        :param precedence: A non-negative integer value that specifies the precedence of this group
        relative to the other groups that a user can belong to in the user pool.
        :returns: CreateGroupResponse
        :raises InvalidParameterException:
        :raises GroupExistsException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("CreateIdentityProvider")
    def create_identity_provider(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        provider_name: ProviderNameTypeV2,
        provider_type: IdentityProviderTypeType,
        provider_details: ProviderDetailsType,
        attribute_mapping: AttributeMappingType = None,
        idp_identifiers: IdpIdentifiersListType = None,
        **kwargs,
    ) -> CreateIdentityProviderResponse:
        """Adds a configuration and trust relationship between a third-party
        identity provider (IdP) and a user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param provider_name: The IdP name.
        :param provider_type: The IdP type.
        :param provider_details: The scopes, URLs, and identifiers for your external identity provider.
        :param attribute_mapping: A mapping of IdP attributes to standard and custom user pool attributes.
        :param idp_identifiers: A list of IdP identifiers.
        :returns: CreateIdentityProviderResponse
        :raises InvalidParameterException:
        :raises DuplicateProviderException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("CreateManagedLoginBranding")
    def create_managed_login_branding(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType,
        use_cognito_provided_values: BooleanType = None,
        settings: Document = None,
        assets: AssetListType = None,
        **kwargs,
    ) -> CreateManagedLoginBrandingResponse:
        """Creates a new set of branding settings for a user pool style and
        associates it with an app client. This operation is the programmatic
        option for the creation of a new style in the branding designer.

        Provides values for UI customization in a ``Settings`` JSON object and
        image files in an ``Assets`` array. To send the JSON object ``Document``
        type parameter in ``Settings``, you might need to update to the most
        recent version of your Amazon Web Services SDK.

        This operation has a 2-megabyte request-size limit and include the CSS
        settings and image assets for your app client. Your branding settings
        might exceed 2MB in size. Amazon Cognito doesn't require that you pass
        all parameters in one request and preserves existing style settings that
        you don't specify. If your request is larger than 2MB, separate it into
        multiple requests, each with a size smaller than the limit.

        For more information, see `API and SDK operations for managed login
        branding <https://docs.aws.amazon.com/cognito/latest/developerguide/managed-login-brandingdesigner.html#branding-designer-api>`__

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The ID of the user pool where you want to create a new branding style.
        :param client_id: The app client that you want to create the branding style for.
        :param use_cognito_provided_values: When true, applies the default branding style options.
        :param settings: A JSON file, encoded as a ``Document`` type, with the the settings that
        you want to apply to your style.
        :param assets: An array of image files that you want to apply to roles like
        backgrounds, logos, and icons.
        :returns: CreateManagedLoginBrandingResponse
        :raises ResourceNotFoundException:
        :raises ConcurrentModificationException:
        :raises ManagedLoginBrandingExistsException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises LimitExceededException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("CreateResourceServer")
    def create_resource_server(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        identifier: ResourceServerIdentifierType,
        name: ResourceServerNameType,
        scopes: ResourceServerScopeListType = None,
        **kwargs,
    ) -> CreateResourceServerResponse:
        """Creates a new OAuth2.0 resource server and defines custom scopes within
        it.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param identifier: A unique resource server identifier for the resource server.
        :param name: A friendly name for the resource server.
        :param scopes: A list of scopes.
        :returns: CreateResourceServerResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("CreateUserImportJob")
    def create_user_import_job(
        self,
        context: RequestContext,
        job_name: UserImportJobNameType,
        user_pool_id: UserPoolIdType,
        cloud_watch_logs_role_arn: ArnType,
        **kwargs,
    ) -> CreateUserImportJobResponse:
        """Creates a user import job.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param job_name: The job name for the user import job.
        :param user_pool_id: The user pool ID for the user pool that the users are being imported
        into.
        :param cloud_watch_logs_role_arn: The role ARN for the Amazon CloudWatch Logs Logging role for the user
        import job.
        :returns: CreateUserImportJobResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises PreconditionNotMetException:
        :raises NotAuthorizedException:
        :raises LimitExceededException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("CreateUserPool")
    def create_user_pool(
        self,
        context: RequestContext,
        pool_name: UserPoolNameType,
        policies: UserPoolPolicyType = None,
        deletion_protection: DeletionProtectionType = None,
        lambda_config: LambdaConfigType = None,
        auto_verified_attributes: VerifiedAttributesListType = None,
        alias_attributes: AliasAttributesListType = None,
        username_attributes: UsernameAttributesListType = None,
        sms_verification_message: SmsVerificationMessageType = None,
        email_verification_message: EmailVerificationMessageType = None,
        email_verification_subject: EmailVerificationSubjectType = None,
        verification_message_template: VerificationMessageTemplateType = None,
        sms_authentication_message: SmsVerificationMessageType = None,
        mfa_configuration: UserPoolMfaType = None,
        user_attribute_update_settings: UserAttributeUpdateSettingsType = None,
        device_configuration: DeviceConfigurationType = None,
        email_configuration: EmailConfigurationType = None,
        sms_configuration: SmsConfigurationType = None,
        user_pool_tags: UserPoolTagsType = None,
        admin_create_user_config: AdminCreateUserConfigType = None,
        schema: SchemaAttributesListType = None,
        user_pool_add_ons: UserPoolAddOnsType = None,
        username_configuration: UsernameConfigurationType = None,
        account_recovery_setting: AccountRecoverySettingType = None,
        user_pool_tier: UserPoolTierType = None,
        **kwargs,
    ) -> CreateUserPoolResponse:
        """This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        Creates a new Amazon Cognito user pool and sets the password policy for
        the pool.

        If you don't provide a value for an attribute, Amazon Cognito sets it to
        its default value.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param pool_name: A string used to name the user pool.
        :param policies: The policies associated with the new user pool.
        :param deletion_protection: When active, ``DeletionProtection`` prevents accidental deletion of your
        user pool.
        :param lambda_config: A collection of user pool Lambda triggers.
        :param auto_verified_attributes: The attributes to be auto-verified.
        :param alias_attributes: Attributes supported as an alias for this user pool.
        :param username_attributes: Specifies whether a user can use an email address or phone number as a
        username when they sign up.
        :param sms_verification_message: This parameter is no longer used.
        :param email_verification_message: This parameter is no longer used.
        :param email_verification_subject: This parameter is no longer used.
        :param verification_message_template: The template for the verification message that your user pool delivers
        to users who set an email address or phone number attribute.
        :param sms_authentication_message: A string representing the SMS authentication message.
        :param mfa_configuration: Specifies MFA configuration details.
        :param user_attribute_update_settings: The settings for updates to user attributes.
        :param device_configuration: The device-remembering configuration for a user pool.
        :param email_configuration: The email configuration of your user pool.
        :param sms_configuration: The SMS configuration with the settings that your Amazon Cognito user
        pool must use to send an SMS message from your Amazon Web Services
        account through Amazon Simple Notification Service.
        :param user_pool_tags: The tag keys and values to assign to the user pool.
        :param admin_create_user_config: The configuration for ``AdminCreateUser`` requests.
        :param schema: An array of schema attributes for the new user pool.
        :param user_pool_add_ons: User pool add-ons.
        :param username_configuration: Case sensitivity on the username input for the selected sign-in option.
        :param account_recovery_setting: The available verified method a user can use to recover their password
        when they call ``ForgotPassword``.
        :param user_pool_tier: The user pool `feature
        plan <https://docs.
        :returns: CreateUserPoolResponse
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises NotAuthorizedException:
        :raises UserPoolTaggingException:
        :raises InternalErrorException:
        :raises TierChangeNotAllowedException:
        :raises FeatureUnavailableInTierException:
        """
        raise NotImplementedError

    @handler("CreateUserPoolClient")
    def create_user_pool_client(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_name: ClientNameType,
        generate_secret: GenerateSecret = None,
        refresh_token_validity: RefreshTokenValidityType = None,
        access_token_validity: AccessTokenValidityType = None,
        id_token_validity: IdTokenValidityType = None,
        token_validity_units: TokenValidityUnitsType = None,
        read_attributes: ClientPermissionListType = None,
        write_attributes: ClientPermissionListType = None,
        explicit_auth_flows: ExplicitAuthFlowsListType = None,
        supported_identity_providers: SupportedIdentityProvidersListType = None,
        callback_urls: CallbackURLsListType = None,
        logout_urls: LogoutURLsListType = None,
        default_redirect_uri: RedirectUrlType = None,
        allowed_o_auth_flows: OAuthFlowsType = None,
        allowed_o_auth_scopes: ScopeListType = None,
        allowed_o_auth_flows_user_pool_client: BooleanType = None,
        analytics_configuration: AnalyticsConfigurationType = None,
        prevent_user_existence_errors: PreventUserExistenceErrorTypes = None,
        enable_token_revocation: WrappedBooleanType = None,
        enable_propagate_additional_user_context_data: WrappedBooleanType = None,
        auth_session_validity: AuthSessionValidityType = None,
        **kwargs,
    ) -> CreateUserPoolClientResponse:
        """Creates the user pool client.

        When you create a new user pool client, token revocation is
        automatically activated. For more information about revoking tokens, see
        `RevokeToken <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RevokeToken.html>`__.

        If you don't provide a value for an attribute, Amazon Cognito sets it to
        its default value.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to create a user pool
        client.
        :param client_name: The client name for the user pool client you would like to create.
        :param generate_secret: Boolean to specify whether you want to generate a secret for the user
        pool client being created.
        :param refresh_token_validity: The refresh token time limit.
        :param access_token_validity: The access token time limit.
        :param id_token_validity: The ID token time limit.
        :param token_validity_units: The units in which the validity times are represented.
        :param read_attributes: The list of user attributes that you want your app client to have read
        access to.
        :param write_attributes: The list of user attributes that you want your app client to have write
        access to.
        :param explicit_auth_flows: The authentication flows that you want your user pool client to support.
        :param supported_identity_providers: A list of provider names for the identity providers (IdPs) that are
        supported on this client.
        :param callback_urls: A list of allowed redirect (callback) URLs for the IdPs.
        :param logout_urls: A list of allowed logout URLs for the IdPs.
        :param default_redirect_uri: The default redirect URI.
        :param allowed_o_auth_flows: The OAuth grant types that you want your app client to generate.
        :param allowed_o_auth_scopes: The allowed OAuth scopes.
        :param allowed_o_auth_flows_user_pool_client: Set to ``true`` to use OAuth 2.
        :param analytics_configuration: The user pool analytics configuration for collecting metrics and sending
        them to your Amazon Pinpoint campaign.
        :param prevent_user_existence_errors: Errors and responses that you want Amazon Cognito APIs to return during
        authentication, account confirmation, and password recovery when the
        user doesn't exist in the user pool.
        :param enable_token_revocation: Activates or deactivates token revocation.
        :param enable_propagate_additional_user_context_data: Activates the propagation of additional user context data.
        :param auth_session_validity: Amazon Cognito creates a session token for each API request in an
        authentication flow.
        :returns: CreateUserPoolClientResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises NotAuthorizedException:
        :raises ScopeDoesNotExistException:
        :raises InvalidOAuthFlowException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("CreateUserPoolDomain")
    def create_user_pool_domain(
        self,
        context: RequestContext,
        domain: DomainType,
        user_pool_id: UserPoolIdType,
        managed_login_version: WrappedIntegerType = None,
        custom_domain_config: CustomDomainConfigType = None,
        **kwargs,
    ) -> CreateUserPoolDomainResponse:
        """Creates a new domain for a user pool. The domain hosts user pool domain
        services like managed login, the hosted UI (classic), and the user pool
        authorization server.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param domain: The domain string.
        :param user_pool_id: The ID of the user pool where you want to add a domain.
        :param managed_login_version: The version of managed login branding that you want to apply to your
        domain.
        :param custom_domain_config: The configuration for a custom domain that hosts the sign-up and sign-in
        webpages for your application.
        :returns: CreateUserPoolDomainResponse
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        :raises InternalErrorException:
        :raises FeatureUnavailableInTierException:
        """
        raise NotImplementedError

    @handler("DeleteGroup")
    def delete_group(
        self,
        context: RequestContext,
        group_name: GroupNameType,
        user_pool_id: UserPoolIdType,
        **kwargs,
    ) -> None:
        """Deletes a group.

        Calling this action requires developer credentials.

        :param group_name: The name of the group.
        :param user_pool_id: The user pool ID for the user pool.
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DeleteIdentityProvider")
    def delete_identity_provider(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        provider_name: ProviderNameType,
        **kwargs,
    ) -> None:
        """Deletes an IdP for a user pool.

        :param user_pool_id: The user pool ID.
        :param provider_name: The IdP name.
        :raises InvalidParameterException:
        :raises UnsupportedIdentityProviderException:
        :raises ConcurrentModificationException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DeleteManagedLoginBranding")
    def delete_managed_login_branding(
        self,
        context: RequestContext,
        managed_login_branding_id: ManagedLoginBrandingIdType,
        user_pool_id: UserPoolIdType,
        **kwargs,
    ) -> None:
        """Deletes a managed login branding style. When you delete a style, you
        delete the branding association for an app client and restore it to
        default settings.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param managed_login_branding_id: The ID of the managed login branding style that you want to delete.
        :param user_pool_id: The ID of the user pool that contains the managed login branding style
        that you want to delete.
        :raises ResourceNotFoundException:
        :raises ConcurrentModificationException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DeleteResourceServer")
    def delete_resource_server(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        identifier: ResourceServerIdentifierType,
        **kwargs,
    ) -> None:
        """Deletes a resource server.

        :param user_pool_id: The user pool ID for the user pool that hosts the resource server.
        :param identifier: The identifier for the resource server.
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DeleteUser")
    def delete_user(self, context: RequestContext, access_token: TokenModelType, **kwargs) -> None:
        """Allows a user to delete their own user profile.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose user
        profile you want to delete.
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteUserAttributes")
    def delete_user_attributes(
        self,
        context: RequestContext,
        user_attribute_names: AttributeNameListType,
        access_token: TokenModelType,
        **kwargs,
    ) -> DeleteUserAttributesResponse:
        """Deletes the attributes for a user.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param user_attribute_names: An array of strings representing the user attribute names you want to
        delete.
        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        attributes you want to delete.
        :returns: DeleteUserAttributesResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteUserPool")
    def delete_user_pool(
        self, context: RequestContext, user_pool_id: UserPoolIdType, **kwargs
    ) -> None:
        """Deletes the specified Amazon Cognito user pool.

        :param user_pool_id: The user pool ID for the user pool you want to delete.
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserImportInProgressException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DeleteUserPoolClient")
    def delete_user_pool_client(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType,
        **kwargs,
    ) -> None:
        """Allows the developer to delete the user pool client.

        :param user_pool_id: The user pool ID for the user pool where you want to delete the client.
        :param client_id: The app client ID of the app associated with the user pool.
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises ConcurrentModificationException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DeleteUserPoolDomain")
    def delete_user_pool_domain(
        self, context: RequestContext, domain: DomainType, user_pool_id: UserPoolIdType, **kwargs
    ) -> DeleteUserPoolDomainResponse:
        """Deletes a domain for a user pool.

        :param domain: The domain string.
        :param user_pool_id: The user pool ID.
        :returns: DeleteUserPoolDomainResponse
        :raises NotAuthorizedException:
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DeleteWebAuthnCredential")
    def delete_web_authn_credential(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        credential_id: StringType,
        **kwargs,
    ) -> DeleteWebAuthnCredentialResponse:
        """Deletes a registered passkey, or webauthN, device for the currently
        signed-in user.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        passkey you want to delete.
        :param credential_id: The unique identifier of the passkey that you want to delete.
        :returns: DeleteWebAuthnCredentialResponse
        :raises ForbiddenException:
        :raises InternalErrorException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeIdentityProvider")
    def describe_identity_provider(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        provider_name: ProviderNameType,
        **kwargs,
    ) -> DescribeIdentityProviderResponse:
        """Gets information about a specific IdP.

        :param user_pool_id: The user pool ID.
        :param provider_name: The IdP name.
        :returns: DescribeIdentityProviderResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DescribeManagedLoginBranding")
    def describe_managed_login_branding(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        managed_login_branding_id: ManagedLoginBrandingIdType,
        return_merged_resources: BooleanType = None,
        **kwargs,
    ) -> DescribeManagedLoginBrandingResponse:
        """When given the ID of a managed login branding style, returns detailed
        information about the style.

        :param user_pool_id: The ID of the user pool that contains the managed login branding style
        that you want to get information about.
        :param managed_login_branding_id: The ID of the managed login branding style that you want to get more
        information about.
        :param return_merged_resources: When ``true``, returns values for branding options that are unchanged
        from Amazon Cognito defaults.
        :returns: DescribeManagedLoginBrandingResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DescribeManagedLoginBrandingByClient")
    def describe_managed_login_branding_by_client(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType,
        return_merged_resources: BooleanType = None,
        **kwargs,
    ) -> DescribeManagedLoginBrandingByClientResponse:
        """When given the ID of a user pool app client, returns detailed
        information about the style assigned to the app client.

        :param user_pool_id: The ID of the user pool that contains the app client where you want more
        information about the managed login branding style.
        :param client_id: The app client that's assigned to the branding style that you want more
        information about.
        :param return_merged_resources: When ``true``, returns values for branding options that are unchanged
        from Amazon Cognito defaults.
        :returns: DescribeManagedLoginBrandingByClientResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DescribeResourceServer")
    def describe_resource_server(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        identifier: ResourceServerIdentifierType,
        **kwargs,
    ) -> DescribeResourceServerResponse:
        """Describes a resource server.

        :param user_pool_id: The user pool ID for the user pool that hosts the resource server.
        :param identifier: A unique resource server identifier for the resource server.
        :returns: DescribeResourceServerResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DescribeRiskConfiguration")
    def describe_risk_configuration(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType = None,
        **kwargs,
    ) -> DescribeRiskConfigurationResponse:
        """Describes the risk configuration.

        :param user_pool_id: The user pool ID.
        :param client_id: The app client ID.
        :returns: DescribeRiskConfigurationResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserPoolAddOnNotEnabledException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DescribeUserImportJob")
    def describe_user_import_job(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        job_id: UserImportJobIdType,
        **kwargs,
    ) -> DescribeUserImportJobResponse:
        """Describes the user import job.

        :param user_pool_id: The user pool ID for the user pool that the users are being imported
        into.
        :param job_id: The job ID for the user import job.
        :returns: DescribeUserImportJobResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DescribeUserPool")
    def describe_user_pool(
        self, context: RequestContext, user_pool_id: UserPoolIdType, **kwargs
    ) -> DescribeUserPoolResponse:
        """Returns the configuration information and metadata of the specified user
        pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool you want to describe.
        :returns: DescribeUserPoolResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserPoolTaggingException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DescribeUserPoolClient")
    def describe_user_pool_client(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType,
        **kwargs,
    ) -> DescribeUserPoolClientResponse:
        """Client method for returning the configuration information and metadata
        of the specified user pool app client.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool you want to describe.
        :param client_id: The app client ID of the app associated with the user pool.
        :returns: DescribeUserPoolClientResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("DescribeUserPoolDomain")
    def describe_user_pool_domain(
        self, context: RequestContext, domain: DomainType, **kwargs
    ) -> DescribeUserPoolDomainResponse:
        """Gets information about a domain.

        :param domain: The domain string.
        :returns: DescribeUserPoolDomainResponse
        :raises NotAuthorizedException:
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ForgetDevice")
    def forget_device(
        self,
        context: RequestContext,
        device_key: DeviceKeyType,
        access_token: TokenModelType = None,
        **kwargs,
    ) -> None:
        """Forgets the specified device. For more information about device
        authentication, see `Working with user devices in your user
        pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`__.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param device_key: The device key.
        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        registered device you want to forget.
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InvalidUserPoolConfigurationException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ForgotPassword")
    def forgot_password(
        self,
        context: RequestContext,
        client_id: ClientIdType,
        username: UsernameType,
        secret_hash: SecretHashType = None,
        user_context_data: UserContextDataType = None,
        analytics_metadata: AnalyticsMetadataType = None,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> ForgotPasswordResponse:
        """Calling this API causes a message to be sent to the end user with a
        confirmation code that is required to change the user's password. For
        the ``Username`` parameter, you can use the username or user alias. The
        method used to send the confirmation code is sent according to the
        specified AccountRecoverySetting. For more information, see `Recovering
        User
        Accounts <https://docs.aws.amazon.com/cognito/latest/developerguide/how-to-recover-a-user-account.html>`__
        in the *Amazon Cognito Developer Guide*. To use the confirmation code
        for resetting the password, call
        `ConfirmForgotPassword <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ConfirmForgotPassword.html>`__.

        If neither a verified phone number nor a verified email exists, this API
        returns ``InvalidParameterException``. If your app client has a client
        secret and you don't provide a ``SECRET_HASH`` parameter, this API
        returns ``NotAuthorizedException``.

        To use this API operation, your user pool must have self-service account
        recovery configured. Use
        `AdminSetUserPassword <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminSetUserPassword.html>`__
        if you manage passwords as an administrator.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        :param client_id: The ID of the client associated with the user pool.
        :param username: The username of the user that you want to query or modify.
        :param secret_hash: A keyed-hash message authentication code (HMAC) calculated using the
        secret key of a user pool client and username plus the client ID in the
        message.
        :param user_context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param analytics_metadata: The Amazon Pinpoint analytics metadata that contributes to your metrics
        for ``ForgotPassword`` calls.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: ForgotPasswordResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises NotAuthorizedException:
        :raises InvalidLambdaResponseException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises CodeDeliveryFailureException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("GetCSVHeader")
    def get_csv_header(
        self, context: RequestContext, user_pool_id: UserPoolIdType, **kwargs
    ) -> GetCSVHeaderResponse:
        """Gets the header information for the comma-separated value (CSV) file to
        be used as input for the user import job.

        :param user_pool_id: The user pool ID for the user pool that the users are to be imported
        into.
        :returns: GetCSVHeaderResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("GetDevice")
    def get_device(
        self,
        context: RequestContext,
        device_key: DeviceKeyType,
        access_token: TokenModelType = None,
        **kwargs,
    ) -> GetDeviceResponse:
        """Gets the device. For more information about device authentication, see
        `Working with user devices in your user
        pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`__.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param device_key: The device key.
        :param access_token: A valid access token that Amazon Cognito issued to the user whose device
        information you want to request.
        :returns: GetDeviceResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises InvalidUserPoolConfigurationException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("GetGroup")
    def get_group(
        self,
        context: RequestContext,
        group_name: GroupNameType,
        user_pool_id: UserPoolIdType,
        **kwargs,
    ) -> GetGroupResponse:
        """Gets a group.

        Calling this action requires developer credentials.

        :param group_name: The name of the group.
        :param user_pool_id: The user pool ID for the user pool.
        :returns: GetGroupResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("GetIdentityProviderByIdentifier")
    def get_identity_provider_by_identifier(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        idp_identifier: IdpIdentifierType,
        **kwargs,
    ) -> GetIdentityProviderByIdentifierResponse:
        """Gets the specified IdP.

        :param user_pool_id: The user pool ID.
        :param idp_identifier: The IdP identifier.
        :returns: GetIdentityProviderByIdentifierResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("GetLogDeliveryConfiguration")
    def get_log_delivery_configuration(
        self, context: RequestContext, user_pool_id: UserPoolIdType, **kwargs
    ) -> GetLogDeliveryConfigurationResponse:
        """Gets the logging configuration of a user pool.

        :param user_pool_id: The ID of the user pool that has the logging configuration that you want
        to view.
        :returns: GetLogDeliveryConfigurationResponse
        :raises InvalidParameterException:
        :raises InternalErrorException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetSigningCertificate")
    def get_signing_certificate(
        self, context: RequestContext, user_pool_id: UserPoolIdType, **kwargs
    ) -> GetSigningCertificateResponse:
        """This method takes a user pool ID, and returns the signing certificate.
        The issued certificate is valid for 10 years from the date of issue.

        Amazon Cognito issues and assigns a new signing certificate annually.
        This process returns a new value in the response to
        ``GetSigningCertificate``, but doesn't invalidate the original
        certificate.

        :param user_pool_id: The user pool ID.
        :returns: GetSigningCertificateResponse
        :raises InternalErrorException:
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetUICustomization")
    def get_ui_customization(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType = None,
        **kwargs,
    ) -> GetUICustomizationResponse:
        """Gets the user interface (UI) Customization information for a particular
        app client's app UI, if any such information exists for the client. If
        nothing is set for the particular client, but there is an existing pool
        level customization (the app ``clientId`` is ``ALL``), then that
        information is returned. If nothing is present, then an empty shape is
        returned.

        :param user_pool_id: The user pool ID for the user pool.
        :param client_id: The client ID for the client app.
        :returns: GetUICustomizationResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("GetUser")
    def get_user(
        self, context: RequestContext, access_token: TokenModelType, **kwargs
    ) -> GetUserResponse:
        """Gets the user attributes and metadata for a user.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A non-expired access token for the user whose information you want to
        query.
        :returns: GetUserResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("GetUserAttributeVerificationCode")
    def get_user_attribute_verification_code(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        attribute_name: AttributeNameType,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> GetUserAttributeVerificationCodeResponse:
        """Generates a user attribute verification code for the specified attribute
        name. Sends a message to a user with a code that they must return in a
        VerifyUserAttribute request.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        :param access_token: A non-expired access token for the user whose attribute verification
        code you want to generate.
        :param attribute_name: The attribute name returned by the server response to get the user
        attribute verification code.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: GetUserAttributeVerificationCodeResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises InvalidLambdaResponseException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises CodeDeliveryFailureException:
        :raises LimitExceededException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("GetUserAuthFactors")
    def get_user_auth_factors(
        self, context: RequestContext, access_token: TokenModelType, **kwargs
    ) -> GetUserAuthFactorsResponse:
        """Lists the authentication options for the currently signed-in user.
        Returns the following:

        #. The user's multi-factor authentication (MFA) preferences.

        #. The user's options in the ``USER_AUTH`` flow that they can select in
           a ``SELECT_CHALLENGE`` response or request in a
           ``PREFERRED_CHALLENGE`` request.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        authentication factors you want to view.
        :returns: GetUserAuthFactorsResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("GetUserPoolMfaConfig")
    def get_user_pool_mfa_config(
        self, context: RequestContext, user_pool_id: UserPoolIdType, **kwargs
    ) -> GetUserPoolMfaConfigResponse:
        """Gets the user pool multi-factor authentication (MFA) configuration.

        :param user_pool_id: The user pool ID.
        :returns: GetUserPoolMfaConfigResponse
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("GlobalSignOut")
    def global_sign_out(
        self, context: RequestContext, access_token: TokenModelType, **kwargs
    ) -> GlobalSignOutResponse:
        """Invalidates the identity, access, and refresh tokens that Amazon Cognito
        issued to a user. Call this operation when your user signs out of your
        app. This results in the following behavior.

        -  Amazon Cognito no longer accepts *token-authorized* user operations
           that you authorize with a signed-out user's access tokens. For more
           information, see `Using the Amazon Cognito user pools API and user
           pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

           Amazon Cognito returns an ``Access Token has been revoked`` error
           when your app attempts to authorize a user pools API request with a
           revoked access token that contains the scope
           ``aws.cognito.signin.user.admin``.

        -  Amazon Cognito no longer accepts a signed-out user's ID token in a
           `GetId <https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_GetId.html>`__
           request to an identity pool with ``ServerSideTokenCheck`` enabled for
           its user pool IdP configuration in
           `CognitoIdentityProvider <https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_CognitoIdentityProvider.html>`__.

        -  Amazon Cognito no longer accepts a signed-out user's refresh tokens
           in refresh requests.

        Other requests might be valid until your user's token expires.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user who you want
        to sign out.
        :returns: GlobalSignOutResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("InitiateAuth")
    def initiate_auth(
        self,
        context: RequestContext,
        auth_flow: AuthFlowType,
        client_id: ClientIdType,
        auth_parameters: AuthParametersType = None,
        client_metadata: ClientMetadataType = None,
        analytics_metadata: AnalyticsMetadataType = None,
        user_context_data: UserContextDataType = None,
        session: SessionType = None,
        **kwargs,
    ) -> InitiateAuthResponse:
        """Initiates sign-in for a user in the Amazon Cognito user directory. You
        can't sign in a user with a federated IdP with ``InitiateAuth``. For
        more information, see `Adding user pool sign-in through a third
        party <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-identity-federation.html>`__.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        :param auth_flow: The authentication flow that you want to initiate.
        :param client_id: The app client ID.
        :param auth_parameters: The authentication parameters.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for
        certain custom workflows that this action triggers.
        :param analytics_metadata: The Amazon Pinpoint analytics metadata that contributes to your metrics
        for ``InitiateAuth`` calls.
        :param user_context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param session: The optional session ID from a ``ConfirmSignUp`` API request.
        :returns: InitiateAuthResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises UnexpectedLambdaException:
        :raises InvalidUserPoolConfigurationException:
        :raises UserLambdaValidationException:
        :raises InvalidLambdaResponseException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListDevices")
    def list_devices(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        limit: QueryLimitType = None,
        pagination_token: SearchPaginationTokenType = None,
        **kwargs,
    ) -> ListDevicesResponse:
        """Lists the sign-in devices that Amazon Cognito has registered to the
        current user. For more information about device authentication, see
        `Working with user devices in your user
        pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`__.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose list
        of devices you want to view.
        :param limit: The limit of the device request.
        :param pagination_token: This API operation returns a limited number of results.
        :returns: ListDevicesResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises InvalidUserPoolConfigurationException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListGroups")
    def list_groups(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        limit: QueryLimitType = None,
        next_token: PaginationKey = None,
        **kwargs,
    ) -> ListGroupsResponse:
        """Lists the groups associated with a user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param limit: The limit of the request to list groups.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :returns: ListGroupsResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListIdentityProviders")
    def list_identity_providers(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        max_results: ListProvidersLimitType = None,
        next_token: PaginationKeyType = None,
        **kwargs,
    ) -> ListIdentityProvidersResponse:
        """Lists information about all IdPs for a user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param max_results: The maximum number of IdPs to return.
        :param next_token: A pagination token.
        :returns: ListIdentityProvidersResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListResourceServers")
    def list_resource_servers(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        max_results: ListResourceServersLimitType = None,
        next_token: PaginationKeyType = None,
        **kwargs,
    ) -> ListResourceServersResponse:
        """Lists the resource servers for a user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param max_results: The maximum number of resource servers to return.
        :param next_token: A pagination token.
        :returns: ListResourceServersResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: ArnType, **kwargs
    ) -> ListTagsForResourceResponse:
        """Lists the tags that are assigned to an Amazon Cognito user pool.

        A tag is a label that you can apply to user pools to categorize and
        manage them in different ways, such as by purpose, owner, environment,
        or other criteria.

        You can use this action up to 10 times per second, per account.

        :param resource_arn: The Amazon Resource Name (ARN) of the user pool that the tags are
        assigned to.
        :returns: ListTagsForResourceResponse
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InvalidParameterException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListUserImportJobs")
    def list_user_import_jobs(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        max_results: PoolQueryLimitType,
        pagination_token: PaginationKeyType = None,
        **kwargs,
    ) -> ListUserImportJobsResponse:
        """Lists user import jobs for a user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool that the users are being imported
        into.
        :param max_results: The maximum number of import jobs you want the request to return.
        :param pagination_token: This API operation returns a limited number of results.
        :returns: ListUserImportJobsResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListUserPoolClients")
    def list_user_pool_clients(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        max_results: QueryLimit = None,
        next_token: PaginationKey = None,
        **kwargs,
    ) -> ListUserPoolClientsResponse:
        """Lists the clients that have been created for the specified user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to list user pool
        clients.
        :param max_results: The maximum number of results you want the request to return when
        listing the user pool clients.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :returns: ListUserPoolClientsResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListUserPools")
    def list_user_pools(
        self,
        context: RequestContext,
        max_results: PoolQueryLimitType,
        next_token: PaginationKeyType = None,
        **kwargs,
    ) -> ListUserPoolsResponse:
        """Lists the user pools associated with an Amazon Web Services account.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param max_results: The maximum number of results you want the request to return when
        listing the user pools.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :returns: ListUserPoolsResponse
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListUsers")
    def list_users(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        attributes_to_get: SearchedAttributeNamesListType = None,
        limit: QueryLimitType = None,
        pagination_token: SearchPaginationTokenType = None,
        filter: UserFilterType = None,
        **kwargs,
    ) -> ListUsersResponse:
        """Lists users and their basic details in a user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool on which the search should be
        performed.
        :param attributes_to_get: A JSON array of user attribute names, for example ``given_name``, that
        you want Amazon Cognito to include in the response for each user.
        :param limit: Maximum number of users to be returned.
        :param pagination_token: This API operation returns a limited number of results.
        :param filter: A filter string of the form
        ``"AttributeName Filter-Type "AttributeValue"``.
        :returns: ListUsersResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListUsersInGroup")
    def list_users_in_group(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        group_name: GroupNameType,
        limit: QueryLimitType = None,
        next_token: PaginationKey = None,
        **kwargs,
    ) -> ListUsersInGroupResponse:
        """Lists the users in the specified group.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param group_name: The name of the group.
        :param limit: The maximum number of users that you want to retrieve before pagination.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :returns: ListUsersInGroupResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("ListWebAuthnCredentials")
    def list_web_authn_credentials(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        next_token: PaginationKey = None,
        max_results: WebAuthnCredentialsQueryLimitType = None,
        **kwargs,
    ) -> ListWebAuthnCredentialsResponse:
        """Generates a list of the current user's registered passkey, or webauthN,
        credentials.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        registered passkeys you want to list.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :param max_results: The maximum number of the user's passkey credentials that you want to
        return.
        :returns: ListWebAuthnCredentialsResponse
        :raises ForbiddenException:
        :raises InternalErrorException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        """
        raise NotImplementedError

    @handler("ResendConfirmationCode")
    def resend_confirmation_code(
        self,
        context: RequestContext,
        client_id: ClientIdType,
        username: UsernameType,
        secret_hash: SecretHashType = None,
        user_context_data: UserContextDataType = None,
        analytics_metadata: AnalyticsMetadataType = None,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> ResendConfirmationCodeResponse:
        """Resends the confirmation (for confirmation of registration) to a
        specific user in the user pool.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        :param client_id: The ID of the client associated with the user pool.
        :param username: The username of the user that you want to query or modify.
        :param secret_hash: A keyed-hash message authentication code (HMAC) calculated using the
        secret key of a user pool client and username plus the client ID in the
        message.
        :param user_context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param analytics_metadata: The Amazon Pinpoint analytics metadata that contributes to your metrics
        for ``ResendConfirmationCode`` calls.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: ResendConfirmationCodeResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises NotAuthorizedException:
        :raises InvalidLambdaResponseException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises CodeDeliveryFailureException:
        :raises UserNotFoundException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("RespondToAuthChallenge")
    def respond_to_auth_challenge(
        self,
        context: RequestContext,
        client_id: ClientIdType,
        challenge_name: ChallengeNameType,
        session: SessionType = None,
        challenge_responses: ChallengeResponsesType = None,
        analytics_metadata: AnalyticsMetadataType = None,
        user_context_data: UserContextDataType = None,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> RespondToAuthChallengeResponse:
        """Some API operations in a user pool generate a challenge, like a prompt
        for an MFA code, for device authentication that bypasses MFA, or for a
        custom authentication challenge. A ``RespondToAuthChallenge`` API
        request provides the answer to that challenge, like a code or a secure
        remote password (SRP). The parameters of a response to an authentication
        challenge vary with the type of challenge.

        For more information about custom authentication challenges, see `Custom
        authentication challenge Lambda
        triggers <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html>`__.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        :param client_id: The app client ID.
        :param challenge_name: The challenge name.
        :param session: The session that should be passed both ways in challenge-response calls
        to the service.
        :param challenge_responses: The responses to the challenge that you received in the previous
        request.
        :param analytics_metadata: The Amazon Pinpoint analytics metadata that contributes to your metrics
        for ``RespondToAuthChallenge`` calls.
        :param user_context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: RespondToAuthChallengeResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises CodeMismatchException:
        :raises ExpiredCodeException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises InvalidPasswordException:
        :raises PasswordHistoryPolicyViolationException:
        :raises InvalidLambdaResponseException:
        :raises TooManyRequestsException:
        :raises InvalidUserPoolConfigurationException:
        :raises MFAMethodNotFoundException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises AliasExistsException:
        :raises InternalErrorException:
        :raises SoftwareTokenMFANotFoundException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("RevokeToken")
    def revoke_token(
        self,
        context: RequestContext,
        token: TokenModelType,
        client_id: ClientIdType,
        client_secret: ClientSecretType = None,
        **kwargs,
    ) -> RevokeTokenResponse:
        """Revokes all of the access tokens generated by, and at the same time as,
        the specified refresh token. After a token is revoked, you can't use the
        revoked token to access Amazon Cognito user APIs, or to authorize access
        to your resource server.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param token: The refresh token that you want to revoke.
        :param client_id: The client ID for the token that you want to revoke.
        :param client_secret: The secret for the client ID.
        :returns: RevokeTokenResponse
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        :raises UnauthorizedException:
        :raises InvalidParameterException:
        :raises UnsupportedOperationException:
        :raises UnsupportedTokenTypeException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("SetLogDeliveryConfiguration")
    def set_log_delivery_configuration(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        log_configurations: LogConfigurationListType,
        **kwargs,
    ) -> SetLogDeliveryConfigurationResponse:
        """Sets up or modifies the logging configuration of a user pool. User pools
        can export user notification logs and advanced security features user
        activity logs.

        :param user_pool_id: The ID of the user pool where you want to configure logging.
        :param log_configurations: A collection of the logging configurations for a user pool.
        :returns: SetLogDeliveryConfigurationResponse
        :raises InvalidParameterException:
        :raises InternalErrorException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises ResourceNotFoundException:
        :raises FeatureUnavailableInTierException:
        """
        raise NotImplementedError

    @handler("SetRiskConfiguration")
    def set_risk_configuration(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType = None,
        compromised_credentials_risk_configuration: CompromisedCredentialsRiskConfigurationType = None,
        account_takeover_risk_configuration: AccountTakeoverRiskConfigurationType = None,
        risk_exception_configuration: RiskExceptionConfigurationType = None,
        **kwargs,
    ) -> SetRiskConfigurationResponse:
        """Configures actions on detected risks. To delete the risk configuration
        for ``UserPoolId`` or ``ClientId``, pass null values for all four
        configuration types.

        To activate Amazon Cognito advanced security features, update the user
        pool to include the ``UserPoolAddOns`` key ``AdvancedSecurityMode``.

        :param user_pool_id: The user pool ID.
        :param client_id: The app client ID.
        :param compromised_credentials_risk_configuration: The compromised credentials risk configuration.
        :param account_takeover_risk_configuration: The account takeover risk configuration.
        :param risk_exception_configuration: The configuration to override the risk decision.
        :returns: SetRiskConfigurationResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserPoolAddOnNotEnabledException:
        :raises CodeDeliveryFailureException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("SetUICustomization")
    def set_ui_customization(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType = None,
        css: CSSType = None,
        image_file: ImageFileType = None,
        **kwargs,
    ) -> SetUICustomizationResponse:
        """Sets the user interface (UI) customization information for a user pool's
        built-in app UI.

        You can specify app UI customization settings for a single client (with
        a specific ``clientId``) or for all clients (by setting the ``clientId``
        to ``ALL``). If you specify ``ALL``, the default configuration is used
        for every client that has no previously set UI customization. If you
        specify UI customization settings for a particular client, it will no
        longer return to the ``ALL`` configuration.

        To use this API, your user pool must have a domain associated with it.
        Otherwise, there is no place to host the app's pages, and the service
        will throw an error.

        :param user_pool_id: The user pool ID for the user pool.
        :param client_id: The client ID for the client app.
        :param css: The CSS values in the UI customization.
        :param image_file: The uploaded logo image for the UI customization.
        :returns: SetUICustomizationResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("SetUserMFAPreference")
    def set_user_mfa_preference(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        sms_mfa_settings: SMSMfaSettingsType = None,
        software_token_mfa_settings: SoftwareTokenMfaSettingsType = None,
        email_mfa_settings: EmailMfaSettingsType = None,
        **kwargs,
    ) -> SetUserMFAPreferenceResponse:
        """Set the user's multi-factor authentication (MFA) method preference,
        including which MFA factors are activated and if any are preferred. Only
        one factor can be set as preferred. The preferred MFA factor will be
        used to authenticate a user if multiple factors are activated. If
        multiple options are activated and no preference is set, a challenge to
        choose an MFA option will be returned during sign-in. If an MFA type is
        activated for a user, the user will be prompted for MFA during all
        sign-in attempts unless device tracking is turned on and the device has
        been trusted. If you want MFA to be applied selectively based on the
        assessed risk level of sign-in attempts, deactivate MFA for users and
        turn on Adaptive Authentication for the user pool.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose MFA
        preference you want to set.
        :param sms_mfa_settings: User preferences for SMS message MFA.
        :param software_token_mfa_settings: User preferences for time-based one-time password (TOTP) MFA.
        :param email_mfa_settings: User preferences for email message MFA.
        :returns: SetUserMFAPreferenceResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("SetUserPoolMfaConfig")
    def set_user_pool_mfa_config(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        sms_mfa_configuration: SmsMfaConfigType = None,
        software_token_mfa_configuration: SoftwareTokenMfaConfigType = None,
        email_mfa_configuration: EmailMfaConfigType = None,
        mfa_configuration: UserPoolMfaType = None,
        web_authn_configuration: WebAuthnConfigurationType = None,
        **kwargs,
    ) -> SetUserPoolMfaConfigResponse:
        """Sets the user pool multi-factor authentication (MFA) and passkey
        configuration.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        :param user_pool_id: The user pool ID.
        :param sms_mfa_configuration: Configures user pool SMS messages for MFA.
        :param software_token_mfa_configuration: Configures a user pool for time-based one-time password (TOTP) MFA.
        :param email_mfa_configuration: Configures user pool email messages for MFA.
        :param mfa_configuration: The MFA configuration.
        :param web_authn_configuration: The configuration of your user pool for passkey, or webauthN,
        authentication and registration.
        :returns: SetUserPoolMfaConfigResponse
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises ConcurrentModificationException:
        :raises ResourceNotFoundException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        :raises FeatureUnavailableInTierException:
        """
        raise NotImplementedError

    @handler("SetUserSettings")
    def set_user_settings(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        mfa_options: MFAOptionListType,
        **kwargs,
    ) -> SetUserSettingsResponse:
        """*This action is no longer supported.* You can use it to configure only
        SMS MFA. You can't use it to configure time-based one-time password
        (TOTP) software token MFA. To configure either type of MFA, use
        `SetUserMFAPreference <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_SetUserMFAPreference.html>`__
        instead.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose user
        settings you want to configure.
        :param mfa_options: You can use this parameter only to set an SMS configuration that uses
        SMS for delivery.
        :returns: SetUserSettingsResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("SignUp")
    def sign_up(
        self,
        context: RequestContext,
        client_id: ClientIdType,
        username: UsernameType,
        secret_hash: SecretHashType = None,
        password: PasswordType = None,
        user_attributes: AttributeListType = None,
        validation_data: AttributeListType = None,
        analytics_metadata: AnalyticsMetadataType = None,
        user_context_data: UserContextDataType = None,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> SignUpResponse:
        """Registers the user in the specified user pool and creates a user name,
        password, and user attributes.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        You might receive a ``LimitExceeded`` exception in response to this
        request if you have exceeded a rate quota for email or SMS messages, and
        if your user pool automatically verifies email addresses or phone
        numbers. When you get this exception in the response, the user is
        successfully created and is in an ``UNCONFIRMED`` state. You can send a
        new code with the
        `ResendConfirmationCode <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_ResendConfirmationCode.html>`__
        request, or confirm the user as an administrator with an
        `AdminConfirmSignUp <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminConfirmSignUp.html>`__
        request.

        :param client_id: The ID of the client associated with the user pool.
        :param username: The username of the user that you want to sign up.
        :param secret_hash: A keyed-hash message authentication code (HMAC) calculated using the
        secret key of a user pool client and username plus the client ID in the
        message.
        :param password: The password of the user you want to register.
        :param user_attributes: An array of name-value pairs representing user attributes.
        :param validation_data: Temporary user attributes that contribute to the outcomes of your pre
        sign-up Lambda trigger.
        :param analytics_metadata: The Amazon Pinpoint analytics metadata that contributes to your metrics
        for ``SignUp`` calls.
        :param user_context_data: Contextual data about your user session, such as the device fingerprint,
        IP address, or location.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action triggers.
        :returns: SignUpResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises NotAuthorizedException:
        :raises InvalidPasswordException:
        :raises InvalidLambdaResponseException:
        :raises UsernameExistsException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        :raises LimitExceededException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises CodeDeliveryFailureException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("StartUserImportJob")
    def start_user_import_job(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        job_id: UserImportJobIdType,
        **kwargs,
    ) -> StartUserImportJobResponse:
        """Starts the user import.

        :param user_pool_id: The user pool ID for the user pool that the users are being imported
        into.
        :param job_id: The job ID for the user import job.
        :returns: StartUserImportJobResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        :raises PreconditionNotMetException:
        :raises NotAuthorizedException:
        """
        raise NotImplementedError

    @handler("StartWebAuthnRegistration")
    def start_web_authn_registration(
        self, context: RequestContext, access_token: TokenModelType, **kwargs
    ) -> StartWebAuthnRegistrationResponse:
        """Requests credential creation options from your user pool for
        registration of a passkey authenticator. Returns information about the
        user pool, the user profile, and authentication requirements. Users must
        provide this information in their request to enroll your application
        with their passkey provider.

        After users present this data and register with their passkey provider,
        return the response to your user pool in a
        `CompleteWebAuthnRegistration <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_CompleteWebAuthnRegistration.html>`__
        API request.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        passkey metadata you want to generate.
        :returns: StartWebAuthnRegistrationResponse
        :raises ForbiddenException:
        :raises InternalErrorException:
        :raises InvalidParameterException:
        :raises LimitExceededException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises WebAuthnNotEnabledException:
        :raises WebAuthnConfigurationMissingException:
        """
        raise NotImplementedError

    @handler("StopUserImportJob")
    def stop_user_import_job(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        job_id: UserImportJobIdType,
        **kwargs,
    ) -> StopUserImportJobResponse:
        """Stops the user import job.

        :param user_pool_id: The user pool ID for the user pool that the users are being imported
        into.
        :param job_id: The job ID for the user import job.
        :returns: StopUserImportJobResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        :raises PreconditionNotMetException:
        :raises NotAuthorizedException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: ArnType, tags: UserPoolTagsType, **kwargs
    ) -> TagResourceResponse:
        """Assigns a set of tags to an Amazon Cognito user pool. A tag is a label
        that you can use to categorize and manage user pools in different ways,
        such as by purpose, owner, environment, or other criteria.

        Each tag consists of a key and value, both of which you define. A key is
        a general category for more specific values. For example, if you have
        two versions of a user pool, one for testing and another for production,
        you might assign an ``Environment`` tag key to both user pools. The
        value of this key might be ``Test`` for one user pool, and
        ``Production`` for the other.

        Tags are useful for cost tracking and access control. You can activate
        your tags so that they appear on the Billing and Cost Management
        console, where you can track the costs associated with your user pools.
        In an Identity and Access Management policy, you can constrain
        permissions for user pools based on specific tags or tag values.

        You can use this action up to 5 times per second, per account. A user
        pool can have as many as 50 tags.

        :param resource_arn: The Amazon Resource Name (ARN) of the user pool to assign the tags to.
        :param tags: The tags to assign to the user pool.
        :returns: TagResourceResponse
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InvalidParameterException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self,
        context: RequestContext,
        resource_arn: ArnType,
        tag_keys: UserPoolTagsListType,
        **kwargs,
    ) -> UntagResourceResponse:
        """Removes the specified tags from an Amazon Cognito user pool. You can use
        this action up to 5 times per second, per account.

        :param resource_arn: The Amazon Resource Name (ARN) of the user pool that the tags are
        assigned to.
        :param tag_keys: The keys of the tags to remove from the user pool.
        :returns: UntagResourceResponse
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InvalidParameterException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("UpdateAuthEventFeedback")
    def update_auth_event_feedback(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        username: UsernameType,
        event_id: EventIdType,
        feedback_token: TokenModelType,
        feedback_value: FeedbackValueType,
        **kwargs,
    ) -> UpdateAuthEventFeedbackResponse:
        """Provides the feedback for an authentication event, whether it was from a
        valid user or not. This feedback is used for improving the risk
        evaluation decision for the user pool as part of Amazon Cognito advanced
        security.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param user_pool_id: The user pool ID.
        :param username: The username of the user that you want to query or modify.
        :param event_id: The event ID.
        :param feedback_token: The feedback token.
        :param feedback_value: The authentication event feedback value.
        :returns: UpdateAuthEventFeedbackResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserNotFoundException:
        :raises UserPoolAddOnNotEnabledException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("UpdateDeviceStatus")
    def update_device_status(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        device_key: DeviceKeyType,
        device_remembered_status: DeviceRememberedStatusType = None,
        **kwargs,
    ) -> UpdateDeviceStatusResponse:
        """Updates the device status. For more information about device
        authentication, see `Working with user devices in your user
        pool <https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-device-tracking.html>`__.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose device
        status you want to update.
        :param device_key: The device key.
        :param device_remembered_status: The status of whether a device is remembered.
        :returns: UpdateDeviceStatusResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises InvalidUserPoolConfigurationException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateGroup")
    def update_group(
        self,
        context: RequestContext,
        group_name: GroupNameType,
        user_pool_id: UserPoolIdType,
        description: DescriptionType = None,
        role_arn: ArnType = None,
        precedence: PrecedenceType = None,
        **kwargs,
    ) -> UpdateGroupResponse:
        """Updates the specified group with the specified attributes.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param group_name: The name of the group.
        :param user_pool_id: The user pool ID for the user pool.
        :param description: A string containing the new description of the group.
        :param role_arn: The new role Amazon Resource Name (ARN) for the group.
        :param precedence: The new precedence value for the group.
        :returns: UpdateGroupResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("UpdateIdentityProvider")
    def update_identity_provider(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        provider_name: ProviderNameType,
        provider_details: ProviderDetailsType = None,
        attribute_mapping: AttributeMappingType = None,
        idp_identifiers: IdpIdentifiersListType = None,
        **kwargs,
    ) -> UpdateIdentityProviderResponse:
        """Updates IdP information for a user pool.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID.
        :param provider_name: The IdP name.
        :param provider_details: The scopes, URLs, and identifiers for your external identity provider.
        :param attribute_mapping: The IdP attribute mapping to be changed.
        :param idp_identifiers: A list of IdP identifiers.
        :returns: UpdateIdentityProviderResponse
        :raises InvalidParameterException:
        :raises UnsupportedIdentityProviderException:
        :raises ResourceNotFoundException:
        :raises ConcurrentModificationException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("UpdateManagedLoginBranding")
    def update_managed_login_branding(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType = None,
        managed_login_branding_id: ManagedLoginBrandingIdType = None,
        use_cognito_provided_values: BooleanType = None,
        settings: Document = None,
        assets: AssetListType = None,
        **kwargs,
    ) -> UpdateManagedLoginBrandingResponse:
        """Configures the branding settings for a user pool style. This operation
        is the programmatic option for the configuration of a style in the
        branding designer.

        Provides values for UI customization in a ``Settings`` JSON object and
        image files in an ``Assets`` array.

        This operation has a 2-megabyte request-size limit and include the CSS
        settings and image assets for your app client. Your branding settings
        might exceed 2MB in size. Amazon Cognito doesn't require that you pass
        all parameters in one request and preserves existing style settings that
        you don't specify. If your request is larger than 2MB, separate it into
        multiple requests, each with a size smaller than the limit.

        For more information, see `API and SDK operations for managed login
        branding <https://docs.aws.amazon.com/cognito/latest/developerguide/managed-login-brandingdesigner.html#branding-designer-api>`__.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The ID of the user pool that contains the managed login branding style
        that you want to update.
        :param managed_login_branding_id: The ID of the managed login branding style that you want to update.
        :param use_cognito_provided_values: When true, applies the default branding style options.
        :param settings: A JSON file, encoded as a ``Document`` type, with the the settings that
        you want to apply to your style.
        :param assets: An array of image files that you want to apply to roles like
        backgrounds, logos, and icons.
        :returns: UpdateManagedLoginBrandingResponse
        :raises ResourceNotFoundException:
        :raises ConcurrentModificationException:
        :raises InvalidParameterException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("UpdateResourceServer")
    def update_resource_server(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        identifier: ResourceServerIdentifierType,
        name: ResourceServerNameType,
        scopes: ResourceServerScopeListType = None,
        **kwargs,
    ) -> UpdateResourceServerResponse:
        """Updates the name and scopes of resource server. All other fields are
        read-only.

        If you don't provide a value for an attribute, it is set to the default
        value.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool.
        :param identifier: A unique resource server identifier for the resource server.
        :param name: The name of the resource server.
        :param scopes: The scope values to be set for the resource server.
        :returns: UpdateResourceServerResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("UpdateUserAttributes")
    def update_user_attributes(
        self,
        context: RequestContext,
        user_attributes: AttributeListType,
        access_token: TokenModelType,
        client_metadata: ClientMetadataType = None,
        **kwargs,
    ) -> UpdateUserAttributesResponse:
        """With this operation, your users can update one or more of their
        attributes with their own credentials. You authorize this API request
        with the user's access token. To delete an attribute from your user,
        submit the attribute in your API request with a blank value. Custom
        attribute values in this request must include the ``custom:`` prefix.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        :param user_attributes: An array of name-value pairs representing user attributes.
        :param access_token: A valid access token that Amazon Cognito issued to the user whose user
        attributes you want to update.
        :param client_metadata: A map of custom key-value pairs that you can provide as input for any
        custom workflows that this action initiates.
        :returns: UpdateUserAttributesResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises CodeMismatchException:
        :raises ExpiredCodeException:
        :raises NotAuthorizedException:
        :raises UnexpectedLambdaException:
        :raises UserLambdaValidationException:
        :raises InvalidLambdaResponseException:
        :raises TooManyRequestsException:
        :raises AliasExistsException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises CodeDeliveryFailureException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateUserPool")
    def update_user_pool(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        policies: UserPoolPolicyType = None,
        deletion_protection: DeletionProtectionType = None,
        lambda_config: LambdaConfigType = None,
        auto_verified_attributes: VerifiedAttributesListType = None,
        sms_verification_message: SmsVerificationMessageType = None,
        email_verification_message: EmailVerificationMessageType = None,
        email_verification_subject: EmailVerificationSubjectType = None,
        verification_message_template: VerificationMessageTemplateType = None,
        sms_authentication_message: SmsVerificationMessageType = None,
        user_attribute_update_settings: UserAttributeUpdateSettingsType = None,
        mfa_configuration: UserPoolMfaType = None,
        device_configuration: DeviceConfigurationType = None,
        email_configuration: EmailConfigurationType = None,
        sms_configuration: SmsConfigurationType = None,
        user_pool_tags: UserPoolTagsType = None,
        admin_create_user_config: AdminCreateUserConfigType = None,
        user_pool_add_ons: UserPoolAddOnsType = None,
        account_recovery_setting: AccountRecoverySettingType = None,
        pool_name: UserPoolNameType = None,
        user_pool_tier: UserPoolTierType = None,
        **kwargs,
    ) -> UpdateUserPoolResponse:
        """This action might generate an SMS text message. Starting June 1, 2021,
        US telecom carriers require you to register an origination phone number
        before you can send SMS messages to US phone numbers. If you use SMS
        text messages in Amazon Cognito, you must register a phone number with
        `Amazon Pinpoint <https://console.aws.amazon.com/pinpoint/home/>`__.
        Amazon Cognito uses the registered number automatically. Otherwise,
        Amazon Cognito users who must receive SMS messages might not be able to
        sign up, activate their accounts, or sign in.

        If you have never used SMS text messages with Amazon Cognito or any
        other Amazon Web Services service, Amazon Simple Notification Service
        might place your account in the SMS sandbox. In `sandbox
        mode <https://docs.aws.amazon.com/sns/latest/dg/sns-sms-sandbox.html>`__
        , you can send messages only to verified phone numbers. After you test
        your app while in the sandbox environment, you can move out of the
        sandbox and into production. For more information, see `SMS message
        settings for Amazon Cognito user
        pools <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html>`__
        in the *Amazon Cognito Developer Guide*.

        Updates the specified user pool with the specified attributes. You can
        get a list of the current user pool settings using
        `DescribeUserPool <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPool.html>`__.

        If you don't provide a value for an attribute, Amazon Cognito sets it to
        its default value.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool you want to update.
        :param policies: A container with the policies you want to update in a user pool.
        :param deletion_protection: When active, ``DeletionProtection`` prevents accidental deletion of your
        user pool.
        :param lambda_config: The Lambda configuration information from the request to update the user
        pool.
        :param auto_verified_attributes: The attributes that are automatically verified when Amazon Cognito
        requests to update user pools.
        :param sms_verification_message: This parameter is no longer used.
        :param email_verification_message: This parameter is no longer used.
        :param email_verification_subject: This parameter is no longer used.
        :param verification_message_template: The template for verification messages.
        :param sms_authentication_message: The contents of the SMS authentication message.
        :param user_attribute_update_settings: The settings for updates to user attributes.
        :param mfa_configuration: Possible values include:

        -  ``OFF`` - MFA tokens aren't required and can't be specified during
           user registration.
        :param device_configuration: The device-remembering configuration for a user pool.
        :param email_configuration: The email configuration of your user pool.
        :param sms_configuration: The SMS configuration with the settings that your Amazon Cognito user
        pool must use to send an SMS message from your Amazon Web Services
        account through Amazon Simple Notification Service.
        :param user_pool_tags: The tag keys and values to assign to the user pool.
        :param admin_create_user_config: The configuration for ``AdminCreateUser`` requests.
        :param user_pool_add_ons: User pool add-ons.
        :param account_recovery_setting: The available verified method a user can use to recover their password
        when they call ``ForgotPassword``.
        :param pool_name: The updated name of your user pool.
        :param user_pool_tier: The user pool `feature
        plan <https://docs.
        :returns: UpdateUserPoolResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises ConcurrentModificationException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises UserImportInProgressException:
        :raises InternalErrorException:
        :raises InvalidSmsRoleAccessPolicyException:
        :raises InvalidSmsRoleTrustRelationshipException:
        :raises UserPoolTaggingException:
        :raises InvalidEmailRoleAccessPolicyException:
        :raises TierChangeNotAllowedException:
        :raises FeatureUnavailableInTierException:
        """
        raise NotImplementedError

    @handler("UpdateUserPoolClient")
    def update_user_pool_client(
        self,
        context: RequestContext,
        user_pool_id: UserPoolIdType,
        client_id: ClientIdType,
        client_name: ClientNameType = None,
        refresh_token_validity: RefreshTokenValidityType = None,
        access_token_validity: AccessTokenValidityType = None,
        id_token_validity: IdTokenValidityType = None,
        token_validity_units: TokenValidityUnitsType = None,
        read_attributes: ClientPermissionListType = None,
        write_attributes: ClientPermissionListType = None,
        explicit_auth_flows: ExplicitAuthFlowsListType = None,
        supported_identity_providers: SupportedIdentityProvidersListType = None,
        callback_urls: CallbackURLsListType = None,
        logout_urls: LogoutURLsListType = None,
        default_redirect_uri: RedirectUrlType = None,
        allowed_o_auth_flows: OAuthFlowsType = None,
        allowed_o_auth_scopes: ScopeListType = None,
        allowed_o_auth_flows_user_pool_client: BooleanType = None,
        analytics_configuration: AnalyticsConfigurationType = None,
        prevent_user_existence_errors: PreventUserExistenceErrorTypes = None,
        enable_token_revocation: WrappedBooleanType = None,
        enable_propagate_additional_user_context_data: WrappedBooleanType = None,
        auth_session_validity: AuthSessionValidityType = None,
        **kwargs,
    ) -> UpdateUserPoolClientResponse:
        """Updates the specified user pool app client with the specified
        attributes. You can get a list of the current user pool app client
        settings using
        `DescribeUserPoolClient <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_DescribeUserPoolClient.html>`__.

        If you don't provide a value for an attribute, Amazon Cognito sets it to
        its default value.

        You can also use this operation to enable token revocation for user pool
        clients. For more information about revoking tokens, see
        `RevokeToken <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RevokeToken.html>`__.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param user_pool_id: The user pool ID for the user pool where you want to update the user
        pool client.
        :param client_id: The ID of the client associated with the user pool.
        :param client_name: The client name from the update user pool client request.
        :param refresh_token_validity: The refresh token time limit.
        :param access_token_validity: The access token time limit.
        :param id_token_validity: The ID token time limit.
        :param token_validity_units: The time units you use when you set the duration of ID, access, and
        refresh tokens.
        :param read_attributes: The list of user attributes that you want your app client to have read
        access to.
        :param write_attributes: The list of user attributes that you want your app client to have write
        access to.
        :param explicit_auth_flows: The authentication flows that you want your user pool client to support.
        :param supported_identity_providers: A list of provider names for the identity providers (IdPs) that are
        supported on this client.
        :param callback_urls: A list of allowed redirect (callback) URLs for the IdPs.
        :param logout_urls: A list of allowed logout URLs for the IdPs.
        :param default_redirect_uri: The default redirect URI.
        :param allowed_o_auth_flows: The allowed OAuth flows.
        :param allowed_o_auth_scopes: The allowed OAuth scopes.
        :param allowed_o_auth_flows_user_pool_client: Set to ``true`` to use OAuth 2.
        :param analytics_configuration: The Amazon Pinpoint analytics configuration necessary to collect metrics
        for this user pool.
        :param prevent_user_existence_errors: Errors and responses that you want Amazon Cognito APIs to return during
        authentication, account confirmation, and password recovery when the
        user doesn't exist in the user pool.
        :param enable_token_revocation: Activates or deactivates token revocation.
        :param enable_propagate_additional_user_context_data: Activates the propagation of additional user context data.
        :param auth_session_validity: Amazon Cognito creates a session token for each API request in an
        authentication flow.
        :returns: UpdateUserPoolClientResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises ConcurrentModificationException:
        :raises TooManyRequestsException:
        :raises NotAuthorizedException:
        :raises ScopeDoesNotExistException:
        :raises InvalidOAuthFlowException:
        :raises InternalErrorException:
        """
        raise NotImplementedError

    @handler("UpdateUserPoolDomain")
    def update_user_pool_domain(
        self,
        context: RequestContext,
        domain: DomainType,
        user_pool_id: UserPoolIdType,
        custom_domain_config: CustomDomainConfigType,
        managed_login_version: WrappedIntegerType = None,
        **kwargs,
    ) -> UpdateUserPoolDomainResponse:
        """Updates the Secure Sockets Layer (SSL) certificate for the custom domain
        for your user pool.

        You can use this operation to provide the Amazon Resource Name (ARN) of
        a new certificate to Amazon Cognito. You can't use it to change the
        domain for a user pool.

        A custom domain is used to host the Amazon Cognito hosted UI, which
        provides sign-up and sign-in pages for your application. When you set up
        a custom domain, you provide a certificate that you manage with
        Certificate Manager (ACM). When necessary, you can use this operation to
        change the certificate that you applied to your custom domain.

        Usually, this is unnecessary following routine certificate renewal with
        ACM. When you renew your existing certificate in ACM, the ARN for your
        certificate remains the same, and your custom domain uses the new
        certificate automatically.

        However, if you replace your existing certificate with a new one, ACM
        gives the new certificate a new ARN. To apply the new certificate to
        your custom domain, you must provide this ARN to Amazon Cognito.

        When you add your new certificate in ACM, you must choose US East (N.
        Virginia) as the Amazon Web Services Region.

        After you submit your request, Amazon Cognito requires up to 1 hour to
        distribute your new certificate to your custom domain.

        For more information about adding a custom domain to your user pool, see
        `Using Your Own Domain for the Hosted
        UI <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html>`__.

        Amazon Cognito evaluates Identity and Access Management (IAM) policies
        in requests for this API operation. For this operation, you must use IAM
        credentials to authorize requests, and you must grant yourself the
        corresponding IAM permission in a policy.

        **Learn more**

        -  `Signing Amazon Web Services API
           Requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html>`__

        -  `Using the Amazon Cognito user pools API and user pool
           endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__

        :param domain: The domain name for the custom domain that hosts the sign-up and sign-in
        pages for your application.
        :param user_pool_id: The ID of the user pool that is associated with the custom domain whose
        certificate you're updating.
        :param custom_domain_config: The configuration for a custom domain that hosts the sign-up and sign-in
        pages for your application.
        :param managed_login_version: A version number that indicates the state of managed login for your
        domain.
        :returns: UpdateUserPoolDomainResponse
        :raises InvalidParameterException:
        :raises NotAuthorizedException:
        :raises ResourceNotFoundException:
        :raises TooManyRequestsException:
        :raises InternalErrorException:
        :raises FeatureUnavailableInTierException:
        """
        raise NotImplementedError

    @handler("VerifySoftwareToken")
    def verify_software_token(
        self,
        context: RequestContext,
        user_code: SoftwareTokenMFAUserCodeType,
        access_token: TokenModelType = None,
        session: SessionType = None,
        friendly_device_name: StringType = None,
        **kwargs,
    ) -> VerifySoftwareTokenResponse:
        """Use this API to register a user's entered time-based one-time password
        (TOTP) code and mark the user's software token MFA status as "verified"
        if successful. The request takes an access token or a session string,
        but not both.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param user_code: The one- time password computed using the secret code returned by
        `AssociateSoftwareToken <https://docs.
        :param access_token: A valid access token that Amazon Cognito issued to the user whose
        software token you want to verify.
        :param session: The session that should be passed both ways in challenge-response calls
        to the service.
        :param friendly_device_name: The friendly device name.
        :returns: VerifySoftwareTokenResponse
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises InvalidUserPoolConfigurationException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises EnableSoftwareTokenMFAException:
        :raises NotAuthorizedException:
        :raises SoftwareTokenMFANotFoundException:
        :raises CodeMismatchException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("VerifyUserAttribute")
    def verify_user_attribute(
        self,
        context: RequestContext,
        access_token: TokenModelType,
        attribute_name: AttributeNameType,
        code: ConfirmationCodeType,
        **kwargs,
    ) -> VerifyUserAttributeResponse:
        """Verifies the specified user attributes in the user pool.

        If your user pool requires verification before Amazon Cognito updates
        the attribute value, VerifyUserAttribute updates the affected attribute
        to its pending value. For more information, see
        `UserAttributeUpdateSettingsType <https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UserAttributeUpdateSettingsType.html>`__.

        Authorize this action with a signed-in user's access token. It must
        include the scope ``aws.cognito.signin.user.admin``.

        Amazon Cognito doesn't evaluate Identity and Access Management (IAM)
        policies in requests for this API operation. For this operation, you
        can't use IAM credentials to authorize requests, and you can't grant IAM
        permissions in policies. For more information about authorization models
        in Amazon Cognito, see `Using the Amazon Cognito user pools API and user
        pool
        endpoints <https://docs.aws.amazon.com/cognito/latest/developerguide/user-pools-API-operations.html>`__.

        :param access_token: A valid access token that Amazon Cognito issued to the user whose user
        attributes you want to verify.
        :param attribute_name: The attribute name in the request to verify user attributes.
        :param code: The verification code in the request to verify user attributes.
        :returns: VerifyUserAttributeResponse
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        :raises CodeMismatchException:
        :raises ExpiredCodeException:
        :raises NotAuthorizedException:
        :raises TooManyRequestsException:
        :raises LimitExceededException:
        :raises PasswordResetRequiredException:
        :raises UserNotFoundException:
        :raises UserNotConfirmedException:
        :raises InternalErrorException:
        :raises AliasExistsException:
        :raises ForbiddenException:
        """
        raise NotImplementedError
