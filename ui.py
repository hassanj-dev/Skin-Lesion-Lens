"""Editorial design layer (CSS + HTML components) for the Skin Lesion Classifier.

Pure presentation: no model, prediction or business logic lives here.
"""
import html as _h

import streamlit as st

# ----------------------------------------------------------------- copy (EN / UR)
UI_STR = {
    "en": {
        "brand_sub": "Skin Lesion Classifier",
        "tabs": ["Analyze", "Results & Export", "Learn"],
        "eyebrow": "Research tool · Dermatology imaging",
        "headline": "A careful second look at every lesion.",
        "sub": "Upload skin photographs and receive an explainable, probability-based reading across nine lesion types. Built for study and research.",
        "disclaimer_title": "Research use only",
        "feats": [("eye", "Explainable", "Heatmaps show where the model looked."),
                  ("layers", "Nine lesion classes", "From common moles to melanoma."),
                  ("download", "Batch and export", "Analyse many photos; export CSV or a report.")],
        "up_eyebrow": "Step 01", "up_title": "Add your photographs",
        "up_sub": "Drop one or many images. Any common format works.",
        "cam_title": "Or use the camera",
        "empty_title": "Begin with a photograph",
        "res_eyebrow": "Step 02", "res_title": "Analysis",
        "export_eyebrow": "Summary", "export_title": "Results and export",
        "learn_eyebrow": "Reference", "learn_title": "Understanding the results",
    },
    "ur": {
        "brand_sub": "جلدی زخم کی درجہ بندی",
        "tabs": ["تجزیہ", "نتائج اور برآمد", "سیکھیں"],
        "eyebrow": "تحقیقی ٹول · جلدی امراض کی امیجنگ",
        "headline": "ہر نشان پر ایک محتاط دوسری نظر۔",
        "sub": "جلد کی تصاویر اپلوڈ کریں اور نو اقسام کے زخموں پر وضاحت کے ساتھ امکانی نتیجہ حاصل کریں۔ مطالعہ اور تحقیق کے لیے بنایا گیا۔",
        "disclaimer_title": "صرف تحقیق کے لیے",
        "feats": [("eye", "قابلِ وضاحت", "ہیٹ میپ دکھاتا ہے کہ ماڈل نے کہاں دیکھا۔"),
                  ("layers", "نو اقسام", "عام تل سے میلانوما تک۔"),
                  ("download", "بیچ اور برآمد", "کئی تصاویر کا تجزیہ کریں، CSV یا رپورٹ حاصل کریں۔")],
        "up_eyebrow": "مرحلہ ۰۱", "up_title": "اپنی تصاویر شامل کریں",
        "up_sub": "ایک یا کئی تصاویر ڈالیں۔ ہر عام فارمیٹ چلتا ہے۔",
        "cam_title": "یا کیمرہ استعمال کریں",
        "empty_title": "ایک تصویر سے آغاز کریں",
        "res_eyebrow": "مرحلہ ۰۲", "res_title": "تجزیہ",
        "export_eyebrow": "خلاصہ", "export_title": "نتائج اور برآمد",
        "learn_eyebrow": "حوالہ", "learn_title": "نتائج کو سمجھنا",
    },
}

ICONS = {
    "upload": '<path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5"/><path d="M4 15v3.5A1.5 1.5 0 0 0 5.5 20h13a1.5 1.5 0 0 0 1.5-1.5V15"/>',
    "camera": '<path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="3.5"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "layers": '<path d="M12 3 3 8l9 5 9-5-9-5z"/><path d="m3 12.5 9 5 9-5"/><path d="m3 17 9 5 9-5" opacity=".5"/>',
    "download": '<path d="M12 4v11m0 0 4.5-4.5M12 15l-4.5-4.5"/><path d="M4 20h16"/>',
    "shield": '<path d="M12 3 5 6v6c0 4.4 3 7.4 7 9 4-1.6 7-4.6 7-9V6l-7-3z"/><path d="m9 12 2 2 4-4"/>',
}


def icon(name, size=20):
    return (f"<svg width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' stroke='currentColor' "
            f"stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'>{ICONS[name]}</svg>")


# ----------------------------------------------------------------- design tokens
LIGHT = """--bg:#F6F2EA;--surface:#FFFFFF;--surface2:#FBF8F2;--ink:#1B2133;--ink2:#3C4357;--muted:#737A8A;
--line:#E4DDD0;--line2:#EFE9DE;--accent:#6D62C9;--lav:#E3DEF6;--lav-ink:#4B3FA8;--peach:#F7E1D2;--peach-ink:#8A4B27;
--sage:#DCE7D7;--sage-ink:#3E6347;--rose:#F1D4CF;--rose-ink:#8C2F2A;--btn:#1B2133;--btn-ink:#F6F2EA;
--shadow:0 1px 2px rgba(27,33,51,.04),0 8px 24px rgba(27,33,51,.05);--amb1:rgba(196,186,240,.55);--amb2:rgba(246,208,182,.5);--amb3:rgba(196,218,190,.45);"""
DARK = """--bg:#101320;--surface:#171B2B;--surface2:#1C2133;--ink:#ECE7DC;--ink2:#C4C7D2;--muted:#8D93A6;
--line:#2A3046;--line2:#222840;--accent:#9A90E8;--lav:#2A2850;--lav-ink:#C9C3F5;--peach:#3A2B26;--peach-ink:#F2C4A6;
--sage:#25352C;--sage-ink:#B5D3BC;--rose:#3C2527;--rose-ink:#F1B3AE;--btn:#ECE7DC;--btn-ink:#101320;
--shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px rgba(0,0,0,.3);--amb1:rgba(98,84,200,.22);--amb2:rgba(190,110,70,.13);--amb3:rgba(60,130,110,.15);"""

