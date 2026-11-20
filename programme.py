from dash import Dash, html, dcc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

type=pd.read_csv("ref\sup_type_antenne.txt", sep=";")
proprietaire=pd.read_csv("ref\sup_proprietaire.txt", sep=";")
nature=pd.read_csv("ref\sup_nature.txt", sep=";")
exploitant=pd.read_csv("ref\sup_exploitant.txt", sep=";")
antenne=pd.read_csv("data\sup_antenne.txt", sep=";")
station=pd.read_csv("data\sup_station.txt", sep=";")
suport=pd.read_csv("data\sup_support.txt", sep=";")

antenne=antenne[['STA_NM_ANFR', 'TAE_ID']]
station=station[['STA_NM_ANFR', 'ADM_ID', 'DTE_EN_SERVICE']]
suport=suport[['STA_NM_ANFR', 'TPO_ID', 'NAT_ID', 'SUP_NM_HAUT', 'COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_CD_NS_LAT', 'COR_NB_SC_LAT', 'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON', 'COR_CD_EW_LON','ADR_NM_CP', 'ADR_LB_LIEU']]

ss = pd.merge(suport, station, on='STA_NM_ANFR', how='left')
ssa = pd.merge(ss, antenne, on='STA_NM_ANFR', how='left')
ssae = pd.merge(ssa, exploitant, on='ADM_ID', how='left')
ssaen = pd.merge(ssae, nature, on='NAT_ID', how='left')
ssaenp = pd.merge(ssaen, proprietaire, on='TPO_ID', how='left')
ssaenpt = pd.merge(ssaenp, type, on='TAE_ID', how='left')

cols_num = ['COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_NB_SC_LAT','COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON']

ssaenpt[cols_num] = ssaenpt[cols_num].apply(pd.to_numeric, errors='coerce')

dir_lat = ssaenpt['COR_CD_NS_LAT'].str.strip().str.upper().map({'N': 1, 'S': -1})
ssaenpt['latitude'] = (ssaenpt['COR_NB_DG_LAT'] + ssaenpt['COR_NB_MN_LAT'].fillna(0) / 60 + ssaenpt['COR_NB_SC_LAT'].fillna(0) / 3600) * dir_lat

dir_lon = ssaenpt['COR_CD_EW_LON'].str.strip().str.upper().map({'E': 1, 'W': -1, 'O': -1})
ssaenpt['longitude'] = (ssaenpt['COR_NB_DG_LON'] + ssaenpt['COR_NB_MN_LON'].fillna(0) / 60 + ssaenpt['COR_NB_SC_LON'].fillna(0) / 3600) * dir_lon

ssaenpt[['latitude', 'longitude']] = ssaenpt[['latitude', 'longitude']].round(6)
ssaenpt=ssaenpt.drop(columns=['COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_CD_NS_LAT', 'COR_NB_SC_LAT', 'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON', 'COR_CD_EW_LON'])



ssaenpt['HAUTEUR_NUM'] = pd.to_numeric(
    ssaenpt['SUP_NM_HAUT'].astype(str).str.replace(',', '.', regex=False),
    errors='coerce'
)
ssaenpt['HAUTEUR_NUM'] = (
    ssaenpt['HAUTEUR_NUM']
    .clip(lower=1)
    .fillna(1)
)

colonnes_texte = ssaenpt.select_dtypes(include=['object', 'string']).columns

ssaenpt[colonnes_texte] = (
    ssaenpt[colonnes_texte]
    .replace(r'^\s*$', 'Inconnu', regex=True)
    .fillna('Inconnu')
)
ssaenpt['DEPARTEMENT'] = (
    ssaenpt['ADR_NM_CP']
    .astype(str)
    .str[:2]
)


carte = px.scatter_map(
        ssaenpt,
        lat='latitude',
        lon='longitude',
        size='HAUTEUR_NUM',
        size_max=15,
        hover_name='ADR_LB_LIEU',
        custom_data=[
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

carte.update_traces(cluster=dict(enabled=True, maxzoom=10))
carte.update_layout(height=800,margin=dict(l=0, r=0, t=50, b=0))

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


app = Dash()

fig_proprio = px.bar(
    ssaenpt['TPO_LB'].value_counts().head(10).reset_index(),
    x='count',
    y='TPO_LB',
    orientation='h',
    title="Top 10 des propriétaires",
    color='count',
    color_continuous_scale='Blues'
)
fig_user = px.bar(
    ssaenpt['ADM_LB_NOM'].value_counts().head(10).reset_index(),
    x='count',
    y='ADM_LB_NOM',
    orientation='h',
    title="Top 10 des Utilisateur",
    color='count',
    color_continuous_scale='sunset'
)
fig_dp = px.bar(
    ssaenpt['DEPARTEMENT'].value_counts().head(10).reset_index(),
    x='count',
    y='DEPARTEMENT',
    orientation='h',
    title="Top 10 des départements",
    color='count',
    color_continuous_scale='speed'
)
app.layout = [
    dag.AgGrid(
        rowData=ssaenpt.to_dict('records'),
        columnDefs=[{"field": i} for i in ssaenpt.columns]
    ),
    dcc.Graph(figure=fig_proprio),
    dcc.Graph(figure=fig_user),
    dcc.Graph(figure=fig_dp),
    dcc.Graph(figure=carte)
]


app.run()