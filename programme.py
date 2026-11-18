import pandas as pd
import plotly.express as px

pd.options.display.max_rows=20
type=pd.read_csv("ref\sup_type_antenne.txt", sep=";")
proprietaire=pd.read_csv("ref\sup_proprietaire.txt", sep=";")
nature=pd.read_csv("ref\sup_nature.txt", sep=";")
exploitant=pd.read_csv("ref\sup_exploitant.txt", sep=";")
antenne=pd.read_csv("data\sup_antenne.txt", sep=";")
antenne=antenne[['STA_NM_ANFR', 'TAE_ID', 'SUP_ID']]
station=pd.read_csv("data\sup_station.txt", sep=";")
station=station[['STA_NM_ANFR', 'ADM_ID']]
suport=pd.read_csv("data\sup_support.txt", sep=";")
suport=suport[['STA_NM_ANFR', 'TPO_ID', 'NAT_ID', 'COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_CD_NS_LAT', 'COR_NB_SC_LAT', 'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON', 'COR_CD_EW_LON']]
ss=pd.merge(suport, station, on='STA_NM_ANFR')
ssa=pd.merge(ss, antenne, on='STA_NM_ANFR')
ssae=pd.merge(ssa, exploitant, on='ADM_ID')
ssaen=pd.merge(ssae, nature, on='NAT_ID')
ssaenp=pd.merge(ssaen, proprietaire, on='TPO_ID')
ssaenpt=pd.merge(ssaenp, type, on='TAE_ID')
cols_numeriques = [
    'COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_NB_SC_LAT',
    'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON'
]
for col in cols_numeriques:
    ssaenpt[col] = ssaenpt[col].str.replace(',', '.').astype(float)
ssaenpt['latitude'] = (
    ssaenpt['COR_NB_DG_LAT'] + 
    ssaenpt['COR_NB_MN_LAT'] / 60 + 
    ssaenpt['COR_NB_SC_LAT'] / 3600
) * ssaenpt['COR_CD_NS_LAT'].str.strip().map({'N': 1, 'S': -1})

ssaenpt['longitude'] = (
    ssaenpt['COR_NB_DG_LON'] + 
    ssaenpt['COR_NB_MN_LON'] / 60 + 
    ssaenpt['COR_NB_SC_LON'] / 3600
) * ssaenpt['COR_CD_EW_LON'].str.strip().map({'E': 1, 'W': -1, 'O': -1})

# 4. Arrondir à 6 décimales (précision d'environ 10 cm, suffisant pour le GPS)
ssaenpt['latitude'] = ssaenpt['latitude'].round(6)
ssaenpt['longitude'] = ssaenpt['longitude'].round(6)
fig = px.scatter_map(
    ssaenpt,
    lat="latitude",
    lon="longitude",
    zoom=5,
    map_style="open-street-map"
)