RISK_CLASS = {"Benign": "sage", "Pre-cancerous": "peach", "Malignant": "rose"}

FONT_IMPORT = """@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600&family=Noto+Naskh+Arabic:wght@400;600&display=swap');"""

CSS = """
:root{--serif:'DM Serif Display','Playfair Display',Georgia,'Times New Roman',serif;--sans:'Inter','Manrope',system-ui,-apple-system,'Segoe UI',sans-serif;--r:12px;}
html,body,[class*="css"],.stApp{font-family:var(--sans)!important;}
.stApp{background:var(--bg);color:var(--ink);}
header[data-testid="stHeader"]{background:transparent;height:0;pointer-events:none!important;}
[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"],[data-testid="stAppDeployButton"]{display:none!important;}
.st-key-topbar{position:relative;z-index:10;}
.block-container{padding:1.2rem 2rem 3rem 2rem;max-width:1180px;}
#MainMenu,footer,[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important;}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li,[data-testid="stMarkdownContainer"] strong,
[data-testid="stWidgetLabel"] *,[data-testid="stCheckbox"] *,[data-testid="stToggle"] *{color:var(--ink);}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] *{color:var(--muted)!important;}

/* ---- top bar */
.st-key-topbar{border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:34px;}
.brand{display:flex;align-items:center;gap:11px;}
.brand .mark{width:34px;height:34px;border-radius:50%;border:1.5px solid var(--ink);display:flex;align-items:center;justify-content:center;}
.brand .mark i{width:12px;height:12px;border-radius:50%;background:var(--accent);display:block;}
.brand b{font-family:var(--serif);font-weight:400;font-size:1.35rem;color:var(--ink);line-height:1;display:block;}
.brand span{font-size:.72rem;color:var(--muted);letter-spacing:.04em;display:block;margin-top:3px;}
[data-baseweb="select"]>div{background:var(--surface)!important;border:1px solid var(--line)!important;border-radius:10px!important;min-height:38px;}
[data-baseweb="select"] *{color:var(--ink)!important;}
[data-baseweb="popover"] [data-baseweb="menu"]{background:var(--surface)!important;}
[data-baseweb="popover"] li{color:var(--ink)!important;background:var(--surface)!important;}
[data-baseweb="popover"] li:hover{background:var(--surface2)!important;}
[data-testid="stPopover"] button,[data-testid="stPopoverButton"]{background:var(--surface)!important;border:1px solid var(--line)!important;
border-radius:10px!important;color:var(--ink)!important;font-weight:500;min-height:38px;box-shadow:none!important;}
[data-testid="stPopoverBody"],[data-baseweb="popover"]>div{background:var(--surface)!important;border:1px solid var(--line);border-radius:14px!important;}

/* ---- hero */
.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:center;padding:18px 0 34px 0;animation:rise .6s ease both;}
.eyebrow{font-size:.72rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);}
.hero h1{font-family:var(--serif);font-weight:400;font-size:3.5rem;line-height:1.04;letter-spacing:-.01em;color:var(--ink);margin:14px 0 18px 0;padding:0;}
.hero p.lead{color:var(--ink2);font-size:1.05rem;line-height:1.65;max-width:520px;margin:0;}
.hero .art{display:flex;justify-content:center;}
.feats{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:4px 0 22px 0;}
.feat{display:flex;gap:14px;padding:20px 22px 20px 0;}
.feat+.feat{padding-left:22px;border-left:1px solid var(--line);}
.feat .ic{color:var(--accent);flex:none;margin-top:2px;}
.feat b{display:block;font-weight:600;font-size:.95rem;color:var(--ink);margin-bottom:3px;}
.feat span{color:var(--muted);font-size:.86rem;line-height:1.5;}
.disc{display:flex;gap:12px;align-items:flex-start;background:var(--peach);color:var(--peach-ink);border-radius:var(--r);padding:13px 16px;font-size:.88rem;line-height:1.5;margin-bottom:40px;}
.disc svg{flex:none;margin-top:1px;}

/* ---- section heads */
.sec{margin:46px 0 20px 0;}.stTabs [data-baseweb="tab-panel"]>div>div:first-child .sec{margin-top:0;}
.sec h2{font-family:var(--serif);font-weight:400;font-size:2.1rem;line-height:1.12;color:var(--ink);margin:8px 0 6px 0;padding:0;letter-spacing:-.005em;}
.sec p{color:var(--muted);margin:0;font-size:.95rem;}
.subsec{font-family:var(--serif);font-size:1.5rem;color:var(--ink);margin:38px 0 14px 0;font-weight:400;}

/* ---- notices */
.note{border-left:3px solid var(--accent);background:var(--surface);border-radius:0 var(--r) var(--r) 0;padding:12px 16px;margin:10px 0;
font-size:.9rem;line-height:1.55;color:var(--ink2);box-shadow:var(--shadow);}
.note.warn{border-left-color:#D9925F;}.note.danger{border-left-color:#C0584F;}.note.info{border-left-color:var(--accent);}
.note b{color:var(--ink);}

/* ---- stats */
.stats{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:4px 0 26px 0;}
.stat{padding:18px 22px 18px 0;animation:rise .5s ease both;}
.stat+.stat{padding-left:22px;border-left:1px solid var(--line);}
.stat .v{font-family:var(--serif);font-size:2.7rem;line-height:1;color:var(--ink);}
.stat .v.red{color:var(--rose-ink);}.stat .v.amber{color:var(--peach-ink);}
.stat .k{color:var(--muted);font-size:.8rem;margin-top:8px;letter-spacing:.02em;}

/* ---- empty state */
.empty{border:1px solid var(--line);background:var(--surface);border-radius:16px;padding:34px 28px;text-align:center;margin-top:14px;box-shadow:var(--shadow);}
.empty .ic{width:54px;height:54px;border-radius:50%;background:var(--lav);color:var(--lav-ink);display:inline-flex;align-items:center;justify-content:center;}
.empty h3{font-family:var(--serif);font-weight:400;font-size:1.6rem;margin:14px 0 6px 0;color:var(--ink);}
.empty p{color:var(--muted);margin:0 auto;max-width:480px;font-size:.92rem;}
.empty .tips{display:flex;gap:8px 18px;justify-content:center;flex-wrap:wrap;margin-top:18px;color:var(--ink2);font-size:.82rem;}
.empty .tips span:before{content:"";display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--accent);margin-right:8px;vertical-align:middle;}

/* ---- result card */
.rcard{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:24px;box-shadow:var(--shadow);animation:rise .55s ease both;}
.cname{font-family:var(--serif);font-weight:400;font-size:2.05rem;line-height:1.08;text-transform:capitalize;color:var(--ink);margin:8px 0 14px 0;}
.conf{display:flex;align-items:baseline;gap:6px;}
.conf .big{font-family:var(--serif);font-size:3rem;line-height:1;color:var(--ink);}
.conf .u{font-family:var(--serif);font-size:1.4rem;color:var(--muted);}
.conf .l{margin-left:8px;color:var(--muted);font-size:.8rem;letter-spacing:.04em;text-transform:uppercase;}
.hair{height:3px;background:var(--line2);border-radius:3px;overflow:hidden;margin:12px 0 16px 0;}
.hair i{display:block;height:100%;background:var(--ink);border-radius:3px;transform-origin:left;animation:grow .9s cubic-bezier(.2,.7,.2,1) both;}
.tags{display:flex;gap:8px;flex-wrap:wrap;}
.tag{display:inline-flex;align-items:center;gap:7px;border-radius:999px;padding:4px 12px;font-size:.76rem;font-weight:600;letter-spacing:.01em;}
.tag i{width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;}
.tag.sage{background:var(--sage);color:var(--sage-ink);}.tag.peach{background:var(--peach);color:var(--peach-ink);}
.tag.rose{background:var(--rose);color:var(--rose-ink);}.tag.unk{background:var(--line2);color:var(--ink2);}.tag.lav{background:var(--lav);color:var(--lav-ink);}
.desc{color:var(--ink2);font-size:.92rem;line-height:1.65;margin:16px 0 4px 0;}
.bars{margin-top:18px;border-top:1px solid var(--line2);padding-top:6px;}
.bar{margin:13px 0;}
.bar .row{display:flex;justify-content:space-between;font-size:.84rem;text-transform:capitalize;margin-bottom:6px;color:var(--ink);}
.bar .row span:last-child{color:var(--muted);font-variant-numeric:tabular-nums;}
.track{background:var(--line2);border-radius:3px;height:4px;overflow:hidden;}
.fill{height:100%;border-radius:3px;background:var(--accent);transform-origin:left;animation:grow .9s cubic-bezier(.2,.7,.2,1) both;}
.fill.top{background:var(--ink);}

/* ---- learn */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.ccard{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:20px;transition:border-color .2s,transform .2s;animation:rise .5s ease both;}
.ccard:hover{border-color:var(--accent);transform:translateY(-2px);}
.ccard .n{font-family:var(--serif);font-size:.95rem;color:var(--muted);display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;}
.ccard h4{font-family:var(--serif);font-weight:400;font-size:1.3rem;margin:0 0 8px 0;text-transform:capitalize;color:var(--ink);}
.ccard p{margin:0;color:var(--ink2);font-size:.86rem;line-height:1.6;}
.abcde{display:grid;grid-template-columns:repeat(5,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
.abox{padding:22px 18px 22px 0;}
.abox+.abox{padding-left:18px;border-left:1px solid var(--line);}
.abox b{display:block;font-family:var(--serif);font-weight:400;font-size:3rem;line-height:1;color:var(--accent);margin-bottom:10px;}
.abox div{font-weight:600;font-size:.92rem;margin-bottom:4px;color:var(--ink);}
.abox span{color:var(--muted);font-size:.82rem;line-height:1.5;display:block;}
.tipgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:0 36px;}
.tip{display:flex;gap:16px;padding:14px 0;border-bottom:1px solid var(--line2);color:var(--ink2);font-size:.92rem;line-height:1.55;}
.tip b{font-family:var(--serif);font-weight:400;color:var(--accent);font-size:1.1rem;flex:none;width:26px;}
.kv{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:6px 22px;}
.kv div{display:flex;justify-content:space-between;gap:20px;padding:13px 0;border-bottom:1px solid var(--line2);font-size:.9rem;}
.kv div:last-child{border-bottom:0;}.kv span:first-child{color:var(--muted);}.kv span:last-child{color:var(--ink);text-align:right;}
.footer{text-align:center;color:var(--muted);font-size:.8rem;margin:56px 0 8px 0;border-top:1px solid var(--line);padding-top:22px;}
.footer b{font-family:var(--serif);font-weight:400;color:var(--ink);font-size:1rem;}
.rtl{direction:rtl;text-align:right;font-family:'Noto Naskh Arabic','Inter',serif!important;}
.rtl h1,.rtl h2,.rtl .cname{font-family:'Noto Naskh Arabic',var(--serif)!important;}

/* ---- tables */
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--surface);margin:8px 0 18px 0;}
.tbl{border-collapse:collapse;width:100%;font-size:.86rem;}
.tbl th{background:var(--surface2);color:var(--muted);text-align:left;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;padding:12px 16px;white-space:nowrap;}
.tbl td{padding:12px 16px;border-top:1px solid var(--line2);color:var(--ink);white-space:nowrap;}
.tbl tr:hover td{background:var(--surface2);}

/* ---- streamlit widgets */
.stTabs [data-baseweb="tab-list"]{gap:30px;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{padding:10px 0;height:auto;background:transparent;color:var(--muted);font-weight:500;font-size:.98rem;}
.stTabs [data-baseweb="tab"] *{color:inherit!important;}
.stTabs [aria-selected="true"]{color:var(--ink)!important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--accent);height:2px;}
.stTabs [data-baseweb="tab-border"]{display:none;}
.stTabs [data-baseweb="tab-panel"]{padding-top:26px;}
[data-testid="stFileUploaderDropzone"]{background:var(--surface);border:1.5px dashed var(--line);border-radius:16px;padding:34px 24px;transition:border-color .2s,background .2s;}
[data-testid="stFileUploaderDropzone"]:hover{border-color:var(--accent);background:var(--surface2);}
[data-testid="stFileUploaderDropzone"] *{color:var(--muted)!important;}
[data-testid="stFileUploaderDropzone"] button{background:var(--btn)!important;color:var(--btn-ink)!important;border:0!important;border-radius:10px;font-weight:600;}
[data-testid="stFileUploaderDropzone"] button *{color:var(--btn-ink)!important;}
[data-testid="stFileUploader"] section+div *{color:var(--ink2)!important;}
[data-testid="stCameraInput"]>div{border-radius:16px;overflow:hidden;border:1px solid var(--line);background:var(--surface);}
[data-testid="stCameraInput"] button{background:var(--btn)!important;color:var(--btn-ink)!important;border:0!important;border-radius:10px;}
[data-testid="stCameraInput"] button *{color:var(--btn-ink)!important;}
[data-testid="stExpander"]{background:var(--surface);border:1px solid var(--line)!important;border-radius:16px!important;overflow:hidden;margin-bottom:14px;box-shadow:var(--shadow);}
[data-testid="stExpander"] summary{font-weight:600;padding:14px 18px;}
[data-testid="stExpander"] summary *{color:var(--ink)!important;}
[data-testid="stExpander"] details{background:var(--surface);}
[data-testid="stImage"] img{border-radius:var(--r);border:1px solid var(--line);}
.stButton>button,[data-testid="stDownloadButton"] button{background:var(--btn);color:var(--btn-ink)!important;border:0;border-radius:10px;font-weight:600;
padding:.62rem 1.3rem;transition:transform .15s,opacity .15s;}
.stButton>button *,[data-testid="stDownloadButton"] button *{color:var(--btn-ink)!important;}
.stButton>button:hover,[data-testid="stDownloadButton"] button:hover{transform:translateY(-1px);opacity:.92;}
[data-testid="stProgress"] *{color:var(--muted)!important;}
[data-testid="stCheckbox"] label span{font-size:.9rem;}

@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
@media(max-width:960px){.hero{grid-template-columns:1fr;gap:10px}.hero .art{order:-1;max-width:260px;margin:0 auto}.hero h1{font-size:2.7rem}
.grid{grid-template-columns:repeat(2,1fr)}.abcde{grid-template-columns:1fr}.abox{padding:16px 0!important;border-left:0!important;border-top:1px solid var(--line)}
.abox:first-child{border-top:0}.tipgrid{grid-template-columns:1fr}}
@media(max-width:700px){.block-container{padding:1rem 1.1rem 3rem 1.1rem}.feats,.stats{grid-template-columns:1fr}
.feat,.stat{padding:16px 0!important;border-left:0!important}.feat+.feat,.stat+.stat{border-top:1px solid var(--line)}
.grid{grid-template-columns:1fr}.hero h1{font-size:2.2rem}.sec h2{font-size:1.7rem}.cname{font-size:1.7rem}}
"""


