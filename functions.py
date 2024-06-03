import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize session state variables
if "number_or_percentage" not in st.session_state:
    st.session_state.number_or_percentage = "Nombre"
if "n_tuto" not in st.session_state:
    st.session_state.n_tuto = 4
if "only_for" not in st.session_state:
    st.session_state.only_for = True
if "selected_tutorials" not in st.session_state:
    st.session_state.selected_tutorials = ['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']

@st.cache_resource
def load_data(file_path):
    """
    Charge les données depuis un fichier Excel et les prétraite.

    Args:
        file_path (str): Le chemin vers le fichier Excel.

    Returns:
        pandas.DataFrame: Les données prétraitées.
    """
    sheet_names = ["TC _ BENIN", "TC_SENEGAL", "TC_COTE IVOIRE", "TC_BURKINA FASO", "TC_TOGO", "TC_GABON"]
    data_frames = []
    for sheet in sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, header=2)
        df = df[['Unnamed: 1', 'Unnamed: 2', 'Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']]
        df.columns = ['Nom', 'Prénoms', 'Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']
        df['Pays'] = sheet.split('_')[1]
        tuto = ['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']
        for t in tuto:
            df[t] = df[t].apply(lambda x: 1 if str(x).strip().upper() == 'OUI' else 0)

        df['Nombre de tutos validés'] = df[['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']].sum(axis=1)
        data_frames.append(df.loc[df["Nom"] != "Example"])

    return pd.concat(data_frames)

def get_data_country(df, country):
    """
    Filtre les données en fonction du pays sélectionné.

    Args:
        df (pandas.DataFrame): Les données à filtrer.
        country (str): Le pays à filtrer.

    Returns:
        pandas.DataFrame: Les données filtrées.
    """
    return df.loc[df["Pays"] == country]

def get_data_tutorial(df, tutorial):
    """
    Filtre les données en fonction des tutoriels sélectionnés.

    Args:
        df (pandas.DataFrame): Les données à filtrer.
        tutorial (list): La liste des tutoriels à filtrer.

    Returns:
        pandas.DataFrame: Les données filtrées.
    """
    col = ["Nom", "Prénoms"]
    for tuto in tutorial:
        col.append(tuto)
    return df[col]

def get_number_of_students(df):
    """
    Obtient le nombre total d'étudiants dans les données.

    Args:
        df (pandas.DataFrame): Les données.

    Returns:
        int: Le nombre total d'étudiants.
    """
    return len(df)

def students_with_min_tutorials(data, min_tutorials):
    """
    Obtient les étudiants ayant suivi un nombre minimum de tutoriels.

    Args:
        data (pandas.DataFrame): Les données.
        min_tutorials (int): Le nombre minimum de tutoriels.

    Returns:
        pandas.DataFrame: Les données filtrées.
    """
    return data.loc[data["Nombre de tutos validés"] >= min_tutorials]

def print_metric_card_number(data):
    """
    Affiche les cartes métriques montrant le nombre d'étudiants en fonction des options sélectionnées.

    Args:
        data (pandas.DataFrame): Les données.
    """
    col_1, col_2, col_3, col_4 = st.columns([1, 1, 1, 1])
    if st.session_state.number_or_percentage == "Nombre":
        with col_1:
            st.metric("**:blue[Total]**", len(data))
        with col_2:
            st.metric(f"**:blue[Ayant suivi au moins {st.session_state.n_tuto} tutoriel]**",
                      value=len(students_with_min_tutorials(data, st.session_state.n_tuto)), delta_color="inverse")
        with col_3:
            st.metric("**:green[Ayant validé le TC]**",
                      value=len(students_with_min_tutorials(data, 8)), delta_color="inverse")
        with col_4:
            st.metric("**:red[N'ayant pas validé le TC]**",
                      value=len(data) - len(students_with_min_tutorials(data, 8)), delta_color="inverse")
    else:
        with col_1:
            st.metric("**:blue[Total]**", 100 * len(data) / len(data))
        with col_2:
            st.metric(f"**:blue[Ayant suivi au moins {st.session_state.n_tuto} tutoriel]**",
                      value=round(100 * len(students_with_min_tutorials(data, st.session_state.n_tuto)) / len(data), 2), delta_color="inverse")
        with col_3:
            st.metric("**:green[Ayant validé le TC]**",
                      value=round(100 * len(students_with_min_tutorials(data, 8)) / len(data), 2), delta_color="inverse")
        with col_4:
            st.metric("**:red[N'ayant pas validé le TC]**",
                      value=round(100 * (len(data) - len(students_with_min_tutorials(data, 8))) / len(data), 2), delta_color="inverse")

