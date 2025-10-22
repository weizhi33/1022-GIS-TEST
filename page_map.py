import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd # / GeoPandas

st.set_page_config(layout="wide")
st.title("Leafmap + GeoPandas (Uß)")

# --- 1. o GeoPandas × ---
# o Natural Earth 110m cultural vectors ö .zip þ
# 修正了第 8 行的语法错误：确保赋值在同一行
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

# GeoPandas ÿïß URL × .zip þ
gdf = gpd.read_file(url)

# (o) ovrß
st.dataframe(gdf.head())

# --- 2. W ---
# W 是指 Leafmap.Map，这里创建地图对象
m = leafmap.Map(center=[0, 0])

# --- 3.  GeoDataFrame à/W ---
# o add_gdf() 
m.add_gdf(
    gdf,
    layer_name="国家边界 (Vector)", # 假设 layer_name 是“国家边界”的中文或您想表示的含义
    style={"fillOpacity": 0, "color": "black", "weight": 0.5}, # 轮廓样式
    # highlight=False ößoÿ
    # n<\=¿o/ó(Tooltip)öù
    highlight=False
)

# à/Wv (óN¿)
m.add_layer_control()

# --- 4. W ---
# W 是指 Streamlit 上的地图显示
m.to_streamlit(height=700)