MOTION = r'''
/* ================= MOTION ================= */
@property --num{syntax:'<integer>';initial-value:0;inherits:false;}
:root{--ease:cubic-bezier(.2,.8,.2,1);}
@keyframes fadeIn{from{opacity:0}}
@keyframes wordUp{from{transform:translateY(108%);opacity:0}}
@keyframes revealUp{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}
@keyframes imgIn{from{opacity:0;transform:scale(.965);filter:blur(5px)}to{opacity:1;transform:none;filter:none}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
@keyframes floatSm{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}
@keyframes drift{0%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(3%,-2%,0) scale(1.05)}100%{transform:translate3d(-3%,3%,0) scale(1.02)}}
@keyframes dotDrift{0%,100%{transform:translate(0,0)}50%{transform:translate(4px,-6px)}}
@keyframes shimmer{from{background-position:200% 0}to{background-position:-200% 0}}
@keyframes countup{from{--num:0}}
@keyframes pop{from{opacity:0;transform:translateY(-6px) scale(.98)}}

/* ambient background: slow, blurred colour fields behind the content */
.stApp::before{content:"";position:fixed;inset:-20%;z-index:0;pointer-events:none;
background:radial-gradient(38% 34% at 18% 22%,var(--amb1),transparent 70%),
radial-gradient(34% 34% at 82% 18%,var(--amb2),transparent 70%),
radial-gradient(40% 40% at 62% 88%,var(--amb3),transparent 70%);
}
[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:transparent!important;}
.stApp{background:var(--bg);}

/* hero choreography */
.fx{animation:revealUp .9s var(--ease) var(--d,0s) both;}
.hero h1 .w{display:inline-block;overflow:hidden;vertical-align:bottom;padding:0 .02em .14em 0;margin-bottom:-.14em;}
.hero h1 .w>span{display:inline-block;animation:wordUp 1s var(--ease) both;}
.hero .art svg{animation:float 9s ease-in-out infinite;transform-origin:center;}
.art .orbit{transform-box:fill-box;transform-origin:center;animation:spin 140s linear infinite;}
.art .breathe{transform-box:fill-box;transform-origin:center;animation:breathe 9s ease-in-out infinite;}
.art .b2{animation-duration:7s;animation-delay:-2s;}
.art .pulse{transform-box:fill-box;transform-origin:center;animation:breathe 6s ease-in-out infinite;}
.art .dot{animation:dotDrift 11s ease-in-out infinite;}.art .d2{animation-delay:-4s;}.art .d3{animation-delay:-7s;}
.feat .ic svg{transition:transform .35s var(--ease);}
.feat:hover .ic svg{transform:translateY(-3px) rotate(-6deg);}
.brand .mark i{transition:transform .35s var(--ease);}
.brand:hover .mark i{transform:scale(1.35);}

/* result reveal: sections of the card appear in sequence, number counts up */
.rcard{animation:fadeIn .6s ease both;transition:box-shadow .3s ease,transform .3s var(--ease),background-color .45s ease,border-color .45s ease;}
.rcard:hover{box-shadow:0 2px 4px rgba(27,33,51,.05),0 16px 36px rgba(27,33,51,.09);transform:translateY(-2px);}
.rcard>*{animation:revealUp .75s var(--ease) both;animation-delay:calc(var(--k,0) * 90ms + 120ms);}
.rcard>*:nth-child(1){--k:0}.rcard>*:nth-child(2){--k:1}.rcard>*:nth-child(3){--k:2}.rcard>*:nth-child(4){--k:3}
.rcard>*:nth-child(5){--k:4}.rcard>*:nth-child(6){--k:5}.rcard>*:nth-child(7){--k:6}
.conf .big{--num:var(--v);counter-reset:n var(--num);animation:countup 1.5s var(--ease) .3s both;}
.conf .big::before{content:counter(n);}
.hair i{animation-delay:.55s;animation-duration:1.2s;}
.fill{animation-delay:calc(.6s + var(--i,0) * .13s);animation-duration:1.1s;}
.tag{transition:transform .2s ease;}.tag:hover{transform:translateY(-1px);}

/* images: fade + gentle scale; the heatmap column arrives a beat later */
[data-testid="stImage"] img{animation:imgIn .8s var(--ease) both;transition:transform .5s var(--ease),box-shadow .3s ease;}
[data-testid="stImage"]:hover img{transform:scale(1.015);}
[data-testid="stHorizontalBlock"]>[data-testid="stColumn"]:nth-child(2) [data-testid="stImage"] img,
[data-testid="stHorizontalBlock"]>[data-testid="column"]:nth-child(2) [data-testid="stImage"] img{animation-duration:1.2s;animation-delay:.3s;}
[data-testid="stFileUploaderFile"]{animation:revealUp .5s var(--ease) both;}

/* upload area */
[data-testid="stFileUploaderDropzone"]{transition:border-color .3s ease,background-color .3s ease,transform .3s var(--ease),box-shadow .3s ease;}
[data-testid="stFileUploaderDropzone"]:hover{transform:translateY(-2px);box-shadow:var(--shadow);}
[data-testid="stFileUploaderDropzone"] svg{animation:floatSm 5s ease-in-out infinite;}
[data-testid="stFileUploaderDropzone"].drag-active{border-color:var(--accent);border-style:solid;background:var(--lav);transform:scale(1.012);box-shadow:0 0 0 6px color-mix(in srgb,var(--accent) 16%,transparent);}
.empty{animation:fadeIn .8s ease both;}
.empty .ic{animation:float 6s ease-in-out infinite;}
.empty .tips span{transition:color .2s ease;}.empty .tips span:hover{color:var(--ink);}

/* analysis progress: smooth fill with a slow shimmer */
[data-testid="stProgress"] [role="progressbar"]{background:var(--line2)!important;border-radius:999px;height:6px!important;overflow:hidden;}
[data-testid="stProgress"] [role="progressbar"]>div{background:linear-gradient(90deg,var(--accent),#B7ACF0,var(--accent))!important;
background-size:200% 100%;animation:shimmer 2.4s linear infinite;transition:width .6s var(--ease)!important;border-radius:999px;}

/* buttons, tabs, cards, popovers */
.stButton>button,[data-testid="stDownloadButton"] button{transition:transform .2s var(--ease),box-shadow .2s ease,opacity .2s ease;}
.stButton>button:hover,[data-testid="stDownloadButton"] button:hover{box-shadow:0 8px 20px rgba(27,33,51,.18);}
.stButton>button:active,[data-testid="stDownloadButton"] button:active{transform:translateY(0) scale(.97);box-shadow:none;}
button:focus-visible,[role="tab"]:focus-visible,summary:focus-visible{outline:2px solid var(--accent)!important;outline-offset:3px;}
.stTabs [data-baseweb="tab"]{position:relative;transition:color .25s ease;}
.stTabs [data-baseweb="tab"]:hover{color:var(--ink)!important;}
.stTabs [data-baseweb="tab"]::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--accent);
opacity:.55;transform:scaleX(0);transform-origin:left;transition:transform .35s var(--ease);}
.stTabs [data-baseweb="tab"]:hover::after{transform:scaleX(1);}
.stTabs [aria-selected="true"]::after{display:none;}
.stTabs [data-baseweb="tab-highlight"]{transition:left .4s var(--ease),width .4s var(--ease),transform .4s var(--ease)!important;}
.stTabs [data-baseweb="tab-panel"]{animation:fadeIn .5s ease both;}
.ccard,.kv,.tbl-wrap,.stat{transition:border-color .25s ease,transform .3s var(--ease),box-shadow .3s ease,background-color .45s ease;}
.ccard:hover{box-shadow:var(--shadow);}
.tip,.abox{transition:background-color .3s ease;}
.abox b{transition:transform .35s var(--ease);}.abox:hover b{transform:translateY(-3px);}
.tbl td{transition:background-color .2s ease;}
[data-testid="stPopoverBody"],[data-baseweb="popover"]>div,[data-baseweb="menu"]{animation:pop .22s var(--ease) both;}
[data-testid="stExpander"] details[open]>div:last-child{animation:revealUp .4s var(--ease) both;}
[data-testid="stExpander"]{transition:border-color .25s ease,box-shadow .3s ease,background-color .45s ease;}
[data-testid="stExpander"]:hover{border-color:var(--accent)!important;}
.note{animation:revealUp .6s var(--ease) both;}
.stElementContainer:has(iframe[height="0"]){position:absolute;width:0;height:0;overflow:hidden;margin:0;}

/* fast reruns: no replayed entrance animations */
.fx,.hero h1 .w>span,.disc,.feat,.rcard,.rcard>*,.note,.stat,.ccard,.empty,.hero,.stTabs [data-baseweb="tab-panel"],[data-testid="stImage"] img{animation:none!important;}
.hero .art svg,.art .orbit,.art .breathe,.art .pulse,.art .dot,.empty .ic,[data-testid="stFileUploaderDropzone"] svg{animation:none!important;}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important;}
.stApp::before{display:none;}}
'''

