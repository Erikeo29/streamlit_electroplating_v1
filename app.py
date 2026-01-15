import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import pandas as pd
from groq import Groq

# --- Configuration de la page ---
st.set_page_config(page_title="Electroplating Simulation Platform", layout="wide")

# --- Chemins ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT_DIR, "docs")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")
DATA_PATH = os.path.join(ROOT_DIR, "data")
CSS_PATH = os.path.join(ASSETS_PATH, "style.css")
STUDY_RESULTS_PATH = os.path.join(ASSETS_PATH, "plating/study_results")

# --- Traductions ---
TRANSLATIONS = {
    "fr": {
        "title": "Plateforme de Simulation d'Électrodéposition",
        "sidebar_title": "Simulation",
        # Navigation groups
        "gen_header": "Général",
        "gen_pages": ["Accueil", "Introduction"],
        "study_header": "Études de modélisation",
        "study_pages": ["Étude 1 (Firedrake)", "Étude 2 (À venir)"],
        "annex_header": "Annexes",
        "annex_pages": ["Conclusion et Perspectives", "Lexique", "Équations clés", "Un peu d'histoire", "Bibliographie"],
        # Version info (NE PAS MODIFIER)
        "version_info": """**Version 1.3.0**
Jan 2026 - *EQU*

**Nouveautés :**
- Bibliographie enrichie (liens gratuits)
- Physique : équations détaillées
- Code : format Jupyter (12 blocs)
- Comparaison côte à côte (81 sims)""",
        # Tabs
        "tabs_plating": ["Physique", "Code", "Résultats (2D)", "Résultats 3D"],
        # Cards
        "card_plating_title": "### Électrodéposition",
        "card_plating_text": "Simulation de dépôt électrolytique et distribution de courant secondaire.",
        # Simulation labels
        "sim_1": "Simulation 1",
        "sim_2": "Simulation 2",
        "btn_compare": "COMPARER",
        "btn_reset": "RÉINITIALISER",
        "combo_unavailable": "Combinaison non disponible",
        "png_viewer": "Comparaison des résultats (2D)",
        "3d_viewer": "Comparaison 3D Interactive",
        "3d_desc": "Visualisation interactive de l'épaisseur de dépôt (extrudée x1000).",
        "3d_not_found": "Fichier de visualisation 3D introuvable.",
        # Parameter labels
        "lbl_ddc": "DDC (A/dm²)",
        "lbl_sigma": "σ (S/m)",
        "lbl_j0": "j₀ (A/m²)",
        "lbl_alpha": "α",
        "lbl_avail_sims": "📋 Simulations disponibles",
        "lbl_select_combo": "Sélectionner une combinaison",
        # Metrics
        "thickness_map": "Carte d'épaisseur",
        "current_density": "Densité de courant",
        "view_3d_iso": "Vue 3D isométrique",
        # Studies
        "title_study_1": "Étude 1 : Distribution de courant secondaire (Firedrake)",
        "title_study_2": "Étude 2 : À venir",
        "placeholder_coming_soon": "Étude à venir - Contenu en cours de préparation",
        # Chatbot
        "chat_title": "Assistant IA",
        "chat_welcome": "Bonjour ! Je suis votre assistant pour comprendre les simulations d'électrodéposition. Posez-moi vos questions sur Butler-Volmer, la distribution de courant, ou l'interprétation des résultats !",
        "chat_placeholder": "Posez votre question...",
        "chat_error": "Erreur de connexion à l'API.",
        "chat_clear": "Effacer",
        "chat_api_missing": "⚠️ Clé API manquante. Configurez GROQ_API_KEY.",
    },
    "en": {
        "title": "Electroplating Simulation Platform",
        "sidebar_title": "Simulation",
        # Navigation groups
        "gen_header": "General",
        "gen_pages": ["Home", "Introduction"],
        "study_header": "Modeling Studies",
        "study_pages": ["Study 1 (Firedrake)", "Study 2 (Coming Soon)"],
        "annex_header": "Appendices",
        "annex_pages": ["Conclusion and Perspectives", "Glossary", "Key Equations", "A Bit of History", "Bibliography"],
        # Version info (DO NOT MODIFY)
        "version_info": """**Version 1.3.0**
Jan 2026 - *EQU*

**What's New:**
- Enhanced bibliography (free links)
- Physics: detailed equations
- Code: Jupyter-style (12 blocks)
- Side-by-side comparison (81 sims)""",
        # Tabs
        "tabs_plating": ["Physics", "Code", "Results (2D)", "Results 3D"],
        # Cards
        "card_plating_title": "### Electroplating",
        "card_plating_text": "Simulation of electrolytic deposition and secondary current distribution.",
        # Simulation labels
        "sim_1": "Simulation 1",
        "sim_2": "Simulation 2",
        "btn_compare": "COMPARE",
        "btn_reset": "RESET",
        "combo_unavailable": "Combination not available",
        "png_viewer": "Results Comparison (2D)",
        "3d_viewer": "Interactive 3D Comparison",
        "3d_desc": "Interactive visualization of deposition thickness (extruded x1000).",
        "3d_not_found": "3D visualization file not found.",
        # Parameter labels
        "lbl_ddc": "DDC (A/dm²)",
        "lbl_sigma": "σ (S/m)",
        "lbl_j0": "j₀ (A/m²)",
        "lbl_alpha": "α",
        "lbl_avail_sims": "📋 Available Simulations",
        "lbl_select_combo": "Select a combination",
        # Metrics
        "thickness_map": "Thickness Map",
        "current_density": "Current Density",
        "view_3d_iso": "3D Isometric View",
        # Studies
        "title_study_1": "Study 1: Secondary Current Distribution (Firedrake)",
        "title_study_2": "Study 2: Coming Soon",
        "placeholder_coming_soon": "Coming Soon - Content under preparation",
        # Chatbot
        "chat_title": "AI Assistant",
        "chat_welcome": "Hello! I'm your assistant to help you understand electroplating simulations. Ask me about Butler-Volmer, current distribution, or results interpretation!",
        "chat_placeholder": "Ask your question...",
        "chat_error": "API connection error.",
        "chat_clear": "Clear",
        "chat_api_missing": "⚠️ API key missing. Configure GROQ_API_KEY.",
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

# --- Chargement CSS externe ---
def load_custom_css():
    """Charge le CSS et les boutons de navigation."""
    css_content = ""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, 'r', encoding='utf-8') as f:
            css_content = f.read()

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
    return f"<style>{css_content}</style>{nav_buttons_html}"

st.markdown(load_custom_css(), unsafe_allow_html=True)

# --- Fonctions Utilitaires ---
def load_file_content(relative_path):
    """Charge un fichier depuis docs/<lang>/relative_path"""
    lang = get_language()
    full_path = os.path.join(DOC_PATH, lang, relative_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return f"Document not found: {relative_path}"

def display_smart_markdown(content):
    """Affiche du markdown avec support des blocs de code."""
    st.markdown(content)

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

def get_available_combinations(df):
    """Retourne la liste des combinaisons disponibles pour le selectbox."""
    combos = []
    for _, row in df.iterrows():
        label = f"ID {int(row['id']):03d} | DDC={row['DDC_target_A_dm2']} | σ={row['sigma_S_m']} | j₀={row['j0_A_m2']} | α={row['alpha']}"
        combos.append((label, row))
    return combos

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

# --- Callbacks pour Navigation (INDEX-based pour éviter bugs de langue) ---
def on_change_gen():
    """Callback quand on sélectionne une page générale."""
    selected = st.session_state.get('_radio_gen')
    if selected is not None:
        gen_pages = TRANSLATIONS[st.session_state.get('lang', 'fr')]["gen_pages"]
        try:
            st.session_state.nav_gen_idx = gen_pages.index(selected)
        except ValueError:
            st.session_state.nav_gen_idx = 0
    st.session_state.nav_study_idx = None
    st.session_state.nav_annex_idx = None

def on_change_study():
    """Callback quand on sélectionne une étude."""
    selected = st.session_state.get('_radio_study')
    if selected is not None:
        study_pages = TRANSLATIONS[st.session_state.get('lang', 'fr')]["study_pages"]
        try:
            st.session_state.nav_study_idx = study_pages.index(selected)
        except ValueError:
            st.session_state.nav_study_idx = 0
    st.session_state.nav_gen_idx = None
    st.session_state.nav_annex_idx = None

def on_change_annex():
    """Callback quand on sélectionne une annexe."""
    selected = st.session_state.get('_radio_annex')
    if selected is not None:
        annex_pages = TRANSLATIONS[st.session_state.get('lang', 'fr')]["annex_pages"]
        try:
            st.session_state.nav_annex_idx = annex_pages.index(selected)
        except ValueError:
            st.session_state.nav_annex_idx = 0
    st.session_state.nav_gen_idx = None
    st.session_state.nav_study_idx = None

# --- Initialisation Centralisée des États ---
DEFAULT_SESSION_STATES = {
    # Navigation (stocke INDEX, pas texte - indépendant de la langue)
    'nav_gen_idx': 0,
    'nav_study_idx': None,
    'nav_annex_idx': None,
    # Visualization states
    'show_png': False,
    'show_3d': False,
    # Chatbot
    'chat_messages': [],
}

for key, default in DEFAULT_SESSION_STATES.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Au premier chargement, s'assurer qu'on est sur Accueil
if (st.session_state.nav_gen_idx is None and
    st.session_state.nav_study_idx is None and
    st.session_state.nav_annex_idx is None):
    st.session_state.nav_gen_idx = 0

# --- Chatbot Functions ---
SYSTEM_PROMPT = """Tu es un assistant expert en électrodéposition et électrochimie computationnelle.

Tu connais parfaitement:
1. **La physique de l'électrodéposition** : Distribution de courant primaire/secondaire, équation de Butler-Volmer, loi de Faraday
2. **Les paramètres clés** :
   - DDC (Densité De Courant) : 4, 8, 12 A/dm²
   - σ (conductivité électrolyte) : 10, 25, 40 S/m
   - j₀ (densité de courant d'échange) : 0.34, 0.68, 1.36 A/m²
   - α (coefficient de transfert) : 0.4, 0.5, 0.6
3. **Les métriques** :
   - CV% (Coefficient de Variation) : mesure l'uniformité du dépôt
   - Épaisseur moyenne (µm)
   - Throwing Power
4. **L'implémentation Firedrake** : FEM, maillage GMSH, solveur Newton

Réponds de manière concise et scientifiquement rigoureuse.
Utilise LaTeX pour les équations (format $equation$).
Réponds dans la langue de l'utilisateur.
"""

def is_chatbot_enabled():
    """Vérifie si le chatbot doit être affiché."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", None)
        except Exception:
            pass
    return bool(api_key)

def get_groq_client():
    """Retourne le client Groq si la clé API est disponible."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", None)
        except Exception:
            pass
    if api_key:
        return Groq(api_key=api_key)
    return None

def stream_groq_response(user_message: str):
    """Génère la réponse de Groq (Llama 3) en streaming."""
    client = get_groq_client()
    if not client:
        yield t("chat_api_missing")
        return

    st.session_state.chat_messages.append({"role": "user", "content": user_message})

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(st.session_state.chat_messages)

        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            stream=True
        )

        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                full_response += text
                yield text

        st.session_state.chat_messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        yield f"{t('chat_error')} ({str(e)[:50]}...)"

