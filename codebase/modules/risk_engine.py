"""Risk scoring and display helpers."""

RISK_CONFIG = {
    "thấp":          {"score": 15,  "color": "#28a745", "bg": "#d4edda", "icon": "✅", "label": "THẤP"},
    "trung bình":    {"score": 45,  "color": "#ffc107", "bg": "#fff3cd", "icon": "⚠️", "label": "TRUNG BÌNH"},
    "cao":           {"score": 75,  "color": "#fd7e14", "bg": "#fde5cc", "icon": "🔴", "label": "CAO"},
    "khẩn cấp":      {"score": 100, "color": "#dc3545", "bg": "#f8d7da", "icon": "🚨", "label": "KHẨN CẤP"},
    "an toàn":       {"score": 5,   "color": "#198754", "bg": "#d1e7dd", "icon": "✅", "label": "AN TOÀN"},
}

INTERACTION_SEVERITY_CONFIG = {
    "nhẹ":            {"color": "#28a745", "icon": "🟡", "score": 10},
    "trung bình":     {"color": "#ffc107", "icon": "🟠", "score": 30},
    "nặng":           {"color": "#fd7e14", "icon": "🔴", "score": 60},
    "chống chỉ định": {"color": "#dc3545", "icon": "🚫", "score": 100},
}


def get_risk_config(risk_level: str) -> dict:
    return RISK_CONFIG.get(risk_level, RISK_CONFIG["thấp"])


def evaluate_prescription_risk(medications: list[str], interactions: list[dict]) -> dict:
    risk_factors = []

    # Polypharmacy risk
    med_count = len(medications)
    if med_count >= 10:
        risk_factors.append({"factor": "Đa thuốc nghiêm trọng", "detail": f"{med_count} loại thuốc cùng lúc", "severity": "nặng"})
    elif med_count >= 6:
        risk_factors.append({"factor": "Đa thuốc", "detail": f"{med_count} loại thuốc - nguy cơ tương tác tăng", "severity": "trung bình"})

    # Interaction risk
    for interaction in interactions:
        sev = interaction.get("severity", "nhẹ")
        risk_factors.append({
            "factor": f"Tương tác: {interaction['drug_a']} ↔ {interaction['drug_b']}",
            "detail": interaction["description"],
            "severity": sev,
        })

    # Determine overall risk
    if any(r["severity"] == "chống chỉ định" for r in risk_factors):
        overall = "khẩn cấp"
    elif any(r["severity"] == "nặng" for r in risk_factors):
        overall = "cao"
    elif any(r["severity"] == "trung bình" for r in risk_factors):
        overall = "trung bình"
    elif risk_factors:
        overall = "thấp"
    else:
        overall = "an toàn"

    cfg = get_risk_config(overall)
    return {
        "overall_risk": overall,
        "risk_score": cfg["score"],
        "risk_factors": risk_factors,
        **cfg,
    }


def risk_score_bar(score: int) -> str:
    """Return a simple text-based progress representation."""
    filled = int(score / 10)
    empty = 10 - filled
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {score}/100"
