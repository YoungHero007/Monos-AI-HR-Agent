from __future__ import annotations

import re
from datetime import datetime

import requests
import streamlit as st

st.set_page_config(page_title="MONOS HR Portal", page_icon="🧑‍💼", layout="wide")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --monos-bg: #f3efe9;
            --monos-card: #fffdfb;
            --monos-panel: #f8f5f2;
            --monos-primary: #1f2f2f;
            --monos-primary-soft: #2b4b46;
            --monos-accent: #d8b35f;
            --monos-accent-soft: #efe0b8;
            --monos-text: #181818;
            --monos-muted: #5b5b5b;
            --monos-border: #e3ddd6;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: var(--monos-bg);
            color: var(--monos-text);
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: var(--monos-bg);
        }

        [data-testid="stSidebar"] {
            background: #f7f4f1;
            border-right: 1px solid var(--monos-border);
        }

        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        .stButton > button,
        .stDownloadButton > button,
        .stFormSubmitButton > button {
            background: linear-gradient(180deg, #1d3b36 0%, #173230 100%);
            color: #fff;
            border: 0;
            border-radius: 12px;
            padding: 0.65rem 1rem;
            font-weight: 600;
            box-shadow: none;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stFormSubmitButton > button:hover {
            background: linear-gradient(180deg, #224a45 0%, #183832 100%);
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
            box-shadow: 0 2px 10px rgba(32, 35, 34, 0.03);
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
            letter-spacing: -0.02em;
        }

        .monos-header {
            background: rgba(255,255,255,0.45);
            border: 1px solid var(--monos-border);
            border-radius: 18px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            box-shadow: 0 6px 16px rgba(26, 37, 35, 0.04);
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
            background: linear-gradient(180deg, #1d2b2b 0%, #2d4a45 100%);
            color: #f9e7b4;
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
            background: rgba(23, 33, 33, 0.05);
            border: 1px solid var(--monos-border);
            color: var(--monos-primary);
            text-decoration: none;
            font-weight: 600;
        }

        .monos-link:hover {
            background: rgba(23, 33, 33, 0.08);
            text-decoration: none;
        }

        .monos-card {
            background: var(--monos-card);
            border: 1px solid var(--monos-border);
            border-radius: 18px;
            padding: 1.2rem;
            box-shadow: 0 8px 18px rgba(15, 22, 21, 0.03);
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
    "marital_status": "Гэрлэсэн",
    "emergency_contact_name": "Энхжаргал Бат",
    "emergency_contact_phone": "+976 99112244",
    "driver_license": "AB-123456",
    "profession": "Брэнд менежер",
    "qualification": "Тийм",
}

HR_EMAIL = "monosubmonos@gmail.com"
LEGALINFO_URL = "https://r.jina.ai/http://legalinfo.mn/mn"

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


def load_legal_info() -> list[tuple[str, str]]:
    try:
        response = requests.get(LEGALINFO_URL, timeout=20, headers={"Accept": "text/plain"})
        response.raise_for_status()
        text = response.text
        matches = re.findall(
            r"\[([^\]]+)\]\(https?:\/\/legalinfo\.mn\/mn\/law\/\d+\)\s*\((\d+)\)",
            text,
        )
        return [(label.strip(), count) for label, count in matches[:5]]
    except Exception:
        return []


def render_login():
    monos_header()
    st.title("MONOS HR Portal")
    st.caption("Employee access")

    with st.form("login_form"):
        employee_id = st.text_input("Employee ID", value="EMP001")
        password = st.text_input("Password", type="password", value="demo123")
        submitted = st.form_submit_button("Login")

        if submitted:
            if employee_id == EMPLOYEE["id"] and password == "demo123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Нэвтрэх мэдээлэл буруу байна.")

    st.info("Demo login: Employee: EMP001 / demo123 | Admin: admin / admin123")


def render_dashboard():
    monos_header()
    employee = get_employee()
    st.title(f"Сайн байна уу, {employee['name']} 👋")
    st.caption("Таны ажилтай холбоотой бүх мэдээлэл энд байна.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Сарын үндсэн цалин", employee["salary"])
    col2.metric("Үлдсэн амралт", f"{employee['leave_remaining']} хоног")
    col3.metric("Хүсэлтүүд", "2")
    col4.metric("Ажилласан", "4.2 жил 2 сар")

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
        for label, count in legal_items:
            st.markdown(f"- **{label}** — {count}")
        st.caption("Эх сурвалж: legalinfo.mn")
    else:
        st.warning("legalinfo.mn-ээс live мэдээлэл татаж чадсангүй. Дараагийн удаа дахин оролдоно.")


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
        st.metric("Үндсэн цалин", employee["salary"])
        st.download_button(
            label="Template татах",
            data=b"Monos HR Salary Template",
            file_name="Monos_Calingiin_Todorhoilolt_Template.txt",
            mime="text/plain",
        )

    with col2:
        st.subheader("Ажлын тодорхойлолт")
        st.write("Таны албан тушаалын зорилго, үүрэг, шаардлагыг харах болон PDF татах боломжтой.")
        if st.button("PDF татах"):
            st.success("Ажлын тодорхойлолтын PDF бэлэн боллоо (demo).")


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
                    f"Employee ID: {employee['id']}\n"
                    f"Чөлөөний төрөл: {leave_type}\n"
                    f"Эхлэх огноо: {start_date}\n"
                    f"Дуусах огноо: {end_date}\n"
                    f"Нийт хоног: {total_days}\n"
                    f"Шалтгаан: {reason or 'Тодорхой шалтгаан оруулаагүй'}\n\n"
                    "Энэхүү хүсэлтийг хүлээн авч шийдвэрлэнэ үү."
                )
                st.markdown(f"[HR руу илгээх]({generate_mailto(HR_EMAIL, subject, body)})")
                st.success("Хүсэлт бэлэн боллоо. Mail client нээгдэх болно.")

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
                f"Employee ID: {employee['id']}\n"
                f"Ангилал: {category}\n"
                f"Асуулт: {question or 'Асуулт оруулаагүй'}\n\n"
                "Хариу өгнө үү."
            )
            st.markdown(f"[HR руу илгээх]({generate_mailto(HR_EMAIL, subject, body)})")
            st.success("Асуулт бэлэн боллоо. Mail client нээгдэх болно.")


def render_admin():
    monos_header()
    st.title("Admin mode")
    st.caption("Системийн тойм болон статус.")
    st.markdown("- Идэвхтэй ажилтнууд — 128")
    st.markdown("- Үйлдэлтэй хүсэлт — 18")
    st.markdown("- Системийн төлөв — Healthy")


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

    pages = list(NAV_ITEMS.keys())
    with st.sidebar:
        st.title("MONOS HR")
        selection = st.selectbox("Navigation", options=pages, index=pages.index(st.session_state.current_page), format_func=lambda x: NAV_ITEMS[x])
        st.session_state.current_page = selection
        st.button("Logout", on_click=lambda: st.session_state.__setitem__("authenticated", False))

    render_page(st.session_state.current_page)