DRAG_JS = """
<script>
(function () {
  var d = window.parent.document;
  if (d.__lensDrag) return;
  d.__lensDrag = true;
  var timer;
  function off() { d.querySelectorAll('.drag-active').forEach(function (z) { z.classList.remove('drag-active'); }); }
  d.addEventListener('dragover', function (e) {
    if (!e.dataTransfer || Array.prototype.indexOf.call(e.dataTransfer.types || [], 'Files') < 0) return;
    d.querySelectorAll('[data-testid="stFileUploaderDropzone"]').forEach(function (z) { z.classList.add('drag-active'); });
    clearTimeout(timer); timer = setTimeout(off, 160);
  });
  d.addEventListener('drop', off);
})();
</script>
"""


def enhance_js():
    """Tiny optional script: highlights the upload area while a file is dragged over the page.
    Everything else in the motion system is pure CSS. If the iframe cannot run, nothing breaks."""
    try:
        import streamlit.components.v1 as components
        components.html(DRAG_JS, height=0)
    except Exception:  # noqa: BLE001
        pass


def inject_css(theme="light"):
    vars_ = DARK if theme == "dark" else LIGHT
    st.markdown(f"<style>{FONT_IMPORT}:root{{{vars_}}}{CSS}{MOTION}</style>", unsafe_allow_html=True)


