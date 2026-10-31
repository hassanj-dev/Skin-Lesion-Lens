"""Pure-Python helpers (no TensorFlow) for the Skin Lesion Classifier app."""
import base64
import html
import io
from datetime import datetime

import numpy as np
from PIL import Image, ImageOps

# Optional: HEIC/HEIF photos from iPhones (pip install pillow-heif)
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except Exception:  # noqa: BLE001
    pass

# Image formats listed in the UI hint (any format Pillow can read is accepted)
SUPPORTED_HINT = "JPG, JPEG, PNG, WEBP, BMP, TIFF, GIF, JFIF, ICO, (HEIC if pillow-heif is installed)"

CLASS_INFO = {
    "actinic keratosis": ("Pre-cancerous",
        "A rough, scaly patch caused by long-term sun damage. It can develop into squamous cell carcinoma if untreated."),
    "basal cell carcinoma": ("Malignant",
        "The most common skin cancer. It grows slowly and rarely spreads, but needs treatment."),
    "dermatofibroma": ("Benign",
        "A firm, harmless skin nodule, often on the legs. Usually needs no treatment."),
    "melanoma": ("Malignant",
        "The most dangerous skin cancer. Early detection greatly improves outcomes, so any suspicious or changing mole should be checked promptly."),
    "nevus": ("Benign",
        "A common mole. Most are harmless, but changes in size, shape or colour should be checked."),
    "pigmented benign keratosis": ("Benign",
        "A harmless pigmented growth, often called a sun spot or age spot."),
    "seborrheic keratosis": ("Benign",
        "A common, harmless 'stuck-on' wart-like growth that appears with age."),
    "squamous cell carcinoma": ("Malignant",
        "The second most common skin cancer. It can spread if not treated, so it needs medical evaluation."),
    "vascular lesion": ("Benign",
        "A lesion made of blood vessels, such as a cherry angioma. Usually harmless."),
}
ALERT_RISKS = {"Malignant", "Pre-cancerous"}

STRINGS = {
    "en": {
        "title": "Skin Lesion Classifier",
        "disclaimer": "Research prototype for education only. It is **not** a medical device and cannot diagnose cancer. See a dermatologist for any concerning skin change.",
        "upload": "Upload one or more lesion photos (any image format)",
        "camera": "Or take a photo with your camera",
        "most_likely": "Most likely",
        "alert": "This result is potentially cancerous or pre-cancerous. Please have the lesion examined by a dermatologist.",
        "low_conf": "Low confidence: the model is unsure. Treat this result with extra caution.",
        "no_input": "Upload an image or use the camera to get started.",
    },
    "ur": {
        "title": "جلدی زخم کی درجہ بندی",
        "disclaimer": "یہ صرف تعلیمی مقصد کے لیے ایک تحقیقی نمونہ ہے۔ یہ طبی آلہ **نہیں** ہے اور کینسر کی تشخیص نہیں کر سکتا۔ جلد میں کسی بھی تشویشناک تبدیلی پر ماہرِ جلد سے رجوع کریں۔",
        "upload": "ایک یا زیادہ تصاویر اپلوڈ کریں (کسی بھی فارمیٹ میں)",
        "camera": "یا کیمرے سے تصویر لیں",
        "most_likely": "سب سے ممکنہ نتیجہ",
        "alert": "یہ نتیجہ ممکنہ طور پر کینسر یا کینسر سے پہلے کی حالت ظاہر کرتا ہے۔ براہِ کرم فوراً ماہرِ جلد سے معائنہ کروائیں۔",
        "low_conf": "کم اعتماد: ماڈل کو یقین نہیں ہے۔ اس نتیجے پر احتیاط سے بھروسہ کریں۔",
        "no_input": "شروع کرنے کے لیے تصویر اپلوڈ کریں یا کیمرہ استعمال کریں۔",
    },
}


