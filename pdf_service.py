def generate_payment_receipt(payment, db: Session):
    pdf = ReceiptPDF()
    pdf.add_page()
    # ... [rest of PDF content]

    receipt_no = f"EM-{payment.id:06d}"
    filename = RECEIPTS_DIR / f"receipt_{payment.id}.pdf"
    pdf.output(str(filename))

    # Save to DB
    payment.receipt_path = str(filename)
    payment.receipt_number = receipt_no
    db.commit()
    db.refresh(payment)

    return filename, receipt_no