def _md(html_str):
    st.markdown(html_str, unsafe_allow_html=True)


def esc(x):
    return _h.escape(str(x))


def _rtl(rtl):
    return " rtl" if rtl else ""


# ----------------------------------------------------------------- components
def brand(sub):
    _md(f"<div class='brand'><div class='mark'><i></i></div><div><b>Lesion Lens</b><span>{esc(sub)}</span></div></div>")


HERO_ART = """<svg viewBox='0 0 320 320' width='100%' style='max-width:360px' role='img' aria-label='Abstract dermoscopy illustration'>
<circle cx='160' cy='160' r='150' style='fill:var(--surface2);stroke:var(--line)' stroke-width='1.2'/>
<circle class='orbit' cx='160' cy='160' r='122' fill='none' style='stroke:var(--ink)' stroke-opacity='.28' stroke-dasharray='1.5 6' stroke-linecap='round'/>
<circle cx='160' cy='160' r='96' fill='none' style='stroke:var(--line)' stroke-width='1'/>
<path class='breathe' d='M160 98C196 90 226 120 219 158C213 193 183 216 148 210C112 204 97 169 107 138C115 113 137 102 160 98Z' style='fill:var(--peach);stroke:var(--peach-ink)' stroke-opacity='.55' stroke-width='1.2'/>
<path class='breathe b2' d='M162 124C184 121 200 140 196 160C192 181 172 192 153 187C134 182 127 163 133 147C138 134 148 126 162 124Z' style='fill:var(--lav);stroke:var(--accent)' stroke-width='1.2'/>
<circle class='pulse' cx='163' cy='158' r='15' style='fill:var(--accent)' fill-opacity='.55'/>
<g style='stroke:var(--ink)' stroke-opacity='.5' stroke-width='1.2' stroke-linecap='round'>
<path d='M160 6v16M160 298v16M6 160h16M298 160h16'/></g>
<circle class='dot d1' cx='238' cy='96' r='5' style='fill:var(--sage)' stroke-width='0'/><circle class='dot d2' cx='86' cy='222' r='4' style='fill:var(--sage)'/>
<circle class='dot d3' cx='244' cy='236' r='3' style='fill:var(--lav)'/>
<path d='M222 236l30 24' style='stroke:var(--ink)' stroke-opacity='.4' stroke-width='1.2'/>
<text x='312' y='276' text-anchor='end' font-size='9' letter-spacing='1.5' style='fill:var(--muted);font-family:Inter,sans-serif'>GRAD-CAM</text>
</svg>"""


