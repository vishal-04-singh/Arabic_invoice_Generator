from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
import os
import json

pdfmetrics.registerFont(TTFont('ArabicFont', 'Amiri-Regular.ttf'))

def arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def convert_to_arabic_numerals(text):
    arabic_digits = {'0':'٠','1':'١','2':'٢','3':'٣','4':'٤','5':'٥','6':'٦','7':'٧','8':'٨','9':'٩'}
    return ''.join(arabic_digits.get(c, c) for c in text)

# ... [previous imports remain the same]

def generate_invoice(data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    line_height = 16

    header_color = HexColor('#1F487E')
    accent_color = HexColor('#FF914D')
    gray = HexColor('#E8E8E8')
    dark = HexColor('#555')

    # Header Background
    c.setFillColor(header_color)
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)

    # Company Logo
    logo_path = "company2_logo.webp"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, margin, height - 80, width=45*mm, height=30*mm,
                    preserveAspectRatio=True, mask='auto')
    else:
        c.setFillColor(white)
        c.setFont("ArabicFont", 10)
        c.drawString(margin, height - 50, arabic_text("[شعار الشركة]"))

    # Invoice Title
    c.setFillColor(white)
    c.setFont("ArabicFont", 30)
    c.drawCentredString(width / 2, height - 60, arabic_text("فــاتــورة ضريبية"))

    # Invoice Info Box
    c.setFillColor(gray)
    c.rect(width - 200, height - 190, 180, 80, fill=1, stroke=0)

    invoice_info = [
        ("رقم:", convert_to_arabic_numerals(data["invoice_no"])),
        ("تاريخ:", convert_to_arabic_numerals(data["invoice_date"])),
        ("الاستحقاق:", convert_to_arabic_numerals(data["due_date"]))
    ]
    c.setFont("ArabicFont", 12)
    y = height - 130
    for label, val in invoice_info:
        c.setFillColor(dark)
        c.drawRightString(width - 30, y, arabic_text(label))
        c.setFillColor(black)
        c.drawRightString(width - 120, y, val)
        y -= 20

    # Sender Info
    sender_info = [
        "شركة البرمجيات الحديثة",
        "الخبر، المملكة العربية السعودية",
        "الرقم الضريبي: ٣٠٠٩٨٧٦٥٤٣٢١"
    ]
    y = height - 210
    for line in sender_info:
        c.drawString(margin, y, arabic_text(line))
        y -= 18

    # Client Info
    y = height - 240
    for line in data["client_info"]:
        c.drawRightString(width - margin, y, arabic_text(line))
        y -= 18

    # Items Table Header
    c.setFillColor(accent_color)
    c.rect(margin, y - 20, width - 2 * margin, 25, fill=1, stroke=0)
    c.setFont("ArabicFont", 12)
    c.setFillColor(white)
    c.drawRightString(width - margin - 10, y - 5, arabic_text("الوصف"))
    c.drawCentredString(width / 2, y - 5, arabic_text("الكمية"))
    c.drawString(margin + 10, y - 5, arabic_text("المجموع"))

    # Table rows
    y -= 35
    subtotal = 0
    for desc, unit, qty, total in data["items"]:
        c.setFillColor(black)
        c.setFont("ArabicFont", 11)
        c.drawRightString(width - margin - 10, y, arabic_text(desc))
        c.drawCentredString(width / 2, y, convert_to_arabic_numerals(qty))
        c.drawString(margin + 10, y, arabic_text(total))
        subtotal += float(total)
        y -= 20

    # Totals
    discount = subtotal * 0.10
    vat = (subtotal - discount) * 0.15
    total = subtotal - discount + vat

    y -= 30
    c.setFont("ArabicFont", 11)
    totals = [
        (arabic_text("المجموع الفرعي:"), f"{subtotal:.2f}"),
        (arabic_text("الخصم (١٠٪):"), f"{discount:.2f}"),
        (arabic_text("ضريبة القيمة المضافة (١٥٪):"), f"{vat:.2f}"),
        (arabic_text("المجموع النهائي:"), f"{total:.2f}")
    ]
    for label, value in totals:
        c.setFillColor(dark)
        c.drawRightString(width - margin, y, label)
        c.setFillColor(black)
        c.drawString(margin + 10, y, arabic_text(f"ريال {value}"))
        y -= 20

    # Footer
    c.setFont("ArabicFont", 12)
    c.drawCentredString(width / 2, 40, arabic_text("شكراً لتعاملكم معنا"))
    c.save()
    print(f"✅ Company2 invoice saved: {os.path.abspath(output_path)}")


# Run for each invoice
if __name__ == "__main__":
    with open("2.json", "r", encoding="utf-8") as f:
        invoices = json.load(f)

    for invoice in invoices:
        file_name = f"{invoice['invoice_no']}.pdf"
        generate_invoice(invoice, file_name)
