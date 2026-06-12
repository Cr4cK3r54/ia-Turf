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
    .login-container {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 30px;
    }
    textarea {
        font-size: 15px !important;
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
        st.markdown("<h2 style='margin-bottom: 0;'>🧠 IA Turf Expert</h2>", unsafe_allow_html=True)
    with col_logout:
        if st.button("🚪"):
            st.session_state['authentified'] = False
            st.rerun()
            
    st.markdown("<p style='color: gray; font-size: 14px;'>Analyse mathématique basée sur de vraies données</p>", unsafe_allow_html=True)

    # Clé API
    API_KEY = st.sidebar.text_input("Clé API Google Gemini", type="password", value="")

    st.markdown("### 📝 Données de la course")
    
    nom_course = st.text_input("Nom de la course", placeholder="Ex: R1 C1 - Prix d'Amérique")
    
    st.markdown("**Copier-coller le pronostic de la presse ou la liste des partants :**")
    st.caption("Ouvre vite ton appli de Turf (PMU, Zone-Turf, etc.), sélectionne le pronostic de la presse ou la liste des 8 chevaux favoris, et colle-les brut ci-dessous :")
    
    donnees_brutes = st.text_area(
        "Données de la presse à analyser", 
        height=150, 
        placeholder="Exemple à coller :\n1 - Idao de Tillard (Favori, D4, forme excellente)\n4 - Horsy Dream (Régulier, ferré)\n7 - Go On Boy (Bel engagement)\n12 - Ampia Mede Sm (En baisse)..."
    )

    bouton_analyse = st.button("🎯 GENERER LE TICKET PAR IA")

    if bouton_analyse:
        if not API_KEY:
            st.warning("⚠️ Ajoute ta clé API Gemini dans le menu de gauche.")
        elif not donnees_brutes or not nom_course:
            st.error("Veuillez remplir le nom de la course et y coller les données des chevaux.")
        else:
            with st.spinner("📊 L'IA applique les filtres mathématiques et élimine les faux favoris..."):
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                    
                    prompt = f"""
                    Tu es un algorithme de tri et un expert professionnel du Turf. Tu dois analyser de manière STRICTE les données réelles fournies ci-dessous pour la course '{nom_course}'. Tu as interdiction d'inventer des chevaux qui ne sont pas dans la liste.
                    
                    Voici les données brutes de la course :
                    \"\"\"{donnees_brutes}\"\"\"
                    
                    En te basant UNIQUEMENT sur ces données textuelles, applique les règles suivantes :
                    1. Repère le cheval qui a les meilleures garanties (mention 'excellent', 'D4', 'favori logique'). Il sera ton Simple Gagnant.
                    2. Repère le cheval le plus régulier pour assurer le Simple Placé.
                    3. Construis un Couplé/Trio logique avec les 3 meilleurs numéros de la liste.
                    4. Identifie s'il y a un cheval mentionné comme 'fatigué', 'en baisse', ou 'ferré' alors qu'il est meilleur déferré, et place-le en "Cheval à éviter".
                    
                    Génère le rapport final structuré EXACTEMENT ainsi, sans aucune phrase d'introduction :
                    
                    <h3>🏆 TICKET RECOMMANDÉ PMU (VRAIS PARTANTS)</h3>
                    <ul>
                        <li><b>Simple Gagnant :</b> [Numéro + Nom du cheval choisi comme base gagnante dans la liste]</li>
                        <li><b>Simple Placé Sécurité :</b> [Numéro + Nom du deuxième choix]</li>
                        <li><b>Le Couplé ou Trio à tenter :</b> [3 numéros de la liste séparés par des tirets]</li>
                    </ul>
                    
                    <h3>🧐 CRITÈRES RETENUS PAR L'IA</h3>
                    <p><b>Le point fort du gagnant :</b> [Explique brièvement pourquoi ce cheval de la liste a été choisi]</p>
                    <p><b>Le favori suspect à ÉVITER :</b> [Donne le numéro du cheval de la liste qui présente un risque (forme en baisse, mauvaise config)]</p>
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.markdown(f"### 📋 Pronostic Certifié : {nom_course}")
                    st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de l'analyse : {e}")