def _words(text, start=0.18, step=0.075):
    """Split a headline into masked words so each can slide up in sequence."""
    return " ".join(f"<span class='w'><span style='animation-delay:{start + i * step:.2f}s'>{esc(w)}</span></span>"
                    for i, w in enumerate(text.split(" ")))


def hero(S, rtl=False):
    feats = "".join(
        f"<div class='feat fx' style='--d:{0.85 + k * 0.13:.2f}s'><div class='ic'>{icon(i, 22)}</div>"
        f"<div><b>{esc(t)}</b><span>{esc(d)}</span></div></div>" for k, (i, t, d) in enumerate(S["feats"]))
    _md(f"<div class='hero{_rtl(rtl)}'><div><div class='eyebrow fx' style='--d:.05s'>{esc(S['eyebrow'])}</div>"
        f"<h1 aria-label='{esc(S['headline'])}'>{_words(S['headline'])}</h1>"
        f"<p class='lead fx' style='--d:.7s'>{esc(S['sub'])}</p></div><div class='art fx' style='--d:.25s'>{HERO_ART}</div></div>"
        f"<div class='feats{_rtl(rtl)}'>{feats}</div>")


def disclaimer(S, text, rtl=False):
    text = esc(text).replace("**", "")
    _md(f"<div class='disc fx{_rtl(rtl)}' style='--d:1.2s'>{icon('shield', 20)}<div><b>{esc(S['disclaimer_title'])}.</b> {text}</div></div>")


