import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Electroplating Simulation Platform", layout="wide")

# --- Chemins ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT_DIR, "docs")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")
DATA_PATH = os.path.join(ROOT_DIR, "data")
CSS_PATH = os.path.join(ASSETS_PATH, "style.css")
STUDY_RESULTS_PATH = os.path.join(ASSETS_PATH, "plating/study_results")

# --- Chargement CSS externe ---
if os.path.exists(CSS_PATH):
    with open(CSS_PATH, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- Boutons Navigation HTML ---
nav_buttons_html = """
<a href="#top" class="nav-button back-to-top" title="Retour en haut / Back to top">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12 4l-8 8h5v8h6v-8h5z"/>
    </svg>
</a>
<a href="#bottom" class="nav-button scroll-to-bottom" title="Aller en bas / Go to bottom">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12 20l8-8h-5V4h-6v8H4z"/>
    </svg>
</a>
<div id="top"></div>
"""
st.markdown(nav_buttons_html, unsafe_allow_html=True)

# --- Traductions ---
TRANSLATIONS = {
    "fr": {
        "title": "Plateforme de Simulation d'Électrodéposition",
        "sidebar_title": "Simulation",
        "gen_header": "Général",
        "gen_pages": ["Accueil"],
        "plating_header": "Électrodéposition",
        "plating_pages": [
            "Introduction", "Python (Firedrake & PyVista)", "Conclusion",
            "Équations clés", "Lexique", "Un peu d'histoire", "Bibliographie"
        ],
        "version_info": """**Version 1.3.0**
Jan 2026 - *EQU*

**Nouveautés :**
- Bibliographie enrichie (liens gratuits)
- Physique : équations détaillées
- Code : format Jupyter (12 blocs)
- Comparaison côte à côte (81 sims)""",
        "tabs_plating": ["Physique", "Code", "Comparaison PNG", "Comparaison 3D"],
        "card_plating_title": "### Électrodéposition",
        "card_plating_text": "Simulation de dépôt électrolytique et distribution de courant secondaire.",
        "sim_1": "Simulation 1",
        "sim_2": "Simulation 2",
        "btn_compare": "COMPARER",
        "combo_unavailable": "Combinaison non disponible",
        "png_viewer": "Comparaison des résultats (PNG)",
        "3d_viewer": "Comparaison 3D Interactive",
        "3d_desc": "Visualisation interactive de l'épaisseur de dépôt (extrudée x1000).",
        "3d_not_found": "Fichier de visualisation 3D introuvable.",
        "lbl_ddc": "DDC (A/dm²)",
        "lbl_sigma": "σ (S/m)",
        "lbl_j0": "j₀ (A/m²)",
        "lbl_alpha": "α",
        "thickness_map": "Carte d'épaisseur",
        "current_density": "Densité de courant",
        "view_3d_iso": "Vue 3D isométrique"
    },
    "en": {
        "title": "Electroplating Simulation Platform",
        "sidebar_title": "Simulation",
        "gen_header": "General",
        "gen_pages": ["Home"],
        "plating_header": "Electroplating",
        "plating_pages": [
            "Introduction", "Python (Firedrake & PyVista)", "Conclusion",
            "Key Equations", "Glossary", "A Bit of History", "Bibliography"
        ],
        "version_info": """**Version 1.3.0**
Jan 2026 - *EQU*

**What's New:**
- Enhanced bibliography (free links)
- Physics: detailed equations
- Code: Jupyter-style (12 blocks)
- Side-by-side comparison (81 sims)""",
        "tabs_plating": ["Physics", "Code", "PNG Comparison", "3D Comparison"],
        "card_plating_title": "### Electroplating",
        "card_plating_text": "Simulation of electrolytic deposition and secondary current distribution.",
        "sim_1": "Simulation 1",
        "sim_2": "Simulation 2",
        "btn_compare": "COMPARE",
        "combo_unavailable": "Combination not available",
        "png_viewer": "Results Comparison (PNG)",
        "3d_viewer": "Interactive 3D Comparison",
        "3d_desc": "Interactive visualization of deposition thickness (extruded x1000).",
        "3d_not_found": "3D visualization file not found.",
        "lbl_ddc": "DDC (A/dm²)",
        "lbl_sigma": "σ (S/m)",
        "lbl_j0": "j₀ (A/m²)",
        "lbl_alpha": "α",
        "thickness_map": "Thickness Map",
        "current_density": "Current Density",
        "view_3d_iso": "3D Isometric View"
    }
}

# --- Fonctions de Langue ---
def get_language():
    if 'lang' not in st.session_state:
        st.session_state.lang = 'fr'
    return st.session_state.lang

def t(key):
    """Retourne la traduction pour la clé donnée."""
    lang = get_language()
    return TRANSLATIONS[lang].get(key, key)

def load_file_content(relative_path):
    lang = get_language()
    full_path = os.path.join(DOC_PATH, lang, relative_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return f"File not found: {relative_path}"

def display_smart_markdown(content):
    st.markdown(content)

def search_images(base_path, extensions=['.png', '.jpg', '.jpeg']):
    images = []
    if not os.path.exists(base_path):
        return images
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                images.append(os.path.join(root, file))
    return images

@st.cache_data(ttl=600)
def load_ed_mapping():
    """Charge le mapping des simulations ED depuis le CSV."""
    try:
        csv_path = os.path.join(DATA_PATH, 'ED_mapping.csv')
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8', decimal=',')
        return df
    except Exception as e:
        st.error(f"Erreur chargement CSV: {e}")
        return pd.DataFrame()

def get_simulation_by_params(df, ddc, sigma, j0, alpha):
    """Trouve une simulation par ses paramètres (première correspondance)."""
    mask = (
        (df['DDC_target_A_dm2'] == ddc) &
        (df['sigma_S_m'] == sigma) &
        (df['j0_A_m2'] == j0) &
        (df['alpha'] == alpha)
    )
    matches = df[mask]
    if len(matches) > 0:
        return matches.iloc[0]
    return None

def get_simulation_files(sim_row):
    """Retourne les chemins des fichiers pour une simulation."""
    if sim_row is None:
        return None
    sim_id = f"{int(sim_row['id']):03d}"
    return {
        'thickness': os.path.join(STUDY_RESULTS_PATH, f"{sim_id}_ED_thickness_map.png"),
        'current': os.path.join(STUDY_RESULTS_PATH, f"{sim_id}_ED_current_density.png"),
        '3d_iso': os.path.join(STUDY_RESULTS_PATH, f"{sim_id}_ED_3D_iso.png"),
        '3d_html': os.path.join(STUDY_RESULTS_PATH, f"{sim_id}_ED_3D_interactive.html"),
        'cv': sim_row['CV_percent'],
        'thickness_avg': sim_row['thickness_avg_um'],
    }

# --- Callbacks pour Navigation ---
def on_change_gen():
    st.session_state.nav_plating = None

def on_change_plating():
    st.session_state.nav_gen = None

# --- Initialisation des États (clés statiques) ---
if 'nav_gen' not in st.session_state:
    st.session_state.nav_gen = t("gen_pages")[0]
if 'nav_plating' not in st.session_state:
    st.session_state.nav_plating = None

# --- Barre Latérale ---

# Sélecteur de langue avec conservation de la page
old_lang = st.session_state.get('lang', 'fr')
lang_selection = st.sidebar.radio(
    "Language",
    ["🇫🇷 FR", "🇬🇧 EN"],
    horizontal=True,
    label_visibility="collapsed",
    index=0 if old_lang == "fr" else 1
)
new_lang = "fr" if "FR" in lang_selection else "en"

# Si la langue change, convertir la sélection actuelle
if new_lang != old_lang:
    old_gen_pages = TRANSLATIONS[old_lang]["gen_pages"]
    old_plating_pages = TRANSLATIONS[old_lang]["plating_pages"]
    new_gen_pages = TRANSLATIONS[new_lang]["gen_pages"]
    new_plating_pages = TRANSLATIONS[new_lang]["plating_pages"]

    if st.session_state.nav_gen and st.session_state.nav_gen in old_gen_pages:
        idx = old_gen_pages.index(st.session_state.nav_gen)
        st.session_state.nav_gen = new_gen_pages[idx]
    elif st.session_state.nav_plating and st.session_state.nav_plating in old_plating_pages:
        idx = old_plating_pages.index(st.session_state.nav_plating)
        st.session_state.nav_plating = new_plating_pages[idx]
    else:
        # Par défaut, sélectionner Accueil/Home
        st.session_state.nav_gen = new_gen_pages[0]
        st.session_state.nav_plating = None

    st.session_state.lang = new_lang
    st.rerun()

st.session_state.lang = new_lang

st.sidebar.title(t("sidebar_title"))
st.sidebar.markdown("---")

# Navigation Général
st.sidebar.subheader(t("gen_header"))
nav_gen = st.sidebar.radio(
    "Nav Gen",
    t("gen_pages"),
    key="nav_gen",
    on_change=on_change_gen,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Navigation Plating
st.sidebar.subheader(t("plating_header"))
nav_plating = st.sidebar.radio(
    "Nav Plating",
    t("plating_pages"),
    key="nav_plating",
    index=None,
    on_change=on_change_plating,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(t("version_info"))

# --- Déterminer la page active ---
selected_page = None
if nav_plating:
    selected_page = nav_plating
elif nav_gen:
    selected_page = nav_gen
else:
    selected_page = t("gen_pages")[0]

# --- Pages ---
gen_pages = t("gen_pages")
plating_pages = t("plating_pages")

# ===== PAGE ACCUEIL =====
if selected_page == gen_pages[0]:
    st.title(t("title"))
    st.markdown(load_file_content("accueil/accueil.md"))
    st.success(t("card_plating_title"))
    st.write(t("card_plating_text"))

# ===== PAGES PLATING =====
elif selected_page in plating_pages:
    idx = plating_pages.index(selected_page)
    st.title(f"Plating : {selected_page}")

    files = [
        "intro/intro_plating.md",
        ("physics/plating_physics.md", "code/plating_code.md"),  # Tabbed with 3D
        "conclusion/plating_conclusion.md",
        "equations/plating_equations.md",
        "lexique/plating_lexique.md",
        "histoire/plating_histoire.md",
        "biblio/plating_biblio.md"
    ]

    try:
        target = files[idx]

        if isinstance(target, tuple):
            # Page avec onglets (Python Firedrake) - Comparaison de simulations
            tabs = st.tabs(t("tabs_plating"))

            # Charger le mapping des simulations
            df_mapping = load_ed_mapping()

            # Valeurs disponibles pour les sélecteurs
            ddc_values = [4.0, 8.0, 12.0]
            sigma_values = [10.0, 25.0, 40.0]
            j0_values = [0.34, 0.68, 1.36]
            alpha_values = [0.4, 0.5, 0.6]

            with tabs[0]:  # Physique
                st.markdown(load_file_content(target[0]))

            with tabs[1]:  # Code
                st.markdown(load_file_content(target[1]))

            with tabs[2]:  # Comparaison PNG
                st.subheader(t("png_viewer"))

                # Zone de sélection des paramètres (layout compact)
                with st.container(border=True):
                    lbl, c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1, 1])
                    with lbl: st.markdown(f"**{t('sim_1')}**")
                    with c1: s1_ddc = st.selectbox(t("lbl_ddc"), ddc_values, key="png_s1_ddc")
                    with c2: s1_sigma = st.selectbox(t("lbl_sigma"), sigma_values, key="png_s1_sigma")
                    with c3: s1_j0 = st.selectbox(t("lbl_j0"), j0_values, key="png_s1_j0")
                    with c4: s1_alpha = st.selectbox(t("lbl_alpha"), alpha_values, key="png_s1_alpha")

                    lbl, c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1, 1])
                    with lbl: st.markdown(f"**{t('sim_2')}**")
                    with c1: s2_ddc = st.selectbox(t("lbl_ddc"), ddc_values, key="png_s2_ddc", index=1)
                    with c2: s2_sigma = st.selectbox(t("lbl_sigma"), sigma_values, key="png_s2_sigma", index=1)
                    with c3: s2_j0 = st.selectbox(t("lbl_j0"), j0_values, key="png_s2_j0", index=1)
                    with c4: s2_alpha = st.selectbox(t("lbl_alpha"), alpha_values, key="png_s2_alpha", index=1)

                    _, btn_col, _ = st.columns([1, 2, 1])
                    with btn_col:
                        btn_png = st.button(t("btn_compare"), type="primary", use_container_width=True, key="btn_png")

                # Affichage des résultats
                if btn_png or st.session_state.get('show_png', False):
                    st.session_state.show_png = True

                    sim1 = get_simulation_by_params(df_mapping, s1_ddc, s1_sigma, s1_j0, s1_alpha)
                    sim2 = get_simulation_by_params(df_mapping, s2_ddc, s2_sigma, s2_j0, s2_alpha)
                    files1 = get_simulation_files(sim1)
                    files2 = get_simulation_files(sim2)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"### {t('sim_1')}")
                        if files1:
                            st.caption(f"CV = {files1['cv']:.2f}% | Épaisseur moy. = {files1['thickness_avg']:.3f} µm")
                            st.markdown(f"**{t('thickness_map')}**")
                            if os.path.exists(files1['thickness']):
                                st.image(files1['thickness'], use_container_width=True)
                            st.markdown(f"**{t('current_density')}**")
                            if os.path.exists(files1['current']):
                                st.image(files1['current'], use_container_width=True)
                            st.markdown(f"**{t('view_3d_iso')}**")
                            if os.path.exists(files1['3d_iso']):
                                st.image(files1['3d_iso'], use_container_width=True)
                        else:
                            st.warning(t("combo_unavailable"))

                    with col2:
                        st.markdown(f"### {t('sim_2')}")
                        if files2:
                            st.caption(f"CV = {files2['cv']:.2f}% | Épaisseur moy. = {files2['thickness_avg']:.3f} µm")
                            st.markdown(f"**{t('thickness_map')}**")
                            if os.path.exists(files2['thickness']):
                                st.image(files2['thickness'], use_container_width=True)
                            st.markdown(f"**{t('current_density')}**")
                            if os.path.exists(files2['current']):
                                st.image(files2['current'], use_container_width=True)
                            st.markdown(f"**{t('view_3d_iso')}**")
                            if os.path.exists(files2['3d_iso']):
                                st.image(files2['3d_iso'], use_container_width=True)
                        else:
                            st.warning(t("combo_unavailable"))

            with tabs[3]:  # Comparaison 3D
                st.subheader(t("3d_viewer"))
                st.info(t("3d_desc"))

                # Zone de sélection des paramètres (layout compact)
                with st.container(border=True):
                    lbl, c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1, 1])
                    with lbl: st.markdown(f"**{t('sim_1')}**")
                    with c1: s1_ddc_3d = st.selectbox(t("lbl_ddc"), ddc_values, key="3d_s1_ddc")
                    with c2: s1_sigma_3d = st.selectbox(t("lbl_sigma"), sigma_values, key="3d_s1_sigma")
                    with c3: s1_j0_3d = st.selectbox(t("lbl_j0"), j0_values, key="3d_s1_j0")
                    with c4: s1_alpha_3d = st.selectbox(t("lbl_alpha"), alpha_values, key="3d_s1_alpha")

                    lbl, c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1, 1])
                    with lbl: st.markdown(f"**{t('sim_2')}**")
                    with c1: s2_ddc_3d = st.selectbox(t("lbl_ddc"), ddc_values, key="3d_s2_ddc", index=1)
                    with c2: s2_sigma_3d = st.selectbox(t("lbl_sigma"), sigma_values, key="3d_s2_sigma", index=1)
                    with c3: s2_j0_3d = st.selectbox(t("lbl_j0"), j0_values, key="3d_s2_j0", index=1)
                    with c4: s2_alpha_3d = st.selectbox(t("lbl_alpha"), alpha_values, key="3d_s2_alpha", index=1)

                    _, btn_col, _ = st.columns([1, 2, 1])
                    with btn_col:
                        btn_3d = st.button(t("btn_compare"), type="primary", use_container_width=True, key="btn_3d")

                # Affichage des visualisations 3D
                if btn_3d or st.session_state.get('show_3d', False):
                    st.session_state.show_3d = True

                    sim1_3d = get_simulation_by_params(df_mapping, s1_ddc_3d, s1_sigma_3d, s1_j0_3d, s1_alpha_3d)
                    sim2_3d = get_simulation_by_params(df_mapping, s2_ddc_3d, s2_sigma_3d, s2_j0_3d, s2_alpha_3d)
                    files1_3d = get_simulation_files(sim1_3d)
                    files2_3d = get_simulation_files(sim2_3d)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"### {t('sim_1')}")
                        if files1_3d and os.path.exists(files1_3d['3d_html']):
                            st.caption(f"CV = {files1_3d['cv']:.2f}%")
                            try:
                                with open(files1_3d['3d_html'], 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                                components.html(html_content, height=500, scrolling=False)
                            except Exception as e:
                                st.error(f"Erreur: {e}")
                        else:
                            st.warning(t("combo_unavailable"))

                    with col2:
                        st.markdown(f"### {t('sim_2')}")
                        if files2_3d and os.path.exists(files2_3d['3d_html']):
                            st.caption(f"CV = {files2_3d['cv']:.2f}%")
                            try:
                                with open(files2_3d['3d_html'], 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                                components.html(html_content, height=500, scrolling=False)
                            except Exception as e:
                                st.error(f"Erreur: {e}")
                        else:
                            st.warning(t("combo_unavailable"))

        else:
            st.markdown(load_file_content(target))

    except Exception as e:
        st.error(f"Navigation Error: {e}")

# --- Ancre de fin de page ---
st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)
