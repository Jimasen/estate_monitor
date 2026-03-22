from sqlalchemy.orm import configure_mappers

# import all models so SQLAlchemy se# check_models.py
"""
Validate all SQLAlchemy models and their relationships.
Detects mapper errors, missing back_populates, or circular references.
"""

import sys
import traceback
from sqlalchemy.orm import configure_mappers
from sqlalchemy.exc import InvalidRequestError

# Import all your models here
# This ensures they are registered in SQLAlchemy before checking
try:
    from app.models import (
        User,
        Tenant,
        Owner,
        Property,
        RentPayment,
        TenantComment,
        Subscription,
        Transaction,
        Role,
        Estate,
        EntityComment,
        OwnerProfile,
        TenantProfile,
        OwnerComment,
        Audit,
        AuditLog,
        LateFee,
        Pricing,
        RecommendationBlock,
        CarouselAd,
        SubscriptionPayment,
        UserMedia,
        CorporateAccount,
        AppSettings,
        UtilityBill,  # canonical
        Utility       # alias
    )
except Exception as e:
    print("ERROR importing models:", e)
    traceback.print_exc()
    sys.exit(1)

print("✅ All models imported successfully.\n")

# Check mapper configuration
try:
    configure_mappers()
    print("✅ All mappers configured successfully. No mapping errors detected.")
except InvalidRequestError as e:
    print("❌ MAPPER ERROR DETECTED:")
    print(str(e))
    print("\nHint: Check your relationships and back_populates. Ensure that:")
    print("  - All relationship targets exist and are imported before usage.")
    print("  - No class name strings point to aliases instead of canonical models.")
    print("  - Utility alias should not be used as a relationship target.")
    sys.exit(1)
except Exception as e:
    print("❌ Unexpected error during mapper configuration:")
    traceback.print_exc()
    sys.exit(1)

# Optional: Print all mapped classes
try:
    from sqlalchemy.orm import class_mapper
    print("\nMapped classes:")
    for cls in [
        User, Tenant, Owner, Property, RentPayment, TenantComment,
        Subscription, Transaction, Role, Estate, EntityComment,
        OwnerProfile, TenantProfile, OwnerComment, Audit, AuditLog,
        LateFee, Pricing, RecommendationBlock, CarouselAd,
        SubscriptionPayment, UserMedia, CorporateAccount,
        AppSettings, UtilityBill
    ]:
        mapper = class_mapper(cls)
        print(f" - {cls.__name__} -> table: {mapper.tables[0].name}")
except Exception as e:
    print("⚠️ Warning: Could not list mapped classes:", e)