def section(eyebrow, title, sub="", rtl=False):
    s = f"<p>{esc(sub)}</p>" if sub else ""
    _md(f"<div class='sec{_rtl(rtl)}'><div class='eyebrow'>{esc(eyebrow)}</div><h2>{esc(title)}</h2>{s}</div>")


def subsection(text, rtl=False):
    _md(f"<div class='subsec{_rtl(rtl)}'>{esc(text)}</div>")


def notice(text, kind="info", icon=None, rtl=False):   # `icon` kept for API compatibility
    _md(f"<div class='note {kind}{_rtl(rtl)}'>{esc(text).replace('**', '')}</div>")


def stat_cards(items):
    """items: (label, value, css-class)"""
    cards = "".join(f"<div class='stat'><div class='v {c}'>{esc(v)}</div><div class='k'>{esc(k)}</div></div>" for k, v, c in items)
    _md(f"<div class='stats'>{cards}</div>")


def empty_state(title, text, tips):
    t = "".join(f"<span>{esc(x)}</span>" for x in tips)
    _md(f"<div class='empty'><div class='ic'>{icon('upload', 24)}</div><h3>{esc(title)}</h3><p>{esc(text)}</p><div class='tips'>{t}</div></div>")


def risk_pill(risk):
    cls = RISK_CLASS.get(risk, "unk")
    return f"<span class='tag {cls}'><i></i>{esc(risk)}</span>"


