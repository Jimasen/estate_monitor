from app.services.executive_service import revenue_summary
from app.services.pdf_service import generate_pdf

def generate_executive_report(db):
    data = revenue_summary(db)
    return generate_pdf("pdf/owner_report.html", data)
