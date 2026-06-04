import requests
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RXNORM_BASE_URL, REQUEST_TIMEOUT


def search_drug(name: str) -> list[dict]:
    """Search RxNorm for a drug name, return top candidates."""
    try:
        r = requests.get(
            f"{RXNORM_BASE_URL}/drugs.json",
            params={"name": name},
            timeout=REQUEST_TIMEOUT,
        )
        if r.status_code != 200:
            return []
        data = r.json()
        results = []
        for group in data.get("drugGroup", {}).get("conceptGroup", []):
            for prop in group.get("conceptProperties", []):
                results.append({
                    "rxcui": prop.get("rxcui"),
                    "name": prop.get("name"),
                    "synonym": prop.get("synonym", ""),
                    "tty": prop.get("tty"),
                })
        return results[:5]
    except Exception:
        return []


def get_properties(rxcui: str) -> dict:
    try:
        r = requests.get(
            f"{RXNORM_BASE_URL}/rxcui/{rxcui}/properties.json",
            timeout=REQUEST_TIMEOUT,
        )
        if r.status_code == 200:
            return r.json().get("properties", {})
        return {}
    except Exception:
        return {}


def get_related(rxcui: str, relation: str = "ingredients") -> list:
    """Get related concepts (e.g. ingredients, clinical drugs)."""
    try:
        r = requests.get(
            f"{RXNORM_BASE_URL}/rxcui/{rxcui}/related.json",
            params={"tty": "IN+PIN+BN"},
            timeout=REQUEST_TIMEOUT,
        )
        if r.status_code == 200:
            groups = r.json().get("relatedGroup", {}).get("conceptGroup", [])
            out = []
            for g in groups:
                for p in g.get("conceptProperties", []):
                    out.append(p.get("name", ""))
            return out
        return []
    except Exception:
        return []


def normalize(drug_name: str) -> dict:
    """Best-effort normalization: return first RxNorm hit or fallback."""
    hits = search_drug(drug_name)
    return hits[0] if hits else {"name": drug_name, "rxcui": None}
