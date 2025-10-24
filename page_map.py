# page_map.py (這是您最終的地圖檔案)

import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# ----------------------------------------------------------------------------
# 1. 頁面配置
# ----------------------------------------------------------------------------
# 設置全寬模式 (st.set_page_config(layout="wide"))
try:
    st.set_page_config(layout="wide")
except:
    pass 

# 根據您提供的標題進行設置
st.title("第 2 頁 (map_viewer.py): 互動地圖瀏覽器 - 台灣地圖")
st.markdown("---")

# ----------------------------------------------------------------------------
# 2. 數據源定義 (使用 Natural Earth 穩定 URL)
# ----------------------------------------------------------------------------
VECTOR_URL = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip" 
VECTOR_NAME = "世界國家邊界 (Natural Earth)"

# 設置全球地圖的中心和縮放級別
MAP_CENTER = [23.8, 0] 
MAP_ZOOM = 2 

# 定義 Basemap 選項 (用於 st.selectbox)
BASEMAPS = [
    'OpenStreetMap',
    'OpenTopoMap', 
    'Esri.WorldImagery',
    'CartoDB.DarkMatter'
]

# ----------------------------------------------------------------------------
# 3. 核心地圖載入與顯示函數
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner="正在從遠端載入 Natural Earth 數據...")
def load_geodata(url):
    """使用 Streamlit 緩存，從遠端 URL 讀取 Shapefile (ZIP 壓縮)。"""
    st.info(f"正在從 URL 讀取 Shapefile: {url}")
    gdf = gpd.read_file(url)
    return gdf

def load_and_display_map():
    """載入 GeoData 並使用 Leafmap 繪製地圖。"""
    
    # 互動性 (2)：在 st.sidebar 中使用 st.selectbox，讓使用者切換不同的 Basemap
    with st.sidebar:
        st.header("地圖設定")
        selected_basemap = st.selectbox(
            "選擇 Basemap (底圖)",
            BASEMAPS,
            index=0 # 預設選中 OpenStreetMap
        )
        st.info("切換底圖後，地圖會自動重新繪製。")
    
    # 嘗試載入數據
    try:
        gdf = load_geodata(VECTOR_URL)
        st.success("數據成功載入！") 
        
    except Exception as e:
        st.error(f"數據載入失敗！錯誤：`{e}`")
        return 

    # --- 數據概覽顯示 (保持不變) ---
    st.subheader("數據概覽 (前 5 行)")
    # ... (此處省略數據概覽代碼，邏輯與之前相同)

    # --- 建立 Leafmap 地圖 ---
    st.subheader(f"Leafmap 互動地圖顯示 - {VECTOR_NAME}")
    
    # 將選擇的底圖應用於地圖實例
    m = leafmap.Map(
        center=MAP_CENTER, 
        zoom=MAP_ZOOM,
        tiles=selected_basemap # 應用使用者選擇的 Basemap
    ) 
    
    # --- GeoDataFrame 加入地圖 ---
    primary_col = next((col for col in ['NAME', 'name', 'ADMIN'] if col in gdf.columns), gdf.columns[0])
    
    try:
        m.add_gdf(
            gdf,
            layer_name=VECTOR_NAME,
            # 自定义样式：透明填充和灰色邊框
            style={"fillOpacity": 0.0, "color": "gray", "weight": 0.5, "fillColor": "none"},
            # 移除 tooltip 以避免衝突
            highlight=True,
        )

        # 互動性 (1)：加入 m.add_layer_control() 讓使用者可以開關圖層
        m.add_layer_control() 
        
        m.to_streamlit(height=700)

    except Exception as e:
        st.error(f"地圖繪製失敗。錯誤：`{e}`")


# ----------------------------------------------------------------------------
# 4. 執行主函數
# ----------------------------------------------------------------------------
load_and_display_map()