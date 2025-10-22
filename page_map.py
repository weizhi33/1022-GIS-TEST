# page_map.py (這是您最終的地圖檔案)

import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# ----------------------------------------------------------------------------
# 1. 頁面配置
# ----------------------------------------------------------------------------
# 設置全寬模式 (建議只在主程式 st.set_page_config 中設置一次)
try:
    st.set_page_config(layout="wide")
except:
    pass 

st.title("第 2 頁 (page_map.py): 互動地圖瀏覽器 - 世界國家邊界")
st.markdown("---")

# ----------------------------------------------------------------------------
# 2. 數據源定義 (使用老師提供的 Natural Earth 穩定 URL)
# ----------------------------------------------------------------------------
# GeoPandas 直接從遠端 ZIP URL 讀取 Shapefile
VECTOR_URL = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip" 
VECTOR_NAME = "世界國家邊界 (Natural Earth)"

# 設置全球地圖的中心和縮放級別
MAP_CENTER = [23.8, 0] # 將中心稍微往西移，讓亞洲更居中
MAP_ZOOM = 2 # 縮放級別調小，以便看到全世界

# ----------------------------------------------------------------------------
# 3. 核心地圖載入與顯示函數
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner="正在從遠端載入 Natural Earth 數據...")
def load_geodata(url):
    """
    使用 Streamlit 緩存，從遠端 URL 讀取 Shapefile (ZIP 壓縮)。
    """
    st.info(f"正在從 URL 讀取 Shapefile: {url}")
    gdf = gpd.read_file(url)
    return gdf

def load_and_display_map():
    """載入 GeoData 並使用 Leafmap 繪製地圖。"""
    
    # 嘗試載入數據
    try:
        gdf = load_geodata(VECTOR_URL)
        st.success("數據成功載入！") #
        
    except Exception as e:
        st.error(f"數據載入失敗！請檢查您的網絡連線。錯誤：`{e}`")
        return 

    # --- 數據概覽顯示 ---
    st.subheader("數據概覽 (前 5 行)")
    
    # Natural Earth 數據通常有 'NAME' 欄位
    potential_cols = ['NAME', 'name', 'ADMIN']
    primary_col = next((col for col in potential_cols if col in gdf.columns), gdf.columns[0])
    
    cols_to_display = [col for col in gdf.columns if col != 'geometry'][:5]
    if primary_col not in cols_to_display:
        cols_to_display.insert(0, primary_col)
    cols_to_display = [col for col in cols_to_display if col != 'geometry']
    
    st.dataframe(gdf[cols_to_display].head(), use_container_width=True)

    # --- 建立 Leafmap 地圖 ---
    st.subheader("Leafmap 互動地圖顯示 - 世界國家邊界")
    
    m = leafmap.Map(
        center=MAP_CENTER, 
        zoom=MAP_ZOOM,
        tiles='OpenStreetMap' 
    ) 
    
    # --- GeoDataFrame 加入地圖 ---
    tooltip_col = primary_col
    
    try:
        m.add_gdf(
            gdf,
            layer_name=VECTOR_NAME,
            # 自定义样式：透明填充和灰色邊框
            style={"fillOpacity": 0.0, "color": "gray", "weight": 0.5, "fillColor": "none"},
            
            # 💡 關鍵修正：直接傳遞 GeoDataFrame 的屬性 (Pandas DataFrame 部分)
            # 解決 'tooltip_initializer' 錯誤
            tooltip=gdf[[tooltip_col]], 
            
            highlight=True,
        )

        m.add_layer_control()
        m.to_streamlit(height=700)

    except Exception as e:
        st.error(f"地圖繪製失敗。錯誤：`{e}`")


# ----------------------------------------------------------------------------
# 4. 執行主函數
# ----------------------------------------------------------------------------
load_and_display_map()