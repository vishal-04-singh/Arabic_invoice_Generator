import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

from template_company1 import generate_invoice as gen1
from template_company2 import generate_invoice as gen2
from template_company3 import generate_invoice as gen3

TEMPLATES = {
    "Company 1 - Classic": ("1.json", gen1),
    "Company 2 - Modern": ("2.json", gen2),
    "Company 3 - Professional": ("3.json", gen3),
}

def generate_selected_invoice():
    selected = company_var.get()
    if selected not in TEMPLATES:
        messagebox.showwarning("Warning", "Please select a company")
        return

    json_file, generator = TEMPLATES[selected]

    try:
        file_path = filedialog.askopenfilename(initialfile=json_file, filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            invoices = json.load(f)

        for invoice in invoices:
            file_name = f"{invoice['invoice_no']}.pdf"
            generator(invoice, file_name)

        messagebox.showinfo("Success", f"All invoices generated successfully for {selected}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("Invoice Generator")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="🧾 Select a company to generate invoices", font=("Arial", 14)).pack(pady=20)

company_var = tk.StringVar(value="Company 1 - Classic")
for name in TEMPLATES.keys():
    tk.Radiobutton(root, text=name, variable=company_var, value=name, font=("Arial", 12)).pack(anchor="w", padx=40)

tk.Button(root, text="📤 Generate Invoices", command=generate_selected_invoice, font=("Arial", 12), bg="#4CAF50", fg="black").pack(pady=30)

root.mainloop()