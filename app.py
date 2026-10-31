"""Skin Lesion Classifier: Streamlit app (v2).

Run:  streamlit run app.py
Needs in this folder: final_model.keras (from Kaggle outputs/), class_names.json, helpers.py
Research prototype only; not a medical diagnosis.
"""
import io
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from PIL import Image
from tensorflow import keras
import matplotlib

matplotlib.use("Agg")
from matplotlib import colormaps

import helpers as H
import ui

HERE = Path(__file__).parent
MODEL_PATH = next((HERE / n for n in ("final_model.keras", "skin_lesion_model.keras")
                   if (HERE / n).exists()), HERE / "final_model.keras")
CLASSES_PATH = HERE / "class_names.json"
IMG_SIZE = (224, 224)

st.set_page_config(page_title="Skin Lesion Classifier", page_icon="🩺", layout="wide", initial_sidebar_state="collapsed")


# ------------------------------------------------------------------ model
@st.cache_resource(show_spinner="Loading model...")
def load_model():
    model = keras.models.load_model(MODEL_PATH)
    class_names = json.loads(CLASSES_PATH.read_text())
    conv_model, head = None, None  # Grad-CAM is optional
    try:
        idx = next(i for i, l in enumerate(model.layers)
                   if isinstance(l, keras.Model)
                   and any(sub.name == "top_activation" for sub in l.layers))
        backbone = model.layers[idx]
        head = model.layers[idx + 1:]
        conv_model = keras.Model(backbone.input,
                                 [backbone.get_layer("top_activation").output, backbone.output])
    except Exception as err:  # noqa: BLE001
        print("Grad-CAM disabled:", err)
    return model, class_names, conv_model, head


def to_array(img: Image.Image) -> np.ndarray:
    return np.asarray(img.convert("RGB").resize(IMG_SIZE), dtype=np.float32)  # 0-255 for EfficientNet


@st.cache_data(show_spinner=False, max_entries=64)
def run_inference(img_bytes: bytes, tta: bool):
    model = load_model()[0]
    x = tf.convert_to_tensor(to_array(H.load_image(img_bytes))[None, ...])
    views = [x, tf.image.flip_left_right(x), tf.image.flip_up_down(x),
             tf.image.flip_up_down(tf.image.flip_left_right(x))] if tta else [x]
    return np.mean([model(v, training=False).numpy() for v in views], axis=0)[0]


def gradcam(conv_model, head, arr, class_index):
    x = tf.convert_to_tensor(arr[None, ...])
    with tf.GradientTape() as tape:
        conv_out, feats = conv_model(x, training=False)
        tape.watch(conv_out)
        y = feats
        for layer in head:
            y = layer(y, training=False)
        score = y[:, class_index]
    grads = tape.gradient(score, conv_out)
    pooled = tf.reduce_mean(grads, axis=(0, 1, 2))
    heat = tf.nn.relu(tf.reduce_sum(conv_out[0] * pooled, axis=-1))
    return (heat / (tf.reduce_max(heat) + 1e-8)).numpy()


@st.cache_data(show_spinner=False, max_entries=64)
def cached_cam(img_bytes, class_index, _conv_model, _head):
    arr = to_array(H.load_image(img_bytes))
    return gradcam(_conv_model, _head, arr, class_index)


@st.cache_data(show_spinner=False, max_entries=64)
def cached_quality(img_bytes):
    return H.quality_report(H.load_image(img_bytes))


def overlay(arr, heat, alpha):
    heat_img = Image.fromarray(np.uint8(255 * heat)).resize(IMG_SIZE, Image.BILINEAR)
    colored = colormaps["jet"](np.asarray(heat_img) / 255.0)[..., :3]
    return np.clip((1 - alpha) * (arr / 255.0) + alpha * colored, 0, 1)


def show_image(img, caption=None):
    try:
        st.image(img, caption=caption, width="stretch")
    except Exception:  # noqa: BLE001  (older Streamlit versions)
        st.image(img, caption=caption, use_container_width=True)


# ------------------------------------------------------------------ top bar + settings
with st.container(key="topbar"):
    theme = "light"
    c_brand, c_gap, c_lang, c_set = st.columns([3.0, 3.6, 1.6, 1.5], vertical_alignment="center")
    with c_lang:
        lang = "ur" if st.selectbox("Language", ["English", "اردو"], label_visibility="collapsed", key="lang") == "اردو" else "en"
    with c_set:
        try:
            _pop = st.popover("Settings", icon=":material/tune:", width="stretch")
        except TypeError:  # older Streamlit
            _pop = st.popover("Settings", use_container_width=True)
        with _pop:
            use_tta = st.checkbox("Test-time augmentation (steadier, slower)", value=True)
            show_cam = st.checkbox("Show Grad-CAM heatmap", value=True)
            cam_alpha = st.slider("Heatmap opacity", 0.1, 0.9, 0.4, 0.05)
            top_k = st.slider("Classes to show", 1, 9, 3)
            conf_threshold = st.slider("Low-confidence threshold", 0.2, 0.9, 0.5, 0.05)
            st.caption(f"Supported: {H.SUPPORTED_HINT}")
    T = H.STRINGS[lang]
    S = ui.UI_STR[lang]
    with c_brand:
        ui.brand(S["brand_sub"])

