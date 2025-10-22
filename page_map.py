import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd # / GeoPandas
st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (Uß)")
# --- 1. o GeoPandas × ---
# o Natural Earth 110m cultural vectors ö .zip þ
url =
"https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zi
p"
# GeoPandas ÿïß URL × .zip þ
gdf = gpd.read_file(url)
# (o) ovrß
st.dataframe(gdf.head())
# --- 2. W ---
m = leafmap.Map(center=[0, 0])
# --- 3.  GeoDataFrame à/W ---
# o add_gdf() 
m.add_gdf(
gdf,
layer_name="_} (Vector)",
style={"fillOpacity": 0, "color": "black", "weight": 0.5}, # ún}
# highlight=False ößoÿ
# n<\=¿o/ó(Tooltip)öù
highlight=False
)
# à/Wv (óN¿)
m.add_layer_control()
# --- 4. W ---
m.to_streamlit(height=700)
