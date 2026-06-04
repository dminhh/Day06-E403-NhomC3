import json
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

try:
    from openai import OpenAI
    _client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
except Exception:
    _client = None


def _chat(messages: list, temperature: float = 0.3, max_tokens: int = 16000) -> str:
    if _client is None:
        return '{"error": "Không kết nối được LLM"}'
    try:
        resp = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        choice = resp.choices[0]
        content = choice.message.content
        if content is None:
            content = getattr(choice.message, "reasoning", None) or ""
        return content.strip() if content else '{"error": "Phản hồi rỗng từ LLM"}'
    except Exception as e:
        return f'{{"error": "{str(e)}"}}'


def _safe_json(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
        return {"raw": text}


def validate_prescription_image(ocr_text: str) -> dict:
    """Kiểm tra xem ảnh có phải đơn thuốc/hóa đơn thuốc không."""
    prompt = f"""Bạn là chuyên gia y tế. Đọc văn bản OCR sau và xác định xem đây có phải đơn thuốc hoặc hóa đơn thuốc không.

Văn bản OCR:
{ocr_text[:1000]}

Trả về JSON (không thêm text ngoài JSON):
{{
  "is_prescription": true/false,
  "is_pharmacy_invoice": true/false,
  "confidence": "cao/trung bình/thấp",
  "reason": "lý do ngắn gọn",
  "image_quality": "rõ/mờ/thiếu thông tin"
}}"""
    result = _chat([{"role": "user", "content": prompt}], temperature=0.1, max_tokens=500)
    return _safe_json(result)


def extract_drug_from_image_text(ocr_text: str) -> dict:
    """Nhận diện tên thuốc từ văn bản OCR ảnh thuốc."""
    prompt = f"""Bạn là dược sĩ AI. Đọc văn bản OCR từ ảnh hộp/gói thuốc và trích xuất thông tin.

Văn bản OCR:
{ocr_text}

Trả về JSON (không thêm text ngoài JSON):
{{
  "drug_name": "tên thuốc chính",
  "brand_name": "tên thương mại",
  "active_ingredient": "hoạt chất",
  "strength": "hàm lượng",
  "manufacturer": "nhà sản xuất",
  "is_drug": true/false
}}"""
    result = _chat([{"role": "user", "content": prompt}], temperature=0.1, max_tokens=500)
    return _safe_json(result)


def extract_prescription(ocr_text: str) -> dict:
    prompt = f"""Bạn là chuyên gia phân tích đơn thuốc y tế Việt Nam.
Hãy phân tích văn bản OCR từ đơn thuốc sau và trích xuất thông tin dưới dạng JSON.

Văn bản OCR:
{ocr_text}

Trả về JSON hợp lệ (không thêm text ngoài JSON):
{{
  "patient_name": "tên bệnh nhân hoặc rỗng nếu không có",
  "age": "tuổi hoặc rỗng",
  "gender": "giới tính hoặc rỗng",
  "diagnosis": "chẩn đoán hoặc rỗng",
  "date": "ngày kê đơn hoặc rỗng",
  "doctor_name": "tên bác sĩ hoặc rỗng",
  "hospital": "bệnh viện hoặc rỗng",
  "missing_info": ["danh sách thông tin bị thiếu"],
  "medications": [
    {{
      "name": "tên thuốc",
      "dosage": "liều lượng hoặc rỗng",
      "frequency": "tần suất hoặc rỗng",
      "duration": "thời gian dùng hoặc rỗng",
      "instructions": "hướng dẫn đặc biệt hoặc rỗng",
      "quantity": "số lượng hoặc rỗng",
      "found_in_database": true
    }}
  ]
}}"""
    result = _chat([{"role": "user", "content": prompt}], temperature=0.1)
    return _safe_json(result)


def parse_symptoms(symptom_text: str, context: str = "") -> dict:
    extra = f"\nThông tin bổ sung: {context}" if context else ""
    prompt = f"""Bạn là bác sĩ AI Việt Nam chuyên đánh giá triệu chứng.
Phân tích triệu chứng sau và trả về JSON (không thêm text ngoài JSON):

Triệu chứng: {symptom_text}{extra}

{{
  "symptoms_identified": ["danh sách triệu chứng"],
  "severity": "nhẹ | trung bình | nặng | nguy hiểm",
  "affected_systems": ["hệ cơ quan bị ảnh hưởng"],
  "need_followup": true,
  "followup_questions": ["câu hỏi cần hỏi thêm"],
  "preliminary_assessment": "đánh giá sơ bộ bằng tiếng Việt"
}}"""
    result = _chat([{"role": "user", "content": prompt}], temperature=0.2)
    return _safe_json(result)


def analyze_risk(symptoms_data: str, rules_matched: list) -> dict:
    rules_text = json.dumps(rules_matched, ensure_ascii=False, indent=2) if rules_matched else "Không có"
    prompt = f"""Bạn là bác sĩ AI đánh giá rủi ro sức khỏe.

Triệu chứng: {symptoms_data}
Quy tắc y tế: {rules_text}

Trả về JSON (không thêm text ngoài JSON):
{{
  "risk_level": "thấp | trung bình | cao | khẩn cấp",
  "risk_score": 0,
  "possible_conditions": ["các bệnh có thể"],
  "red_flags": ["dấu hiệu nguy hiểm"],
  "recommendations": ["khuyến nghị"],
  "seek_emergency": false,
  "lifestyle_advice": ["lời khuyên"],
  "explanation": "giải thích chi tiết bằng tiếng Việt"
}}"""
    result = _chat([{"role": "user", "content": prompt}], temperature=0.2)
    return _safe_json(result)


def explain_prescription(drug_info: str, dangerous_interactions: list, patient_info: dict) -> str:
    """Tạo giải thích đơn thuốc — chỉ cảnh báo tương tác NGUY HIỂM, không có risk score."""
    ix_text = ""
    if dangerous_interactions:
        ix_text = "\n\n⚠️ TƯƠNG TÁC NGUY HIỂM CẦN CHÚ Ý:\n" + "\n".join(
            f"- {i['drug_a']} + {i['drug_b']}: {i['description']}" for i in dangerous_interactions
        )

    prompt = f"""Bạn là dược sĩ AI giải thích đơn thuốc cho bệnh nhân Việt Nam.

Thông tin thuốc: {drug_info}{ix_text}
Thông tin bệnh nhân: {json.dumps(patient_info, ensure_ascii=False)}

Viết giải thích HOÀN TOÀN BẰNG TIẾNG VIỆT, dùng định dạng markdown đơn giản (chỉ dùng ### tiêu đề, - danh sách, **in đậm**). KHÔNG dùng bảng markdown (|---|).

Cấu trúc:

### 💊 Tóm tắt các thuốc
(Mỗi thuốc: tên, công dụng chính, lưu ý quan trọng — dùng danh sách gạch đầu dòng)

### 📋 Hướng dẫn sử dụng
(Thời điểm uống, uống với gì, cách uống)

### ⚠️ Cảnh báo quan trọng
(Chỉ liệt kê nếu có tương tác nguy hiểm hoặc chống chỉ định thực sự)

### 🔴 Dấu hiệu cần gặp bác sĩ ngay
(Liệt kê cụ thể)

### 📝 Lưu ý thêm
(Thức ăn/đồ uống cần tránh, bảo quản thuốc)

Viết ngắn gọn, rõ ràng, thân thiện."""
    return _chat([{"role": "user", "content": prompt}], temperature=0.4)


def translate_fda_section(text: str, section_name: str) -> str:
    """Dịch một section từ OpenFDA (tiếng Anh) sang tiếng Việt ngắn gọn."""
    if not text or len(text.strip()) < 10:
        return "Không có thông tin."
    # Cắt bớt trước khi dịch để tiết kiệm token
    text_cut = text[:1200].rsplit(".", 1)[0] + "." if len(text) > 1200 else text
    prompt = f"""Dịch đoạn thông tin thuốc sau từ tiếng Anh sang tiếng Việt, ngắn gọn và dễ hiểu.
Chỉ dịch nội dung chính, bỏ các mã tham chiếu, số footnote (*1, *2...).
Phần: {section_name}

{text_cut}

Trả về bản dịch tiếng Việt, không thêm giải thích."""
    return _chat([{"role": "user", "content": prompt}], temperature=0.2, max_tokens=2000)


def translate_adverse_events(events: list[str]) -> list[str]:
    """Dịch danh sách tác dụng phụ y tế sang tiếng Việt."""
    if not events:
        return []

    # Bảng dịch nhanh cho các thuật ngữ phổ biến (không cần gọi LLM)
    _quick = {
        "HEADACHE": "Đau đầu", "NAUSEA": "Buồn nôn", "VOMITING": "Nôn mửa",
        "DIZZINESS": "Chóng mặt", "FATIGUE": "Mệt mỏi", "DIARRHOEA": "Tiêu chảy",
        "RASH": "Phát ban", "PYREXIA": "Sốt", "PAIN": "Đau",
        "INSOMNIA": "Mất ngủ", "COUGH": "Ho", "DYSPNOEA": "Khó thở",
        "PRURITUS": "Ngứa", "CONSTIPATION": "Táo bón", "ANXIETY": "Lo âu",
        "DRUG ABUSE": "Sử dụng thuốc sai mục đích",
        "DRUG INTERACTION": "Tương tác thuốc",
        "DRUG INEFFECTIVE": "Thuốc kém hiệu quả",
        "LOSS OF CONSCIOUSNESS": "Mất ý thức",
        "PRODUCT QUALITY ISSUE": "Vấn đề chất lượng",
        "ORAL DISCOMFORT": "Khó chịu miệng",
        "ORAL MUCOSAL EXFOLIATION": "Bong niêm mạc miệng",
        "GLOSSODYNIA": "Đau lưỡi",
        "APPLICATION SITE BURN": "Bỏng tại chỗ bôi",
        "INCORRECT ROUTE OF DRUG ADMINISTRATION": "Sai đường dùng thuốc",
        "INTENTIONAL DRUG MISUSE": "Cố tình dùng thuốc sai",
        "OFF LABEL USE": "Dùng ngoài chỉ định",
        "PARADOXICAL DRUG REACTION": "Phản ứng nghịch lý",
        "DRUG REACTION WITH EOSINOPHILIA AND SYSTEMIC SYMPTOMS": "Phản ứng thuốc toàn thân",
        "DRUG-INDUCED LIVER INJURY": "Tổn thương gan do thuốc",
    }

    results = []
    missing_idx = []  # index cần gọi LLM
    missing_terms = []

    for i, e in enumerate(events):
        key = e.strip().upper()
        if key in _quick:
            results.append(_quick[key])
        else:
            results.append(None)
            missing_idx.append(i)
            missing_terms.append(e)

    # Gọi LLM chỉ cho các term chưa có trong bảng
    if missing_terms:
        items = "\n".join(missing_terms)
        prompt = (
            f"Dịch {len(missing_terms)} thuật ngữ y tế sau sang tiếng Việt.\n"
            f"Chỉ trả về bản dịch, mỗi dòng một mục, không giải thích:\n{items}"
        )
        raw = _chat([{"role": "user", "content": prompt}], temperature=0.0, max_tokens=400)

        # Trích xuất: ưu tiên phần sau "->" hoặc sau quotes, bỏ prefix tiếng Anh
        translated = []
        for line in raw.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            # Lấy phần sau dấu -> nếu có
            if "->" in line:
                line = line.split("->")[-1].strip()
            # Bỏ dấu nháy đơn/kép
            line = line.strip("\"'""''")
            # Bỏ prefix số/gạch
            line = line.lstrip("-•1234567890. ").strip()
            # Chỉ giữ nếu có chữ và không quá dài
            if line and len(line) < 60 and any(c.isalpha() for c in line):
                translated.append(line)

        for i, idx in enumerate(missing_idx):
            results[idx] = translated[i] if i < len(translated) else missing_terms[i]

    return [r or events[i] for i, r in enumerate(results)]


def translate_recall(reason: str) -> str:
    """Dịch lý do thu hồi thuốc sang tiếng Việt."""
    if not reason or not reason.strip():
        return "Không rõ lý do."
    prompt = f"Dịch sang tiếng Việt, ngắn gọn 1-2 câu, chỉ trả về bản dịch: {reason[:500]}"
    return _chat([{"role": "user", "content": prompt}], temperature=0.1, max_tokens=500)


def format_ocr_text(raw_ocr: str) -> str:
    """Làm sạch và định dạng văn bản OCR thành dạng dễ đọc."""
    prompt = f"""Đây là văn bản OCR thô từ ảnh hóa đơn/đơn thuốc, có thể bị lỗi font, thiếu dấu.
Hãy làm sạch và định dạng lại thành văn bản tiếng Việt dễ đọc.
Giữ nguyên thông tin, chỉ sửa lỗi OCR rõ ràng (ví dụ: "dn" → "đơn", "thuoc" → "thuốc").
Trình bày dạng danh sách ngắn gọn nếu là hóa đơn.

Văn bản OCR:
{raw_ocr[:1500]}

Trả về văn bản đã làm sạch, không giải thích thêm."""
    return _chat([{"role": "user", "content": prompt}], temperature=0.1, max_tokens=2000)


def explain_symptoms_result(risk_data: dict, symptom_assessment: dict) -> str:
    prompt = f"""Bạn là bác sĩ AI giải thích kết quả đánh giá sức khỏe cho bệnh nhân Việt Nam.

Đánh giá: {json.dumps(risk_data, ensure_ascii=False)}
Triệu chứng: {json.dumps(symptom_assessment, ensure_ascii=False)}

Viết giải thích bằng tiếng Việt dùng markdown đơn giản (### tiêu đề, - danh sách, **in đậm**). KHÔNG dùng bảng.

### 🩺 Tình trạng hiện tại
### 🔍 Nguyên nhân có thể
### ✅ Hành động cần làm ngay
### 🏠 Chăm sóc tại nhà
### 🚨 Khi nào phải đến bệnh viện

Viết ấm áp, không gây hoảng sợ nhưng đầy đủ thông tin."""
    return _chat([{"role": "user", "content": prompt}], temperature=0.4)
