import requests
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENFDA_BASE_URL, REQUEST_TIMEOUT


def _get(endpoint: str, params: dict) -> dict | None:
    try:
        r = requests.get(f"{OPENFDA_BASE_URL}/{endpoint}", params=params, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None


def get_label(drug_name: str) -> dict | None:
    """Fetch drug label information."""
    data = _get(
        "label.json",
        {"search": f'(openfda.brand_name:"{drug_name}"+openfda.generic_name:"{drug_name}")', "limit": 1},
    )
    if not data or not data.get("results"):
        # Fallback: broader search
        data = _get("label.json", {"search": drug_name, "limit": 1})

    if data and data.get("results"):
        r = data["results"][0]
        openfda = r.get("openfda", {})
        return {
            "brand_names": openfda.get("brand_name", []),
            "generic_names": openfda.get("generic_name", []),
            "manufacturer": openfda.get("manufacturer_name", []),
            "route": openfda.get("route", []),
            "warnings": r.get("warnings", r.get("warnings_and_cautions", ["Không có thông tin"])),
            "indications": r.get("indications_and_usage", ["Không có thông tin"]),
            "contraindications": r.get("contraindications", ["Không có thông tin"]),
            "adverse_reactions": r.get("adverse_reactions", ["Không có thông tin"]),
            "dosage": r.get("dosage_and_administration", ["Không có thông tin"]),
            "drug_interactions": r.get("drug_interactions", ["Không có thông tin"]),
            "pregnancy": r.get("pregnancy", ["Không có thông tin"]),
        }
    return None


def get_adverse_events(drug_name: str, limit: int = 5) -> list[str]:
    """Top adverse event reactions reported for a drug."""
    data = _get(
        "event.json",
        {
            "search": f'patient.drug.medicinalproduct:"{drug_name}"',
            "count": "patient.reaction.reactionmeddrapt.exact",
            "limit": limit,
        },
    )
    if data and data.get("results"):
        return [item["term"] for item in data["results"]]
    return []


def get_recalls(drug_name: str, limit: int = 3) -> list[dict]:
    """Check for recent recalls of a drug."""
    data = _get(
        "enforcement.json",
        {"search": f'product_description:"{drug_name}"', "limit": limit},
    )
    if data and data.get("results"):
        return [
            {
                "reason": r.get("reason_for_recall", ""),
                "date": r.get("recall_initiation_date", ""),
                "status": r.get("status", ""),
            }
            for r in data["results"]
        ]
    return []
