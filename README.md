# iVoice – Arabic Invoice Generator

iVoice is a Python-based, GUI-powered tool for generating professional Arabic (RTL) PDF invoices customized for different companies. It uses the ReportLab library, supports Arabic text rendering, and enables easy invoice creation from structured JSON data.

## Features

- **Arabic PDF Invoice Generation**: Creates print-ready invoices with proper Arabic text shaping and RTL layout.
- **Multiple Professional Templates**: Three distinct company templates, each with its own branding, color, and layout.
- **User-Friendly GUI**: A simple Tkinter interface lets you select a company and generate invoices in bulk from JSON files.
- **Custom Fonts**: Uses Amiri, an open-source Arabic font, for elegant, readable output.
- **Automatic Calculations**: Subtotal, discount, VAT, and grand total are calculated and displayed.
- **Company Logos**: Add your company’s logo to personalize the invoices.

## Project Structure

```
.
├── gui.py
├── template_company1.py
├── template_company2.py
├── template_company3.py
├── Amiri-Regular.ttf
├── 1.json
├── 2.json
├── 3.json
├── 1.webp          # Logo for Company 1
├── company2_logo.webp
├── company3_logo.png
└── README.md
```

## Requirements

- Python 3.7+
- [ReportLab](https://www.reportlab.com/dev/install/open_source/)
- [arabic_reshaper](https://pypi.org/project/arabic-reshaper/)
- [python-bidi](https://pypi.org/project/python-bidi/)
- Tkinter (usually included with Python)

Install dependencies via pip:

```bash
pip install reportlab arabic-reshaper python-bidi
```

If Tkinter is missing, install it according to your OS instructions.

## Setup

1. **Fonts**:  
   Place `Amiri-Regular.ttf` in your project directory.  
   [Download Amiri font here](https://www.amirifont.org/).

2. **Logos**:  
   Place your company logos as the following files (or update the script paths if you use different names):
   - `1.webp` (for Company 1/classic)
   - `company2_logo.webp` (for Company 2/modern)
   - `company3_logo.png` (for Company 3/professional)

3. **JSON Data**:  
   Prepare invoice data in JSON format. Each template expects a different JSON file (`1.json`, `2.json`, `3.json`), but the structure for each invoice inside is similar.

### Example JSON Structure (`1.json` or `2.json` or `3.json`)
```json
[
  {
    "invoice_no": "1001",
    "invoice_date": "2025-06-27",
    "due_date": "2025-07-11",
    "client_info": [
      "اسم العميل",
      "العنوان",
      "هاتف: ٠٥٠٠٠٠٠٠٠٠",
      "البريد الإلكتروني: client@email.com"
    ],
    "items": [
      ["خدمة استضافة", "شهر", "1", "500.00"],
      ["تصميم موقع", "مشروع", "1", "1500.00"]
    ]
  }
]
```
- `invoice_no`, `invoice_date`, and `due_date`: Invoice metadata.
- `client_info`: List of client details (each as a string).
- `items`: List of invoice lines. Each item is `[description, unit, quantity, total]`.

> **Tip**: You can have multiple invoices in a single JSON file for batch generation.

## Usage

1. **Launch the GUI:**
   ```bash
   python gui.py
   ```
2. **Select a company template** from the radio buttons.
3. **Click "Generate Invoices"** – you will be prompted to select a JSON file with your invoice data.
4. **Check the output PDFs**: For each invoice entry, a PDF will be generated in the working directory, named by `invoice_no`.

## How It Works

- The GUI (`gui.py`) lets you select your company template and a JSON file.
- Each template script (`template_company1.py`, etc.) sets a different layout, branding, and calculations (such as discount rates).
- The Arabic font and text direction handling is enabled via Amiri font, `arabic_reshaper`, and `python-bidi`.
- The code automatically handles Arabic numerals and ensures PDF output is ready for RTL reading.

## Customization

- **Add more companies**: Copy a template file, adjust the branding/layout/colors, and add it to `TEMPLATES` in `gui.py`.
- **Change colors/layout**: Edit the corresponding template file.
- **Change discount/VAT rates**: Modify the calculation logic in each template file.

## License

This project is open source and free to use for personal or commercial needs.

---

## Troubleshooting

- **Font not found**: Ensure `Amiri-Regular.ttf` is present in your working directory.
- **Arabic not displaying correctly in PDF**: Verify that `arabic_reshaper` and `python-bidi` are installed and used.
- **Logo not appearing**: Check the image file path and format; only PNG and WEBP are supported as coded.

## Contact

For feature requests or issues, open a GitHub issue or contact the maintainer.

---

**Enjoy fast, beautiful Arabic invoice generation!**