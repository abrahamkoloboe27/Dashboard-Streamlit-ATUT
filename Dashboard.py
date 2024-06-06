import streamlit as st
import pandas as pd
from functions import *
import plotly.express as px

# Initialize session state variables
if "number_or_percentage" not in st.session_state:
    st.session_state.number_or_percentage = "Nombre"
if "n_tuto" not in st.session_state:
    st.session_state.n_tuto = 4
if "only_for" not in st.session_state:
    st.session_state.only_for = True
if "selected_tutorials" not in st.session_state:
    st.session_state.selected_tutorials = ['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']

# Configure the page
st.set_page_config(
    page_title="Dashboard ATUT",
    page_icon=":📊",
    layout="wide",
)
st.title(":blue[Tableau de bord ATUT 2024] 📊🚀")

# Load data
if st.sidebar.toggle("Générer des données aléartoires"):
    file = 1
else :
    with st.expander("Importez les données", False) : 
        file = st.file_uploader("Importer vos données ici", type=["xlsx","xls"])

# Vérification si un fichier a été téléchargé
if file is not None:
  if file == 1 : 
      df, df_ = generate_data()
      if st.sidebar.checkbox("Affricher les données", False) : 
          with st.expander("Données crées", False) : 
               st.dataframe(df_ ,use_container_width=True)
  else : 
      df = load_data(file)

  # Create tabs for each country
  countries_tab = ["Tous les pays 🇧🇯🇸🇳🇨🇮🇧🇫🇹🇬🇬🇦","BENIN 🇧🇯", "SENEGAL 🇸🇳", "COTE IVOIRE 🇨🇮", "BURKINA FASO 🇧🇫", "TOGO 🇹🇬", "GABON 🇬🇦"]
  countries = [" "," BENIN", "SENEGAL", "COTE IVOIRE", "BURKINA FASO", "TOGO", "GABON"]
  tabs = st.tabs(countries_tab)

  # Add sidebar widgets
  st.session_state.number_or_percentage = st.sidebar.radio("Nombre/Pourcentage", ["Nombre", "Pourcentage"], horizontal=True)
  st.session_state.only_for = st.sidebar.toggle("Tous les étudiants", st.session_state.only_for)
  st.session_state.n_tuto = st.sidebar.slider(label="Nombre tutoriels", min_value=1, max_value=8, value=st.session_state.n_tuto, step=1)
  st.session_state.selected_tutorials = st.sidebar.multiselect("Tutoriels sélectionnés",
                                                              ['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8'])
  with st.sidebar : 
        st.markdown("""
        ## Auteur
        :blue[Abraham KOLOBOE]
        * Email : <abklb27@gmail.com>
        * WhatsApp : +229 91 83 84 21
        * Linkedin : [Abraham KOLOBOE](https://www.linkedin.com/in/abraham-zacharie-koloboe-data-science-ia-generative-llms-machine-learning)
                    """)
  # Iterate over tabs and display data for each country
  for tab, country in zip(tabs, countries):
      with tab:
        if tab == tabs[0] :
          
          with st.expander("Pays",False):
            selected_countries = st.multiselect("Pays", countries[1:], default= countries[1:])
          data = df.loc[df["Pays"].isin(selected_countries)]
          print_metric_card_number(data)
          col_1, col_2 = st.columns([2, 1])
          

          with col_1:
            plot_tutorial_validation_final(data)
          with col_2:
            plot_donut_chart_selected_tutorials(data, st.session_state.selected_tutorials)

          col1, col2 = st.columns(2)
          with col1:
            plot_students_with_n_subjects(data, st.session_state.n_tuto )
          with col2:
            plot_students_with_n_subjects(data, 8)

        else :
          data = df.loc[df["Pays"] == country]
          print_metric_card_number(data)
          col_1, col_2 = st.columns([2, 1])
          with col_1:
              plot_tutorial_validation_final(data)
          with col_2:
              plot_donut_chart_selected_tutorials(data, st.session_state.selected_tutorials)
else : 
    with st.sidebar : 
        st.markdown("""
        ## Auteur
        :blue[Abraham KOLOBOE]
        * Email : <abklb27@gmail.com>
        * WhatsApp : +229 91 83 84 21
        * Linkedin : [Abraham KOLOBOE](https://www.linkedin.com/in/abraham-zacharie-koloboe-data-science-ia-generative-llms-machine-learning)
                    """)
    if st.sidebar.toggle("Readme", True) :
        st.markdown("""   
    ## Description
    Dashboard-Streamlit-ATUT est une application Streamlit conçue pour ATUT (African Trade Unionist Training) afin de visualiser et analyser diverses métriques de données. Ce projet offre des tableaux de bord interactifs, facilitant une prise de décision éclairée et des insights basés sur les données.
    
    ## Fonctionnalités
    - Visualisation de données interactive
    - Interface conviviale
    - Mises à jour des données en temps réel
    - Tableaux de bord personnalisables
    
    ## Installation
    1. Clonez le dépôt :
       ```bash
       git clone https://github.com/abrahamkoloboe27/Dashboard-Streamlit-ATUT.git
       ```
    2. Accédez au répertoire du projet :
       ```bash
       cd Dashboard-Streamlit-ATUT
       ```
    3. Installez les dépendances requises :
       ```bash
       pip install -r requirements.txt
       ```
    
    ## Utilisation
    1. Lancez l'application Streamlit :
       ```bash
       streamlit run Dashboard.py
       ```
    2. Ouvrez votre navigateur web et allez à `http://localhost:8501` pour accéder au tableau de bord.
    
    ## Démo Vidéo
    Pour voir une démonstration de l'application, regardez cette vidéo :
    
    [![Regardez la vidéo démo ](https://img.youtube.com/vi/8l90vuGmUhY/0.jpg)](https://www.youtube.com/watch?v=8l90vuGmUhY&ab_channel=AbrahamKoloboe)
    
    
    Cette vidéo montre comment utiliser les différentes fonctionnalités de l'application, y compris la visualisation des données en temps réel et la personnalisation des tableaux de bord.
    
    ## Contribution
    Les contributions sont les bienvenues ! Veuillez forker le dépôt et soumettre une pull request. Si vous avez des idées d'améliorations ou des suggestions, n'hésitez pas à laisser vos commentaires et avis.
    
    ## Contact
    Pour toute question ou problème, veuillez contacter Abraham Koloboe à [abklb27@gmail.com](abklb27@gmail.com).
    
    ## Licence
    Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
    ```
    
        """)
    else : 
        st.video("démo.mp4")
