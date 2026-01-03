import streamlit as st
import base64
import os
import streamlit.components.v1 as components

# --- Configuration de la page ---
st.set_page_config(page_title="Electroplating Simulation Platform", layout="wide")

# --- Styles CSS personnalisés (Look Académique/Latex) ---
custom_css = """
<style>
/* Masquer éléments Streamlit inutiles */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}

/* Style des onglets */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
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

/* Bouton retour en haut */
.back-to-top {
    position: fixed;
    bottom: 50%;
    right: 30px;
    z-index: 9999;
    background-color: #004b87;
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
}
.back-to-top:hover {
    background-color: #003366;
    transform: scale(1.1);
}

/* Style scientifique (Latex-like) */
.main {
    font-family: 'serif';
}
h1, h2, h3 {
    color: #004b87;
}
</style>

<!-- Bouton retour en haut -->
<a href="#top" class="back-to-top" title="Retour en haut">&#8679;</a>
<div id="top"></div>
"
st.markdown(custom_css, unsafe_allow_html=True)

# --- Chemins ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT_DIR, "docs")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")

# --- Dictionnaire de Traduction UI ---
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
        "version_info": "**Version 1.1.0**\nJan 2026\n*EQU*\n\n**Nouveautés :**\n- Visualisation 3D Interactive (PyVista)\n- Intégration Firedrake\n\n**Précédemment (1.0.1) :**\n- Support bilingue FR/EN",
        "tabs_plating": ["Physique", "Code", "Visualisation 3D", "Exemples GIF", "Exemples PNG"],
        "card_plating_title": "### Électrodéposition",
        "card_plating_text": "Simulation de dépôt électrolytique et distribution de courant secondaire.",
        "gif_coming_soon": "Visualisation dynamique (Gifs) - À venir",
        "no_gif": "Aucune animation GIF disponible pour le moment.",
        "png_thickness": "Cartes d'épaisseur",
        "3d_interactive": "Visualisation 3D Interactive",
        "3d_desc": "Visualisation interactive de l'épaisseur de dépôt (extrudée x1000). Utilisez la souris pour tourner, zoomer et explorer la géométrie.",
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
        "version_info": "**Version 1.1.0**\nJan 2026\n*EQU*\n\n**New Features:**\n- Interactive 3D Visualization (PyVista)\n- Firedrake Integration\n\n**Previously (1.0.1):**\n- Bilingual support FR/EN",
        "tabs_plating": ["Physics", "Code", "3D Visualization", "GIF Examples", "PNG Examples"],
        "card_plating_title": "### Electroplating",
        "card_plating_text": "Simulation of electrolytic deposition and secondary current distribution.",
        "gif_coming_soon": "Dynamic Visualization (Gifs) - Coming Soon",
        "no_gif": "No GIF animation available at the moment.",
        "png_thickness": "Thickness Maps",
        "3d_interactive": "Interactive 3D Visualization",
        "3d_desc": "Interactive visualization of deposition thickness (extruded x1000). Use mouse to rotate, zoom, and explore geometry.",
        "3d_not_found": "3D visualization file not found."
    }
}

# --- Fonctions Utilitaires ---
def get_language():
    if 'lang' not in st.session_state:
        st.session_state.lang = 'fr'
    return st.session_state.lang

def t(key):
    lang = get_language()
    return TRANSLATIONS[lang].get(key, key)

def load_file_content(relative_path):
    lang = get_language()
    full_path = os.path.join(DOC_PATH, lang, relative_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f: return f.read()
    except Exception: return f"Document not found / Document non trouvé : {os.path.join(lang, relative_path)}"

def display_smart_markdown(content):
    if "```python" in content:
        parts = content.split("```python")
        for i, part in enumerate(parts):
            if i > 0:
                if "```" in part:
                    code, text = part.split("```", 1)
                    st.code(code.strip(), language='python')
                    if text.strip(): st.markdown(text)
                else:
                    st.code(part.strip(), language='python')
            elif part.strip():
                st.markdown(part)
    elif "```cpp" in content:
        parts = content.split("```cpp")
        for i, part in enumerate(parts):
            if i > 0:
                if "```" in part:
                    code, text = part.split("```", 1)
                    st.code(code.strip(), language='cpp')
                    if text.strip(): st.markdown(text)
                else:
                    st.code(part.strip(), language='cpp')
            elif part.strip():
                st.markdown(part)
    else:
        st.markdown(content)

def search_images(base_path, extensions=['.png', '.jpg', '.jpeg']):
    images = []
    if not os.path.exists(base_path): return images
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                images.append(os.path.join(root, file))
    return images

# --- Barre Latérale ---

# Sélecteur de langue
col_l1, col_l2 = st.sidebar.columns(2)
lang_selection = st.sidebar.radio(
    "Language",
    ["🇫🇷 FR", "🇬🇧 EN"],
    horizontal=True,
    label_visibility="collapsed"
)

if "FR" in lang_selection:
    st.session_state.lang = "fr"
else:
    st.session_state.lang = "en"

st.sidebar.title(t("sidebar_title"))

# Callbacks
def on_change_gen():
    st.session_state.nav_plating = None

def on_change_plating():
    st.session_state.nav_gen = None

# Init states
if 'nav_gen' not in st.session_state: st.session_state.nav_gen = t("gen_home")
if 'nav_plating' not in st.session_state: st.session_state.nav_plating = None

# Navigation
st.sidebar.subheader(t("gen_header"))
main_nav = st.sidebar.radio(
    "Nav Gen", 
    [t("gen_home")],
    key="nav_gen", 
    on_change=on_change_gen,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.subheader(t("plating_header"))
plating_nav = st.sidebar.radio(
    "Nav Plating", 
    t("plating_modules"),
    key="nav_plating",
    index=None,
    on_change=on_change_plating,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(t("version_info"))

# --- Mapping Modules (FR/EN correspondence) ---
modules_pl = TRANSLATIONS["fr"]["plating_modules"]
modules_pl_en = TRANSLATIONS["en"]["plating_modules"]

# --- Contenu Principal ---

# ACCUEIL
if main_nav == t("gen_home") and plating_nav is None:
    st.title(t("title"))
    st.markdown(load_file_content("accueil/accueil.md"))
    
    st.success(t("card_plating_title"))
    res_img = os.path.join(ASSETS_PATH, "plating/results/plating_result_refined.png")
    if os.path.exists(res_img):
        st.image(res_img, use_container_width=True)
    elif os.path.exists(os.path.join(ASSETS_PATH, "plating/results/plating_result_example.png")):
         st.image(os.path.join(ASSETS_PATH, "plating/results/plating_result_example.png"), use_container_width=True)
    
    st.write(t("card_plating_text"))

# PLATING PAGES
elif plating_nav:
    st.title(f"Plating : {plating_nav}")
    
    try:
        idx = modules_pl.index(plating_nav)
    except ValueError:
        idx = modules_pl_en.index(plating_nav)

    # 0: Intro
    if idx == 0:
        display_smart_markdown(load_file_content("intro/intro_plating.md"))
    
    # 1: Python (Firedrake & PyVista) - PREVIOUSLY "Antigravity"
    elif idx == 1:
        tabs = st.tabs(t("tabs_plating"))
        
        # Tab 1: Physics
        with tabs[0]:
            display_smart_markdown(load_file_content("physics/plating_antigravity.md")
            
        # Tab 2: Code
        with tabs[1]:
            display_smart_markdown(load_file_content("code/plating_antigravity_code.md")
            
        # Tab 3: 3D Visualization (NEW)
        with tabs[2]:
            st.subheader(t("3d_interactive"))
            st.info(t("3d_desc"))
            
            html_file_path = os.path.join(ASSETS_PATH, "plating/results/3d_view.html")
            if os.path.exists(html_file_path):
                with open(html_file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                components.html(html_content, height=600, scrolling=False)
            else:
                st.warning(t("3d_not_found"))

        # Tab 4: GIF
        with tabs[3]:
             st.info(t("gif_coming_soon"))
             gifs = search_images(os.path.join(ASSETS_PATH, "plating/results"), ['.gif'])
             if gifs:
                for gif in gifs:
                    st.image(gif, caption=os.path.basename(gif), use_container_width=True)
             else:
                st.warning(t("no_gif"))
        
        # Tab 5: PNG
        with tabs[4]:
            st.subheader(t("png_thickness"))
            # Prioritize the refined result if available
            res_img_refined = os.path.join(ASSETS_PATH, "plating/results/plating_result_refined.png")
            res_img_example = os.path.join(ASSETS_PATH, "plating/results/plating_result_example.png")
            
            if os.path.exists(res_img_refined):
                st.image(res_img_refined, caption="Thickness Distribution (Refined Mesh)", use_container_width=True)
            elif os.path.exists(res_img_example):
                st.image(res_img_example, caption="Thickness Distribution (Example)", use_container_width=True)

    # 2: Conclusion
    elif idx == 2:
        display_smart_markdown(load_file_content("conclusion/plating_conclusion.md"))
    # 3: Equations
    elif idx == 3:
        display_smart_markdown(load_file_content("equations/plating_equations.md"))
    # 4: Lexique
    elif idx == 4:
        display_smart_markdown(load_file_content("lexique/plating_lexique.md")
    # 5: Histoire
    elif idx == 5:
        display_smart_markdown(load_file_content("histoire/plating_histoire.md"))
    # 6: Bibliographie
    elif idx == 6:
        display_smart_markdown(load_file_content("biblio/plating_biblio.md"))
