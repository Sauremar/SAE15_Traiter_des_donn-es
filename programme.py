import pandas as pd
import plotly.express as px

type=pd.read_csv("ref\sup_type_antenne.txt", sep=";")
proprietaire=pd.read_csv("ref\sup_proprietaire.txt", sep=";")
nature=pd.read_csv("ref\sup_nature.txt", sep=";")
exploitant=pd.read_csv("ref\sup_exploitant.txt", sep=";")
antenne=pd.read_csv("data\sup_antenne.txt", sep=";")
antenne=antenne[['STA_NM_ANFR', 'TAE_ID']]
station=pd.read_csv("data\sup_station.txt", sep=";")
station=station[['STA_NM_ANFR', 'ADM_ID', 'DTE_EN_SERVICE']]
suport=pd.read_csv("data\sup_support.txt", sep=";")
suport=suport[['STA_NM_ANFR', 'TPO_ID', 'NAT_ID', 'SUP_NM_HAUT', 'COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_CD_NS_LAT', 'COR_NB_SC_LAT', 'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON', 'COR_CD_EW_LON','ADR_NM_CP', 'ADR_LB_LIEU']]
ss=pd.merge(suport, station, on='STA_NM_ANFR')
ssa=pd.merge(ss, antenne, on='STA_NM_ANFR')
ssae=pd.merge(ssa, exploitant, on='ADM_ID')
ssaen=pd.merge(ssae, nature, on='NAT_ID')
ssaenp=pd.merge(ssaen, proprietaire, on='TPO_ID')
ssaenpt=pd.merge(ssaenp, type, on='TAE_ID')
cols_num = [
    'COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_NB_SC_LAT',
    'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON'
]
ssaenpt[cols_num] = ssaenpt[cols_num].apply(pd.to_numeric, errors='coerce')
dir_lat = ssaenpt['COR_CD_NS_LAT'].str.strip().str.upper().map({'N': 1, 'S': -1})
ssaenpt['latitude'] = (
    ssaenpt['COR_NB_DG_LAT'] + 
    ssaenpt['COR_NB_MN_LAT'].fillna(0) / 60 + 
    ssaenpt['COR_NB_SC_LAT'].fillna(0) / 3600
) * dir_lat
dir_lon = ssaenpt['COR_CD_EW_LON'].str.strip().str.upper().map({'E': 1, 'W': -1, 'O': -1})
ssaenpt['longitude'] = (
    ssaenpt['COR_NB_DG_LON'] + 
    ssaenpt['COR_NB_MN_LON'].fillna(0) / 60 + 
    ssaenpt['COR_NB_SC_LON'].fillna(0) / 3600
) * dir_lon
ssaenpt[['latitude', 'longitude']] = ssaenpt[['latitude', 'longitude']].round(6)
ssaenpt=ssaenpt.drop(columns=['COR_NB_DG_LAT', 'COR_NB_MN_LAT', 'COR_CD_NS_LAT', 'COR_NB_SC_LAT', 'COR_NB_DG_LON', 'COR_NB_MN_LON', 'COR_NB_SC_LON', 'COR_CD_EW_LON'])
print(ssaenpt.shape)

fig = px.scatter_map(ssaenpt,
                     hover_name='ADR_LB_LIEU',
                     hover_data=['DTE_EN_SERVICE','SUP_NM_HAUT', 'ADR_NM_CP'],
                     lat='latitude',
                     lon='longitude',
                     map_style="satellite-streets",
                     )
fig.update_traces(cluster=dict(enabled=True, maxzoom=10), )
fig.show(renderer="browser")
print(ssaenpt)