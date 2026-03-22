from sqlalchemy.orm import Session
from app.models.pricing import CountryPricing, PricingPlan

def get_country_pricing(db: Session, country_id: int):
    return (
        db.query(CountryPricing, PricingPlan)
        .join(PricingPlan)
        .filter(CountryPricing.country_id==country_id)
        .filter(CountryPricing.active==True)
        .all()
    )
