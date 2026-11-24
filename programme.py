#Importing the Dash, Plotly, and Pandas modules

from dash import Dash, html, dcc, Input, Output #dash : page management
import dash_ag_grid as dag  #table visualization
import pandas as pd #data management    
import plotly.express as px #graphics maker

#creating dataframe
type=pd.read_csv("ref\sup_type_antenne.txt", sep=";")   #dataframe name = pd.read_csv("file path", separator)
proprietaire=pd.read_csv("ref\sup_proprietaire.txt", sep=";")
nature=pd.read_csv("ref\sup_nature.txt", sep=";")
exploitant=pd.read_csv("ref\sup_exploitant.txt", sep=";")
antenne=pd.read_csv("data\sup_antenne.txt", sep=";")
station=pd.read_csv("data\sup_station.txt", sep=";")
suport=pd.read_csv("data\sup_support.txt", sep=";")

#column management 
antenne=antenne[['STA_NM_ANFR', 'TAE_ID']]  
station=station[['STA_NM_ANFR', 'ADM_ID', 'DTE_EN_SERVICE']]
suport=suport[['STA_NM_ANFR', 'TPO_ID', 'NAT_ID', 'SUP_NM_HAUT', 'COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_CD_NS_LAT', 'COR_NB_SC_LAT', 'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON', 'COR_CD_EW_LON','ADR_NM_CP', 'ADR_LB_LIEU']]

#merging all dataframe throught correponding column
ss = pd.merge(suport, station, on='STA_NM_ANFR', how='left')   #new dataframe = pd.merge(dataframe1,dataframe2, correponding column, keeping dataframe1 info)
ssa = pd.merge(ss, antenne, on='STA_NM_ANFR', how='left')
ssae = pd.merge(ssa, exploitant, on='ADM_ID', how='left')
ssaen = pd.merge(ssae, nature, on='NAT_ID', how='left')
ssaenp = pd.merge(ssaen, proprietaire, on='TPO_ID', how='left')
ssaenpt = pd.merge(ssaenp, type, on='TAE_ID', how='left')

#list of coordinate columns
cols_num = ['COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_NB_SC_LAT','COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON']

#converting coordinates to numeric values
ssaenpt[cols_num] = ssaenpt[cols_num].apply(pd.to_numeric, errors='coerce')

#calculating the coordinates from WGS 84
dir_lat = ssaenpt['COR_CD_NS_LAT'].str.strip().str.upper().map({'N': 1, 'S': -1})   #create a dictionnary for latitude with n = 1 and s = -1
ssaenpt['latitude'] = (ssaenpt['COR_NB_DG_LAT'] + ssaenpt['COR_NB_MN_LAT'].fillna(0) / 60 + ssaenpt['COR_NB_SC_LAT'].fillna(0) / 3600) * dir_lat    #calculating the latitude

dir_lon = ssaenpt['COR_CD_EW_LON'].str.strip().str.upper().map({'E': 1, 'W': -1, 'O': -1})   #create a dictionnary for longitude with e = 1 and w = -1
ssaenpt['longitude'] = (ssaenpt['COR_NB_DG_LON'] + ssaenpt['COR_NB_MN_LON'].fillna(0) / 60 + ssaenpt['COR_NB_SC_LON'].fillna(0) / 3600) * dir_lon   #calculating the longitude

ssaenpt[['latitude', 'longitude']] = ssaenpt[['latitude', 'longitude']].round(6) #rounding to 6 decimal places
ssaenpt=ssaenpt.drop(columns=['COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_CD_NS_LAT', 'COR_NB_SC_LAT', 'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON', 'COR_CD_EW_LON'])  #Removing WGS 84 coordinates


#Verifying data
ssaenpt['HAUTEUR_NUM'] = pd.to_numeric(
    ssaenpt['SUP_NM_HAUT'].astype(str).str.replace(',', '.', regex=False),
    errors='coerce'
)

#put all invalid heights to 1
ssaenpt['HAUTEUR_NUM'] = (
    ssaenpt['HAUTEUR_NUM']
    .clip(lower=1)
    .fillna(1)
)

#put all the unvalid data to "Inconnu"
colonnes_texte = ssaenpt.select_dtypes(include=['object', 'string']).columns
ssaenpt[colonnes_texte] = (
    ssaenpt[colonnes_texte]
    .replace(r'^\s*$', 'Inconnu', regex=True)
    .fillna('Inconnu')
)

#creating column "Departement" from the two first digits of the postal address
ssaenpt['DEPARTEMENT'] = (
    ssaenpt['ADR_NM_CP']
    .astype(str)
    .str[:2]
)

#creating the map with the dataframe
carte = px.scatter_map(
        ssaenpt,
        lat='latitude',
        lon='longitude',
        size='HAUTEUR_NUM',
        size_max=15,
        hover_name='ADR_LB_LIEU',
        custom_data=[       #customable display 
            'DTE_EN_SERVICE',
            'SUP_NM_HAUT',
            'ADR_NM_CP',
            'TPO_LB',
            'NAT_LB_NOM',
            'TAE_LB',
            'ADM_LB_NOM'
        ],
        title='Cartographie des supports radioélectriques'
    )