def plot_tutorial_validation(data):
    """
    Trace un graphique à barres montrant le nombre ou le pourcentage d'étudiants ayant validé ou non chaque tutoriel.

    Args:
        data (pandas.DataFrame): Les données.
    """
    # Vérifie si l'utilisateur veut afficher le nombre ou le pourcentage de personnes
    if st.session_state.number_or_percentage == "Nombre":
        # Crée un DataFrame pour stocker le nombre de tutoriels validés et non validés
        tutorial_counts = pd.DataFrame({
            'Tutoriels': [],
            'Validé': [],
            'Non Validé': []
        })

        # Itère sur chaque colonne de tutoriel
        for tutorial in ['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']:
            # Compte le nombre de personnes ayant validé et non validé le tutoriel
            validated_count = data[data[tutorial] == 1].shape[0]
            not_validated_count = data[data[tutorial] == 0].shape[0]

            # Crée un nouveau DataFrame avec les résultats et le concatène avec le DataFrame tutorial_counts
            new_row = pd.DataFrame({
                'Tutoriels': [tutorial],
                'Validé': [validated_count],
                'Non Validé': [not_validated_count]
            })
            tutorial_counts = pd.concat([tutorial_counts, new_row], ignore_index=True)

        # Crée un graphique à barres avec Plotly
        fig = px.bar(tutorial_counts, x='Tutoriels', y=['Validé', 'Non Validé'],
                     labels={'Tutoriels': 'Tutoriels', 'value': "Nombre d'étudiants"},
                     title='Nombre de validation par tutoriel',
                     color_discrete_map={'Validé': 'blue', 'Non Validé': 'red'})

        # Affiche le graphique
        st.plotly_chart(fig)

    else:
        # Crée un DataFrame pour stocker le pourcentage de tutoriels validés et non validés
        tutorial_percentages = pd.DataFrame({
            'Tutoriels': [],
            'Validé': [],
            'Non Validé': []
        })

        # Itère sur chaque colonne de tutoriel
        for tutorial in ['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']:
            # Compte le nombre de personnes ayant validé et non validé le tutoriel
            validated_count = data[data[tutorial] == 1].shape[0]
            not_validated_count = data[data[tutorial] == 0].shape[0]

            # Calcule le pourcentage de personnes ayant validé et non validé le tutoriel
            total_count = validated_count + not_validated_count
            validated_percentage = validated_count / total_count * 100
            not_validated_percentage = not_validated_count / total_count * 100

            # Crée un nouveau DataFrame avec les résultats et le concatène avec le DataFrame tutorial_percentages
            new_row = pd.DataFrame({
                'Tutoriels': [tutorial],
                'Validé': [validated_percentage],
                'Non Validé': [not_validated_percentage]
            })
            tutorial_percentages = pd.concat([tutorial_percentages, new_row], ignore_index=True)

        # Crée un graphique à barres avec Plotly
        fig = px.bar(tutorial_percentages, x='Tutoriels', y=['Validé', 'Non Validé'],
                     labels={'Tutoriels': 'Tutoriels', 'value': "Pourcentage d'étudiants"},
                     title='Pourcentage de validation par tutoriel',
                     color_discrete_map={'Validé': 'blue', 'Non Validé': 'red'})

        # Affiche le graphique
        st.plotly_chart(fig)

