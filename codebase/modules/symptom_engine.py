"""Rule-based symptom assessment engine."""

RULES: list[dict] = [
    {
        "id": "emergency_cardiac",
        "category": "Tim mạch khẩn cấp",
        "triggers": ["đau ngực dữ dội", "đau ngực lan cánh tay", "đau ngực lan hàm", "ngừng tim", "khó thở đột ngột nghiêm trọng"],
        "risk_level": "khẩn cấp",
        "action": "Gọi cấp cứu 115 NGAY - Nghi ngờ nhồi máu cơ tim",
        "seek_emergency": True,
    },
    {
        "id": "emergency_stroke",
        "category": "Đột quỵ",
        "triggers": ["liệt một bên mặt", "liệt tay chân một bên", "nói ngọng đột ngột", "méo miệng đột ngột", "mất thị lực đột ngột"],
        "risk_level": "khẩn cấp",
        "action": "Gọi cấp cứu 115 NGAY - Nghi ngờ đột quỵ (FAST: mặt - tay - nói - thời gian)",
        "seek_emergency": True,
    },
    {
        "id": "emergency_breathing",
        "category": "Suy hô hấp",
        "triggers": ["khó thở nghiêm trọng", "không thở được", "môi tím tái", "ngạt thở"],
        "risk_level": "khẩn cấp",
        "action": "Gọi cấp cứu 115 - Suy hô hấp cấp",
        "seek_emergency": True,
    },
    {
        "id": "emergency_consciousness",
        "category": "Rối loạn ý thức",
        "triggers": ["mất ý thức", "co giật", "hôn mê", "không phản ứng"],
        "risk_level": "khẩn cấp",
        "action": "Gọi cấp cứu 115 - Rối loạn ý thức cần xử trí khẩn cấp",
        "seek_emergency": True,
    },
    {
        "id": "emergency_bleeding",
        "category": "Xuất huyết nghiêm trọng",
        "triggers": ["nôn máu", "xuất huyết ồ ạt", "đại tiện ra máu nhiều", "ho ra máu nhiều"],
        "risk_level": "khẩn cấp",
        "action": "Đến cấp cứu ngay - Xuất huyết nghiêm trọng",
        "seek_emergency": True,
    },
    {
        "id": "high_fever",
        "category": "Sốt cao",
        "triggers": ["sốt cao trên 39", "sốt trên 40 độ", "sốt cao không hạ"],
        "risk_level": "cao",
        "action": "Đến cơ sở y tế trong vòng vài giờ",
        "seek_emergency": False,
    },
    {
        "id": "chest_pain_mild",
        "category": "Đau ngực",
        "triggers": ["đau ngực", "tức ngực", "nặng ngực"],
        "risk_level": "cao",
        "action": "Cần đánh giá y tế ngay trong ngày - Loại trừ bệnh tim mạch",
        "seek_emergency": False,
    },
    {
        "id": "severe_headache",
        "category": "Đau đầu nghiêm trọng",
        "triggers": ["đau đầu dữ dội đột ngột", "đau đầu như sét đánh", "đau đầu kèm cứng gáy"],
        "risk_level": "cao",
        "action": "Đến bệnh viện ngay - Loại trừ xuất huyết não, viêm màng não",
        "seek_emergency": False,
    },
    {
        "id": "abdominal_severe",
        "category": "Đau bụng nghiêm trọng",
        "triggers": ["đau bụng dữ dội", "đau bụng không dứt", "bụng cứng như gỗ"],
        "risk_level": "cao",
        "action": "Đến cơ sở y tế ngay - Có thể là cấp cứu ngoại khoa",
        "seek_emergency": False,
    },
    {
        "id": "respiratory_moderate",
        "category": "Vấn đề hô hấp",
        "triggers": ["khó thở", "thở khò khè", "đau khi thở"],
        "risk_level": "trung bình",
        "action": "Đến gặp bác sĩ trong ngày, đặc biệt nếu có tiền sử hen hoặc tim mạch",
        "seek_emergency": False,
    },
    {
        "id": "gi_bleeding_mild",
        "category": "Xuất huyết tiêu hóa nhẹ",
        "triggers": ["phân đen", "phân có máu", "tiểu ra máu", "ho ra máu"],
        "risk_level": "cao",
        "action": "Đến bệnh viện trong ngày để xét nghiệm",
        "seek_emergency": False,
    },
    {
        "id": "fever_moderate",
        "category": "Sốt",
        "triggers": ["sốt", "nóng người", "ớn lạnh", "rét run"],
        "risk_level": "trung bình",
        "action": "Theo dõi nhiệt độ, hạ sốt và bù nước. Gặp bác sĩ nếu sốt > 38.5°C hoặc kéo dài > 3 ngày",
        "seek_emergency": False,
    },
    {
        "id": "gi_moderate",
        "category": "Tiêu hóa",
        "triggers": ["tiêu chảy", "nôn mửa", "đau bụng", "buồn nôn", "đầy hơi"],
        "risk_level": "trung bình",
        "action": "Bù nước, nghỉ ngơi. Đến bác sĩ nếu kéo dài hơn 48 giờ hoặc có máu",
        "seek_emergency": False,
    },
    {
        "id": "neurological_moderate",
        "category": "Thần kinh",
        "triggers": ["chóng mặt", "hoa mắt", "tê bì tay chân", "mất thăng bằng"],
        "risk_level": "trung bình",
        "action": "Theo dõi, hạn chế lái xe. Gặp bác sĩ nếu kéo dài hoặc tái phát",
        "seek_emergency": False,
    },
    {
        "id": "musculoskeletal",
        "category": "Cơ xương khớp",
        "triggers": ["đau khớp", "sưng khớp", "cứng khớp buổi sáng", "đau cơ"],
        "risk_level": "thấp",
        "action": "Nghỉ ngơi, chườm lạnh/nóng. Gặp bác sĩ nếu kéo dài hơn 2 tuần",
        "seek_emergency": False,
    },
    {
        "id": "urt_infection",
        "category": "Nhiễm trùng hô hấp trên",
        "triggers": ["ho", "sổ mũi", "đau họng", "nghẹt mũi", "hắt hơi"],
        "risk_level": "thấp",
        "action": "Nghỉ ngơi đủ giấc, uống nhiều nước. Gặp bác sĩ nếu sốt cao hoặc kéo dài > 7 ngày",
        "seek_emergency": False,
    },
    {
        "id": "fatigue",
        "category": "Mệt mỏi",
        "triggers": ["mệt mỏi", "kiệt sức", "không có năng lượng", "ngủ nhiều vẫn mệt"],
        "risk_level": "thấp",
        "action": "Nghỉ ngơi, cải thiện chế độ ngủ và ăn uống. Xét nghiệm nếu mệt mỏi kéo dài > 2 tuần",
        "seek_emergency": False,
    },
]

