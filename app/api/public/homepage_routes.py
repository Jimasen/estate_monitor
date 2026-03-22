from fastapi import APIRouter

router = APIRouter(prefix="/api/public", tags=["Public"])

@router.get("/homepage")
async def homepage_content():
    return {
        "hero": {
            "title": "Find Your Dream Property",
            "subtitle": "Invest, Buy, or Rent across Africa",
            "image": "/static/images/hero.jpg"
        },
        "features": [
            {
                "title": "Property Marketplace",
                "description": "Buy and sell verified properties",
                "image": "/static/images/feature_marketplace.jpg"
            },
            {
                "title": "Investment Pool",
                "description": "Invest in real estate with others",
                "image": "/static/images/feature_investment.jpg"
            },
            {
                "title": "Property Map",
                "description": "Discover properties visually on the map",
                "image": "/static/images/feature_map.jpg"
            }
        ],
        "footer": {
            "text": "Estate Monitor © 2026"
        }
    }

