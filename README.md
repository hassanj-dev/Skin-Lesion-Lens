# Lesion Lens: Skin Lesion Classifier (Streamlit app, v6 editorial UI + motion design)

Put `final_model.keras` (from your Kaggle notebook outputs) in this folder next to `app.py`.
Keep these files together: app.py, ui.py, helpers.py, class_names.json, .streamlit/config.toml

    pip install -r requirements.txt
    streamlit run app.py

UI: top navigation bar (language, dark mode, settings popover), editorial hero, Analyze /
Results & Export / Learn tabs. Model, inference, Grad-CAM, TTA and export logic are unchanged.

Research prototype only; not a medical diagnosis.