ui.inject_css(theme)
ui.enhance_js()
RTL = lang == "ur"

# ------------------------------------------------------------------ hero
ui.hero(S, rtl=RTL)
ui.disclaimer(S, T["disclaimer"], rtl=RTL)

if not MODEL_PATH.exists() or not CLASSES_PATH.exists():
    st.error("Model file not found. Put `final_model.keras` (downloaded from Kaggle) "
             "in the same folder as `app.py`.")
    st.stop()

model, class_names, conv_model, head = load_model()
tab_analyze, tab_results, tab_learn = st.tabs(S["tabs"])

# ------------------------------------------------------------------ analyze
with tab_analyze:
    ui.section(S["up_eyebrow"], S["up_title"], S["up_sub"], rtl=RTL)
    col_up, col_cam = st.columns([2, 1], gap="large")
    with col_up:
        files = st.file_uploader(T["upload"], accept_multiple_files=True, label_visibility="collapsed",
                                 key="uploader", help=f"Any image format works. {H.SUPPORTED_HINT}")
        st.caption(f"{H.SUPPORTED_HINT}")
    with col_cam:
        with st.expander(S["cam_title"], icon=":material/photo_camera:"):
            cam = st.camera_input("Camera", label_visibility="collapsed")

    items = [(f.name, f.getvalue()) for f in (files or [])]
    if cam is not None:
        items.append((f"camera_{datetime.now():%H%M%S}.jpg", cam.getvalue()))

    records = []
    if not items:
        ui.empty_state(S["empty_title"], T["no_input"],
                       ["Bright, even light", "In focus, 10-15 cm away", "Lesion centred", "JPG, PNG, WEBP and more"])
    else:
        progress = st.progress(0.0, text="Analyzing...")
        for n, (name, raw) in enumerate(items):
            progress.progress((n + 1) / len(items), text=f"Analyzing {name} ({n + 1}/{len(items)})")
            try:
                img = H.load_image(raw)
            except Exception as err:  # noqa: BLE001
                st.error(f"Could not read **{name}** as an image: {err}")
                continue
            probs = run_inference(raw, use_tta)
            order = np.argsort(probs)[::-1]
            top, second = int(order[0]), int(order[1])
            risk, desc = H.CLASS_INFO.get(class_names[top], ("Unknown", ""))
            quality = cached_quality(raw)
            records.append({"name": name, "image": img, "raw": raw, "probs": probs, "order": order,
                            "top": top, "risk": risk, "desc": desc, "quality": quality,
                            "entropy": H.normalized_entropy(probs),
                            "second": f"{class_names[second]} ({probs[second]:.1%})"})
        progress.empty()

        st.write("")
        ui.section(S["res_eyebrow"], S["res_title"], rtl=RTL)
        flagged = sum(r["risk"] in H.ALERT_RISKS for r in records)
        ui.stat_cards([
            ("Images analyzed", len(records), ""),
            ("Potentially cancerous / pre-cancerous", flagged, "red" if flagged else ""),
            ("Low-confidence results", sum(r["probs"][r["top"]] < conf_threshold for r in records), "amber"),
        ])

        for i, r in enumerate(records):
            conf = float(r["probs"][r["top"]])
            label = f"{r['name']}  ·  {class_names[r['top']]} ({conf:.1%})  ·  {r['risk']}"
            with st.expander(label, expanded=(len(records) == 1 or i == 0)):
                c1, c2, c3 = st.columns([1, 1, 1.3], gap="medium")
                with c1:
                    show_image(r["image"], "Uploaded")
                with c2:
                    if show_cam and conv_model is not None:
                        try:
                            arr = to_array(r["image"])
                            heat = cached_cam(r["raw"], r["top"], conv_model, head)
                            show_image(overlay(arr, heat, cam_alpha),
                                       "Grad-CAM: where the model looked")
                        except Exception as err:  # noqa: BLE001
                            st.caption(f"Grad-CAM unavailable: {err}")
                with c3:
                    ui.result_card(r["name"], class_names[r["top"]], conf, r["risk"], r["desc"], r["entropy"],
                                   [(class_names[j], float(r["probs"][j])) for j in r["order"][:top_k]],
                                   T["most_likely"], rtl=RTL)
                if r["risk"] in H.ALERT_RISKS:
                    ui.notice(T["alert"], "danger", rtl=RTL)
                if conf < conf_threshold:
                    ui.notice(T["low_conf"], "info", rtl=RTL)
                for w in r["quality"]["warnings"]:
                    ui.notice(f"Photo quality: {w}", "warn")
                # (Streamlit does not allow an expander inside an expander, so use a checkbox)
                if st.checkbox("Show all class probabilities & image details", key=f"details_{i}"):
                    ui.table(pd.DataFrame({"class": [class_names[j] for j in r["order"]],
                                           "probability": [float(r["probs"][j]) for j in r["order"]]}))
                    q = r["quality"]
                    st.caption(f"Size {q['size'][0]}x{q['size'][1]} | sharpness {q['sharpness']} | "
                               f"brightness {q['brightness']} | contrast {q['contrast']}")

