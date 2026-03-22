# app/models/__init__.py

from .company import Company
from .pricing import Pricing
from .user import User
from .tenant import Tenant
from .owner import Owner
from .property import Property
from .payment import RentPayment
from .page_block import PageBlock
from .tenant_comment import TenantComment
from .subscription import Subscription
from .transaction import Transaction
from .role import Role
from .estate import Estate
from .entity_comment import EntityComment
from .owner_profile import OwnerProfile
from .tenant_profile import TenantProfile
from .owner_comment import OwnerComment
from .audit import Audit
from .audit_log import AuditLog
from .late_fee import LateFee
from .marketing import RecommendationBlock, CarouselAd
from .subscription_payment import SubscriptionPayment
from .user_media import UserMedia
from .corporate import CorporateAccount
from .app_settings import AppSettings
from .utility_bill import UtilityBill

# Optional alias
Utility = UtilityBill

__all__ = [
    "Company",
    "Pricing",
    "User",
    "Tenant",
    "Owner",
    "Property",
    "RentPayment",
    "PageBlock",
    "TenantComment",
    "Subscription",
    "Transaction",
    "Role",
    "Estate",
    "EntityComment",
    "OwnerProfile",
    "TenantProfile",
    "OwnerComment",
    "Audit",
    "AuditLog",
    "LateFee",
    "RecommendationBlock",
    "CarouselAd",
    "SubscriptionPayment",
    "UserMedia",
    "CorporateAccount",
    "AppSettings",
    "UtilityBill",
    "Utility",
]
