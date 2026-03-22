from fastapi import APIRouter

router = APIRouter()

@router.get("/homepage")
def get_homepage():

    return {
        "hero_images": [
            {
                "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994",
                "title": "Find Your Dream Property",
                "subtitle": "Buy • Rent • Invest across Africa"
            },
            {
                "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
                "title": "Modern Living",
                "subtitle": "Smart homes for smart investors"
            }
        ],

        "features": [
            {
                "title": "Property Marketplace",
                "icon": "home",
                "description": "Buy verified properties safely"
            },
            {
                "title": "Smart Property Map",
                "icon": "map",
                "description": "Explore properties visually"
            },
            {
                "title": "Investment Pool",
                "icon": "trending",
                "description": "Invest together and earn"
            }
        ],

        "properties": [
            {
                "title": "Luxury Apartment",
                "price": "₦35,000,000",
                "image": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2"
            },
            {
                "title": "Modern Duplex",
                "price": "₦80,000,000",
                "image": "https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4"
            },
            {
                "title": "Smart City Home",
                "price": "₦55,000,000",
                "image": "https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6"
            }
        ]
    }