carte.update_traces(cluster=dict(enabled=True, maxzoom=10)) #group together points for optimisation
carte.update_layout(height=800,margin=dict(l=0, r=0, t=50, b=0))

#customize display 
carte.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br>" +
        "Date de mise en service: %{customdata[0]}<br>" +
        "Hauteur: %{customdata[1]} m<br>" +
        "Code postal: %{customdata[2]}<br>" +
        "Propriétaire: %{customdata[3]}<br>" +
        "Type de support: %{customdata[4]}<br>" +
        "Type d'antenne: %{customdata[5]}<br>" +
        "Exploitant: %{customdata[6]}<br>"
    )

#removing the column that we don't need anymore
ssaenpt=ssaenpt.drop(columns=['STA_NM_ANFR', 'TPO_ID', 'NAT_ID', 'SUP_NM_HAUT','ADM_ID', 'TAE_ID'])
#renaming column to be understandable
ssaenpt=ssaenpt.rename(columns={'TPO_LB': "Proprietaire", 'NAT_LB_NOM': 'Type de support', 'ADR_LB_LIEU': 'Lieu', "ADR_NM_CP": "Code postal", "HAUTEUR_NUM": "Hauteur(m)", "TAE_LB": "Type d'antenne", "DTE_EN_SERVICE": "Date de mise en service"})

#creating dash page
app = Dash()

#creating info for the date's graph
df_date = ssaenpt.copy()

df_date["Date de mise en service"] = pd.to_datetime(
    df_date["Date de mise en service"],
    errors="coerce",
    dayfirst=True
)

df_date = df_date[
    df_date["Date de mise en service"] >= pd.Timestamp("2020-01-01")    #starting date
]

df_date = (
    df_date.groupby("Date de mise en service")
    .size()
    .reset_index(name="Nombre de supports")
    .sort_values("Date de mise en service")
)
#creating the date's graph
fig_date = px.line(
    df_date,
    x="Date de mise en service",
    y="Nombre de supports",
    markers=True,
    title="Mises en service depuis 2020"
)
#creating the owner of the antennas graph
fig_proprio = px.bar(
    ssaenpt['Proprietaire'].value_counts().head(10).reset_index(),
    x='count',
    y='Proprietaire',
    orientation='h',
    title="Top 10 des propriétaires",
    color='count',
    color_continuous_scale='Blues'
)
#renaming column to be understandable
ssaenpt=ssaenpt.rename(columns={'ADM_LB_NOM': "Utilisateur"})

#Creating users graph
fig_user = px.bar(
    ssaenpt['Utilisateur'].value_counts().head(10).reset_index(),
    x='count',
    y='Utilisateur',
    orientation='h',
    title="Top 10 des Utilisateur",
    color='count',
    color_continuous_scale='sunset'
)

#creating departement graph
fig_dp = px.bar(
    ssaenpt['DEPARTEMENT'].value_counts().head(10).reset_index(),
    x='count',
    y='DEPARTEMENT',
    orientation='h',
    title="Top 10 des départements",
    color='count',
    color_continuous_scale='speed'
)

#configuring dash page
app.layout = html.Div([

    html.H3("Recherche dans le tableau"),

    dcc.Input( #creating an input to search throught a table
        id="recherche-tableau",
        type="text",
        placeholder="🔎 Rechercher dans le tableau...",
        debounce=True,
        style={
            "width": "100%",
            "padding": "12px",
            "marginBottom": "15px",
            "border": "1px solid #ccc",
            "borderRadius": "8px",
            "fontSize": "16px"
        }
    ),

    dag.AgGrid( #creating the table from ssaenpt dataframe
        id="tableau-donnees",
        rowData=ssaenpt.to_dict('records'),
        columnDefs=[{"field": i} for i in ssaenpt.columns],
        dashGridOptions={
            "quickFilterText": "",
            "pagination": True,
            "paginationPageSize": 10
        },
        defaultColDef={ #adding filter
            "sortable": True,
            "filter": True,
            "resizable": True
        },
        style={"height": "500px", "width": "100%"}
    ),
    #adding every graph apart from the map
    dcc.Graph(figure=fig_proprio),
    dcc.Graph(figure=fig_user),
    dcc.Graph(figure=fig_dp),
    dcc.Graph(figure=fig_date),
    dcc.Graph(figure=carte)
])
#configuring the input
@app.callback(
    Output("tableau-donnees", "dashGridOptions"),
    Input("recherche-tableau", "value"),
    prevent_initial_call=False
)
def filtrer_tableau(valeur_recherche):

    return {
        "quickFilterText": valeur_recherche or "",
        "pagination": True,
        "paginationPageSize": 10
    }

def filtrer_tableau(valeur_recherche):
    return {"quickFilterText": valeur_recherche or ""}

#showing the map in a browser
carte.show(renderer="browser")
#lanching the dash page
app.run()