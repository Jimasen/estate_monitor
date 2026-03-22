from fastapi import APIRouter

router = APIRouter()

@router.get("/api/banners")
def get_banners():
    return [
        {"image_url": "/static/banners/banner1.jpg"},
        {"image_url": "/static/banners/banner2.jpg"},
        {"image_url": "/static/banners/banner3.jpg"},
        {"image_url": "/static/banners/banner4.jpg"},
    ]

