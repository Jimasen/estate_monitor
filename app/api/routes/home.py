from fastapi import APIRouter

router = APIRouter(tags=["Home"])

@router.get("/api/home")
async def get_homepage():
    return {
        "blocks": [
            {
                "type": "banner",
                "title": "Welcome to Estate Monitor",
                "image": "https://via.placeholder.com/800x300",
                "size": "large"
            },
            {
                "type": "grid",
                "columns": 4,
                "items": [
                    {"title": "Properties", "image": "https://via.placeholder.com/100"},
                    {"title": "Tenants"},
                    {"title": "Payments"},
                    {"title": "Reports"}
                ]
            },
            {
                "type": "carousel",
                "items": [
                    {"title": "Promo 1", "image": "https://via.placeholder.com/200"},
                    {"title": "Promo 2", "image": "https://via.placeholder.com/200"}
                ]
            }
        ]
    }
