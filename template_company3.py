from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, white, HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
import os
import json

# Register Arabic font
pdfmetrics.registerFont(TTFont('ArabicFont', 'Amiri-Regular.ttf'))

def arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

def convert_to_arabic_numerals(text):
    arabic_digits = {'0':'٠','1':'١','2':'٢','3':'٣','4':'٤','5':'٥','6':'٦','7':'٧','8':'٨','9':'٩'}
    return ''.join(arabic_digits.get(c, c) for c in text)

def generate_invoice(data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 25 * mm
    line_height = 18

    # Colors
    dark_blue = HexColor("#1E3D58")
    soft_gray = HexColor("#F5F5F5")
    strong_gray = HexColor("#999999")

    # --- Header (Logo + Title)
    logo_path = "company3_logo.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, margin, height - 60, width=45*mm, height=25*mm, mask='auto', preserveAspectRatio=True)

    c.setFont("ArabicFont", 26)
    c.setFillColor(dark_blue)
    c.drawRightString(width - margin, height - 40, arabic_text("فــاتــورة ضريبية"))

    # --- Invoice Info Box
    c.setFont("ArabicFont", 12)
    info_box_y = height - 90
    invoice_details = [
        ("رقم الفاتورة:", convert_to_arabic_numerals(data["invoice_no"])),
        ("تاريخ الإصدار:", convert_to_arabic_numerals(data["invoice_date"])),
        ("تاريخ الاستحقاق:", convert_to_arabic_numerals(data["due_date"]))
    ]
    for label, val in invoice_details:
        c.setFillColor(black)
        c.drawRightString(width - margin, info_box_y, arabic_text(label + " " + val))
        info_box_y -= line_height

    # --- Sender Info
    sender_y = info_box_y - 15
    c.setFont("ArabicFont", 11)
    sender_info = [
        "شركة حلول النظم المتقدمة",
        "الدمام، المملكة العربية السعودية",
        "الرقم الضريبي: ٣٠٠٣٣٢٢١١٤٤٥"
    ]
    c.drawString(margin, sender_y, arabic_text("معلومات الشركة:"))
    sender_y -= line_height
    for line in sender_info:
        c.drawString(margin + 10, sender_y, arabic_text(line))
        sender_y -= line_height

    # --- Client Info
    client_y = sender_y - 10
    c.drawRightString(width - margin, client_y, arabic_text("معلومات العميل:"))
    client_y -= line_height
    for line in data["client_info"]:
        c.drawRightString(width - margin - 10, client_y, arabic_text(line))
        client_y -= line_height

    # --- Table Headers
    table_y = client_y - 30
    c.setFillColor(soft_gray)
    c.rect(margin, table_y, width - 2 * margin, 25, fill=1, stroke=0)
    c.setFont("ArabicFont", 12)
    c.setFillColor(black)
    c.drawString(margin + 5, table_y + 7, arabic_text("الوصف"))
    c.drawCentredString(width / 2, table_y + 7, arabic_text("الكمية"))
    c.drawRightString(width - margin - 5, table_y + 7, arabic_text("المجموع"))

    # --- Items
    c.setFont("ArabicFont", 11)
    y = table_y - 25
    subtotal = 0
    for desc, unit, qty, total in data["items"]:
        c.drawString(margin + 5, y, arabic_text(desc))
        c.drawCentredString(width / 2, y, convert_to_arabic_numerals(qty))
        c.drawRightString(width - margin - 5, y, arabic_text(f"ريال {total}"))
        subtotal += float(total)
        y -= line_height

    # --- Totals
    discount = subtotal * 0.10
    vat = (subtotal - discount) * 0.15
    grand_total = subtotal - discount + vat

    y -= 30
    c.setFont("ArabicFont", 11)
    totals = [
        ("المجموع الفرعي:", subtotal),
        ("الخصم (١٠٪):", discount),
        ("ضريبة القيمة المضافة (١٥٪):", vat),
        ("المجموع النهائي:", grand_total),
    ]
    for label, amount in totals:
        c.setFillColor(strong_gray)
        c.drawRightString(width - margin, y, arabic_text(label))
        c.setFillColor(black)
        c.drawString(margin + 10, y, arabic_text(f"ريال {amount:.2f}"))
        y -= line_height

    # --- Notes or Thank You
    y = 50
    c.setFont("ArabicFont", 12)
    c.setFillColor(dark_blue)
    c.drawCentredString(width / 2, y, arabic_text("نشكركم على ثقتكم بنا"))
    c.save()
    print(f"✅ Company 3 professional invoice created: {os.path.abspath(output_path)}")

# Load and Generate
if __name__ == "__main__":
    with open("3.json", "r", encoding="utf-8") as f:
        invoices = json.load(f)
    for invoice in invoices:
        file_name = f"{invoice['invoice_no']}.pdf"
        generate_invoice(invoice, file_name)
