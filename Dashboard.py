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
    page_title="Dashboard Africa Tech Up Tour",
    page_icon=":📊🚀🌍",
    layout="wide",
)
st.header(":blue[Tableau de bord ATUT 2024] 📊🚀🌍", divider = "rainbow")
if st.sidebar.toggle("A propos de l'auteur"):
    with st.expander("Auteur", True) : 
        c1, c2 = st.columns([1,2])
        with c1 :
            st.image("About the author.png")
        with c2 : 
            st.header(""" **S. Abraham Z. KOLOBOE**""")
            st.markdown("""
                
                *:blue[Data Scientist | Ingénieur en Mathématiques et Modélisation]*

                Bonjour,

                Je suis Abraham, un Data Scientist et Ingénieur en Mathématiques et Modélisation. 
                Mon expertise se situe dans les domaines des sciences de données et de l'intelligence artificielle. 
                Avec une approche technique et concise, je m'engage à fournir des solutions efficaces et précises dans mes projets.
                        
                * Email : <abklb27@gmail.com>
                * WhatsApp : +229 91 83 84 21
                * Linkedin : [Abraham KOLOBOE](https://www.linkedin.com/in/abraham-zacharie-koloboe-data-science-ia-generative-llms-machine-learning)
                    
                                    """)
        
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
            plot_students_with_n_subjects(data, st.session_state.n_tuto , df=df)
          with col2:
            plot_students_with_n_subjects(data, 8, df=df)

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
            ### 🚀 Découvrez le Dashboard Africa Tech Up Tour 🌍


            🎉 **Nouvelle Innovation** : Suivez et analysez facilement les progrès des étudiants africains en Data et IA avec notre tout nouveau dashboard interactif ! 📊


            📚 Le **Africa Tech Up Tour** est une initiative exceptionnelle qui vise à former les étudiants africains dans les domaines de la data et de l'intelligence artificielle. 
            La formation est divisée en deux parties : un **tronc commun** et des **spécialités**. 
            Les étudiants valident des tutoriels et renseignent leurs progrès dans un fichier Google Sheets. 
            Notre dashboard utilise ce fichier pour fournir une visualisation claire et interactive des données, essentielle pour les organisateurs. 🧠💻
            
            *:red[Si vous n'avez pas ces données à votre disposition une option pour générer des données factices pour vous permettre de tester cette application est disponible spécialement pour vous.]*  😁 🥰

            **:blue[Valeur ajoutée]**
                    
            🌟 **Visualisation des Progrès** : Affiche les statistiques des tutoriels suivis et validés par les étudiants.
            
            🌟 **Filtrage Avancé** : Permet de filtrer les données par nombre minimum de tutoriels suivis et de se concentrer sur les étudiants actifs.
            
            🌟 **Options d'Affichage** : Visualisez les données en normes ou en pourcentages pour une meilleure interprétation.
            
            🌟 **Données Synthétiques** : Génération de datasets factices pour tester et comprendre les fonctionnalités sans accès au fichier réel.

            Ces outils sont essentiels pour les organisateurs afin de suivre l'engagement des étudiants et ajuster les formations en conséquence. 📈

            **:red[Outils Utilisés]** 🔧 
            
            Pour la construction de ce dashboard, plusieurs outils et technologies ont été utilisés :
            - **Python** 🐍 : Langage de programmation principal.
            - **Streamlit** 🌐 : Framework pour créer des applications web interactives.
            - **Pandas** 🐼 : Manipulation et analyse des données.
            - **Plotly Express** 📊 : Visualisation interactive des données.
            - **ChatGPT** 🤖 : Génération de noms aléatoires pour les datasets synthétiques.


            📢 **:red[Tester le Dashboard]** : 
                    
            Vous avez la possibilité de tester le dashboard grâce à une fonction qui permet de générer des données synthétiques à partir de listes de noms et prénoms créées avec ChatGPT. Ces données sont totalement aléatoires, changeant à chaque utilisation, y compris le nombre d'étudiants, les noms, et les proportions des tutoriels validés. Cela permet à ceux qui n'ont pas les données de l'Africa Tech Up Tour de tester le dashboard et de nous donner leur avis. 🎲
            
            Le lien vers l'application : [Application](https://dashboard-app-atut.streamlit.app/)

            📢 **:blue[Appel à Contribution]** : 
            
            Vous pouvez consulter le code source sur [GitHub](https://github.com/abrahamkoloboe27/Dashboard-Streamlit-ATUT). Pour les étudiants de l'Africa Tech Up Tour et tous ceux qui s'initient à GitHub, c'est une excellente opportunité pour montrer votre maîtrise de GitHub ! Ajoutez votre nom au dataset généré aléatoirement, créez une nouvelle branche, faites vos modifications et soumettez une pull request pour devenir contributeur de ce projet open source. ✍️

            📊**:blue[Analyse des Données]**  :

                    
            Nous vous encourageons également à utiliser le dashboard pour faire une analyse des données. Identifiez les indicateurs clés, expliquez les informations que les données révèlent, et discutez des décisions que l'on pourrait prendre en fonction de ces informations. Un excellent exercice de storytelling pour démontrer vos compétences en analyse de données et en prise de décision basée sur les données.

            N'hésitez pas à me donner votre avis sur le dashboard, comment nous pourrions l'améliorer et le tester. 🔍



            Merci de votre soutien ! 🙏

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

            [![Regardez la vidéo démo 🎥 ](https://img.youtube.com/vi/8l90vuGmUhY/0.jpg)](https://www.youtube.com/watch?v=8l90vuGmUhY&ab_channel=AbrahamKoloboe)


            Cette vidéo montre comment utiliser les différentes fonctionnalités de l'application, y compris la visualisation des données en temps réel et la personnalisation des tableaux de bord.

            ## Contribution
            Les contributions sont les bienvenues ! Veuillez forker le dépôt et soumettre une pull request. Si vous avez des idées d'améliorations ou des suggestions, n'hésitez pas à laisser vos commentaires et avis.

            ## Contact
            Pour toute question ou problème, veuillez contacter Abraham Koloboe à [abklb27@gmail.com](abklb27@gmail.com).

            ## Licence
            Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
            ```
            Merci de votre soutien ! 🙏
        """)
    else : 
        st.video("démo.webm")
