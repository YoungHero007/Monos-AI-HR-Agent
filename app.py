from pathlib import Path
import base64
import json
import zipfile
import xml.etree.ElementTree as ET

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).parent


def load_employees():
    workbook = ROOT / "Monos_HR_Web_Test_Data_100_Employees.xlsx"
    with zipfile.ZipFile(workbook) as archive:
        xml = ET.fromstring(archive.read("xl/worksheets/sheet2.xml"))
    namespace = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rows = []
    for row in xml.findall("main:sheetData/main:row", namespace):
        values = []
        for cell in row.findall("main:c", namespace):
            reference = cell.attrib.get("r", "A1")
            column = 0
            for character in reference:
                if character.isalpha():
                    column = column * 26 + ord(character.upper()) - 64
                else:
                    break
            column -= 1
            inline = cell.find("main:is/main:t", namespace)
            value = inline.text if inline is not None and inline.text else ""
            while len(values) <= column:
                values.append("")
            values[column] = value
        if values:
            rows.append(values)
    headers = rows[0]
    return [dict(zip(headers, row)) for row in rows[1:]]

st.set_page_config(
    page_title="Monos HR | Employee Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")
employee_data = json.dumps(load_employees(), ensure_ascii=False)
css = (ROOT / "styles.css").read_text(encoding="utf-8")
logo_css = (ROOT / "pharmacy-logo.css").read_text(encoding="utf-8")
javascript = (ROOT / "app.js").read_text(encoding="utf-8")
auth = (ROOT / "auth.js").read_text(encoding="utf-8")
salary_pdf = (ROOT / "salary-pdf.js").read_text(encoding="utf-8")
mail_config = (ROOT / "mail-config.js").read_text(encoding="utf-8")
jobs = (ROOT / "jobs.js").read_text(encoding="utf-8")
portal_links = (ROOT / "portal-links.js").read_text(encoding="utf-8")
template = base64.b64encode((ROOT / "Тодорхойлолт загвар.pdf").read_bytes()).decode("ascii")
html = html.replace(
    '<script src="app.js"></script>',
    f"<script>window.HR_EMPLOYEES={employee_data};</script><script src=\"app.js\"></script>",
).replace(
    '<link rel="stylesheet" href="styles.css" />',
    f"<style>{css}{logo_css}</style>",
).replace(
    '<script src="app.js"></script>',
    f"<script>{javascript}</script>",
).replace(
    '<script src="auth.js"></script>',
    f"<script>{auth}</script>",
).replace(
    '<script src="salary-pdf.js"></script>',
    f"<script>{salary_pdf}</script>",
).replace(
    '<script src="mail-config.js"></script>',
    f"<script>{mail_config}</script>",
).replace(
    '<script src="jobs.js"></script>',
    f"<script>{jobs}</script>",
).replace(
    '<script src="portal-links.js"></script>',
    f"<script>{portal_links}</script>",
).replace(
    "./Monos_Calingiin_Todorhoilolt_Template.docx",
    f"data:application/pdf;base64,{template}",
)
components.html(html, height=1100, scrolling=True)
