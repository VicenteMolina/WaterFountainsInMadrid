import pandas as pd
import geopandas as gpd
from IPython.display import display
import folium
from shapely.geometry import Point, shape

#Loading data from public csv (attached)
fuentes_df = pd.read_csv("Inventario_Fuentes2019.csv", encoding= 'unicode_escape',sep = ';') 

#Cleaing and glanze of latitued and longiuted columns
fuentes_df = fuentes_df.dropna(subset=['LATITUD', 'LONGITUD'])
fuentes_df.dtypes
fuentes_df['LONGITUD'] = pd.to_numeric(fuentes_df.LONGITUD, errors='coerce')
fuentes_df['LATITUD'] = pd.to_numeric(fuentes_df.LATITUD, errors='coerce')

fuentes_df.ESTADO.drop_duplicates()

fuentes_df["ESTADO"] = fuentes_df.ESTADO.str.upper()
fuentes_df["ESTADO"] = fuentes_df["ESTADO"].str.strip()

fuentes_df.ESTADO.drop_duplicates()


#Working with latitude and longitude points
locs_geometry = [Point(xy) for xy in zip(fuentes_df.LONGITUD,
                                         fuentes_df.LATITUD)]
crs = {'init': 'epsg:4326'}
# Coordinate Reference Systems, "epsg:4326" is a common projection of WGS84 Latitude/Longitude
locs_gdf = gpd.GeoDataFrame(fuentes_df, crs=crs, geometry=locs_geometry)

locs_gdf.dropna()


#Details for map in folium
locs_map = folium.Map(location=[40.402051, -3.694083],
                      zoom_start=13, tiles='cartodbpositron')

feature_ea = folium.FeatureGroup(name='EN SERVICIO')
feature_pr = folium.FeatureGroup(name='FUERA DE SERVICIO')

for i, v in locs_gdf.iterrows():
    
    popup = """
    Distrito : <b>%s</b><br>
    Zona Verde o Via Publica : <b>%s</b><br>
    Direccion : <b>%s</b><br>
    Estado : <b>%s</b><br>
    """ % (v['DISTRITO'], v['ZONA VERDE / \nVIA PUBLICA'], v['DIRECCION'], v['ESTADO'])
    
    if v['ESTADO'] == 'EN SERVICIO':
        folium.CircleMarker(location=[v['LATITUD'], v['LONGITUD']],
                            radius=1,
                            tooltip=popup,
                            color='#FFBA00',
                            fill_color='#FFBA00',
                            fill=True).add_to(feature_ea)
    elif v['ESTADO'] == 'FUERA DE SERVICIO':
        folium.CircleMarker(location=[v['LATITUD'], v['LONGITUD']],
                            radius=1,
                            tooltip=popup,
                            color='#087FBF',
                            fill_color='#087FBF',
                            fill=True).add_to(feature_pr)


feature_ea.add_to(locs_map)
feature_pr.add_to(locs_map)
folium.LayerControl(collapsed=False).add_to(locs_map)


display(locs_map)
