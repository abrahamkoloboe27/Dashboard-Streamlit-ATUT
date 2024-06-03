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

# Load data
file = st.sidebar.file_uploader("Importer vos données ici", type=["xlsx","xls"])

# Vérification si un fichier a été téléchargé
if file is not None:
  df = load_data(file)

  # Create tabs for each country
  countries_tab = ["Tous les pays 🇧🇯🇸🇳🇨🇮🇧🇫🇹🇬🇬🇦","BENIN 🇧🇯", "SENEGAL 🇸🇳", "COTE IVOIRE 🇨🇮", "BURKINA FASO 🇧🇫", "TOGO 🇹🇬", "GABON 🇬🇦"]
  countries = [" "," BENIN", "SENEGAL", "COTE IVOIRE", "BURKINA FASO", "TOGO", "GABON"]
  tabs = st.tabs(countries_tab)

  # Add sidebar widgets
  st.session_state.number_or_percentage = st.sidebar.radio("Nombre/Pourcentage", ["Nombre", "Pourcentage"], horizontal=True)
  st.session_state.only_for = st.sidebar.checkbox("Tous les étudiants", st.session_state.only_for)
  st.session_state.n_tuto = st.sidebar.slider(label="Nombre tutoriels", min_value=1, max_value=8, value=st.session_state.n_tuto, step=1)
  st.session_state.selected_tutorials = st.sidebar.multiselect("Tutoriels sélectionnés",
                                                              ['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8'])

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
