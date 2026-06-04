"""
PaddleOCR 2.7.x wrapper.
is_available() chỉ kiểm tra import, không init engine sớm.
Engine init lazy khi extract_text() được gọi lần đầu.
"""
import io
import numpy as np
from PIL import Image

_ocr_engine = None
_engine_tried = False
_engine_error: str = ""
_ocr_version: str = ""


def _pkg_available() -> bool:
    """Kiểm tra nhanh xem paddleocr có import được không."""
    try:
        import paddleocr
        global _ocr_version
        _ocr_version = getattr(paddleocr, "__version__", "2.x")
        return True
    except Exception as e:
        global _engine_error
        _engine_error = str(e)
        return False


def _get_engine():
    global _ocr_engine, _engine_tried, _engine_error
    if _engine_tried:
        return _ocr_engine
    _engine_tried = True
    try:
        from paddleocr import PaddleOCR
        _ocr_engine = PaddleOCR(use_angle_cls=True, lang="vi", show_log=False)
    except Exception as e:
        _engine_error = str(e)
        _ocr_engine = None
    return _ocr_engine


def is_available() -> bool:
    """True nếu paddleocr package cài được — không cần init engine."""
    return _pkg_available()


def get_version() -> str:
    _pkg_available()
    return _ocr_version


def get_error() -> str:
    return _engine_error


def extract_text(image_file) -> tuple[str, float]:
    if not _pkg_available():
        return "", 0.0

    engine = _get_engine()
    if engine is None:
        return f"__error__:{_engine_error}", 0.0

    try:
        if isinstance(image_file, Image.Image):
            img = image_file
        else:
            img = Image.open(io.BytesIO(image_file.read()))
            try:
                image_file.seek(0)
            except Exception:
                pass

        if img.mode != "RGB":
            img = img.convert("RGB")

        result = engine.ocr(np.array(img), cls=True)

        lines, confs = [], []
        if result and result[0]:
            for line in result[0]:
                if line and len(line) >= 2:
                    text, conf = line[1][0], line[1][1]
                    if conf > 0.4 and text.strip():
                        lines.append(text.strip())
                        confs.append(conf)

        avg_conf = round(sum(confs) / len(confs), 3) if confs else 0.0
        return "\n".join(lines), avg_conf

    except Exception as e:
        return f"Lỗi OCR: {e}", 0.0