def plot_tutorial_validation_final(data):
    """
    Trace un graphique à barres montrant le nombre ou le pourcentage d'étudiants ayant validé ou non les tutoriels sélectionnés.

    Args:
        data (pandas.DataFrame): Les données.
    """
    if st.session_state.only_for:
        plot_tutorial_validation(data)
    else:
        plot_tutorial_validation(students_with_min_tutorials(data, st.session_state.n_tuto))

def get_students_with_selected_tutorials(data, tutorials):
    """
    Obtient les étudiants ayant suivi les tutoriels sélectionnés.

    Args:
        data (pandas.DataFrame): Les données.
        tutorials (list): La liste des tutoriels sélectionnés.

    Returns:
        pandas.DataFrame: Les données filtrées.
    """
    # Filtre les données pour inclure uniquement les étudiants ayant suivi tous les tutoriels sélectionnés
    selected_data = data[data[tutorials].all(axis=1)]
    return selected_data

def plot_donut_chart_selected_tutorials(data, tutorials):
    """
    Trace un graphique en anneau montrant le nombre ou le pourcentage d'étudiants ayant validé ou non les tutoriels sélectionnés.

    Args:
        data (pandas.DataFrame): Les données.
        tutorials (list): La liste des tutoriels sélectionnés.
    """
    # Filtre les données pour inclure uniquement les étudiants ayant suivi tous les tutoriels sélectionnés
    selected_data = data[data[tutorials].all(axis=1)]

    # Calcule le nombre ou le pourcentage d'étudiants ayant suivi les tutoriels sélectionnés
    completed = len(selected_data)
    not_completed = len(data) - completed

    # Crée un graphique en anneau avec Plotly
    labels = ['Validé', 'Non Validé']
    values = [completed, not_completed]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
    fig.update_layout(title=f"Tutorials: {', '.join(tutorials)}")

    # Affiche le graphique
    st.plotly_chart(fig)

def get_students_with_n_subjects(data, n):
    """
    Returns the number of students who have validated a given number of subjects by country.

    Args:
        data (pandas.DataFrame): The data.
        n (int): The number of subjects.

    Returns:
        pandas.DataFrame: The number of students who have validated n subjects by country.
    """
    # Filter the data to include only students who have validated n subjects
    filtered_data = data[data['Nombre de tutos validés'] >=n]

    # Group the data by country and count the number of students in each group
    grouped_data = filtered_data.groupby('Pays').size().reset_index(name='Nombre d\'étudiants')
    for pays in grouped_data["Pays"].unique() : 
      grouped_data["Pourcentage d'étudiants"] = 100 * grouped_data['Nombre d\'étudiants'] / len(get_data_country(data,pays))
    #st.write(grouped_data)
    return grouped_data



def plot_students_with_n_subjects(data, n):
    """
    Creates a barplot using Plotly to represent the number of students who have validated a given number of subjects by country.

    Args:
        data (pandas.DataFrame): The data.
        n (int): The number of subjects.
    """
    # Get the number of students who have validated n subjects by country
    students_with_n_subjects = get_students_with_n_subjects(data, n)
    if n == 8 : 
      # Create a barplot using Plotly
      fig = px.bar(students_with_n_subjects, x='Pays', y='Nombre d\'étudiants',
                  labels={'Pays': 'Pays', 'Nombre d\'étudiants': f'Nombre d\'étudiants ayant validé le TC'},
                  title=f'Nombre d\'étudiants ayant le TC par pays')
    else : 
      # Create a barplot using Plotly
      fig = px.bar(students_with_n_subjects, x='Pays', y='Nombre d\'étudiants',
                  labels={'Pays': 'Pays', 'Nombre d\'étudiants': f'Nombre d\'étudiants ayant validé au moins {n} matières'},
                  title=f'Nombre d\'étudiants ayant validé {n} matières par pays')

    # Show the plot
    st.plotly_chart(fig)
