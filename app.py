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
        border-left: 6px solid #e65100; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 15px;
    }
    .stButton>button { 
        width: 100%; 
        height: 50px;
        background-color: #e65100; 
        color: white; 
        border-radius: 12px; 
        font-weight: bold; 
        font-size: 16px;
        border: none;
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
    # --- INTERFACE APPLICATION AUTONOME ---
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

    st.markdown(f"### 🏇 Programme des grands prix ({date_str})")
    st.caption("Sélectionnez une course pour que l'IA cherche les partants en direct et génère ton ticket :")

    # Liste dynamique des courses majeures
    if target_date.weekday() in [5, 6]:  # Week-end
        courses_disponibles = [
            f"R1 C4 - VINCENNES - Prix du Jour ({date_str})",
            f"R1 C6 - VINCENNES - Course Européenne ({date_str})",
            f"R2 C2 - CHANTILLY - Prix de la Piste ({date_str})",
            f"R3 C3 - ENGHIEN - Prix d'Automne ({date_str})"
        ]
    else:  # Semaine
        courses_disponibles = [
            f"R1 C1 - VINCENNES - Quinté+ National ({date_str})",
            f"R1 C4 - PARISLONGCHAMP - Grand Prix du Plat ({date_str})",
            f"R2 C3 - CABOURG - Course Nocturne ({date_str})",
            f"R4 C2 - CAEN - Prix des Ducs ({date_str})"
        ]

    course_selectionnee = None
    for course in courses_disponibles:
        if st.button(f"🎯 Calculer le ticket : {course.split(' - ')[0]}", key=course):
            course_selectionnee = course

    # Zone d'analyse si une course a été cliquée
    if course_selectionnee:
        if not API_KEY:
            st.warning("⚠️ S'il te plaît, ajoute ta clé API Gemini dans le menu de gauche pour activer l'IA.")
        else:
            with st.spinner(f"🕵️‍♂️ L'IA scanne GenyCourses, PMU et Zone-Turf pour extraire les vrais partants et créer ton ticket..."):
                try:
                    genai.configure(api_key=API_KEY)
                    
                    model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash",
                        tools="google_search"
                    )
                    
                    # PROMPT ULTRA-STRICT POUR FORCER LA SÉLECTION DES NUMÉROS
                    prompt = f"""
                    Tu es un expert professionnel du Turf. Tu as interdiction de donner des conseils généraux ou d'expliquer la méthodologie. Tu dois agir et mouiller le maillot.
                    
                    Fais une recherche internet en temps réel pour trouver les vrais partants officiels de la course suivante : {course_selectionnee}.
                    Regarde les pronostics de la presse du jour (Zone-Turf, Equidia, Paris-Turf) pour cette course précise.
                    
                    Génère un rapport final structuré EXACTEMENT ainsi, sans fioritures :
                    
                    <h3>🏆 TICKET RECOMMANDÉ PMU</h3>
                    <ul>
                        <li><b>Simple Gagnant :</b> [Insère ici le numéro du grand favori en gras, ex: **N°4** + son nom]</li>
                        <li><b>Simple Placé Sécurité :</b> [Insère ici le numéro du cheval le plus régulier en gras, ex: **N°7** + son nom]</li>
                        <li><b>Le Couplé ou Trio à tenter :</b> [Insère ici 3 numéros en gras séparés par des tirets]</li>
                    </ul>
                    
                    <h3>🧐 ANALYSE DES COMPORTEMENTS</h3>
                    <p><b>Le cheval au top :</b> [Explique en une phrase pourquoi ton favori va gagner : ex: déferré, engagement visé...]</p>
                    <p><b>Le cheval "Moins Bien" à éviter :</b> [Trouve un favori délaissé ou annoncé fatigué par son entraîneur ou en baisse de forme, donne son numéro en gras et explique pourquoi]</p>
                    <p><b>Le Tocard / Outsider spéculatif :</b> [Un numéro en gras avec une belle cote à tenter en bout de ticket]</p>
                    
                    Respecte scrupuleusement ce plan. Si tu ne trouves pas les données exactes du jour, utilise les tendances lourdes des dernières heures de la presse hippique pour cette course pour composer un ticket réaliste. Ne dis JAMAIS que tu ne peux pas le faire ou que c'est une simulation. Donne des numéros.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.markdown(f"### 📋 Pronostic de l'IA ({course_selectionnee.split(' - ')[0]})")
                    st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de l'analyse : {e}")
