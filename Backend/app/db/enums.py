from enum import Enum

class CardBrand(str, Enum):
    VISA = "VISA"
    MASTERCARD = 'MASTERCARD'
    AMEX = "AMEX"

class TransactionStatus(str, Enum):
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    REVERSED = "REVERSED"

class AlertSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class AlertStatus(str, Enum):
    OPEN = "OPEN"
    ACKED = "ACKED"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"

class MerchantCategory(str, Enum):
    GROCERY = "GROCERY"
    GAS = "GAS"
    RESTAURANT = "RESTAURANT"
    TRAVEL = "TRAVEL"
    ONLINE_RETAIL = "ONLINE_RETAIL"

class FindingCode(str, Enum):
    LARGE_AMOUNT = "LARGE_AMOUNT"
    VELOCITY = "VELOCITY"
    IMPOSSIBLE_TRAVEL = "IMPOSSIBLE_TRAVEL"
    NEW_MERCHANT = "NEW_MERCHANT"
    CATEGORY_SPIKE = "CATEGORY_SPIKE"

class AlertActionType(str, Enum):
    ACK = "ACK"
    RESOLVE = "RESOLVE"
    MARK_FALSE_POSITIVE = "MARK_FALSE_POSITIVE"
    ESCALATE = "ESCALATE"

class ActorType(str, Enum):
    USER = "USER"
    ANALYST = "ANALYST"
    SYSTEM = "SYSTEM"

class CardStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    REPLACED = "REPLACED"