def result_card(label, class_name, conf, risk, desc, uncertainty, items, eyebrow, rtl=False):
    """items: list of (class, prob) for the probability bars. `label` kept for API compatibility."""
    bars = "".join(
        f"<div class='bar' style='--i:{i}'><div class='row'><span>{esc(c)}</span><span>{p:.1%}</span></div>"
        f"<div class='track'><div class='fill{' top' if i == 0 else ''}' style='width:{max(p, 0.006) * 100:.1f}%'></div></div></div>"
        for i, (c, p) in enumerate(items))
    _md(f"<div class='rcard{_rtl(rtl)}'><div class='eyebrow'>{esc(eyebrow)}</div><div class='cname'>{esc(class_name)}</div>"
        f"<div class='conf'><span class='big' style='--v:{conf * 100:.0f}' role='img' aria-label='{conf * 100:.0f} percent'></span><span class='u'>%</span><span class='l'>confidence</span></div>"
        f"<div class='hair'><i style='width:{conf * 100:.1f}%'></i></div>"
        f"<div class='tags'>{risk_pill(risk)}<span class='tag lav'>Uncertainty {uncertainty:.2f}</span></div>"
        f"<div class='desc'>{esc(desc)}</div><div class='bars'>{bars}</div></div>")


def class_cards(entries):
    """entries: (name, risk, about)"""
    cards = "".join(f"<div class='ccard'><div class='n'><span>{i:02d}</span>{risk_pill(r)}</div><h4>{esc(n)}</h4><p>{esc(a)}</p></div>"
                    for i, (n, r, a) in enumerate(entries, 1))
    _md(f"<div class='grid'>{cards}</div>")


def abcde(items):
    boxes = "".join(f"<div class='abox'><b>{esc(l)}</b><div>{esc(t)}</div><span>{esc(d)}</span></div>" for l, t, d in items)
    _md(f"<div class='abcde'>{boxes}</div>")


def tips(items):
    body = "".join(f"<div class='tip'><b>{i:02d}</b><div>{esc(t)}</div></div>" for i, t in enumerate(items, 1))
    _md(f"<div class='tipgrid'>{body}</div>")


def key_values(pairs):
    body = "".join(f"<div><span>{esc(k)}</span><span>{esc(v)}</span></div>" for k, v in pairs)
    _md(f"<div class='kv'>{body}</div>")


def table(df):
    """Theme-aware HTML table (st.dataframe ignores the custom theme)."""
    head = "".join(f"<th>{esc(c)}</th>" for c in df.columns)
    rows = []
    for _, row in df.iterrows():
        cells = []
        for c, v in row.items():
            if c in ("risk_group", "risk group"):
                cells.append(f"<td>{risk_pill(v)}</td>")
            elif isinstance(v, float):
                cells.append(f"<td>{v:.4g}</td>")
            else:
                cells.append(f"<td>{esc(v)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    _md(f"<div class='tbl-wrap'><table class='tbl'><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>")


def bars(rows):
    """rows: (label, fraction 0-1, display text) -> themed horizontal bars."""
    body = "".join(
        f"<div class='bar' style='--i:{i}'><div class='row'><span>{esc(l)}</span><span>{esc(t)}</span></div>"
        f"<div class='track'><div class='fill{' top' if i == 0 else ''}' style='width:{max(f, 0.01) * 100:.1f}%'></div></div></div>"
        for i, (l, f, t) in enumerate(rows))
    _md(f"<div class='rcard'><div class='bars' style='margin-top:0;border-top:0;padding-top:0'>{body}</div></div>")


def footer(text):
    _md(f"<div class='footer'><b>Lesion Lens</b><br>{esc(text)}</div>")