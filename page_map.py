import streamlit as st
import leafmap.foliumap as leafmap
st.set_page_config(layout="wide") # Wÿ¿¯
st.title("Leafmap ×W½")
# 1. W{þ (m)
# center=[, ], zoom=
m = leafmap.Map(center=[24.0, 121.0], zoom=7) # 
# 2. (ÿ)  m Nò/W
m.add_basemap("OpenTopoMap") # W (OpenTopoMap )
# 3. W{þ Streamlit
m.to_streamlit(height=600)
