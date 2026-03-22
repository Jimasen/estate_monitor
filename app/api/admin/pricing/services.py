from sqlalchemy.orm import Session
from app.models.country import Country
from app.models.pricing_plan import PricingPlan
from app.models.country_pricing import CountryPricing
from .schemas import CountryPricingCreate, PricingUpdate


# -------------------------------
# Create new pricing entry
# -------------------------------
def create_pricing(db: Session, pricing: CountryPricingCreate) -> CountryPricing:
    country = db.query(Country).filter(Country.id == pricing.country_id).first()
    plan = db.query(PricingPlan).filter(PricingPlan.id == pricing.plan_id).first()

    if not country or not plan:
        raise ValueError("Country or Plan does not exist")

    new_pricing = CountryPricing(
        country_id=pricing.country_id,
        plan_id=pricing.plan_id,
        monthly_price=pricing.monthly_price,
        yearly_price=pricing.yearly_price,
        promo_price=pricing.promo_price,
        trial_days=pricing.trial_days,
        active=True
    )
    db.add(new_pricing)
    db.commit()
    db.refresh(new_pricing)
    return new_pricing


# -------------------------------
# List all active pricing
# -------------------------------
def get_pricing_list(db: Session):
    pricing_entries = (
        db.query(CountryPricing, PricingPlan, Country)
        .join(PricingPlan, PricingPlan.id == CountryPricing.plan_id)
        .join(Country, Country.id == CountryPricing.country_id)
        .filter(CountryPricing.active == True)
        .all()
    )

    result = []
    for pricing, plan, country in pricing_entries:
        result.append({
            "id": pricing.id,
            "country": {"id": country.id, "name": country.name, "code": country.code, "currency": country.currency},
            "plan": {"id": plan.id, "name": plan.name, "features": plan.features},
            "monthly_price": pricing.monthly_price,
            "yearly_price": pricing.yearly_price,
            "promo_price": pricing.promo_price,
            "trial_days": pricing.trial_days,
            "active": pricing.active
        })
    return result


# -------------------------------
# Update or create pricing
# -------------------------------
def update_pricing(db: Session, data: PricingUpdate):
    # Lookup by country code and plan name (your original style)
    country = db.query(Country).filter(Country.code == data.country_code).first()
    plan = db.query(PricingPlan).filter(PricingPlan.name == data.plan_name).first()

    if not country or not plan:
        return None

    pricing = (
        db.query(CountryPricing)
        .filter(CountryPricing.country_id == country.id)
        .filter(CountryPricing.plan_id == plan.id)
        .first()
    )

    if not pricing:
        pricing = CountryPricing(country_id=country.id, plan_id=plan.id)
        db.add(pricing)

    # Update only provided fields
    if data.monthly_price is not None:
        pricing.monthly_price = data.monthly_price
    if data.yearly_price is not None:
        pricing.yearly_price = data.yearly_price
    if data.promo_price is not None:
        pricing.promo_price = data.promo_price
    if data.trial_days is not None:
        pricing.trial_days = data.trial_days
    if data.active is not None:
        pricing.active = data.active

    db.commit()
    db.refresh(pricing)
    return pricing
