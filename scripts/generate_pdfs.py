#!/usr/bin/env python3
"""Generate program PDFs from measures.yaml."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "measures.yaml"
PDF_DIR = ROOT / "docs" / "assets" / "pdf"
JSON_OUT = ROOT / "docs" / "assets" / "data" / "measures.json"


class ProgramPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "LED - Liberte Environnement Democratie", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def sanitize(text: str) -> str:
    replacements = {
        "«": '"',
        "»": '"',
        "—": "-",
        "–": "-",
        "'": "'",
        "'": "'",
        """: '"',
        """: '"',
        "…": "...",
        "€": "EUR",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


def ensure_space(pdf: ProgramPDF, height: float = 20):
    if pdf.get_y() + height > pdf.page_break_trigger:
        pdf.add_page()


def write_paragraph(pdf: ProgramPDF, text: str, size: int = 11):
    ensure_space(pdf, 12)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", size)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(pdf.epw, 6, sanitize(text), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def write_title(pdf: ProgramPDF, text: str, size: int = 16):
    ensure_space(pdf, 16)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", size)
    pdf.set_text_color(0, 82, 147)
    pdf.multi_cell(pdf.epw, 8, sanitize(text), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)


def write_section(pdf: ProgramPDF, text: str):
    ensure_space(pdf, 14)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(0, 120, 80)
    pdf.multi_cell(pdf.epw, 7, sanitize(text), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def generate_general_pdf(lang: str, data: dict) -> Path:
    pdf = ProgramPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    if lang == "fr":
        write_title(pdf, "Projet de programme - Parti LED", 18)
        write_title(pdf, "(Liberte, Environnement, Democratie)", 14)
        write_paragraph(
            pdf,
            "Presidence francaise 2027. Document de structuration des idees. "
            "Mise en forme et non validation ou analyse du contenu.",
            10,
        )
        pdf.ln(4)
        for section in data["sections"]:
            write_section(pdf, section["title_fr"])
            for i, measure in enumerate(section["measures"], 1):
                ensure_space(pdf, 16)
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(40, 40, 40)
                pdf.multi_cell(pdf.epw, 6, sanitize(f"{i}. {measure['title_fr']}"), new_x="LMARGIN", new_y="NEXT")
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(pdf.epw, 5, sanitize(measure["summary_fr"]), new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)
        out = PDF_DIR / "fr" / "programme-general.pdf"
    else:
        write_title(pdf, "Program Draft - LED Party", 18)
        write_title(pdf, "(Liberty, Environment, Democracy)", 14)
        write_paragraph(
            pdf,
            "French Presidential Election 2027. Document structuring ideas. "
            "Formatting only, not validation or analysis of content.",
            10,
        )
        pdf.ln(4)
        for section in data["sections"]:
            write_section(pdf, section["title_en"])
            for i, measure in enumerate(section["measures"], 1):
                ensure_space(pdf, 16)
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(40, 40, 40)
                pdf.multi_cell(pdf.epw, 6, sanitize(f"{i}. {measure['title_en']}"), new_x="LMARGIN", new_y="NEXT")
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(pdf.epw, 5, sanitize(measure["summary_en"]), new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)
        out = PDF_DIR / "en" / "program-general.pdf"

    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    return out


def generate_measure_pdf(measure: dict, section_title: str, lang: str) -> Path:
    pdf = ProgramPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    if lang == "fr":
        title = measure["title_fr"]
        summary = measure["summary_fr"]
        header = section_title if isinstance(section_title, str) else section_title
        subtitle = "Fiche mesure - Parti LED"
    else:
        title = measure["title_en"]
        summary = measure["summary_en"]
        header = section_title
        subtitle = "Measure sheet - LED Party"

    write_paragraph(pdf, subtitle, 10)
    write_paragraph(pdf, sanitize(header), 11)
    write_title(pdf, title, 16)
    write_paragraph(pdf, summary, 12)
    write_paragraph(
        pdf,
        "Document detaille a completer. Consultez led-initiative.fr pour les mises a jour."
        if lang == "fr"
        else "Detailed document to be completed. Visit led-initiative.fr for updates.",
        10,
    )

    out = PDF_DIR / lang / "mesures" / f"{measure['id']}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    return out


def export_json(data: dict) -> Path:
    sections = []
    for section in data["sections"]:
        sections.append(
            {
                "id": section["id"],
                "title_fr": section["title_fr"],
                "title_en": section["title_en"],
                "measures": [
                    {
                        "id": m["id"],
                        "title_fr": m["title_fr"],
                        "title_en": m["title_en"],
                        "summary_fr": m["summary_fr"],
                        "summary_en": m["summary_en"],
                        "pdf_fr": f"assets/pdf/fr/mesures/{m['id']}.pdf",
                        "pdf_en": f"assets/pdf/en/mesures/{m['id']}.pdf",
                    }
                    for m in section["measures"]
                ],
            }
        )

    payload = {
        "manifeste_url": data.get("manifeste_url", ""),
        "sections": sections,
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return JSON_OUT


def main():
    data = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))

    print("Generating general program PDFs...")
    generate_general_pdf("fr", data)
    generate_general_pdf("en", data)

    count = 0
    for section in data["sections"]:
        for measure in section["measures"]:
            generate_measure_pdf(measure, section["title_fr"], "fr")
            generate_measure_pdf(measure, section["title_en"], "en")
            count += 1

    export_json(data)
    print(f"Done: 2 general PDFs, {count * 2} measure PDFs, JSON exported.")


if __name__ == "__main__":
    main()