RISK_HIERARCHY = ["thấp", "trung bình", "cao", "khẩn cấp"]


def _normalize(text: str) -> str:
    """Simple accent-stripping for better fuzzy matching."""
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def assess(symptom_text: str) -> dict:
    """
    Rule-based assessment of symptoms.
    Returns matched rules, overall risk, all matched triggers.
    """
    text_lower = symptom_text.lower()
    text_normalized = _normalize(symptom_text)
    matched_rules = []
    highest_idx = 0

    for rule in RULES:
        triggered_by = [
            t for t in rule["triggers"]
            if t in text_lower or _normalize(t) in text_normalized
        ]
        if triggered_by:
            matched_rules.append({
                "id": rule["id"],
                "category": rule["category"],
                "triggered_by": triggered_by,
                "risk_level": rule["risk_level"],
                "action": rule["action"],
                "seek_emergency": rule["seek_emergency"],
            })
            idx = RISK_HIERARCHY.index(rule["risk_level"]) if rule["risk_level"] in RISK_HIERARCHY else 0
            highest_idx = max(highest_idx, idx)

    overall_risk = RISK_HIERARCHY[highest_idx] if matched_rules else "thấp"
    seek_emergency = any(r["seek_emergency"] for r in matched_rules)
    all_triggers = list({t for r in matched_rules for t in r["triggered_by"]})

    return {
        "matched_rules": matched_rules,
        "overall_risk": overall_risk,
        "seek_emergency": seek_emergency,
        "all_matched_symptoms": all_triggers,
    }


FOLLOWUP_MAP = {
    "đau": ["Cơn đau xuất hiện từ khi nào?", "Mức độ đau 1-10?", "Đau liên tục hay từng cơn?", "Đau lan không? Lan đi đâu?"],
    "sốt": ["Nhiệt độ hiện tại là bao nhiêu?", "Sốt bao lâu rồi?", "Kèm ớn lạnh, ra mồ hôi không?"],
    "ho": ["Ho có đờm không? Màu đờm gì?", "Ho kéo dài bao lâu?", "Ho nặng hơn vào thời điểm nào?"],
    "tiêu chảy": ["Đi bao nhiêu lần/ngày?", "Có máu trong phân không?", "Có dấu hiệu mất nước (môi khô, tiểu ít)?"],
    "nôn": ["Nôn bao nhiêu lần?", "Chất nôn màu gì?", "Đau bụng kèm theo không?"],
    "chóng mặt": ["Chóng mặt khi nằm xuống hay đứng lên?", "Có ù tai không?", "Từng bị té ngã chưa?"],
    "khó thở": ["Khó thở khi nào (lúc nghỉ hay gắng sức)?", "Có tiếng ran khi thở không?", "Tiền sử hen suyễn?"],
    "đau đầu": ["Đau vùng nào của đầu?", "Kèm buồn nôn, sợ ánh sáng không?", "Đã uống thuốc gì chưa?"],
}

GENERIC_FOLLOWUP = [
    "Triệu chứng xuất hiện từ khi nào?",
    "Có tiền sử bệnh mãn tính không (tiểu đường, huyết áp, tim mạch...)?",
    "Hiện đang dùng thuốc gì không?",
    "Có dị ứng thuốc hoặc thực phẩm không?",
]


def get_followup_questions(symptom_text: str) -> list[str]:
    text_lower = symptom_text.lower()
    questions = []
    for keyword, qs in FOLLOWUP_MAP.items():
        if keyword in text_lower:
            questions.extend(qs[:2])
    if not questions:
        questions = GENERIC_FOLLOWUP
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for q in questions:
        if q not in seen:
            seen.add(q)
            unique.append(q)
    return unique[:5]
