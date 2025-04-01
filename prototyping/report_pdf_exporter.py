# report_pdf_exporter.py
import pdfkit
import os
from jinja2 import Template


def export_report_to_pdf(output: dict, output_pdf_path: str = "final_report.pdf") -> str:
    research_steps = output.get("research_steps", "")
    if isinstance(research_steps, list):
        research_steps = "\n".join([f"- {r}" for r in research_steps])

    sources = output.get("sources", "")
    if isinstance(sources, list):
        sources = "\n".join([f"- {s}" for s in sources])

    image_path = output.get("image_path", "")
    image_section = f"<h2>Graph Visualization</h2><img src='{image_path}' width='600'/>" if image_path else ""

    # Use Jinja2 template for HTML layout
    html_template = Template("""
    <html>
    <head><title>Mini Manus Report</title></head>
    <body style="font-family: Arial;">
        <h1>INTRODUCTION</h1><p>{{ introduction }}</p>
        <h2>RESEARCH STEPS</h2><pre>{{ research_steps }}</pre>
        <h2>REPORT</h2><p>{{ main_body }}</p>
        {{ image_section|safe }}
        <h2>CONCLUSION</h2><p>{{ conclusion }}</p>
        <h2>SOURCES</h2><pre>{{ sources }}</pre>
    </body>
    </html>
    """)

    html_content = html_template.render(
        introduction=output.get("introduction", ""),
        research_steps=research_steps,
        main_body=output.get("main_body", ""),
        conclusion=output.get("conclusion", ""),
        sources=sources,
        image_section=image_section
    )

    # Convert HTML to PDF
    pdfkit.from_string(html_content, output_pdf_path)
    return output_pdf_path