def load_image(file_or_bytes):
    """Open any Pillow-readable image and return an upright RGB PIL image."""
    data = file_or_bytes if isinstance(file_or_bytes, (bytes, bytearray)) else file_or_bytes.read()
    img = Image.open(io.BytesIO(data))
    try:
        img.seek(0)                       # first frame of GIF / multi-page TIFF
    except Exception:  # noqa: BLE001
        pass
    img = ImageOps.exif_transpose(img)    # respect phone-camera rotation
    if img.mode in ("RGBA", "LA", "P"):   # flatten transparency on white
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img)
    return img.convert("RGB")


def quality_report(img):
    """Cheap heuristics that warn about photos likely to give unreliable results."""
    w, h = img.size
    small = img.copy()
    small.thumbnail((512, 512))
    g = np.asarray(small.convert("L"), dtype=np.float64)
    lap = 4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    sharp, bright, contrast = float(lap.var()), float(g.mean()), float(g.std())
    warnings = []
    if min(w, h) < 150:
        warnings.append(f"Very small image ({w}x{h}); use a higher-resolution photo.")
    if sharp < 30:
        warnings.append("Image looks blurry; retake it in focus.")
    if bright < 45:
        warnings.append("Image is very dark; use better lighting.")
    if bright > 215:
        warnings.append("Image is very bright or overexposed.")
    if contrast < 20:
        warnings.append("Very low contrast; the lesion may not be clearly visible.")
    return {"size": (w, h), "sharpness": round(sharp, 1), "brightness": round(bright, 1),
            "contrast": round(contrast, 1), "warnings": warnings}


def normalized_entropy(probs):
    """0 = completely certain, 1 = completely undecided."""
    p = np.clip(np.asarray(probs, dtype=np.float64), 1e-12, 1.0)
    return float(-(p * np.log(p)).sum() / np.log(len(p)))


def _thumb_b64(img, size=160):
    t = img.copy(); t.thumbnail((size, size))
    buf = io.BytesIO(); t.save(buf, format="JPEG", quality=80)
    return base64.b64encode(buf.getvalue()).decode()


def build_html_report(rows):
    """rows: list of dicts with keys image(PIL), name, prediction, confidence, risk, second, warnings."""
    parts = ["<html><head><meta charset='utf-8'><title>Skin Lesion Report</title>"
             "<link href='https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;600&display=swap' rel='stylesheet'>"
             "<style>body{font-family:Inter,Arial,sans-serif;margin:2.5rem;color:#1B2133;background:#F6F2EA}"
             "h1{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:2.4rem;margin:0 0 6px 0}"
             "table{border-collapse:collapse;width:100%;background:#fff}td,th{border:1px solid #E4DDD0;padding:10px;vertical-align:top;font-size:.9rem}"
             "th{background:#FBF8F2;color:#737A8A;text-transform:uppercase;font-size:.72rem;letter-spacing:.08em;text-align:left}"
             ".alert{color:#8C2F2A;font-weight:600}img{border-radius:8px}@media print{body{background:#fff;margin:1rem}}</style></head><body>",
             "<h1>Skin Lesion Classification Report</h1>",
             f"<p>Generated {datetime.now():%Y-%m-%d %H:%M}</p>",
             "<p><b>Research prototype only; not a medical diagnosis.</b> "
             "Consult a dermatologist about any concerning skin change.</p>",
             "<table><tr><th>Image</th><th>File</th><th>Prediction</th><th>Confidence</th>"
             "<th>Risk group</th><th>Runner-up</th><th>Notes</th></tr>"]
    for r in rows:
        cls = "alert" if r["risk"] in ALERT_RISKS else ""
        parts.append(
            f"<tr><td><img src='data:image/jpeg;base64,{_thumb_b64(r['image'])}'></td>"
            f"<td>{html.escape(r['name'])}</td><td class='{cls}'>{html.escape(r['prediction'])}</td>"
            f"<td>{r['confidence']:.1%}</td><td class='{cls}'>{html.escape(r['risk'])}</td>"
            f"<td>{html.escape(r['second'])}</td><td>{html.escape('; '.join(r['warnings']) or '-')}</td></tr>")
    parts.append("</table></body></html>")
    return "".join(parts)
