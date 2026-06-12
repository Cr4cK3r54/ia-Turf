import streamlit as st
import google.generativeai as genai

# Configuration de l'affichage iPhone
st.set_page_config(page_title="IA Turf Pro", page_icon="🏇", layout="centered")

# --- DESIGN MODERNE IPHONE ---
st.markdown("""
    <style>
    .report-box { 
        padding: 18px; 
        border-radius: 12px; 
        background-color: #ffffff; 
        border-left: 6px solid #1e88e5; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 15px;
    }
    .stButton>button { 
        width: 100%; 
        height: 55px;
        background-color: #1e88e5; 
        color: white; 
        border-radius: 12px; 
        font-weight: bold; 
        font-size: 18px;
        border: none;
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
    # --- INTERFACE APPLICATION AUTONOME ---
    col_header, col_logout = st.columns([4, 1])
    with col_header:
        st.markdown("<h2 style='margin-bottom: 0;'>🧠 IA Turf Autonome</h2>", unsafe_allow_html=True)
    with col_logout:
        if st.button("🚪"):
            st.session_state['authentified'] = False
            st.rerun()
            
    st.markdown("<p style='color: gray; font-size: 14px;'>Recherche et analyse 100% automatisées</p>", unsafe_allow_html=True)

    # Configuration de la clé API secrète (Gracieuse et indispensable pour l'IA)
    # Tu peux obtenir ta clé gratuite sur Google AI Studio
    API_KEY = st.sidebar.text_input("Clé API Google Gemini", type="password", value="")

    st.markdown("### 📅 Quelle course analyser ?")
    st.caption("L'IA va chercher sur le web les partants, l'état du terrain, la météo et les échos des pistes pour cette course.")
    
    reunion_course = st.text_input("Réunion et Course", placeholder="Ex: R1 C4 Vincennes")
    date_course = st.selectbox("Date de la course", ["Aujourd'hui", "Demain"])

    bouton_analyse = st.button("🎯 LANCER LE SCAN ET L'ANALYSE IA")

    if bouton_analyse:
        if not API_KEY:
            st.warning("⚠️ S'il te plaît, ajoute ta clé API Gemini gratuite dans le menu à gauche pour activer le moteur de l'IA.")
        elif not reunion_course:
            st.error("Veuillez entrer une réunion et un numéro de course.")
        else:
            with st.spinner("🕵️‍♂️ L'IA navigue sur les sites de turf, compile la musique des chevaux et analyse les dernières déclarations..."):
                try:
                    # Initialisation de l'IA Google
                    genai.configure(api_key=API_KEY)
                    
                    # Configuration de l'IA avec accès aux outils de recherche Google en temps réel
                    model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash",
                        tools=[{"google_search": {}}] # Permet à l'IA de chercher en direct sur le web
                    )
                    
                    # Consignes strictes données à l'IA pour l'analyse
                    prompt = f"""
                    Tu es un expert mondial en analyse de données hippiques (Turf / PMU). 
                    Fais une recherche approfondie sur le web concernant la course suivante : {reunion_course} prévue pour {date_course}.
                    
                    Tu dois analyser :
                    1. La liste des partants officiels.
                    2. La forme récente des chevaux (la musique) et des jockeys.
                    3. Les conditions de course (météo, état du terrain/piste).
                    4. Les bruits d'écurie ou les chevaux signalés "moins bien" ou "visant cette course" par les entraîneurs.

                    Rédige un rapport clair, direct et accessible pour un novice. 
                    Utilise du HTML propre avec des balises <b> pour mettre en valeur les numéros de chevaux à jouer.
                    Donne précisément quel cheval jouer en Simple Gagnant/Placé et quelles sont les bases solides.
                    Indique s'il y a un favori suspecté d'être "moins bien" à éviter.
                    """
                    
                    # Exécution de la requête
                    response = model.generate_content(prompt)
                    
                    # Affichage du résultat final sur l'iPhone
                    st.markdown("### 📋 Rapport d'Analyse Automatique")
                    st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de l'analyse : {e}")
