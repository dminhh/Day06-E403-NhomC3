"""
AI Chăm Sóc Sức Khỏe - Ứng dụng chính
"""

import json
import sys
import os

import streamlit as st

# ── Page config (MUST be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="AI Chăm Sóc Sức Khỏe",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "AI Chăm Sóc Sức Khỏe v1.0 - Hỗ trợ phân tích đơn thuốc và triệu chứng",
    },
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules import llm, ocr, rxnorm, openfda, drug_interaction, symptom_engine, risk_engine

# ── CSS Styling ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Animated gradient header ── */
    .main-header {
        background: linear-gradient(135deg, #1a73e8 0%, #0052cc 50%, #003d99 100%);
        background-size: 200% 200%;
        animation: gradientShift 6s ease infinite;
        color: white;
        padding: 2.2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 32px rgba(26,115,232,0.35);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%; right: -20%;
        width: 300px; height: 300px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }
    .main-header::after {
        content: "";
        position: absolute;
        bottom: -40%; left: -10%;
        width: 200px; height: 200px;
        background: rgba(255,255,255,0.04);
        border-radius: 50%;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header h1 {
        margin: 0; font-size: 2rem; font-weight: 800;
        letter-spacing: -0.5px; position: relative; z-index: 1;
    }
    .main-header p {
        margin: 0.5rem 0 0; opacity: 0.88; font-size: 0.98rem;
        font-weight: 400; position: relative; z-index: 1;
    }

    /* ── Risk cards with animation ── */
    .risk-card {
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        margin: 0.7rem 0;
        border-left: 5px solid;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        animation: slideIn 0.3s ease;
    }
    .risk-card:hover { transform: translateX(3px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    .risk-emergency { background:linear-gradient(135deg,#fff5f5,#fed7d7); border-color:#dc3545; }
    .risk-high      { background:linear-gradient(135deg,#fffaf0,#feebc8); border-color:#fd7e14; }
    .risk-medium    { background:linear-gradient(135deg,#fffff0,#fefcbf); border-color:#ffc107; }
    .risk-low       { background:linear-gradient(135deg,#f0fff4,#c6f6d5); border-color:#28a745; }
    .risk-safe      { background:linear-gradient(135deg,#f0fff4,#c6f6d5); border-color:#198754; }

    /* ── Drug cards ── */
    .drug-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin: 0.6rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: box-shadow 0.2s ease;
    }
    .drug-card:hover { box-shadow: 0 4px 16px rgba(26,115,232,0.15); }
    .drug-card h4 { color: #1a73e8; margin: 0 0 0.6rem; font-size: 1rem; font-weight: 700; }
    .drug-card table { font-size: 0.84rem; }
    .drug-card td:first-child { color: #64748b; width: 110px; padding: 2px 8px 2px 0; }
    .drug-card td:last-child { color: #1e293b; font-weight: 500; }

    /* ── Badges ── */
    .interaction-badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 0.2rem;
        letter-spacing: 0.01em;
    }
    .badge-danger  { background:#fee2e2; color:#dc2626; border:1px solid #fca5a5; }
    .badge-warning { background:#fef3c7; color:#d97706; border:1px solid #fcd34d; }
    .badge-info    { background:#dbeafe; color:#2563eb; border:1px solid #93c5fd; }
    .badge-success { background:#dcfce7; color:#16a34a; border:1px solid #86efac; }

    /* ── Section headers ── */
    .section-header {
        background: linear-gradient(90deg, #eff6ff, #f8faff);
        border-left: 4px solid #1a73e8;
        padding: 0.55rem 1rem;
        border-radius: 0 10px 10px 0;
        margin: 1.2rem 0 0.8rem;
        font-weight: 700;
        font-size: 0.9rem;
        color: #1a73e8;
        letter-spacing: 0.01em;
    }

    /* ── Follow-up questions ── */
    .followup-question {
        background: linear-gradient(135deg, #f0f7ff, #eff6ff);
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        padding: 0.55rem 0.9rem;
        margin: 0.35rem 0;
        color: #1e3a5f;
        font-size: 0.88rem;
        font-weight: 500;
    }

    /* ── Metric boxes ── */
    .metric-box {
        background: white;
        border-radius: 14px;
        padding: 1.1rem 0.8rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
        transition: transform 0.15s ease;
    }
    .metric-box:hover { transform: translateY(-2px); }
    .metric-box .value { font-size: 1.05rem; font-weight: 700; color: #1e293b; line-height: 1.3; }
    .metric-box .label { font-size: 0.72rem; color: #94a3b8; margin-top: 0.25rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

    /* ── Risk score progress bar ── */
    .risk-bar-wrap {
        background: #f1f5f9;
        border-radius: 99px;
        height: 10px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .risk-bar-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 0.8s cubic-bezier(.4,0,.2,1);
    }

    /* ── Disclaimer ── */
    .disclaimer {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border: 1px solid #fcd34d;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #92400e;
        margin: 1rem 0;
        line-height: 1.5;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(26,115,232,0.3) !important;
        letter-spacing: 0.01em !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(26,115,232,0.4) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── Result explanation panel ── */
    .result-explanation {
        background: white;
        border-radius: 16px;
        padding: 1.6rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
        line-height: 1.8;
        font-size: 0.93rem;
        color: #334155;
        animation: fadeIn 0.4s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Sidebar ── */
    div[data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #f8faff 0%, #f1f5f9 100%);
    }

    /* ── Sidebar logo ── */
    .sidebar-logo {
        text-align: center;
        padding: 1.2rem 0 0.8rem;
    }
    .sidebar-logo .pulse-ring {
        display: inline-block;
        width: 72px; height: 72px;
        background: linear-gradient(135deg, #1a73e8, #0052cc);
        border-radius: 50%;
        font-size: 2rem;
        line-height: 72px;
        box-shadow: 0 0 0 0 rgba(26,115,232,0.4);
        animation: pulse 2.5s infinite;
    }
    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(26,115,232,0.4); }
        70%  { box-shadow: 0 0 0 12px rgba(26,115,232,0); }
        100% { box-shadow: 0 0 0 0 rgba(26,115,232,0); }
    }
    .sidebar-logo h2 { color: #1a73e8; font-size: 1.15rem; font-weight: 800; margin: 0.5rem 0 0.1rem; }
    .sidebar-logo small { color: #94a3b8; font-size: 0.75rem; }

    /* ── Emergency banner ── */
    .emergency-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        border-radius: 14px;
        padding: 1rem 1.3rem;
        margin: 0.5rem 0;
        animation: emergencyPulse 1s ease infinite;
        box-shadow: 0 4px 20px rgba(220,38,38,0.4);
    }
    @keyframes emergencyPulse {
        0%, 100% { box-shadow: 0 4px 20px rgba(220,38,38,0.4); }
        50%       { box-shadow: 0 4px 28px rgba(220,38,38,0.7); }
    }

    /* ── Status chip ── */
    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.3rem 0.8rem;
        border-radius: 99px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .chip-ok   { background:#dcfce7; color:#166534; }
    .chip-warn { background:#fef3c7; color:#92400e; }
    .chip-err  { background:#fee2e2; color:#991b1b; }

    /* ── Streamlit overrides ── */
    [data-testid="stExpander"] { border-radius: 12px !important; border: 1px solid #e2e8f0 !important; }
    .stTextArea textarea { border-radius: 10px !important; border: 1px solid #cbd5e1 !important; font-size: 0.92rem !important; }
    .stTextInput input { border-radius: 10px !important; border: 1px solid #cbd5e1 !important; }
    [data-testid="stFileUploader"] { border-radius: 12px !important; }
    .stRadio label { font-size: 0.9rem !important; }
    .stTabs [data-baseweb="tab"] { font-weight: 600 !important; font-size: 0.85rem !important; }
    .stTabs [aria-selected="true"] { color: #1a73e8 !important; }
    div.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ── Helper utilities ─────────────────────────────────────────────────────────

def risk_card_class(level: str) -> str:
    mapping = {
        "khẩn cấp": "risk-emergency",
        "cao": "risk-high",
        "trung bình": "risk-medium",
        "thấp": "risk-low",
        "an toàn": "risk-safe",
    }
    return mapping.get(level, "risk-low")


def render_risk_banner(risk_level: str, risk_score: int, icon: str, label: str):
    css_class = risk_card_class(risk_level)
    cfg = risk_engine.get_risk_config(risk_level)
    bar_color = cfg["color"]
    bar_width = max(4, risk_score)
    st.markdown(
        f"""<div class="risk-card {css_class}">
        <div style="display:flex;align-items:center;justify-content:space-between">
            <div>
                <span style="font-size:1.6rem">{icon}</span>
                <strong style="font-size:1.05rem; margin-left:0.5rem">Mức độ rủi ro</strong>
            </div>
            <span style="background:{bar_color};color:white;padding:0.3rem 1rem;
                         border-radius:99px;font-size:0.85rem;font-weight:700;
                         letter-spacing:0.05em">{label}</span>
        </div>
        <div class="risk-bar-wrap" style="margin-top:0.7rem">
            <div class="risk-bar-fill" style="width:{bar_width}%;background:{bar_color}"></div>
        </div>
        <small style="color:#64748b">{risk_score}/100 điểm rủi ro</small>
        </div>""",
        unsafe_allow_html=True,
    )


def render_interaction(ix: dict):
    sev = ix.get("severity", "nhẹ")
    cfg = drug_interaction.SEVERITY_EMOJI.get(sev, "⚠️")
    color = drug_interaction.SEVERITY_COLORS.get(sev, "#ffc107")
    st.markdown(
        f"""<div class="risk-card" style="border-color:{color}; background:{color}22">
        <strong>{cfg} {ix['drug_a']} ↔ {ix['drug_b']}</strong>
        <span style="float:right; background:{color}; color:{'white' if sev in ['nặng','chống chỉ định'] else '#212529'};
              padding:2px 10px; border-radius:20px; font-size:0.8rem; font-weight:600">{sev.upper()}</span>
        <br/><p style="margin:0.5rem 0 0.2rem">{ix['description']}</p>
        <p style="margin:0; font-weight:600; color:#495057">💡 {ix['recommendation']}</p>
        </div>""",
        unsafe_allow_html=True,
    )


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>
        <div class='pulse-ring'>🏥</div>
        <h2>AI Sức Khỏe</h2>
        <small>v1.0 | GPT-OSS-20B</small>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Chức năng",
        ["🔬 Phân tích đơn thuốc", "💊 Tra cứu thuốc"],
        label_visibility="collapsed",
    )

    st.divider()

    # Quick stats row
    import sys
    ocr_ok = ocr.is_available()
    ocr_ver = ocr.get_version() if ocr_ok else ocr.get_error()
    ocr_label = f"✅ v{ocr_ver}" if ocr_ok else "⚠️ Chưa cài"
    ocr_cls   = "chip-ok" if ocr_ok else "chip-warn"
    st.markdown(f"""
    <div style='font-size:0.82rem; color:#64748b; margin-bottom:0.5rem'>
        <b>PaddleOCR:</b> <span class='status-chip {ocr_cls}'>{ocr_label}</span>
    </div>
    <div style='font-size:0.82rem; color:#64748b; margin-bottom:0.5rem'>
        <b>LLM:</b> <span class='status-chip chip-ok'>✅ GPT-OSS-20B</span>
    </div>
    <div style='font-size:0.82rem; color:#64748b'>
        <b>APIs:</b> <span class='status-chip chip-ok'>✅ RxNorm + FDA</span>
    </div>
    """, unsafe_allow_html=True)

    if not ocr_ok:
        with st.expander("🔍 Lỗi OCR chi tiết"):
            st.code(f"Python: {sys.executable}\nLỗi: {ocr.get_error()}", language="text")

    st.divider()

    st.markdown("""
    <div class='disclaimer'>
    ⚕️ <b>Lưu ý y tế:</b> Chỉ mang tính tham khảo.
    Luôn hỏi ý kiến bác sĩ trước khi quyết định.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size:0.85rem; color:#475569; line-height:2'>
    📞 Cấp cứu: <b style='color:#dc2626'>115</b><br/>
    📞 Sức khỏe: <b>1800 9095</b>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1 — ĐƠN THUỐC
# ═══════════════════════════════════════════════════════════════════════════

if page == "🔬 Phân tích đơn thuốc":
    st.markdown("""
    <div class='main-header'>
        <h1>🔬 Phân tích đơn thuốc</h1>
        <p>Tải ảnh đơn thuốc hoặc nhập tay để nhận hướng dẫn sử dụng chi tiết</p>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("<div class='section-header'>📄 Nhập thông tin đơn thuốc</div>", unsafe_allow_html=True)
        input_method = st.radio("Phương thức nhập", ["📷 Tải ảnh đơn thuốc", "✏️ Nhập tay văn bản"], horizontal=True)
        ocr_text = ""

        if input_method == "📷 Tải ảnh đơn thuốc":
            uploaded = st.file_uploader("Chọn ảnh đơn thuốc", type=["jpg","jpeg","png","bmp","tiff"])
            if uploaded:
                st.image(uploaded, caption="Ảnh đơn thuốc")
                if ocr.is_available():
                    with st.spinner("🔍 Đang đọc văn bản từ ảnh..."):
                        ocr_text, confidence = ocr.extract_text(uploaded)
                    if ocr_text.startswith("__error__:"):
                        st.warning(f"⚠️ OCR lỗi: `{ocr_text.replace('__error__:','')[:100]}`")
                        ocr_text = ""
                    elif ocr_text and not ocr_text.startswith("Lỗi"):
                        # Validate xem có phải đơn thuốc không
                        with st.spinner("🔎 Kiểm tra nội dung ảnh..."):
                            check = llm.validate_prescription_image(ocr_text)
                        is_rx = check.get("is_prescription") or check.get("is_pharmacy_invoice")
                        quality = check.get("image_quality", "rõ")
                        if not is_rx:
                            st.warning("⚠️ Ảnh không nhận diện đơn thuốc. Vui lòng thử lại ảnh khác.")
                            ocr_text = ""
                        elif quality in ["mờ", "thiếu thông tin"]:
                            st.warning(f"⚠️ Ảnh **{quality}** — một số thông tin có thể không chính xác. Vui lòng kiểm tra lại kết quả.")
                            with st.expander("📝 Văn bản đọc được"):
                                st.text(ocr_text)
                            # Hỏi user bổ sung
                            extra = st.text_area("Bổ sung thông tin còn thiếu (nếu có):", height=80)
                            if extra:
                                ocr_text = ocr_text + "\n" + extra
                        else:
                            st.success(f"✅ Đọc thành công (độ tin cậy: {confidence:.0%})")
                            with st.expander("📝 Văn bản trích xuất (đã làm sạch)"):
                                with st.spinner("Đang định dạng..."):
                                    clean_text = llm.format_ocr_text(ocr_text)
                                st.markdown(clean_text)
                    else:
                        st.warning("⚠️ Không đọc được văn bản. Vui lòng nhập tay.")
                        ocr_text = ""
                else:
                    st.warning("⚠️ PaddleOCR chưa cài. Vui lòng nhập văn bản thủ công.")

                if not ocr_text:
                    ocr_text = st.text_area("Nhập thủ công nội dung đơn thuốc", height=200,
                                            placeholder="Nhập tên thuốc, liều lượng, hướng dẫn...")
        else:
            ocr_text = st.text_area("Nhập nội dung đơn thuốc", height=250,
                placeholder="Bệnh nhân: Nguyễn Văn A, 45 tuổi\nChẩn đoán: Tăng huyết áp\n1. Amlodipine 5mg - 1 viên/ngày\n2. Metformin 500mg - 2 viên/ngày")

        with st.expander("👤 Thông tin bệnh nhân bổ sung (tuỳ chọn)"):
            col_a, col_b = st.columns(2)
            with col_a:
                patient_age = st.number_input("Tuổi", 0, 120, 0)
                patient_weight = st.number_input("Cân nặng (kg)", 0, 300, 0)
            with col_b:
                patient_conditions = st.multiselect("Bệnh nền",
                    ["Tiểu đường","Tăng huyết áp","Suy thận","Suy gan","Tim mạch","Thai kỳ","Cho con bú"])
                patient_allergies = st.text_input("Dị ứng thuốc (nếu có)")

        analyze_btn = st.button("🔍 Phân tích đơn thuốc")

    with col_result:
        if analyze_btn and ocr_text and ocr_text.strip():
            patient_ctx = {
                "age": patient_age or "Không rõ",
                "weight": patient_weight or "Không rõ",
                "conditions": patient_conditions,
                "allergies": patient_allergies,
            }

            # Bước 1: Trích xuất thông tin đơn
            with st.spinner("🤖 AI đang phân tích đơn thuốc..."):
                prescription = llm.extract_prescription(ocr_text)

            if "error" in prescription:
                st.error(f"Lỗi: {prescription.get('raw', prescription['error'])}")
                st.stop()

            # Cảnh báo thông tin thiếu
            missing = prescription.get("missing_info", [])
            if missing:
                st.warning(f"⚠️ Đơn thiếu thông tin: **{', '.join(missing)}**. Vui lòng bổ sung hoặc hỏi lại bác sĩ/dược sĩ.")

            # Thông tin bệnh nhân
            st.markdown("<div class='section-header'>📋 Thông tin đơn thuốc</div>", unsafe_allow_html=True)
            info_cols = st.columns(3)
            with info_cols[0]:
                st.markdown(f"""<div class='metric-box'>
                    <div class='value' style='font-size:1rem'>👤 {prescription.get('patient_name','—')}</div>
                    <div class='label'>Bệnh nhân</div></div>""", unsafe_allow_html=True)
            with info_cols[1]:
                st.markdown(f"""<div class='metric-box'>
                    <div class='value' style='font-size:0.9rem'>🏥 {prescription.get('hospital','—')}</div>
                    <div class='label'>Cơ sở y tế</div></div>""", unsafe_allow_html=True)
            with info_cols[2]:
                st.markdown(f"""<div class='metric-box'>
                    <div class='value' style='font-size:0.9rem'>📅 {prescription.get('date','—')}</div>
                    <div class='label'>Ngày kê đơn</div></div>""", unsafe_allow_html=True)

            if prescription.get("diagnosis"):
                st.info(f"🔍 **Chẩn đoán:** {prescription['diagnosis']}")

            # Danh sách thuốc
            medications = prescription.get("medications", [])
            med_names = [m.get("name","") for m in medications if m.get("name")]

            st.markdown("<div class='section-header'>💊 Danh sách thuốc</div>", unsafe_allow_html=True)
            if medications:
                for med in medications:
                    name = med.get("name", "Không rõ")
                    # Cảnh báo nếu không tìm thấy thuốc
                    not_found = not med.get("found_in_database", True) or (
                        not med.get("dosage") and not med.get("frequency")
                    )
                    border = "border-left: 4px solid #fbbf24;" if not_found else ""
                    st.markdown(f"""<div class='drug-card' style='{border}'>
                        <h4>💊 {name}</h4>
                        <table style='width:100%; font-size:0.85rem'>
                        <tr><td><b>Liều lượng:</b></td><td>{med.get('dosage') or '—'}</td></tr>
                        <tr><td><b>Tần suất:</b></td><td>{med.get('frequency') or '—'}</td></tr>
                        <tr><td><b>Thời gian:</b></td><td>{med.get('duration') or '—'}</td></tr>
                        <tr><td><b>Hướng dẫn:</b></td><td>{med.get('instructions') or '—'}</td></tr>
                        </table>
                        {'<p style="color:#d97706;font-size:0.82rem;margin:0.3rem 0 0">⚠️ Không tìm thấy thông tin đầy đủ — vui lòng hỏi dược sĩ</p>' if not_found else ''}
                        </div>""", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Không nhận dạng được danh sách thuốc. Đơn có thể mờ hoặc thiếu thông tin.")
                st.stop()

            # Bước 2: Kiểm tra tương tác NGUY HIỂM
            dangerous_interactions = []
            if med_names:
                with st.spinner("⚡ Kiểm tra tương tác thuốc..."):
                    all_interactions = drug_interaction.check_interactions(med_names)
                    dangerous_interactions = [i for i in all_interactions
                                              if i.get("severity") in ["nặng","chống chỉ định"]]

                if dangerous_interactions:
                    st.markdown("<div class='section-header'>🚨 Cảnh báo tương tác nguy hiểm</div>", unsafe_allow_html=True)
                    for ix in dangerous_interactions:
                        sev = ix.get("severity","")
                        is_contraindicated = sev == "chống chỉ định"
                        st.markdown(f"""
                        <div style='background:{"#fee2e2" if is_contraindicated else "#fef3c7"};
                                    border:2px solid {"#dc2626" if is_contraindicated else "#f59e0b"};
                                    border-radius:12px;padding:1rem 1.2rem;margin:0.5rem 0'>
                            <div style='font-weight:700;color:{"#991b1b" if is_contraindicated else "#92400e"}'>
                                {"🚫 CHỐNG CHỈ ĐỊNH" if is_contraindicated else "⚠️ TƯƠNG TÁC NGUY HIỂM"}:
                                {ix['drug_a']} + {ix['drug_b']}
                            </div>
                            <p style='margin:0.5rem 0 0.3rem'>{ix['description']}</p>
                            <p style='margin:0;font-weight:600'>💬 <b>Yêu cầu xác nhận lại với bác sĩ trước khi dùng.</b></p>
                        </div>""", unsafe_allow_html=True)

            # Bước 3: Giải thích AI (markdown trực tiếp — không wrap trong HTML)
            with st.spinner("📝 AI đang soạn hướng dẫn sử dụng..."):
                drug_info_str = json.dumps(medications, ensure_ascii=False)
                explanation = llm.explain_prescription(
                    drug_info=drug_info_str,
                    dangerous_interactions=dangerous_interactions,
                    patient_info=patient_ctx,
                )

            st.markdown("<div class='section-header'>📝 Hướng dẫn sử dụng đơn thuốc</div>", unsafe_allow_html=True)
            # Dùng st.markdown trực tiếp để render đúng heading/bold/list
            st.markdown(explanation)

        elif analyze_btn:
            st.warning("⚠️ Vui lòng nhập nội dung đơn thuốc trước khi phân tích.")
        else:
            st.markdown("""
            <div style='text-align:center;padding:3rem;color:#6c757d'>
                <span style='font-size:4rem'>📋</span>
                <p style='margin-top:1rem;font-size:1.1rem'>Tải ảnh hoặc nhập đơn thuốc ở bên trái để bắt đầu</p>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2 — TRA CỨU THUỐC
# ═══════════════════════════════════════════════════════════════════════════

if page == "💊 Tra cứu thuốc":
    st.markdown("""
    <div class='main-header'>
        <h1>💊 Tra cứu thông tin thuốc</h1>
        <p>Tìm kiếm thông tin chi tiết về thuốc từ RxNorm và OpenFDA</p>
    </div>
    """, unsafe_allow_html=True)

    col_search, col_result = st.columns([1, 1.5], gap="large")

    with col_search:
        st.markdown("<div class='section-header'>🔍 Tìm kiếm thuốc</div>", unsafe_allow_html=True)

        search_tab, img_tab = st.tabs(["✏️ Nhập tên thuốc", "📷 Nhận diện qua ảnh"])

        with search_tab:
            drug_query = st.text_input("Tên thuốc", placeholder="VD: Metformin, Aspirin...", key="drug_query")
            search_btn = st.button("🔍 Tra cứu")

        with img_tab:
            drug_img = st.file_uploader("Ảnh hộp/vỉ thuốc", type=["jpg","jpeg","png"], key="drug_img")
            img_search_btn = st.button("🔍 Nhận diện thuốc từ ảnh")
            drug_query_from_img = ""
            if img_search_btn and drug_img:
                if ocr.is_available():
                    with st.spinner("🔍 Đang đọc ảnh thuốc..."):
                        img_text, _ = ocr.extract_text(drug_img)
                    if img_text and not img_text.startswith("Lỗi"):
                        with st.spinner("🤖 Nhận diện tên thuốc..."):
                            drug_info_img = llm.extract_drug_from_image_text(img_text)
                        if drug_info_img.get("is_drug") is False:
                            st.error("❌ Ảnh này không phải hộp thuốc. Vui lòng chụp lại.")
                        else:
                            name = drug_info_img.get("drug_name") or drug_info_img.get("brand_name","")
                            if name:
                                drug_query_from_img = name
                                st.success(f"✅ Nhận diện được: **{name}**")
                                if drug_info_img.get("active_ingredient"):
                                    st.info(f"Hoạt chất: {drug_info_img['active_ingredient']}")
                            else:
                                st.warning("⚠️ Không nhận diện được tên thuốc. Vui lòng nhập tay.")
                    else:
                        st.warning("⚠️ Không đọc được ảnh.")
                else:
                    st.warning("⚠️ PaddleOCR chưa cài.")
            # Dùng tên nhận diện được để tra cứu
            if drug_query_from_img:
                search_btn = True
                drug_query = drug_query_from_img

        st.markdown("<div class='section-header'>⚡ Kiểm tra tương tác nhiều thuốc</div>", unsafe_allow_html=True)
        multi_drugs = st.text_area("Danh sách thuốc (mỗi dòng một thuốc)", height=120,
                                   placeholder="Metformin\nAspirin\nWarfarin\nOmeprazole")
        check_multi_btn = st.button("⚡ Kiểm tra tương tác")

    with col_result:
        if search_btn and drug_query.strip():
            # RxNorm search
            with st.spinner("🔄 Tìm kiếm trên RxNorm..."):
                rx_results = rxnorm.search_drug(drug_query)

            found_any = False

            if rx_results:
                found_any = True
                st.markdown("<div class='section-header'>📚 Kết quả từ RxNorm</div>", unsafe_allow_html=True)
                for rx in rx_results[:3]:
                    st.markdown(f"""<div class='drug-card'>
                        <h4>💊 {rx['name']}</h4>
                        <small>RxCUI: <code>{rx['rxcui']}</code> | Loại: {rx.get('tty','—')}</small>
                        </div>""", unsafe_allow_html=True)

            with st.spinner("🌐 Lấy thông tin từ OpenFDA..."):
                fda_info = openfda.get_label(drug_query)

            if fda_info:
                found_any = True
                st.markdown("<div class='section-header'>📋 Thông tin chi tiết</div>", unsafe_allow_html=True)
                tab1, tab2, tab3, tab4 = st.tabs(["📖 Chỉ định", "⚠️ Cảnh báo", "🚫 Chống chỉ định", "💊 Liều dùng"])

                with tab1:
                    raw = (fda_info.get("indications",[""])[0] or "").strip()
                    if raw:
                        with st.spinner("Đang dịch..."):
                            st.markdown(llm.translate_fda_section(raw, "Chỉ định & Công dụng"))
                    else:
                        st.info("Không có thông tin.")

                with tab2:
                    raw = (fda_info.get("warnings",[""])[0] or "").strip()
                    if raw:
                        with st.spinner("Đang dịch..."):
                            st.markdown(llm.translate_fda_section(raw, "Cảnh báo"))
                    else:
                        st.info("Không có thông tin.")

                with tab3:
                    raw = (fda_info.get("contraindications",[""])[0] or "").strip()
                    if raw:
                        with st.spinner("Đang dịch..."):
                            st.markdown(llm.translate_fda_section(raw, "Chống chỉ định"))
                    else:
                        st.info("Không có thông tin.")

                with tab4:
                    raw = (fda_info.get("dosage",[""])[0] or "").strip()
                    if raw:
                        with st.spinner("Đang dịch..."):
                            st.markdown(llm.translate_fda_section(raw, "Liều dùng"))
                    else:
                        st.info("Không có thông tin.")

                with st.spinner("📊 Tải & dịch tác dụng phụ..."):
                    adverse_en = openfda.get_adverse_events(drug_query, limit=8)
                    adverse_vi = llm.translate_adverse_events(adverse_en) if adverse_en else []
                if adverse_vi:
                    st.markdown("<div class='section-header'>📊 Tác dụng phụ thường gặp</div>", unsafe_allow_html=True)
                    badges_html = "".join(f"<span class='interaction-badge badge-warning'>{a}</span>" for a in adverse_vi)
                    st.markdown(badges_html, unsafe_allow_html=True)

                with st.spinner("🔔 Kiểm tra thu hồi..."):
                    recalls = openfda.get_recalls(drug_query)
                if recalls:
                    st.warning(f"⚠️ Có **{len(recalls)}** thông báo thu hồi liên quan")
                    for rec in recalls:
                        date_str = rec.get('date', '')
                        date_fmt = f"{date_str[6:8]}/{date_str[4:6]}/{date_str[:4]}" if len(date_str) == 8 else date_str
                        status_vi = {"Ongoing": "Đang xử lý", "Completed": "Đã hoàn tất", "Terminated": "Đã chấm dứt"}.get(rec.get('status',''), rec.get('status',''))
                        with st.spinner("Đang dịch..."):
                            reason_vi = llm.translate_recall(rec.get('reason',''))
                        st.markdown(f"- **{date_fmt}** ({status_vi}): {reason_vi}")

            if not found_any:
                st.error("❌ Không tìm thấy thông tin về thuốc này.")
                st.warning("⚠️ Vui lòng hỏi dược sĩ để được tư vấn chính xác.")

        # Multi-drug interaction check
        if check_multi_btn and multi_drugs.strip():
            drug_list = [d.strip() for d in multi_drugs.strip().split("\n") if d.strip()]
            if len(drug_list) < 2:
                st.warning("Cần ít nhất 2 thuốc để kiểm tra tương tác.")
            else:
                with st.spinner(f"⚡ Kiểm tra tương tác {len(drug_list)} thuốc..."):
                    interactions = drug_interaction.check_interactions(drug_list)

                st.markdown(f"<div class='section-header'>⚡ Kết quả tương tác ({len(drug_list)} thuốc)</div>", unsafe_allow_html=True)

                if interactions:
                    st.warning(f"⚠️ Phát hiện **{len(interactions)}** tương tác thuốc")
                    for ix in interactions:
                        render_interaction(ix)
                else:
                    st.markdown("""<div class='risk-card risk-safe'>
                        ✅ <strong>Không phát hiện tương tác nguy hiểm</strong> trong danh sách thuốc đã nhập.
                        Lưu ý: Cơ sở dữ liệu chưa bao gồm tất cả tương tác.
                        </div>""", unsafe_allow_html=True)

        if not search_btn and not check_multi_btn:
            st.markdown("""
            <div style='text-align:center; padding:3rem; color:#6c757d'>
                <span style='font-size:4rem'>💊</span>
                <p style='font-size:1.1rem; margin-top:1rem'>Nhập tên thuốc để tra cứu thông tin</p>
                <br/>
                <div style='text-align:left; max-width:300px; margin:0 auto'>
                <strong>Thông tin cung cấp:</strong>
                <ul>
                <li>Tên thương mại & generic (RxNorm)</li>
                <li>Chỉ định, chống chỉ định (OpenFDA)</li>
                <li>Cảnh báo & tác dụng phụ</li>
                <li>Liều dùng khuyến cáo</li>
                <li>Kiểm tra thu hồi</li>
                </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center; padding:0.8rem 0 0.4rem'>
    <div style='display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap;margin-bottom:0.5rem'>
        <span style='background:#dbeafe;color:#1d4ed8;padding:0.25rem 0.8rem;border-radius:99px;font-size:0.75rem;font-weight:600'>🤖 GPT-OSS-20B</span>
        <span style='background:#dcfce7;color:#166534;padding:0.25rem 0.8rem;border-radius:99px;font-size:0.75rem;font-weight:600'>📋 PaddleOCR</span>
        <span style='background:#f3e8ff;color:#7c3aed;padding:0.25rem 0.8rem;border-radius:99px;font-size:0.75rem;font-weight:600'>💊 RxNorm</span>
        <span style='background:#fef3c7;color:#d97706;padding:0.25rem 0.8rem;border-radius:99px;font-size:0.75rem;font-weight:600'>🌐 OpenFDA</span>
    </div>
    <div style='color:#94a3b8;font-size:0.78rem'>
        🏥 AI Chăm Sóc Sức Khỏe v1.0 &nbsp;|&nbsp; ⚕️ Chỉ mang tính tham khảo — không thay thế tư vấn y tế chuyên nghiệp
    </div>
</div>
""", unsafe_allow_html=True)
