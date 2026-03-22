from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.lib.units import inch
import os


def generate_invoice(payment):
    file_path = f"/tmp/invoice_{payment.id}.pdf"

    doc = SimpleDocTemplate(file_path)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Estate Monitor Invoice", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    data = [
        ["Tenant", payment.tenant.full_name],
        ["Amount", f"₦{float(payment.amount_due):,.2f}"],
        ["Due Date", payment.due_date.strftime("%Y-%m-%d")],
        ["Status", payment.status],
    ]

    table = Table(data)
    elements.append(table)

    doc.build(elements)

    return file_path
