"""
SoilVision AI PDF Report Generator
Generates downloadable ICAR-aligned Soil Health Card PDF reports using fpdf2.
"""

import io
from fpdf import FPDF


def _safe_text(value):
    """Sanitizes text so built-in FPDF core fonts never fail on special Unicode characters."""
    if value is None:
        return ""
    text = str(value)
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2022": "*",
        "\u00b0": " deg ",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", errors="replace").decode("latin-1")


class _SoilReportPDF(FPDF):
    """Custom PDF layout with SoilVision AI header and footer."""

    def header(self):
        self.set_fill_color(10, 35, 22)
        self.rect(0, 0, 210, 26, "F")
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(74, 222, 128)
        self.set_xy(12, 6)
        self.cell(0, 7, "SoilVision AI - Official Soil Health Card", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(220, 235, 225)
        self.set_x(12)
        self.cell(0, 5, "Rule-Based ICAR & NBSS&LUP Diagnostic Report", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)

    def footer(self):
        self.set_y(-16)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 110, 105)
        self.multi_cell(
            self.epw,
            4,
            "Disclaimer: Educational & rule-based ICAR screening only. Consult your local KVK for lab-certified fertilizer dosing.",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )


def generate_soil_report_pdf(record, analysis):
    """Builds and returns PDF bytes for a saved soil health record and its analysis."""
    pdf = _SoilReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Card & Farm Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 40, 25)
    card_num = f"Card #SV-{record['id']:05d}"
    date_str = str(record.get("created_at") or "Active")[:10]
    pdf.cell(95, 7, _safe_text(card_num))
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(95, 7, _safe_text(f"Date: {date_str}"), align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Farm details box
    pdf.set_fill_color(242, 248, 244)
    pdf.set_draw_color(200, 220, 205)
    pdf.set_font("Helvetica", "", 10)
    location_parts = [p for p in [record.get("district"), record.get("state")] if p]
    location = ", ".join(location_parts) if location_parts else "India"
    meta_lines = [
        f"Farmer / Farm: {record.get('farmer_name') or 'Farmer'}",
        f"Target Crop: {record.get('target_crop') or 'General Farming'}",
        f"Location: {location}",
        f"Soil Type: {record.get('soil_type') or 'General Agro-zone'}",
    ]
    for line in meta_lines:
        pdf.cell(186, 6, _safe_text(line), border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Health Score
    score = analysis.get("health_index")
    if score is not None:
        if score >= 75:
            condition = "Excellent"
        elif score >= 55:
            condition = "Good"
        elif score >= 35:
            condition = "Fair"
        else:
            condition = "Poor / Critical"
    else:
        condition = "Incomplete Data"
    score_display = f"{score}/100" if score is not None else "N/A"

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(22, 120, 58)
    pdf.cell(0, 8, _safe_text(f"Overall Soil Health Score: {score_display} ({condition})"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Parameters Table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(20, 40, 25)
    pdf.cell(0, 7, "Measured Soil Parameters & ICAR Status", new_x="LMARGIN", new_y="NEXT")

    ratings = analysis.get("ratings", {})
    param_rows = [
        ("Soil pH", record.get("ph"), "", "ph"),
        ("Electrical Conductivity (EC)", record.get("ec"), "dS/m", "ec"),
        ("Organic Carbon (OC)", record.get("oc"), "%", "oc"),
        ("Available Nitrogen (N)", record.get("nitrogen"), "kg/ha", "nitrogen"),
        ("Available Phosphorus (P)", record.get("phosphorus"), "kg/ha", "phosphorus"),
        ("Available Potassium (K)", record.get("potassium"), "kg/ha", "potassium"),
        ("Soil Moisture", record.get("moisture"), "%", "moisture"),
        ("Soil Temperature", record.get("temperature"), "deg C", "temperature"),
        ("Zinc (Zn)", record.get("zinc"), "ppm", "zinc"),
        ("Iron (Fe)", record.get("iron"), "ppm", "iron"),
        ("Sulphur (S)", record.get("sulphur"), "ppm", "sulphur"),
        ("Boron (B)", record.get("boron"), "ppm", "boron"),
    ]

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(22, 163, 74)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(70, 7, "Parameter", border=1, fill=True)
    pdf.cell(40, 7, "Measured Value", border=1, fill=True)
    pdf.cell(76, 7, "ICAR Assessment", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 35, 32)
    for label, val, unit, key in param_rows:
        val_str = f"{val} {unit}".strip() if val is not None else "Not Provided"
        rating_info = ratings.get(key, {})
        rating_str = rating_info.get("rating") if isinstance(rating_info, dict) else None
        status_str = rating_str or ("Recorded" if val is not None else "Missing")
        pdf.cell(70, 6, _safe_text(label), border=1)
        pdf.cell(40, 6, _safe_text(val_str), border=1)
        pdf.cell(76, 6, _safe_text(status_str), border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)

    # Smart Soil Prescription Recommendations
    recs = analysis.get("recommendations", [])
    if recs:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(20, 40, 25)
        pdf.cell(pdf.epw, 7, "Your Smart Soil Prescription (Rule-Based ICAR Guidance)", new_x="LMARGIN", new_y="NEXT")
        for idx, rec in enumerate(recs[:8], start=1):
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(22, 120, 58)
            title = f"{idx}. [{rec.get('priority', 'Normal')}] {rec.get('title', 'Recommendation')}"
            pdf.multi_cell(pdf.epw, 5, _safe_text(title), new_x="LMARGIN", new_y="NEXT")
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(40, 45, 42)
            pdf.multi_cell(pdf.epw, 4.5, _safe_text(rec.get("action", "")), new_x="LMARGIN", new_y="NEXT")
            if rec.get("sustainable_tip"):
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Helvetica", "I", 8.5)
                pdf.multi_cell(pdf.epw, 4.5, _safe_text(f"Sustainable Tip: {rec['sustainable_tip']}"), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

    # Return bytes buffer
    raw_bytes = pdf.output()
    return io.BytesIO(raw_bytes)
