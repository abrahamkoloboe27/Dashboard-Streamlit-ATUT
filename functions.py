import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

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
def generate_data():
    """
    Generates an Excel file with multiple sheets, each containing a dataset of random names and responses.

    Parameters:
    file_path (str): The path where the generated Excel file will be saved.

    The sheets and their columns are as follows:
    - Sheets: "TC _ BENIN", "TC_SENEGAL", "TC_COTE IVOIRE", "TC_BURKINA FASO", "TC_TOGO", "TC_GABON"
    - Columns: ['Nom', 'Prénoms', 'Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']

    The values in 'Tuto 1' to 'Tuto 8' columns are randomly assigned as "OUI" or "NON".
    The number of rows in each sheet is a random number between 100 and 500.
    """
    sheet_names = ["TC _ BENIN", "TC_SENEGAL", "TC_COTE IVOIRE", "TC_BURKINA FASO", "TC_TOGO", "TC_GABON"]
    # Define the list of first names and last names for each country
    first_names = {
        "TC _ BENIN": ["Amina", "Koffi", "Akouvi", "Ayélé", "Azizou", "Komi", "Adjovi", "Amivi", "Akou", "Dossou", "Gbénoukpo", "Sètondji", "Yèmiclétor", "Houéto", "Chénavi", "Agnima", "Ezin", "Dosou", "Nononsi", "Damé", "Adjè", "Kossi", "Awo", "Akotchomè", "Kossivi", "Adanlé", "Fidégnon", "Gbedo"],
        "TC_SENEGAL": ["Aboubacar", "Aissatou", "Amadou", "Fatou", "Mariama", "Abdoulaye", "Adama", "Aliou", "Mame", "Sokhna", "Cheikh", "Ousmane", "Saliou", "Ndèye", "Pape", "Thierno", "Souleymane", "Ibrahima", "Bineta", "Awa", "Babacar", "Moussa", "Mamadou", "Djibril", "Lamine", "Seynabou", "Fadel", "Khady"],
        "TC_COTE IVOIRE": ["Adjoua", "Kouadio", "Yao", "Awa", "Adama", "Koffi", "Koudou", "Kouakou", "Brou", "Ahoua", "Kassi", "Kouamé", "Diarrassouba", "Koffi", "Loukou", "Affoué", "Akissi", "Anzian", "Adjoumani", "Atsé", "Blé", "Anoh", "Yao", "Beugré", "Akré", "Kadjo", "Amon", "Yao"],
        "TC_BURKINA FASO": ["Aboubacar", "Ali", "Issa", "Salifou", "Aminata", "Fatoumata", "Moumouni", "Mariam", "Inoussa", "Oumarou", "Halima", "Mahamoudou", "Yacouba", "Oumou", "Souleymane", "Adama", "Fati", "Bakary", "Kadiatou", "Ibrahim", "Zakaria", "Samira", "Boureima", "Assitan", "Binta", "Mamadou", "Koudougou", "Mamadou"],
        "TC_TOGO": ["Akouvi", "Ayélé", "Kossi", "Komi", "Afia", "Mawuli", "Yawo", "Mawuena", "Sena", "Yawo", "Afi", "Kodjo", "Amenyo", "Edem", "Akpene", "Mawuli", "Mawuko", "Abra", "Yao", "Sena", "Kofi", "Yawa", "Efo", "Abla", "Dzifa", "Mawulolo", "Eyram", "Sena"],
        "TC_GABON": ["Aimée", "Ange", "Annie", "Aurélie", "Chantal", "Christelle", "Clarisse", "Danielle", "Dany", "Dorothée", "Elodie", "Evelyne", "Fabienne", "Françoise", "Gisèle", "Irène", "Jocelyne", "Léonie", "Line", "Lucie", "Madeleine", "Marcelle", "Mireille", "Muriel", "Nadège", "Paulette", "Solange", "Sylvie", "Victorine"]
    }

    last_names = {
        "TC _ BENIN": ["Adjakou", "Agbanrin", "Agblévi", "Agossou", "Ahomadégbé", "Amoussou", "Assogba", "Ayivi", "Dossou", "Favi", "Gbédigui", "Houndégla", "Kpadé", "Ligan", "Nonhlanhla", "Tchagouni", "Yayi", "Zinsou", "Boko", "Glele", "Houngbédji", "Adjagba", "Gaba", "Kouassi", "Akpo", "Hodonou", "Hounsou"],
        "TC_SENEGAL": ["Ndiaye", "Diop", "Fall", "Seck", "Faye", "Sow", "Diallo", "Sarr", "Gaye", "Sene", "Ndour", "Gueye", "Ba", "Sy", "Kane", "Thiam", "Diouf", "Ndoye", "Ndiaga", "Sene", "Toure", "Thiam", "Diagne", "Mbaye", "Mbengue", "Camara", "Sall", "Wade", "Coly"],
        "TC_COTE IVOIRE": ["Konan", "Kouassi", "Yao", "Kouadio", "Adou", "Akissi", "Koffi", "Aka", "Assi", "Affi", "Ble", "Amani", "Ehouman", "Aké", "Gnoan", "Dago", "Djoman", "Ebo", "Ouegnin", "Bamba", "Kamagaté", "Loua", "Adou", "Kone", "Bini", "Yao", "Atsé", "Kouassi"],
        "TC_BURKINA FASO": ["Traore", "Ouédraogo", "Sawadogo", "Koulibaly", "Kaboré", "Ilboudo", "Diarra", "Ouattara", "Sanou", "Ouedraogo", "Savadogo", "Kabore", "Zango", "Simporé", "Sorgho", "Barro", "Bationo", "Tamboura", "Zongo", "Bagre", "Kinda", "Kientega", "Pare", "Thiombiano", "Zoungrana", "Zida", "Congo", "Bamogo"],
        "TC_TOGO": ["Adjo", "Agbénou", "Agbévi", "Akakpo", "Anani", "Atsou", "Awudi", "Ayivi", "Bokon", "Dodji", "Dosseh", "Edoh", "Ekoué", "Eklu", "Hounkpati", "Kossi", "Kudjo", "Lompo", "Nyekplé", "Nyuiadzi", "Okou", "Sagbo", "Toffoun", "Wokou", "Yao", "Yèkou", "Zankli", "Dzifa", "Ahiave"],
        "TC_GABON": ["Abessolo", "Akue", "Aworet", "Bikoro", "Boulingui", "Bouzobeyok", "Boussamba", "Boussougou", "Doukaga", "Ebang", "Ekomie", "Essone", "Mabika", "Makaya", "Mandji", "Mba", "Moutiet", "Ndinga", "Nguema", "Ngari", "Nkoghe", "Nzang", "Obiang", "Onanga", "Oye", "Owondo", "Oyono", "Tsiba", "Yombi"]
    }
    # Generate data for each sheet
    data_frames = []
    for sheet_name in sheet_names:
        # Generate random number of rows between 100 and 500
        num_rows = random.randint(250, 800)

        # Generate random names
        names = [(random.choice(first_names[sheet_name]), random.choice(last_names[sheet_name])) for _ in range(num_rows)]

        # Generate random responses for 'Tuto 1' to 'Tuto 8' columns with a decreasing probability of "OUI"
        responses = []
        for i in range(8):
            weight_oui = 0.9 - (i * 0.1)
            weight_non = 1 - weight_oui
            responses.append(random.choices(["OUI", "NON"], weights=[weight_oui, weight_non], k=num_rows))

        # Create a DataFrame for the sheet
        data = pd.DataFrame(names, columns=['Prénoms', 'Nom'])
        data["Nom"] = data["Nom"].str.upper()
        data[['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']] = responses
        data_no_proceed = data.copy()
        # Preprocess the data
        data['Pays'] = sheet_name.split('_')[1]
        tuto = ['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']
        for t in tuto:
            data[t] = data[t].apply(lambda x: 1 if str(x).strip().upper() == 'OUI' else 0)

        data['Nombre de tutos validés'] = data[['Tuto 1', 'Tuto 2', 'Tuto 3', 'Tuto 4', 'Tuto 5', 'Tuto 6', 'Tuto 7', 'Tuto 8']].sum(axis=1)
        data_frames.append(data.loc[data["Nom"] != "Example"])

    # Concatenate the data frames
    return pd.concat(data_frames), data_no_proceed

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
