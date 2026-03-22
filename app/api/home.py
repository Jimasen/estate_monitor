from fastapi import APIRouter

router = APIRouter()

# Example dynamic home content (later this can come from database)
HOME_CONTENT = {
    "hero": {
        "title": "Welcome to Estate Monitor",
        "subtitle": "Manage properties, tenants, and investments seamlessly across Africa",
        "banner_image": "https://yourcdn.com/images/home_banner.jpg",
        "cta_buttons": [
            {"text": "Get Started", "link": "/login"},
            {"text": "Property Marketplace", "link": "/marketplace"}
        ]
    },
    "features": [
        {"title": "Property Manager Tools", "items": [
            "Lease management",
            "Tenant screening",
            "Maintenance tracking"
        ]},
        {"title": "Reporting", "items": [
            "Profit reports",
            "Occupancy reports",
            "Tax-ready financial reports"
        ]},
        {"title": "Maintenance Marketplace", "items": [
            "Plumbers",
            "Electricians",
            "Cleaners",
            "Security services"
        ]}
    ],
    "testimonials": [
        {
            "name": "Jane Doe",
            "role": "Property Manager",
            "text": "Estate Monitor simplified managing multiple properties and tenants in one app.",
            "image": "https://yourcdn.com/images/testimonial1.jpg"
        },
        {
            "name": "John Smith",
            "role": "Investor",
            "text": "Investing in properties through Estate Monitor was seamless and secure.",
            "image": "https://yourcdn.com/images/testimonial2.jpg"
        }
    ],
    "call_to_action": {
        "title": "Ready to take control of your properties?",
        "buttons": [
            {"text": "Sign Up", "link": "/login"},
            {"text": "Explore Marketplace", "link": "/marketplace"}
        ]
    }
}

@router.get("/home")
def get_home():
    """
    Returns dynamic home page content.
    Flutter app will consume this JSON to render home screen sections.
    """
    return HOME_CONTENT

