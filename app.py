import streamlit as st
import base64
import os
import streamlit.components.v1 as components

# --- Configuration de la page ---
st.set_page_config(page_title="Electroplating Simulation Platform", layout="wide")

# --- Styles CSS personnalisés ---
custom_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}

.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 10px 24px;
    background-color: #f0f2f6;
    border-radius: 8px 8px 0 0;
    font-weight: 600;
    font-size: 16px;
}
.stTabs [aria-selected="true"] {
    background-color: #004b87;
    color: white;
}

.nav-button {
    position: fixed;
    right: 30px;
    z-index: 9999;
    background-color: #004b87;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    transition: all 0.2s ease;
}
.nav-button:hover {
    background-color: #003366;
    transform: scale(1.1);
}
.back-to-top { bottom: calc(50% + 30px); }
.scroll-to-bottom { bottom: calc(50% - 30px); }

.main { font-family: 'serif'; }
h1, h2, h3 { color: #004b87; }
</style>

<a href="#top" class="nav-button back-to-top" title="Haut"><svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M12 4l-8 8h5v8h6v-8h5z"/></svg></a>
<a href="#bottom" class="nav-button scroll-to-bottom" title="Bas"><svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M12 20l8-8h-5V4h-6v8H4z"/></svg></a>
<div id="top"></div>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Chemins ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT_DIR, "docs")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")

# --- Traductions ---
TRANSLATIONS = {
    "fr": {
        "title": "Plateforme de Simulation d'Électrodéposition",
        "sidebar_title": "Simulation",
        "gen_header": "Général",
        "gen_home": "Accueil",
        "plating_header": "Électrodéposition",
        "plating_modules": [
            "Introduction", "Python (Firedrake & PyVista)", "Conclusion", 
            "Équations clés", "Lexique", "Un peu d'histoire", "Bibliographie"
        ],
        "version_info": "**Version 1.1.0**\nJan 2026\n*EQU*",
        "tabs_plating": ["Physique", "Code", "Visualisation 3D", "Exemples GIF", "Exemples PNG"],
        "card_plating_title": "### Électrodéposition",
        "card_plating_text": "Simulation de dépôt électrolytique et distribution de courant secondaire.",
        "gif_coming_soon": "Visualisation dynamique (Gifs) - À venir",
        "no_gif": "Aucune animation GIF disponible.",
        "png_thickness": "Cartes d'épaisseur",
        "3d_interactive": "Visualisation 3D Interactive",
        "3d_desc": "Visualisation interactive de l'épaisseur de dépôt (extrudée x1000).",
        "3d_not_found": "Fichier de visualisation 3D introuvable."
    },
    "en": {
        "title": "Electroplating Simulation Platform",
        "sidebar_title": "Simulation",
        "gen_header": "General",
        "gen_home": "Home",
        "plating_header": "Electroplating",
        "plating_modules": [
            "Introduction", "Python (Firedrake & PyVista)", "Conclusion", 
            "Key Equations", "Glossary", "A Bit of History", "Bibliography"
        ],
        "version_info": "**Version 1.1.0**\nJan 2026\n*EQU*",
        "tabs_plating": ["Physics", "Code", "3D Visualization", "GIF Examples", "PNG Examples"],
        "card_plating_title": "### Electroplating",
        "card_plating_text": "Simulation of electrolytic deposition and secondary current distribution.",
        "gif_coming_soon": "Dynamic Visualization (Gifs) - Coming Soon",
        "no_gif": "No GIF animation available.",
        "png_thickness": "Thickness Maps",
        "3d_interactive": "Interactive 3D Visualization",
        "3d_desc": "Interactive visualization of deposition thickness (extruded x1000).",
        "3d_not_found": "3D visualization file not found."
    }
}

def get_language():
    if 'lang' not in st.session_state: st.session_state.lang = 'fr'
    return st.session_state.lang

def t(key): return TRANSLATIONS[get_language()].get(key, key)

