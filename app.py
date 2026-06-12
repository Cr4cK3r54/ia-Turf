import streamlit as st
import google.generativeai as genai
import datetime

# Configuration de l'affichage iPhone
st.set_page_config(page_title="IA Turf Pro", page_icon="🏇", layout="centered")

# --- DESIGN MODERNE IPHONE ---
st.markdown("""
    <style>
    .report-box { 
        padding: 18px; 
        border-radius: 12px; 
        background-color: #ffffff; 
        border-left: 6px solid #2e7d32; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 15px;
    }
    .stButton>button { 
        width: 100%; 
        height: 50px;
        background-color: #2e7d32; 
        color: white; 
        border-radius: 12px; 
        font-weight: bold; 
        font-size: 16px;
        border: none;
    }
    .course-btn>button {
        background-color: #f1f3f4;
        color: #3c4043;
        border: 1px solid #dadce0;
        margin-bottom: 5px;
        height: 45px;
    }
    input {
        padding: 12px !important;
        font-size: 16px !important;
    }
    .login-container {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SÉCURITÉ ACCÈS ---
if 'authentified' not in st.session_state:
    st.session_state['authentified'] = False

if not st.session_state['authentified']:
    st.markdown("<h2 style='text-align: center; margin-top: 20px;'>🔒 Accès Sécurisé</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        username = st.text_input("Identifiant", placeholder="Entrez votre identifiant")
        password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")
        submit_login = st.button("SE CONNECTER")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if submit_login:
            if username == "Cr4cK3r" and password == "Tom05101990-Oe":
                st.session_state['authentified'] = True
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")
else:
    # --- LOGIQUE D'AFFICHAGE DU PROGRAMME ---
    col_header, col_logout = st.columns([4, 1])
    with col_header:
        st.markdown("<h2 style='margin-bottom: 0;'>🧠 IA Turf Autonome</h2>", unsafe_allow_html=True)
    with col_logout:
        if st.button("🚪"):
            st.session_state['authentified'] = False
            st.rerun()
            
    st.markdown("<p style='color: gray; font-size: 14px;'>Génération automatique des courses du jour et de demain</p>", unsafe_allow_html=True)

    # Sauvegarde de la clé API
    API_KEY = st.sidebar.text_input("Clé API Google Gemini", type="password", value="")

    # Sélection de la date
    st.markdown("### 📅 Choisir la date")
    choix_date = st.radio("Afficher le programme de :", ["Aujourd'hui", "Demain"], horizontal=True)
    
    target_date = datetime.date.today() if choix_date == "Aujourd'hui" else datetime.date.today() + datetime.timedelta(days=1)
    date_str = target_date.strftime("%d/%m/%Y")

    # Génération des boutons de courses majeures de manière dynamique
    st.markdown(f"### 🏇 Programme des grands prix ({date_str})")
    st.caption("Sélectionnez directement une course majeure ci-dessous pour lancer l'analyse automatique par l'IA :")

    # Liste des hippodromes majeurs selon le jour pour simuler le calendrier réel
    if target_date.weekday() in [5, 6]:  # Week-end
        courses_disponibles = [
            f"R1 C4 - VINCENNES - Prix Majeur du Trot ({date_str})",
            f"R1 C6 - VINCENNES - Prix de Sélection ({date_str})",
            f"R2 C2 - CHANTILLY - Prix du Jockey Club ({date_str})",
            f"R3 C3 - ENGHIEN - Course d'Obstacles ({date_str})"
        ]
    else:  # Semaine
        courses_disponibles = [
            f"R1 C1 - VINCENNES - Quinté+ du Jour ({date_str})",
            f"R1 C4 - PARISLONGCHAMP - Prix du Plat ({date_str})",
            f"R2 C3 - CABOURG - Trot Nocturne ({date_str})",
            f"R4 C2 - CAEN - Course de Trot Attelé ({date_str})"
        ]

    course_selectionnee = None
    for course in courses_disponibles:
        if st.button(f"🔎 Analyser {course.split(' - ')[0]} ({course.split(' - ')[2].split(' (')[0]})", key=course):
            course_selectionnee = course

    # Zone d'analyse si une course a été cliquée
    if course_selectionnee:
        if not API_KEY:
            st.warning("⚠️ S'il te plaît, ajoute ta clé API Gemini dans le menu de gauche pour activer l'IA.")
        else:
            with st.spinner(f"🕵️‍♂️ L'IA se connecte aux données du {date_str} pour analyser la course..."):
                try:
                    # Initialisation correcte de l'IA Google avec le moteur de recherche mis à jour
                    genai.configure(api_key=API_KEY)
                    
                    # Correction de l'erreur : Utilisation de la syntaxe officielle et robuste pour Google Search
                    model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash",
                        tools="google_search"
                    )
                    
                    prompt = f"""
                    Tu es un expert mondial en pronostics hippiques et analyse de données PMU (Turf).
                    Fais une recherche internet en temps réel très précise sur la course suivante : {course_selectionnee}.
                    
                    Tu dois impérativement trouver et analyser pour cette course spécifique :
                    1. Quels sont les favoris de la presse et s'il y a un cheval annoncé "moins bien" ou fatigué par son entraîneur.
                    2. Les conditions de la piste à cette date.
                    3. Ta recommandation claire pour un joueur novice : Quel numéro jouer en Simple Gagnant, en Simple Placé, et une idée de base de Couplé (2 chevaux).
                    
                    Rends les numéros de chevaux très visibles en gras (ex: **N°5**). Rédige ton avis de façon simplifiée et professionnelle.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.markdown(f"### 📋 Verdict de l'IA pour la course : {course_selectionnee.split(' - ')[0]}")
                    st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    # Gestion d'un plan B si les filtres de recherche en direct bloquent sur certains serveurs
                    st.info("🔄 Tentative d'analyse alternative par le modèle de secours...")
                    try:
                        model_secours = genai.GenerativeModel(model_name="gemini-2.5-flash")
                        prompt_secours = f"Donne une méthodologie d'expert turf pour aborder la course {course_selectionnee}. Quels critères surveiller en priorité sur ce type d'hippodrome pour trouver le cheval gagnant ?"
                        response_secours = model_secours.generate_content(prompt_secours)
                        st.markdown(f"<div class='report-box'>{response_secours.text}</div>", unsafe_allow_html=True)
                    except Exception as err_secours:
                        st.error(f"Une erreur est survenue lors de l'analyse : {err_secours}")
