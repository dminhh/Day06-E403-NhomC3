import json
import os

_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "drug_interactions.json")

_db_cache: dict | None = None


def _load_db() -> dict:
    global _db_cache
    if _db_cache is None:
        try:
            with open(_DB_PATH, "r", encoding="utf-8") as f:
                _db_cache = json.load(f)
        except Exception:
            _db_cache = {"interactions": []}
    return _db_cache


def check_interactions(drug_list: list[str]) -> list[dict]:
    """
    Check a list of drug names against the interaction database.
    Returns list of detected interactions.
    """
    db = _load_db()
    drug_names_lower = [d.lower().strip() for d in drug_list if d]
    found = []
    seen_pairs = set()

    for entry in db.get("interactions", []):
        aliases_a = [x.lower() for x in entry.get("aliases_a", [])] + [entry["drug_a"].lower()]
        aliases_b = [x.lower() for x in entry.get("aliases_b", [])] + [entry["drug_b"].lower()]

        a_match = any(
            any(alias in drug or drug in alias for alias in aliases_a)
            for drug in drug_names_lower
        )
        b_match = any(
            any(alias in drug or drug in alias for alias in aliases_b)
            for drug in drug_names_lower
        )

        if a_match and b_match:
            pair_key = f"{entry['drug_a']}|{entry['drug_b']}"
            if pair_key not in seen_pairs:
                seen_pairs.add(pair_key)
                found.append({
                    "drug_a": entry["drug_a"],
                    "drug_b": entry["drug_b"],
                    "severity": entry["severity"],
                    "description": entry["description_vi"],
                    "recommendation": entry["recommendation_vi"],
                    "mechanism": entry.get("mechanism_vi", ""),
                })

    return found


SEVERITY_ORDER = ["nhẹ", "trung bình", "nặng", "chống chỉ định"]
SEVERITY_COLORS = {
    "nhẹ": "#28a745",
    "trung bình": "#ffc107",
    "nặng": "#fd7e14",
    "chống chỉ định": "#dc3545",
}
SEVERITY_EMOJI = {
    "nhẹ": "🟡",
    "trung bình": "🟠",
    "nặng": "🔴",
    "chống chỉ định": "🚫",
}


def overall_severity(interactions: list[dict]) -> str:
    if not interactions:
        return "an toàn"
    highest = 0
    for i in interactions:
        sev = i.get("severity", "nhẹ")
        idx = SEVERITY_ORDER.index(sev) if sev in SEVERITY_ORDER else 0
        highest = max(highest, idx)
    return SEVERITY_ORDER[highest]