# ------------------------------------------------------------------ results & export
with tab_results:
    ui.section(S["export_eyebrow"], S["export_title"], rtl=RTL)
    if not records:
        ui.empty_state(S["empty_title"], T["no_input"], ["Results table", "CSV export", "Printable report"])
    else:
        df = pd.DataFrame([{
            "file": r["name"],
            "prediction": class_names[r["top"]],
            "confidence": round(float(r["probs"][r["top"]]), 4),
            "risk_group": r["risk"],
            "runner_up": r["second"],
            "uncertainty": round(r["entropy"], 3),
            "quality_warnings": "; ".join(r["quality"]["warnings"]),
            **{f"p_{class_names[j]}": round(float(r["probs"][j]), 4) for j in range(len(class_names))},
        } for r in records])
        ui.stat_cards([
            ("Images analyzed", len(records), ""),
            ("Potentially cancerous / pre-cancerous", sum(r["risk"] in H.ALERT_RISKS for r in records),
             "red" if any(r["risk"] in H.ALERT_RISKS for r in records) else ""),
            ("Low-confidence results", sum(r["probs"][r["top"]] < conf_threshold for r in records), "amber"),
        ])
        ui.table(df)

        d1, d2, _ = st.columns([1, 1.4, 2])
        d1.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"),
                           file_name=f"skin_results_{datetime.now():%Y%m%d_%H%M}.csv", mime="text/csv",
                           icon=":material/download:")
        report_rows = [{"image": r["image"], "name": r["name"], "prediction": class_names[r["top"]],
                        "confidence": float(r["probs"][r["top"]]), "risk": r["risk"],
                        "second": r["second"], "warnings": r["quality"]["warnings"]} for r in records]
        d2.download_button("Download printable report", H.build_html_report(report_rows).encode("utf-8"),
                           file_name=f"skin_report_{datetime.now():%Y%m%d_%H%M}.html", mime="text/html",
                           icon=":material/description:")

        ui.subsection("Predicted class distribution", rtl=RTL)
        vc = df["prediction"].value_counts()
        ui.bars([(k, v / vc.max(), f"{v} image{'s' if v != 1 else ''}") for k, v in vc.items()])

# ------------------------------------------------------------------ learn
with tab_learn:
    ui.section(S["learn_eyebrow"], S["learn_title"], rtl=RTL)
    ui.subsection("The nine lesion classes", rtl=RTL)
    ui.class_cards([(c, H.CLASS_INFO[c][0], H.CLASS_INFO[c][1]) for c in class_names if c in H.CLASS_INFO])
    ui.subsection("The ABCDE rule: when to see a doctor", rtl=RTL)
    ui.abcde([("A", "Asymmetry", "One half does not match the other."),
              ("B", "Border", "Edges are irregular, ragged or blurred."),
              ("C", "Colour", "Several colours or uneven shades."),
              ("D", "Diameter", "Larger than about 6 mm, though melanomas can be smaller."),
              ("E", "Evolving", "Any change in size, shape or colour, or itching and bleeding.")])
    ui.subsection("Tips for a good photograph", rtl=RTL)
    ui.tips(["Use bright, even daylight with no flash glare.",
             "Hold the camera steady, 10-15 cm away, and in focus.",
             "Centre the lesion and fill the frame with it.",
             "Add a ruler or coin for scale, and re-photograph over time."])
    ui.subsection("About this model", rtl=RTL)
    ui.key_values([("Architecture", "EfficientNetB0, fine-tuned"),
                   ("Training data", "About 2,200 ISIC images, 9 classes"),
                   ("Input size", "224 x 224 pixels"),
                   ("Status", "Research prototype; accuracy on real clinical photos is unproven"),
                   ("Intended use", "Learning and research only")])

ui.footer("Research prototype for education only. Not a medical device. Made with Streamlit and TensorFlow.")