# --- Barre Latérale ---

# Sélecteur de langue
old_lang = st.session_state.get('lang', 'fr')
lang_selection = st.sidebar.radio(
    "Language",
    ["🇫🇷 FR", "🇬🇧 EN"],
    horizontal=True,
    label_visibility="collapsed",
    index=0 if old_lang == "fr" else 1
)
new_lang = "fr" if "FR" in lang_selection else "en"

# Si la langue change, simplement rerun (les INDEX sont indépendants de la langue)
if new_lang != old_lang:
    st.session_state.lang = new_lang
    st.rerun()

st.session_state.lang = new_lang

st.sidebar.title(t("sidebar_title"))
st.sidebar.markdown("---")

# Récupérer les listes de pages dans la langue actuelle
gen_pages = t("gen_pages")
study_pages = t("study_pages")
annex_pages = t("annex_pages")

# --- Navigation Groupe 1 : Général ---
st.sidebar.subheader(t("gen_header"))
nav_gen = st.sidebar.radio(
    "Nav Gen",
    gen_pages,
    key="_radio_gen",
    index=st.session_state.nav_gen_idx,
    on_change=on_change_gen,
    label_visibility="collapsed"
)

# --- Chatbot dans la Sidebar (toujours visible) ---
st.sidebar.markdown("---")
with st.sidebar.popover(t("chat_title"), use_container_width=True):
    if is_chatbot_enabled():
        if st.button(t("chat_clear"), use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

        st.markdown("---")

        if not st.session_state.chat_messages:
            st.info(t("chat_welcome"))

        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input(t("chat_placeholder")):
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                st.write_stream(stream_groq_response(prompt))
    else:
        st.warning(t("chat_api_missing"))

# --- Navigation Groupe 2 : Études ---
st.sidebar.markdown("---")
st.sidebar.subheader(t("study_header"))
nav_study = st.sidebar.radio(
    "Nav Study",
    study_pages,
    key="_radio_study",
    index=st.session_state.nav_study_idx,
    on_change=on_change_study,
    label_visibility="collapsed"
)

# --- Navigation Groupe 3 : Annexes ---
st.sidebar.markdown("---")
st.sidebar.subheader(t("annex_header"))
nav_annex = st.sidebar.radio(
    "Nav Annex",
    annex_pages,
    key="_radio_annex",
    index=st.session_state.nav_annex_idx,
    on_change=on_change_annex,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(t("version_info"))

# --- Déterminer la page active ---
# Priorité : études > annexes > général
selected_page = None
if st.session_state.nav_study_idx is not None:
    selected_page = study_pages[st.session_state.nav_study_idx]
elif st.session_state.nav_annex_idx is not None:
    selected_page = annex_pages[st.session_state.nav_annex_idx]
elif st.session_state.nav_gen_idx is not None:
    selected_page = gen_pages[st.session_state.nav_gen_idx]
else:
    selected_page = gen_pages[0]

# --- PAGES ---

# ===== PAGE ACCUEIL (index 0 dans gen_pages) =====
if selected_page == gen_pages[0]:
    st.title(t("title"))
    st.markdown(load_file_content("accueil/accueil.md"))
    st.success(t("card_plating_title"))
    st.write(t("card_plating_text"))

# ===== PAGE INTRODUCTION (index 1 dans gen_pages) =====
elif selected_page == gen_pages[1]:
    st.markdown(load_file_content("intro/intro_plating.md"))

# ===== ÉTUDE 1 : Firedrake (index 0 dans study_pages) =====
elif selected_page == study_pages[0]:
    st.title(t("title_study_1"))

    tabs = st.tabs(t("tabs_plating"))

    # Charger le mapping des simulations
    df_mapping = load_ed_mapping()

    # Préparer les combinaisons pour le menu déroulant
    if not df_mapping.empty:
        combos = get_available_combinations(df_mapping)
        combo_labels = [c[0] for c in combos]
        combo_data = {c[0]: c[1] for c in combos}

    # --- TAB 0 : Physique ---
    with tabs[0]:
        st.markdown(load_file_content("physics/plating_physics.md"))

    # --- TAB 1 : Code ---
    with tabs[1]:
        st.markdown(load_file_content("code/plating_code.md"))

    # --- TAB 2 : Résultats (2D) avec menu déroulant ---
    with tabs[2]:
        st.subheader(t("png_viewer"))

        if not df_mapping.empty:
            # Zone de sélection avec menus déroulants
            with st.container(border=True):
                # Popover pour voir toutes les simulations
                c_pop, _ = st.columns([0.3, 0.7])
                with c_pop:
                    with st.popover(t("lbl_avail_sims"), use_container_width=True):
                        st.dataframe(
                            df_mapping[['id', 'DDC_target_A_dm2', 'sigma_S_m', 'j0_A_m2', 'alpha', 'CV_percent', 'thickness_avg_um']],
                            use_container_width=True, hide_index=True
                        )

                st.markdown(f"**{t('sim_1')}**")
                s1_combo = st.selectbox(
                    t("lbl_select_combo"),
                    combo_labels,
                    key="png_s1_combo",
                    label_visibility="collapsed"
                )

                st.markdown(f"**{t('sim_2')}**")
                s2_combo = st.selectbox(
                    t("lbl_select_combo"),
                    combo_labels,
                    key="png_s2_combo",
                    index=min(1, len(combo_labels) - 1),
                    label_visibility="collapsed"
                )

                _, btn_col, rst_col, _ = st.columns([1, 1, 1, 1])
                with btn_col:
                    btn_png = st.button(t("btn_compare"), type="primary", use_container_width=True, key="btn_png")
                with rst_col:
                    if st.button(t("btn_reset"), type="secondary", use_container_width=True, key="rst_png"):
                        st.session_state.show_png = False
                        st.rerun()

            # Affichage des résultats
            if btn_png or st.session_state.get('show_png', False):
                st.session_state.show_png = True

                sim1 = combo_data.get(s1_combo)
                sim2 = combo_data.get(s2_combo)
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
        else:
            st.info(t("placeholder_coming_soon"))

    # --- TAB 3 : Résultats 3D avec menu déroulant ---
    with tabs[3]:
        st.subheader(t("3d_viewer"))
        st.info(t("3d_desc"))

        if not df_mapping.empty:
            # Zone de sélection avec menus déroulants
            with st.container(border=True):
                st.markdown(f"**{t('sim_1')}**")
                s1_combo_3d = st.selectbox(
                    t("lbl_select_combo"),
                    combo_labels,
                    key="3d_s1_combo",
                    label_visibility="collapsed"
                )

                st.markdown(f"**{t('sim_2')}**")
                s2_combo_3d = st.selectbox(
                    t("lbl_select_combo"),
                    combo_labels,
                    key="3d_s2_combo",
                    index=min(1, len(combo_labels) - 1),
                    label_visibility="collapsed"
                )

                _, btn_col, rst_col, _ = st.columns([1, 1, 1, 1])
                with btn_col:
                    btn_3d = st.button(t("btn_compare"), type="primary", use_container_width=True, key="btn_3d")
                with rst_col:
                    if st.button(t("btn_reset"), type="secondary", use_container_width=True, key="rst_3d"):
                        st.session_state.show_3d = False
                        st.rerun()

            # Affichage des visualisations 3D
            if btn_3d or st.session_state.get('show_3d', False):
                st.session_state.show_3d = True

                sim1_3d = combo_data.get(s1_combo_3d)
                sim2_3d = combo_data.get(s2_combo_3d)
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
            st.info(t("placeholder_coming_soon"))

# ===== ÉTUDE 2 : À venir (index 1 dans study_pages) =====
elif selected_page == study_pages[1]:
    st.title(t("title_study_2"))
    st.info(t("placeholder_coming_soon"))
    st.markdown("""
**Étude prévue / Planned study:**
- Analyse de sensibilité au maillage
- Étude de convergence temporelle
- Mesh sensitivity analysis
- Time convergence study
""")

# ===== PAGES ANNEXES =====
elif selected_page in annex_pages:
    idx = annex_pages.index(selected_page)
    # Ordre: Conclusion et Perspectives / Lexique / Équations / Histoire / Biblio
    annex_files = [
        "conclusion/plating_conclusion.md",
        "lexique/plating_lexique.md",
        "equations/plating_equations.md",
        "histoire/plating_histoire.md",
        "biblio/plating_biblio.md"
    ]

    try:
        st.markdown(load_file_content(annex_files[idx]))
    except Exception as e:
        st.error(f"Erreur de chargement: {e}")

# --- Ancre de fin de page ---
st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)
