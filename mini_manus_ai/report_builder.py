from io import BytesIO
from jinja2 import Template
import pdfkit

def build_report(output: dict):

    research_steps = output["research_steps"]
    if type(research_steps) is list:
        research_steps = "\n".join([f"- {r}" for r in research_steps])
    sources = output["sources"]
    if type(sources) is list:
        sources = "\n".join([f"- {s}" for s in sources])

    image_path = output.get("image_path", "")
    image_section = f"<img src='{image_path}' width='600'/>" if image_path else ""

    html_template = Template("""
    <html>
    <head><title>Mini Manus Report</title></head>
    <body style="font-family: Arial;">
        <h1>ABSTRACT</h1><p>{{ introduction }}</p>
        <h2>RESEARCH STEPS</h2><pre>{{ research_steps }}</pre>
        <h2>REPORT</h2><p>{{ main_body }}</p>
        {{ image_section|safe }}                 
        <h2>SOURCES</h2><pre>{{ sources }}</pre>
    </body>
    </html>
    """)

    html_content = html_template.render(
        introduction=output.get("introduction", ""),
        research_steps=research_steps,
        main_body=output.get("main_body", ""),
        #conclusion=output.get("conclusion", ""),
        sources=sources,
        image_section=image_section
    )

    options = {
        'encoding': 'UTF-8',
        'quiet': ''
    }


    # Convert HTML to PDF
    pdf_bytes = pdfkit.from_string(html_content, False, options=options)

    return pdf_bytes


    return f"""
# ELECTRICITY ANALYSIS REPORT

ABSTRACT
------------
{output["introduction"]}

RESEARCH STEPS
--------------
{research_steps}

REPORT
------
{output["main_body"]}

CONCLUSION
----------
{output["conclusion"]}

SOURCES
-------
{sources}
"""