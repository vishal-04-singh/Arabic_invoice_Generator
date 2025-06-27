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

# Register Arabic font once
pdfmetrics.registerFont(TTFont('ArabicFont', 'Amiri-Regular.ttf'))

def arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def convert_to_arabic_numerals(text):
    arabic_digits = {'0':'٠','1':'١','2':'٢','3':'٣','4':'٤','5':'٥','6':'٦','7':'٧','8':'٨','9':'٩'}
    return ''.join(arabic_digits.get(c, c) for c in text)

def generate_invoice(data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    line_height = 16

    # Colors
    primary_color = HexColor('#2E4057')
    secondary_color = HexColor('#048A81')
    light_gray = HexColor('#F8F9FA')
    lighter_gray = HexColor("#F1F1F1")
    dark_gray = HexColor('#6C757D')

    # Header
    header_height = 80
    c.setFillColor(primary_color)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)

    # Title
    c.setFillColor(white)
    c.setFont("ArabicFont", 28)
    c.drawCentredString(width / 2, height - 45, arabic_text("فــاتــورة"))

    # Logo
    logo_path = "1.webp"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, margin, height - 80, width=50*mm, height=30*mm, preserveAspectRatio=True, mask='auto')
    else:
        c.setFont("ArabicFont", 12)
        c.drawRightString(width - margin, height - 50, arabic_text("[شعار الشركة]"))

    # Invoice Info
    info_box_width = 200
    info_box_height = 80
    info_box_x = width - margin - info_box_width
    info_box_y = height - header_height - 40 - info_box_height
    c.setFillColor(light_gray)
    c.setStrokeColor(dark_gray)
    c.setLineWidth(1)
    c.rect(info_box_x, info_box_y, info_box_width, info_box_height, fill=1)

    c.setFont("ArabicFont", 12)
    invoice_details = [
        (arabic_text("رقم الفاتورة:"), convert_to_arabic_numerals(data["invoice_no"])),
        (arabic_text("التاريخ:"), convert_to_arabic_numerals(data["invoice_date"])),
        (arabic_text("تاريخ الاستحقاق:"), convert_to_arabic_numerals(data["due_date"])),
        (arabic_text("طريقة الدفع:"), arabic_text("تحويل بنكي"))
    ]
    detail_y = info_box_y + info_box_height - 20
    for label, value in invoice_details:
        c.setFillColor(dark_gray)
        c.drawRightString(info_box_x + info_box_width - 10, detail_y, label)
        c.setFillColor(black)
        c.drawRightString(info_box_x + info_box_width - 110, detail_y, value)
        detail_y -= line_height

    # Sender & Client Info
    section_y = info_box_y - 40
    section_h = 140
    col_w = (width - 2 * margin) / 2

    c.setStrokeColor(secondary_color)
    c.setLineWidth(2)
    c.rect(margin, section_y - section_h, col_w * 2, section_h, fill=0)

    # Headers
    c.setFillColor(secondary_color)
    c.rect(margin, section_y - 25, col_w, 25, fill=1, stroke=0)
    c.rect(margin + col_w, section_y - 25, col_w, 25, fill=1, stroke=0)

    c.setFont("ArabicFont", 14)
    c.setFillColor(white)
    c.drawCentredString(margin + col_w / 2, section_y - 15, arabic_text("معلومات المرسل"))
    c.drawCentredString(margin + col_w + col_w / 2, section_y - 15, arabic_text("معلومات العميل"))

    # Static Sender Info
    sender_info = [
        "شركة التقنية العربية المحدودة",
        "الرياض، المملكة العربية السعودية",
        "ص.ب: ١٢٣٤٥",
        "هاتف: +٩٦٦٩٢٠٠٠٩٧٢٢",
        "البريد الإلكتروني: sales@ar-tech.com",
        "الرقم الضريبي: ٣٠٠١٢٣٤٥٦٧٠٠٠٠٣"
    ]
    c.setFont("ArabicFont", 11)
    detail_y = section_y - 45
    for line in sender_info:
        c.setFillColor(black)
        c.drawCentredString(margin + col_w / 2, detail_y, arabic_text(line))
        detail_y -= line_height

    # Dynamic Client Info
    detail_y = section_y - 45
    for line in data["client_info"]:
        c.drawCentredString(margin + col_w + col_w / 2, detail_y, arabic_text(line))
        detail_y -= line_height

    # Table Header
    table_y = section_y - section_h - 40
    table_width = width - 2 * margin
    table_x = margin
    c.setFillColor(primary_color)
    c.rect(table_x, table_y, table_width, 30, fill=1, stroke=0)

    c.setFont("ArabicFont", 12)
    c.setFillColor(white)
    total_x = table_x + 30
    qty_x = table_x + 120
    unit_x = table_x + 200
    desc_x = table_x + 280
    sno_x = table_x + table_width - 30

    c.drawCentredString(total_x, table_y + 10, arabic_text("الإجمالي"))
    c.drawCentredString(qty_x, table_y + 10, arabic_text("الكمية"))
    c.drawCentredString(unit_x, table_y + 10, arabic_text("الوحدة"))
    c.drawString(desc_x, table_y + 10, arabic_text("الوصف"))
    c.drawCentredString(sno_x, table_y + 10, arabic_text("م"))

    # Items
    c.setFont("ArabicFont", 11)
    item_y = table_y - 20
    row_colors = [white, lighter_gray]
    subtotal = 0.0

    for i, (desc, unit, qty, total) in enumerate(data["items"]):
        c.setFillColor(row_colors[i % 2])
        c.rect(table_x, item_y - 5, table_width, 25, fill=1, stroke=0)
        c.setFillColor(black)
        c.drawCentredString(total_x, item_y + 5, arabic_text(f"{total}"))
        c.drawCentredString(qty_x, item_y + 5, convert_to_arabic_numerals(qty))
        c.drawCentredString(unit_x, item_y + 5, arabic_text(unit))
        c.drawString(desc_x, item_y + 5, arabic_text(desc))
        c.drawCentredString(sno_x, item_y + 5, convert_to_arabic_numerals(str(i + 1)))
        item_y -= 25
        subtotal += float(total)

    # Totals
    discount = subtotal * 0.05  # 5% discount
    vat = (subtotal - discount) * 0.15  # 15% VAT
    grand_total = subtotal - discount + vat

    totals_x = margin
    totals_y = item_y - 20
    totals_width = 170
    totals_height = 100
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.rect(totals_x, totals_y - totals_height, totals_width, totals_height, fill=1)

    c.setFont("ArabicFont", 10)
    totals = [
        (arabic_text(f"{subtotal:.2f}"), arabic_text("المجموع الفرعي:")),
        (arabic_text(f"{discount:.2f}"), arabic_text("الخصم (٥٪):")),
        (arabic_text(f"{vat:.2f}"), arabic_text("ضريبة القيمة المضافة (١٥٪):"))
    ]

    total_y = totals_y - 20
    for amount, label in totals:
        c.setFillColor(black)
        c.drawString(totals_x + 20, total_y, amount)
        c.setFillColor(dark_gray)
        c.drawRightString(totals_x + totals_width - 20, total_y, label)
        total_y -= 20

    # Final Total
    final_total_height = 30
    c.setFillColor(secondary_color)
    c.rect(totals_x, totals_y - totals_height, totals_width, final_total_height, fill=1)
    c.setFillColor(white)
    c.setFont("ArabicFont", 11)
    c.drawString(totals_x + 20, totals_y - totals_height + 8, arabic_text(f"ريال {grand_total:.2f}"))
    c.drawRightString(totals_x + totals_width - 20, totals_y - totals_height + 8, arabic_text("المجموع النهائي:"))

    # Payment Terms
    notes_y = totals_y - totals_height - 40
    c.setFillColor(black)
    c.setFont("ArabicFont", 11)
    c.drawRightString(width - margin, notes_y, arabic_text("شروط الدفع:"))

    payment_terms = [
        "• يُرجى الدفع خلال ١٤ يوماً من تاريخ الفاتورة",
        "• الدفع مقبول عبر التحويل البنكي أو الشيك المصدق",
        "• سيتم فرض غرامة تأخير بنسبة ٢٪ شهرياً على المدفوعات المتأخرة"
    ]
    terms_y = notes_y - 15
    c.setFont("ArabicFont", 9)
    for term in payment_terms:
        c.drawRightString(width - margin - 10, terms_y, arabic_text(term))
        terms_y -= 12

    # Footer
    footer_y = 60
    c.setStrokeColor(dark_gray)
    c.setLineWidth(1)
    c.line(margin, footer_y + 10, width - margin, footer_y + 10)

    c.setFont("ArabicFont", 12)
    c.drawCentredString(width / 2, footer_y - 10, arabic_text("شكراً لتعاملكم معنا"))

    # Save
    c.save()
    print(f"✅ Arabic invoice created: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    with open("1.json", "r", encoding="utf-8") as f:
        invoices = json.load(f)

    for invoice in invoices:
        file_name = f"{invoice['invoice_no']}.pdf"
        generate_invoice(invoice, file_name)