def load_file_content(relative_path):
    lang = get_language()
    full_path = os.path.join(DOC_PATH, lang, relative_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f: return f.read()
    except Exception: return f"File not found: {relative_path}"

def search_images(base_path, extensions=['.png', '.jpg', '.jpeg']):
    images = []
    if not os.path.exists(base_path): return images
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                images.append(os.path.join(root, file))
    return images

# --- Sidebar ---
col_l1, col_l2 = st.sidebar.columns(2)
old_lang = st.session_state.get('lang', 'fr')
lang_selection = st.sidebar.radio("Lang", ["🇫🇷 FR", "🇬🇧 EN"], horizontal=True, label_visibility="collapsed", index=0 if old_lang == "fr" else 1)
new_lang = "fr" if "FR" in lang_selection else "en"

# Modules definitions
modules_pl = TRANSLATIONS["fr"]["plating_modules"]
modules_pl_en = TRANSLATIONS["en"]["plating_modules"]

if new_lang != old_lang:
    modules_old = TRANSLATIONS[old_lang]["plating_modules"]
    modules_new = TRANSLATIONS[new_lang]["plating_modules"]
    
    current = st.session_state.get('nav_plating')
    if current and current in modules_old:
        idx = modules_old.index(current)
        st.session_state.nav_plating = modules_new[idx]
        st.session_state.nav_gen = None
    
    st.session_state.lang = new_lang
    st.rerun()

st.session_state.lang = new_lang
st.sidebar.title(t("sidebar_title"))

# Callbacks
def on_change_gen():
    st.session_state.nav_plating = None

def on_change_plating():
    st.session_state.nav_gen = None

# Init states
if 'nav_gen' not in st.session_state and 'nav_plating' not in st.session_state:
    st.session_state.nav_gen = t("gen_home")

# --- Navigation GEN ---
st.sidebar.subheader(t("gen_header"))
gen_options = [t("gen_home")]
gen_args = {
    "label": "Nav Gen",
    "options": gen_options,
    "key": "nav_gen",
    "on_change": on_change_gen,
    "label_visibility": "collapsed"
}
if st.session_state.get("nav_plating") is not None:
    gen_args["index"] = None
elif st.session_state.get("nav_gen") in gen_options:
    gen_args["index"] = gen_options.index(st.session_state.nav_gen)

main_nav = st.sidebar.radio(**gen_args)

st.sidebar.markdown("---")

# --- Navigation Plating ---
st.sidebar.subheader(t("plating_header"))
current_modules = modules_pl if new_lang == "fr" else modules_pl_en

plating_args = {
    "label": "Nav Plating",
    "options": current_modules,
    "key": "nav_plating",
    "on_change": on_change_plating,
    "label_visibility": "collapsed"
}
if st.session_state.get("nav_gen") is not None:
    plating_args["index"] = None
elif st.session_state.get("nav_plating") in current_modules:
    plating_args["index"] = current_modules.index(st.session_state.nav_plating)

plating_nav = st.sidebar.radio(**plating_args)

st.sidebar.markdown("---")
st.sidebar.markdown(t("version_info"))

# --- Content ---
if main_nav == t("gen_home") or (plating_nav is None and main_nav is None):
    st.title(t("title"))
    st.markdown(load_file_content("accueil/accueil.md"))
    st.success(t("card_plating_title"))
    st.write(t("card_plating_text"))

elif plating_nav:
    st.title(f"Plating : {plating_nav}")
    try:
        idx = current_modules.index(plating_nav)
        files = [
            "intro/intro_plating.md",
            ("physics/plating_antigravity.md", "code/plating_antigravity_code.md"), # Tabbed with 3D
            "conclusion/plating_conclusion.md", "equations/plating_equations.md",
            "lexique/plating_lexique.md", "histoire/plating_histoire.md", "biblio/plating_biblio.md"
        ]
        
        target = files[idx]
        
        if isinstance(target, tuple): # Tabs + 3D
            tabs = st.tabs(t("tabs_plating"))
            with tabs[0]: st.markdown(load_file_content(target[0]))
            with tabs[1]: st.markdown(load_file_content(target[1]))
            with tabs[2]: # 3D
                st.subheader(t("3d_interactive"))
                st.info(t("3d_desc"))
                html_path = os.path.join(ASSETS_PATH, "plating/results/3d_view.html")
                if os.path.exists(html_path):
                    with open(html_path,'r',encoding='utf-8') as f:
                        components.html(f.read(), height=600, scrolling=False)
                else:
                    st.warning(t("3d_not_found"))
            with tabs[3]: st.info(t("gif_coming_soon"))
            with tabs[4]: 
                st.subheader(t("png_thickness"))
                res_img = os.path.join(ASSETS_PATH, "plating/results/plating_result_refined.png")
                if os.path.exists(res_img): st.image(res_img, use_container_width=True)
        else:
            st.markdown(load_file_content(target))
            
    except Exception as e:
        st.error(f"Navigation Error: {e}")

st.markdown("<div id=\"bottom\"></div", unsafe_allow_html=True)
