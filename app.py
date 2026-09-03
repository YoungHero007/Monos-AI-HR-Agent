from __future__ import annotations

import re
import hashlib
import json
import os
import sqlite3
from datetime import datetime
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
import requests
import pandas as pd
import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

st.set_page_config(page_title="MONOS HR Portal", page_icon="🧑‍💼", layout="wide")
load_dotenv(Path(__file__).with_name(".env.local"))

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

        :root {
                --monos-bg: #f5f2ec;
                --monos-card: #fffdfa;
                --monos-panel: #f9f7f2;
                --monos-primary: #173b35;
                --monos-primary-soft: #2d6757;
                --monos-accent: #c49a52;
                --monos-accent-soft: #f1e4c9;
                --monos-text: #202622;
                --monos-muted: #6d766f;
                --monos-border: #e4ded2;
                --monos-shadow: 0 18px 45px rgba(35, 52, 43, 0.08);
        }

        html, body, [data-testid="stAppViewContainer"] {
                background: radial-gradient(circle at 92% 0%, rgba(196,154,82,.11), transparent 28rem), var(--monos-bg);
            color: var(--monos-text);
                font-family: 'DM Sans', sans-serif;
        }

        .stApp {
                background: radial-gradient(circle at 92% 0%, rgba(196,154,82,.11), transparent 28rem), var(--monos-bg);
        }

        [data-testid="stSidebar"] {
                background: #eeeae1;
            border-right: 1px solid var(--monos-border);
        }

        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        .block-container {
                padding-top: 2.2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button {
                background: var(--monos-primary);
            color: #fff;
            border: 0;
                border-radius: 10px;
            padding: 0.65rem 1rem;
            font-weight: 600;
                box-shadow: 0 8px 18px rgba(23, 59, 53, 0.15);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stFormSubmitButton > button:hover {
                background: var(--monos-primary-soft);
            color: #fff;
        }

        .stTextInput > div > div > input,
        .stNumberInput input,
        .stSelectbox > div > div,
        .stDateInput > div > div,
        .stTextArea textarea {
                background: var(--monos-card);
            border: 1px solid var(--monos-border);
            border-radius: 12px;
            color: var(--monos-text);
        }

        .stMetric {
                background: var(--monos-card);
            border: 1px solid var(--monos-border);
            border-radius: 16px;
            padding: 1rem;
                box-shadow: var(--monos-shadow);
        }

        .stMetric [data-testid="metric-container"] {
            background: transparent;
        }

        .stMetric [data-testid="stMetricValue"] {
            color: var(--monos-primary-soft);
            font-weight: 700;
        }

        div[data-testid="stVerticalBlock"] > div {
            gap: 0.8rem;
        }

        h1, h2, h3, h4 {
            color: var(--monos-primary);
            font-family: 'Manrope', sans-serif;
            letter-spacing: 0;
        }

        h1 {
            font-size: clamp(2rem, 4vw, 3.2rem);
            font-weight: 800;
        }

        [data-testid="stSidebar"] h1 {
            font-size: 1.6rem;
            letter-spacing: 0.02em;
        }

        label, [data-testid="stMetricLabel"] {
            color: var(--monos-muted) !important;
            font-weight: 600;
        }

        .stDownloadButton > button, .stLinkButton > a {
            border: 1px solid var(--monos-accent);
        }

        .stLinkButton > a {
            background: var(--monos-accent-soft);
            color: var(--monos-primary);
            border-radius: 10px;
            font-weight: 700;
        }

        .monos-header {
                background: rgba(255,253,250,0.82);
            border: 1px solid var(--monos-border);
                border-radius: 12px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
                box-shadow: var(--monos-shadow);
        }

        .monos-brand {
            display: flex;
            align-items: center;
            gap: 0.9rem;
        }

        .monos-logo {
            width: 34px;
            height: 34px;
            border-radius: 10px;
                background: var(--monos-primary);
                color: #f5dfae;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.8rem;
        }

        .monos-brand-text {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--monos-primary);
        }

        .monos-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.65rem 1rem;
            border-radius: 999px;
                background: var(--monos-accent-soft);
            border: 1px solid var(--monos-border);
            color: var(--monos-primary);
            text-decoration: none;
            font-weight: 600;
        }

        .monos-link:hover {
                background: #ead8b4;
            text-decoration: none;
        }

        .monos-card {
            background: var(--monos-card);
            border: 1px solid var(--monos-border);
            border-radius: 12px;
            padding: 1.2rem;
                box-shadow: var(--monos-shadow);
        }

        .monos-subtle {
            color: var(--monos-muted);
            font-size: 0.95rem;
        }

        .monos-badge {
            display: inline-block;
            background: var(--monos-accent-soft);
            color: var(--monos-primary);
            border-radius: 999px;
            padding: 0.3rem 0.7rem;
            font-size: 0.73rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def monos_header():
    st.markdown(
        """
        <div class="monos-header">
            <div class="monos-brand">
                <div class="monos-logo">M</div>
                <div class="monos-brand-text">MONOS | HR Portal</div>
            </div>
            <a class="monos-link" href="https://monos.mn/hr/openjob" target="_blank" rel="noopener noreferrer">
                Монос групп | Хүний нөөц
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


EMPLOYEE = {
    "name": "Батзориг",
    "full_name": "Батзориг Энхтөр",
    "id": "EMP001",
    "position": "Брэнд менежер",
    "department": "Маркетинг",
    "branch": "Төв оффис",
    "salary": "2,500,000 ₮",
    "leave_total": 15,
    "leave_used": 8,
    "leave_remaining": 7,
    "email": "batzorig@monos.mn",
    "phone": "+976 99112233",
    "surname": "Энхтөр",
    "registry_number": "ТЕСТ20260000",
    "salary_amount": 2500000,
    "hire_date": "2024-01-10",
    "marital_status": "Гэрлэсэн",
    "emergency_contact_name": "Энхжаргал Бат",
    "emergency_contact_phone": "+976 99112244",
    "driver_license": "AB-123456",
    "profession": "Брэнд менежер",
    "qualification": "Тийм",
}

HR_EMAIL = "monosubmonos@gmail.com"
LEGALINFO_URL = "https://r.jina.ai/http://legalinfo.mn/mn"
EMPLOYEE_DATA_FILE = Path(__file__).with_name("Monos_HR_Web_Test_Data_100_Employees.xlsx")
USER_DATABASE_FILE = Path(os.getenv("USER_DATABASE_FILE", Path(__file__).with_name("users.db")))
HR_ADMIN = {
    "id": "HR001",
    "name": "Хандсүрэн",
    "surname": "Батбаяр",
    "full_name": "Батбаяр Хандсүрэн",
    "email": "monosubmonos@gmail.com",
    "phone": "77181883",
    "role": "Хүний нөөцийн админ",
}

NAV_ITEMS = {
    "dashboard": "Dashboard",
    "salary": "Цалин",
    "leave": "Амралт, чөлөө",
    "schedule": "Ээлжийн хуваарь",
    "orders": "Тушаал",
    "social": "Нийгмийн даатгал",
    "profile": "Хувийн мэдээлэл",
    "hr": "HR-д асуулт",
    "admin": "Admin mode",
}


if "employee" not in st.session_state:
    st.session_state.employee = EMPLOYEE.copy()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


def get_employee() -> dict:
    return st.session_state.employee


def load_employee_records() -> dict[str, dict]:
    records = {}
    employees = pd.read_excel(EMPLOYEE_DATA_FILE, sheet_name="Ажилтан")
    leave_requests = pd.read_excel(EMPLOYEE_DATA_FILE, sheet_name="Чөлөө_хүсэлт")
    request_counts = leave_requests.groupby("employee_id").size().to_dict()
    for _, row in employees.iterrows():
        employee_id = str(row.get("employee_id", "")).strip()
        if not employee_id or employee_id.lower() == "nan":
            continue
        first_name = str(row.get("Нэр", "")).strip()
        last_name = str(row.get("Овог", "")).strip()
        full_name = " ".join(part for part in (last_name, first_name) if part and part.lower() != "nan")
        records[employee_id.upper()] = {
            **EMPLOYEE,
            "id": employee_id.upper(),
            "name": first_name if first_name.lower() != "nan" else EMPLOYEE["name"],
            "surname": last_name if last_name.lower() != "nan" else "",
            "full_name": full_name or EMPLOYEE["full_name"],
            "phone": str(row.get("Утас", EMPLOYEE["phone"])),
            "email": str(row.get("Имэйл", EMPLOYEE["email"])),
            "registry_number": str(row.get("Регистрийн дугаар", "")),
            "position": str(row.get("Албан тушаал", EMPLOYEE["position"])),
            "department": str(row.get("Хэлтэс", EMPLOYEE["department"])),
            "branch": str(row.get("Салбар", EMPLOYEE["branch"])),
            "salary": f"{int(row.get('Үндсэн цалин', 0)):,} ₮",
            "leave_total": int(row.get("Жилийн амралтын хоног", EMPLOYEE["leave_total"])),
            "leave_remaining": int(row.get("Үлдсэн амралтын хоног", EMPLOYEE["leave_remaining"])),
            "salary_amount": int(row.get("Үндсэн цалин", 0)),
            "hire_date": row.get("Ажилд орсон огноо"),
        }
        records[employee_id.upper()]["leave_used"] = (
            records[employee_id.upper()]["leave_total"] - records[employee_id.upper()]["leave_remaining"]
        )
        hire_date = pd.to_datetime(row.get("Ажилд орсон огноо"), errors="coerce")
        if pd.notna(hire_date):
            today = datetime.now()
            years = today.year - hire_date.year - ((today.month, today.day) < (hire_date.month, hire_date.day))
            anniversary = hire_date.replace(year=hire_date.year + years)
            months = (today.year - anniversary.year) * 12 + today.month - anniversary.month
            if today.day < anniversary.day:
                months -= 1
            records[employee_id.upper()]["service_years"] = max(years, 0)
            records[employee_id.upper()]["service_months"] = max(months, 0)
        else:
            records[employee_id.upper()]["service_years"] = 0
            records[employee_id.upper()]["service_months"] = 0
        records[employee_id.upper()]["request_count"] = int(request_counts.get(employee_id, 0))
    return records


EMPLOYEE_RECORDS = load_employee_records()


def bootstrap_users(records: dict[str, dict]) -> int:
    password_hash = hashlib.sha256("demo123".encode("utf-8")).hexdigest()
    with sqlite3.connect(USER_DATABASE_FILE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                employee_id TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                profile_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        now = datetime.now().isoformat(timespec="seconds")
        for employee_id, profile in records.items():
            connection.execute(
                """
                INSERT INTO users (employee_id, password_hash, profile_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(employee_id) DO UPDATE SET
                    password_hash = excluded.password_hash,
                    profile_json = excluded.profile_json,
                    updated_at = excluded.updated_at
                """,
                (employee_id, password_hash, json.dumps(profile, ensure_ascii=False, default=str), now, now),
            )
        connection.commit()
        return int(connection.execute("SELECT COUNT(*) FROM users").fetchone()[0])


def authenticate_user(employee_id: str, password: str) -> dict | None:
    if employee_id.strip().upper() == HR_ADMIN["id"] and password == "HR001":
        return {**HR_ADMIN, "is_admin": True}
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    with sqlite3.connect(USER_DATABASE_FILE) as connection:
        row = connection.execute(
            "SELECT password_hash, profile_json FROM users WHERE employee_id = ?",
            (employee_id.strip().upper(),),
        ).fetchone()
    if not row or row[0] != password_hash:
        return None
    return json.loads(row[1])


BOOTSTRAPPED_USER_COUNT = bootstrap_users(EMPLOYEE_RECORDS)


def generate_mailto(recipient: str, subject: str, body: str) -> str:
    import urllib.parse

    return (
        "mailto:"
        + urllib.parse.quote(recipient)
        + "?subject="
        + urllib.parse.quote(subject)
        + "&body="
        + urllib.parse.quote(body)
    )


def generate_gmail_compose(recipient: str, subject: str, body: str) -> str:
    import urllib.parse

    query = urllib.parse.urlencode(
        {
            "view": "cm",
            "fs": "1",
            "authuser": "ulziiuuree22@gmail.com",
            "to": recipient,
            "su": subject,
            "body": body,
        }
    )
    return f"https://mail.google.com/mail/?{query}"


def load_legal_info() -> list[tuple[str, str, str]]:
    try:
        response = requests.get(LEGALINFO_URL, timeout=20, headers={"Accept": "text/plain"})
        response.raise_for_status()
        text = response.text
        matches = re.findall(
            r"\[([^\]]+)\]\((https?:\/\/legalinfo\.mn\/mn\/law\/\d+)\)\s*\((\d+)\)",
            text,
        )
        return [(label.strip(), url, count) for label, url, count in matches[:5]]
    except Exception:
        return []


def load_admin_records() -> dict[str, pd.DataFrame]:
    workbook = pd.ExcelFile(EMPLOYEE_DATA_FILE)
    return {
        "salary": pd.read_excel(workbook, sheet_name=8),
        "leave": pd.read_excel(workbook, sheet_name=2),
        "orders": pd.read_excel(workbook, sheet_name=4),
        "profile": pd.read_excel(workbook, sheet_name=1),
    }


def render_ai_chat() -> None:
    employee = get_employee()
    if "ai_chat_messages" not in st.session_state:
        st.session_state.ai_chat_messages = []
    with st.popover("🤖 Monos AI Assistant", use_container_width=False):
        st.markdown("### 🤖 Monos AI Assistant")
        st.caption("Хүний нөөцийн туслах")
        st.link_button("ChatGPT нээх", "https://chatgpt.com/")
        quick_questions = [
            "Миний амралтын үлдэгдэл",
            "Цалингийн тодорхойлолт авах",
            "Чөлөө хэрхэн авах вэ?",
            "HR журам",
            "HR-тэй холбогдох",
        ]
        selected_question = st.selectbox("Quick questions", [""] + quick_questions, label_visibility="collapsed")
        question = st.text_area("Асуулт", value=selected_question, placeholder="Монгол хэлээр асуултаа бичнэ үү...", height=80, label_visibility="collapsed")
        send = st.button("Илгээх", type="primary", use_container_width=True)
        for message in st.session_state.ai_chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if send and question.strip():
            if not os.getenv("OPENAI_API_KEY"):
                st.error("OPENAI_API_KEY тохируулагдаагүй байна. Админ .env.local эсвэл deployment secret-д нэмнэ үү.")
                return
            st.session_state.ai_chat_messages.append({"role": "user", "content": question.strip()})
            with st.chat_message("assistant"):
                with st.spinner("Хариулт бэлтгэж байна..."):
                    response = st.write_stream(stream_openai_reply(st.session_state.ai_chat_messages, employee))
            st.session_state.ai_chat_messages.append({"role": "assistant", "content": response})


def stream_openai_reply(messages: list[dict], employee: dict):
    system_prompt = (
        "Та Monos HR Assistant. Монгол хэлээр эелдэг, товч, мэргэжлийн хариул. "
        "Зөвхөн доорх login хийсэн ажилтны мэдээллийг ашигла. Мэдэхгүй мэдээллийг зохиож болохгүй. "
        f"Одоогийн ажилтны мэдээлэл: {json.dumps(employee, ensure_ascii=False, default=str)}"
    )
    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "stream": True,
        "temperature": 0.2,
        "messages": [{"role": "system", "content": system_prompt}] + messages[-12:],
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"},
            json=payload,
            stream=True,
            timeout=60,
        )
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            delta = json.loads(data).get("choices", [{}])[0].get("delta", {}).get("content")
            if delta:
                yield delta
    except requests.RequestException as error:
        yield f"OpenAI холболт амжилтгүй боллоо: {error}"
    except (KeyError, json.JSONDecodeError):
        yield "AI хариуг боловсруулах үед алдаа гарлаа. Дахин оролдоно уу."


def dataframe_to_excel(dataframe: pd.DataFrame, filename: str) -> None:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Бүртгэл")
    st.download_button(
        "Excel татах",
        data=output.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"download_{filename}",
    )


def render_login():
    monos_header()
    st.title("MONOS HR Portal")
    st.caption("Employee access")

    with st.form("login_form"):
        employee_id = st.text_input("Employee ID", value="EMP001")
        password = st.text_input("Password", type="password", value="demo123")
        submitted = st.form_submit_button("Login")

        if submitted:
            selected_employee = authenticate_user(employee_id, password)
            if selected_employee:
                st.session_state.employee = selected_employee.copy()
                st.session_state.current_page = "admin" if selected_employee.get("is_admin") else "dashboard"
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Нэвтрэх мэдээлэл буруу байна.")

    st.info("Ажилтан: ID + demo123 | HR admin: HR001 / HR001")


def render_dashboard():
    monos_header()
    employee = get_employee()
    st.title(f"Сайн байна уу, {employee['name']} 👋")
    st.caption("Таны ажилтай холбоотой бүх мэдээлэл энд байна.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Сарын үндсэн цалин", employee["salary"])
    col2.metric("Үлдсэн амралт", f"{employee['leave_remaining']} хоног")
    col3.metric("Хүсэлтүүд", employee["request_count"])
    col4.metric("Ажилласан", f"{employee['service_years']} жил {employee['service_months']} сар")

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Сүүлийн үйл ажиллагаа")
        st.markdown(
            """
            - Ээлжийн амралтын хүсэлт — 2026.08.24 · 5 ажлын өдөр · Хүлээгдэж буй
            - Цалингийн тодорхойлолт — 2026.08.18 · PDF татсан · Бэлэн
            - Ажлын цагийн тухай асуулт — 2026.08.15 · HR-д илгээсэн · Нээлттэй
            """
        )

    with right:
        st.subheader("Хурдан үйлдэл")
        if st.button("Чөлөө авах"):
            st.session_state.current_page = "leave"
            st.rerun()
        if st.button("HR-д асуулт"):
            st.session_state.current_page = "hr"
            st.rerun()

    st.subheader("Live эрх зүйн мэдээлэл")
    legal_items = load_legal_info()
    if legal_items:
        for label, url, count in legal_items:
            st.markdown(f"- [{label}]({url}) — {count}")
        st.caption("Эх сурвалж: legalinfo.mn")
    else:
        st.warning("legalinfo.mn-ээс live мэдээлэл татаж чадсангүй. Дараагийн удаа дахин оролдоно.")
    render_ai_chat()


def mongolian_number_words(number: int) -> str:
    ones = ["тэг", "нэг", "хоёр", "гурав", "дөрөв", "тав", "зургаа", "долоо", "найм", "ес"]
    tens = ["", "", "хорь", "гуч", "дөч", "тавь", "жар", "дал", "ная", "ер"]
    if number < 10:
        return ones[number]
    if number < 20:
        return "арван " + ones[number - 10]
    if number < 100:
        return tens[number // 10] if number % 10 == 0 else tens[number // 10] + "ан " + ones[number % 10]
    if number < 1000:
        return ones[number // 100] + " зуун" if number % 100 == 0 else ones[number // 100] + " зуун " + mongolian_number_words(number % 100)
    if number < 1_000_000:
        thousands = number // 1000
        remainder = number % 1000
        result = mongolian_number_words(thousands) + " мянга"
        return result if remainder == 0 else result + " " + mongolian_number_words(remainder)
    millions = number // 1_000_000
    remainder = number % 1_000_000
    result = mongolian_number_words(millions) + " сая"
    return result if remainder == 0 else result + " " + mongolian_number_words(remainder)


def recipient_in_dative_case(recipient: str) -> str:
    recipient = recipient.strip()
    if not recipient:
        return "................................ -д"
    if recipient.lower().endswith("банк"):
        return recipient[:-4] + "банкинд"
    if recipient.endswith(("д", "т", "н")):
        return recipient + "д"
    return recipient + "д"


def next_certificate_number(employee_id: str) -> str:
    if "certificate_numbers" not in st.session_state:
        st.session_state.certificate_numbers = {}
    if employee_id not in st.session_state.certificate_numbers:
        sequence = len(st.session_state.certificate_numbers) + 1
        st.session_state.certificate_numbers[employee_id] = f"А/{datetime.now().year}-{sequence:03d}"
    return st.session_state.certificate_numbers[employee_id]


def register_pdf_fonts() -> None:
    font_candidates = [
        (Path(__file__).with_name("NotoSans-Regular.ttf"), Path(__file__).with_name("NotoSans-Bold.ttf")),
        (Path(r"C:\Windows\Fonts\arial.ttf"), Path(r"C:\Windows\Fonts\arialbd.ttf")),
        (Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")),
    ]
    regular_font, bold_font = next(
        ((regular, bold) for regular, bold in font_candidates if regular.exists() and bold.exists()),
        (None, None),
    )
    if regular_font is None:
        raise RuntimeError("Кирилл үсэг дэмждэг PDF фонт олдсонгүй.")
    if "ArialUnicode" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("ArialUnicode", str(regular_font)))
    if "ArialUnicode-Bold" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("ArialUnicode-Bold", str(bold_font)))


def generate_work_contract_pdf(recipient: str = "", document_number: str = "", document_date=None) -> bytes:
    employee = get_employee()
    template_path = Path(__file__).with_name("Тодорхойлолт загвар.pdf")
    if not template_path.exists():
        template_path = next(
            (path for path in Path.home().joinpath("Downloads").glob("*.pdf") if "Тодорхойлолт" in path.name),
            template_path,
        )

    if template_path.exists():
        overlay_buffer = BytesIO()
        overlay = canvas.Canvas(overlay_buffer, pagesize=A4)
        register_pdf_fonts()
        overlay.setFillColorRGB(1, 1, 1)
        overlay.rect(92, 300, 410, 270, fill=1, stroke=0)
        overlay.setFillColorRGB(0, 0, 0)
        overlay.setFont("ArialUnicode", 10.5)
        overlay.drawString(115, 590, f"Дугаар: {document_number or '........'}")
        overlay.drawRightString(490, 590, f"Огноо: {(document_date or datetime.now().date()).strftime('%Y-%m-%d')}")
        salary_words = mongolian_number_words(employee["salary_amount"])
        hire_date = pd.to_datetime(employee.get("hire_date"), errors="coerce")
        if pd.notna(hire_date):
            start_date = f"{hire_date.year} оны {hire_date.month}-р сараас"
        else:
            start_date = "ажилд орсон өдрөөс"
        body_style = ParagraphStyle(
            "EmbassyCertificateBody",
            fontName="ArialUnicode",
            fontSize=11,
            leading=18,
            alignment=TA_LEFT,
            textColor="#111111",
        )
        body = (
            f"<b>{recipient_in_dative_case(recipient)}</b><br/><br/>"
            f"{employee['surname']} овогтой {employee['name']} /РД: {employee['registry_number']}/ нь "
            f"“Монос Улаанбаатар” ХХК-ийн {employee['branch']} салбар эмийн санд "
            f"{employee['position']} албан тушаалд {start_date} эхлэн ажиллаж байгаа бөгөөд "
            f"сарын дундаж цалин нь {employee['salary_amount']:,} /{salary_words}/ төгрөг болно авдаг нь үнэн болно."
            "<br/><br/>"
            "Энэхүү тодорхойлолтыг гаргаснаар манай компани төлбөрийн болон бусад хариуцлага хүлээхгүй болно."
        )
        paragraph = Paragraph(body, body_style)
        paragraph.wrapOn(overlay, 390, 180)
        paragraph.drawOn(overlay, 105, 355)
        overlay.setFont("ArialUnicode-Bold", 10.5)
        overlay.drawString(125, 320, "ГҮЙЦЭТГЭХ ЗАХИРАЛ")
        overlay.drawString(365, 320, "Л.АЛТАНЦОГТ")
        overlay.setFont("ArialUnicode", 7.5)
        overlay.setFillColorRGB(0.05, 0.42, 0.28)
        overlay.drawString(365, 305, "eSign DEMO: VERIFIED")
        overlay.save()

        template_page = PdfReader(str(template_path)).pages[0]
        overlay_page = PdfReader(BytesIO(overlay_buffer.getvalue())).pages[0]
        template_page.merge_page(overlay_page)
        output = BytesIO()
        writer = PdfWriter()
        writer.add_page(template_page)
        writer.write(output)
        return output.getvalue()

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    register_pdf_fonts()
    addMapping("ArialUnicode", 0, 0, "ArialUnicode")
    addMapping("ArialUnicode", 1, 0, "ArialUnicode-Bold")

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CertificateTitle",
        parent=styles["Title"],
        fontName="ArialUnicode-Bold",
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor="#111111",
        spaceAfter=18,
    )
    body_style = ParagraphStyle(
        "CertificateBody",
        parent=styles["BodyText"],
        fontName="ArialUnicode",
        fontSize=11,
        leading=17,
        alignment=TA_LEFT,
        textColor="#111111",
        spaceAfter=7,
    )
    heading_style = ParagraphStyle(
        "CertificateHeading",
        parent=body_style,
        fontName="ArialUnicode-Bold",
        fontSize=12,
        leading=18,
        spaceBefore=9,
        spaceAfter=8,
    )
    story = []

    story.append(Paragraph("MONOS HR | АЛБАН ТОДОРХОЙЛОЛТ", title_style))
    story.append(Spacer(1, 18))
    story.append(Paragraph(f"Ажилтан: <b>{employee['full_name']}</b>", body_style))
    story.append(Paragraph(f"Албан тушаал: <b>{employee['position']}</b>", body_style))
    story.append(Paragraph(f"Хэлтэс: <b>{employee['department']}</b>", body_style))
    story.append(Paragraph(f"Байршил: <b>{employee['branch']}</b>", body_style))
    story.append(Paragraph(f"Имэйл: <b>{employee['email']}</b>", body_style))
    story.append(Paragraph(f"Утас: <b>{employee['phone']}</b>", body_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Ажлын үүрэг, хариуцлага:", heading_style))
    story.append(Paragraph("- Бүлэг болон компанийн зорилгод нийцүүлэн ажлын даалгавар гүйцэтгэх.", body_style))
    story.append(Paragraph("- Ажлын цагийн дэглэм, аюулгүй байдал, ёс зүй, баримт бичгийн менежментэд анхаарах.", body_style))
    story.append(Paragraph("- Хариуцлагатай, ёс зүйтэй, нээлттэй хамтран ажиллах.", body_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph(f"Мэргэжил: <b>{employee['profession']}</b>", body_style))
    story.append(Paragraph(f"Мэргэшсэн эсэх: <b>{employee['qualification']}</b>", body_style))
    story.append(Paragraph(f"Бүртгэсэн огноо: <b>{datetime.now().strftime('%Y-%m-%d')}</b>", body_style))

    doc.build(story)
    return buffer.getvalue()


def render_salary():
    monos_header()
    employee = get_employee()
    st.title("Цалин ба тодорхойлолт")
    st.caption("Цалингийн мэдээлэл болон албан тодорхойлолт.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Цалингийн тодорхойлолт")
        start_date = st.date_input("Эхлэх огноо", value=datetime(2026, 1, 1).date())
        end_date = st.date_input("Дуусах огноо", value=datetime(2026, 8, 28).date())
        document_number = next_certificate_number(employee["id"])
        st.text_input("Албан тоотын дугаар", value=document_number, disabled=True)
        document_date = st.date_input("Албан тоотын огноо", value=datetime.now().date())
        recipient = st.text_input("Ямар газарт", placeholder="Жишээ: Хаан банк")
        st.caption("Албан тоотын дугаарыг систем автоматаар бүртгэлээ.")
        st.metric("Үндсэн цалин", employee["salary"])
        st.download_button(
            label="Template татах",
            data=b"Monos HR Salary Template",
            file_name="Monos_Calingiin_Todorhoilolt_Template.txt",
            mime="text/plain",
        )

    with col2:
        st.subheader("Ажлын тодорхойлолтын сонголтууд")
        st.write("Таны албан тушаалын зорилго, үүрэг, шаардлагыг харах болон PDF татах боломжтой.")

        pdf_bytes = generate_work_contract_pdf(recipient, document_number, document_date)
        st.markdown("#### Баримт бичгийн үйлдлүүд")
        st.download_button(
            label="PDF татах",
            data=pdf_bytes,
            file_name="Monos_Ajlyn_Todorhoilolt.pdf",
            mime="application/pdf",
            key="certificate_pdf_download",
            use_container_width=True,
        )

        subject = f"Ажлын тодорхойлолт - {employee['full_name']}"
        body = (
            "Сайн байна уу,\n\n"
            f"Ажилтан: {employee['full_name']}\n"
            "Илгээгч: ulziiuuree22@gmail.com\n"
            f"Албан тоотын дугаар: {document_number}\n"
            f"Албан тоотын огноо: {document_date}\n"
            f"Хэнд: {recipient_in_dative_case(recipient)}\n"
            f"Албан тушаал: {employee['position']}\n"
            f"Имэйл: {employee['email']}\n"
            "Гүйцэтгэх захирлын eSign: DEMO VERIFIED\n"
            "Хавсаргасан PDF-ийг татаж авах боломжтой.\n\n"
            "Энэхүү баримт бичгийг тавтай морилно уу."
        )
        st.link_button(
            "HR бүртгэлд илгээх",
            generate_gmail_compose(HR_EMAIL, subject, body),
            use_container_width=True,
        )
        st.caption("Gmail нээгдсэний дараа from хаягийг ulziiuuree22@gmail.com сонгоод Send дарна.")


def render_leave():
    monos_header()
    employee = get_employee()
    st.title("Амралт, чөлөө")
    st.caption("Баланс болон хүсэлтүүдээ удирдаарай.")

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Шинэ чөлөөний хүсэлт")
        with st.form("leave_form"):
            leave_type = st.selectbox("Чөлөөний төрөл", ["Ээлжийн амралт", "Хувийн чөлөө", "Өвчтэй чөлөө"])
            total_days = st.number_input("Нийт хоног", min_value=1, max_value=7, value=1)
            start_date = st.date_input("Эхлэх огноо")
            end_date = st.date_input("Дуусах огноо")
            reason = st.text_area("Шалтгаан", placeholder="Таны шалтгааныг бичнэ үү...")
            submitted = st.form_submit_button("Илгээх")

            if submitted:
                subject = f"Чөлөөний хүсэлт - {employee['id']} - {leave_type}"
                body = (
                    "Сайн байна уу, HR багийнхаан,\n\n"
                    f"Ажилтан: {employee['full_name']}\n"
                    "Илгээгч: ulziiuuree22@gmail.com\n"
                    f"Employee ID: {employee['id']}\n"
                    f"Чөлөөний төрөл: {leave_type}\n"
                    f"Эхлэх огноо: {start_date}\n"
                    f"Дуусах огноо: {end_date}\n"
                    f"Нийт хоног: {total_days}\n"
                    f"Шалтгаан: {reason or 'Тодорхой шалтгаан оруулаагүй'}\n\n"
                    "Энэхүү хүсэлтийг хүлээн авч шийдвэрлэнэ үү."
                )
                st.link_button("Gmail-ээр HR руу илгээх", generate_gmail_compose(HR_EMAIL, subject, body))
                st.caption("Gmail нээгдсэний дараа from хаягийг ulziiuuree22@gmail.com сонгоод Send дарна.")

    with right:
        st.subheader("Амралтын мэдээлэл")
        st.write(f"Одоогийн үлдсэн амралт: **{employee['leave_remaining']}** хоног")
        st.write(f"Ашигласан: **{employee['leave_used']}** хоног")
        st.write(f"Нийт: **{employee['leave_total']}** хоног")


def render_schedule():
    monos_header()
    st.title("Ээлжийн хуваарь")
    st.caption("Ээлж болон ээлжийн тойм.")
    schedule = {
        "Даваа": "09:00–17:30",
        "Мягмар": "09:00–17:30",
        "Лхагва": "09:00–17:30",
        "Пүрэв": "09:00–17:30",
        "Баасан": "09:00–17:30",
    }
    for day, value in schedule.items():
        st.markdown(f"- **{day}** — {value}")


def render_orders():
    monos_header()
    st.title("Тушаал")
    st.caption("Шийдэгдсэн болон хүлээгдэж буй албан тушаалын баримтууд.")
    st.markdown("- Брэндийн стратеги — 2026.08.12 · Батлагдсан")
    st.markdown("- Зар сурталчилгааны төсөл — 2026.08.08 · Хүлээгдэж буй")


def render_social():
    monos_header()
    st.title("Нийгмийн даатгал")
    st.caption("НДШ болон даатгалын мэдээлэл.")
    st.markdown("- Нийт шимтгэл — 625,000 ₮")
    st.markdown("- Хамааралтай — Эрүүл мэнд, тэтгэврийн даатгал")


def render_profile():
    monos_header()
    employee = get_employee()
    st.title("Хувийн мэдээлэл")
    st.caption("Ажилтны мэдээлэл болон холбоо барих.")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Нэр", value=employee["name"])
            email = st.text_input("Имэйл", value=employee["email"])
            phone = st.text_input("Утас", value=employee["phone"])
            marital_status = st.selectbox("Гэрлэлтийн байдал", ["Гэрлэсэн", "Гэрлээгүй", "Тусдаа амьдардаг"], index=["Гэрлэсэн", "Гэрлээгүй", "Тусдаа амьдардаг"].index(employee["marital_status"]))
        with col2:
            last_name = st.text_input("Овог", value=employee["full_name"].split(" ")[-1])
            emergency_contact_name = st.text_input("Холбоо барих хүний нэр", value=employee["emergency_contact_name"])
            emergency_contact_phone = st.text_input("Холбоо барих хүний утас", value=employee["emergency_contact_phone"])
            driver_license = st.text_input("Жолооны үнэмлэх", value=employee["driver_license"])

        profession = st.text_input("Мэргэжил", value=employee["profession"])
        qualification = st.selectbox("Мэргэшсэн эсэх", ["Тийм", "Үгүй"], index=["Тийм", "Үгүй"].index(employee["qualification"]))

        submitted = st.form_submit_button("Хадгалах")
        if submitted:
            employee["name"] = first_name
            employee["full_name"] = f"{first_name} {last_name}"
            employee["email"] = email
            employee["phone"] = phone
            employee["marital_status"] = marital_status
            employee["emergency_contact_name"] = emergency_contact_name
            employee["emergency_contact_phone"] = emergency_contact_phone
            employee["driver_license"] = driver_license
            employee["profession"] = profession
            employee["qualification"] = qualification
            st.session_state.employee = employee
            st.success("Мэдээлэл амжилттай шинэчлэгдлээ.")


def render_hr():
    monos_header()
    employee = get_employee()
    st.title("HR-д асуулт")
    st.caption("Асуултаа илгээж, хариултыг хүлээн авна.")

    with st.form("hr_form"):
        category = st.selectbox("Ангилал", ["Цалин", "Амралт", "Ээлж", "Бусад"])
        question = st.text_area("Асуулт", placeholder="Асуултаа бичнэ үү...")
        submitted = st.form_submit_button("Илгээх")

        if submitted:
            subject = f"HR асуулт - {employee['id']} - {category}"
            body = (
                "Сайн байна уу, HR багийнхаан,\n\n"
                f"Ажилтан: {employee['full_name']}\n"
                "Илгээгч: ulziiuuree22@gmail.com\n"
                f"Employee ID: {employee['id']}\n"
                f"Ангилал: {category}\n"
                f"Асуулт: {question or 'Асуулт оруулаагүй'}\n\n"
                "Хариу өгнө үү."
            )
            st.link_button("Gmail-ээр HR руу илгээх", generate_gmail_compose(HR_EMAIL, subject, body))
            st.caption("Gmail нээгдсэний дараа from хаягийг ulziiuuree22@gmail.com сонгоод Send дарна.")


def render_admin():
    monos_header()
    st.title("HR Admin dashboard")
    st.caption(f"{HR_ADMIN['full_name']} · {HR_ADMIN['email']} · {HR_ADMIN['phone']}")
    records = load_admin_records()
    employees = records["profile"][["employee_id", "Овог", "Нэр", "Имэйл", "Утас"]].copy()
    for frame in records.values():
        frame["Ажилтны нэр"] = frame["employee_id"].map(
            employees.set_index("employee_id").apply(lambda row: f"{row['Овог']} {row['Нэр']}", axis=1)
        )

    salary_tab, leave_tab, orders_tab, profile_tab = st.tabs(
        ["Цалин", "Амралт, чөлөө", "Тушаал", "Хувийн мэдээлэл"]
    )
    with salary_tab:
        st.subheader("Цалингийн бүртгэл")
        st.dataframe(records["salary"], use_container_width=True, hide_index=True)
        dataframe_to_excel(records["salary"], "HR_Цалингийн_бүртгэл.xlsx")
    with leave_tab:
        st.subheader("Амралт, чөлөөний хүсэлтүүд")
        st.dataframe(records["leave"], use_container_width=True, hide_index=True)
        dataframe_to_excel(records["leave"], "HR_Амралт_чөлөөний_хүсэлт.xlsx")
    with orders_tab:
        st.subheader("Компанийн тушаал")
        st.dataframe(records["orders"], use_container_width=True, hide_index=True)
        dataframe_to_excel(records["orders"], "HR_Компанийн_тушаал.xlsx")
    with profile_tab:
        st.subheader("Ажилтны хувийн мэдээлэл")
        st.dataframe(records["profile"], use_container_width=True, hide_index=True)
        dataframe_to_excel(records["profile"], "HR_Ажилтны_хувийн_мэдээлэл.xlsx")


def render_page(page_name: str):
    if page_name == "dashboard":
        render_dashboard()
    elif page_name == "salary":
        render_salary()
    elif page_name == "leave":
        render_leave()
    elif page_name == "schedule":
        render_schedule()
    elif page_name == "orders":
        render_orders()
    elif page_name == "social":
        render_social()
    elif page_name == "profile":
        render_profile()
    elif page_name == "hr":
        render_hr()
    elif page_name == "admin":
        render_admin()
    else:
        render_dashboard()


if not st.session_state.authenticated:
    render_login()
else:
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    pages = ["admin"] if st.session_state.employee.get("is_admin") else list(NAV_ITEMS.keys())
    if st.session_state.current_page not in pages:
        st.session_state.current_page = pages[0]
    with st.sidebar:
        st.title("MONOS HR")
        selection = st.selectbox("Navigation", options=pages, index=pages.index(st.session_state.current_page), format_func=lambda x: NAV_ITEMS[x])
        st.session_state.current_page = selection
        st.button("Logout", on_click=lambda: st.session_state.__setitem__("authenticated", False))

    render_page("admin" if st.session_state.employee.get("is_admin") else st.session_state.current_page)
