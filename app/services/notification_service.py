from app.core.events import on
from app.services.whatsapp_service import send_whatsapp


@on("tenant_created")
def notify_new_tenant(data):

    message = f"New tenant added: {data['tenant']}"

    send_whatsapp(message)
