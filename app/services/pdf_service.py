# app/services/pdf_service.py

from fpdf import FPDF
from pathlib import Path
from datetime import datetime

from app.services.email_service import send_email
from app.models.payment import RentPayment
from app.database.session import get_db
from sqlalchemy.orm import Session

# Directories and constants
RECEIPTS_DIR = Path("storage/receipts")
RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)

LOGO_PATH = Path("app/static/images/logo.png")
COMPANY_NAME = "Estate Monitor"


class ReceiptPDF(FPDF):
    def header(self):
        if LOGO_PATH.exists():
            self.image(str(LOGO_PATH), x=10, y=8, w=30)
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, COMPANY_NAME, ln=True, align="R")
        self.ln(15)


def generate_payment_receipt(payment: RentPayment):
    """Generates a PDF receipt and returns its path and receipt number."""
    pdf = ReceiptPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    receipt_no = f"EM-{payment.id:06d}"

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Payment Receipt", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"Receipt No: {receipt_no}", ln=True)
    pdf.cell(0, 8, f"Tenant: {payment.tenant.tenant.full_name}", ln=True)
    pdf.cell(0, 8, f"Email: {payment.tenant.tenant.email}", ln=True)
    pdf.cell(0, 8, f"Amount Paid: ₦{payment.amount_paid}", ln=True)
    pdf.cell(
        0,
        8,
        f"Date: {payment.paid_at.strftime('%Y-%m-%d %H:%M')}",
        ln=True,
    )

    pdf.ln(15)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 8, "Thank you for your payment.", ln=True, align="C")

    filename = RECEIPTS_DIR / f"receipt_{payment.id}.pdf"
    pdf.output(str(filename))

    # Save receipt info directly into the DB
    db: Session = get_db()
    payment.receipt_path = str(filename)
    payment.receipt_number = receipt_no
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return filename, receipt_no


def send_payment_receipt(payment: RentPayment):
    """Generate receipt PDF (if not already) and send via email."""
    # If receipt already exists, use it; else generate
    if not payment.receipt_path or not payment.receipt_number:
        pdf_file, receipt_no = generate_payment_receipt(payment)
    else:
        pdf_file = Path(payment.receipt_path)
        receipt_no = payment.receipt_number

    send_email(
        to_email=payment.tenant.tenant.email,
        subject=f"Payment Receipt {receipt_no}",
        body=(
            f"Hello {payment.tenant.tenant.full_name},\n\n"
            f"Attached is your payment receipt ({receipt_no}).\n\n"
            "Thank you for your business.\n\n"
            f"{COMPANY_NAME}"
        ),
        attachments=[str(pdf_file)],
    )

    return pdf_file
