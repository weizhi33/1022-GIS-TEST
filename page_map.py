# pages/map_viewer.py

import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# ----------------------------------------------------------------------------
# 1. 頁面配置
# ----------------------------------------------------------------------------
# 建議在啟動時設置一次 (例如在主 App.py 中)，但如果沒有，可以在這裡確保寬屏
# st.set_page_config(layout="wide")

st.title("第 2 頁 (map_viewer.py): 互動地圖瀏覽器 - 台灣地圖")
st.markdown("---")

# ----------------------------------------------------------------------------
# 2. 數據源定義 (替換為一個可用的 GeoJSON URL)
# ----------------------------------------------------------------------------
# 🚨 舊 URL 發生 404 錯誤，請使用以下 URL 替換：
VECTOR_URL = "https://raw.githubusercontent.com/gishub/leafmap/master/examples/data/taiwan_counties.geojson" 
VECTOR_NAME = "台灣縣市邊界 (Leafmap 範例數據)"

# 台灣的中心坐標和合適的縮放級別
TAIWAN_CENTER = [23.8, 120.96]
# TAIWAN_ZOOM 保持不變

# ----------------------------------------------------------------------------
# 3. 核心地圖載入與顯示函數
# ----------------------------------------------------------------------------
@st.cache_data
def load_geodata(url):
    """使用 Streamlit 緩存來避免每次運行都重新下載和讀取數據。"""
    st.info(f"正在從 URL 讀取數據: {url}")
    # 使用 GeoPandas 从 URL 读取数据
    gdf = gpd.read_file(url)
    return gdf

def load_and_display_map():
    """載入 GeoData 並使用 Leafmap 繪製地圖。"""
    
    # 嘗試載入數據
    try:
        gdf = load_geodata(VECTOR_URL)
        
    except Exception as e:
        st.error(f"數據載入失敗。請檢查您的網絡或 GeoJSON URL 是否有效。錯誤：`{e}`")
        st.warning(f"當前使用的 URL：{VECTOR_URL}")
        return # 數據失敗則停止執行地圖繪製

    # --- 數據概覽顯示 ---
    st.subheader("數據概覽 (前 5 行)")
    
    # 動態檢查 GeoDataFrame 的欄位
    # 這裡假設 GeoJSON 數據包含 'COUNTYNAME' (縣市名稱) 或 'NAME'
    primary_col = next((col for col in ['COUNTYNAME', 'name', 'NAME'] if col in gdf.columns), gdf.columns[0])
    
    # 確保只顯示少數幾列，且不顯示 geometry (GeoPandas 的默認顯示可能很慢)
    cols_to_display = [col for col in gdf.columns if col != 'geometry'][:5]
    if primary_col not in cols_to_display:
        cols_to_display.insert(0, primary_col)

    st.dataframe(gdf[cols_to_display].head(), use_container_width=True)

    # --- 建立 Leafmap 地圖 ---
    st.subheader("Leafmap 互動地圖顯示 - 台灣")
    
    # 使用 foliumap 模組
    m = leafmap.Map(
        center=TAIWAN_CENTER, 
        zoom=TAIWAN_ZOOM,
        # 可以指定一個台灣常用的底圖，例如 OpenStreetMap
        tiles='OpenStreetMap' 
    ) 
    
    # --- GeoDataFrame 加入地圖 ---
    # Tooltip 使用我們找到的第一個主要欄位
    tooltip_col = primary_col
    
    try:
        m.add_gdf(
            gdf,
            layer_name=VECTOR_NAME,
            # 自定义样式：輕微填充，黑色邊框
            style={"fillOpacity": 0.5, "color": "black", "weight": 1.0, "fillColor": "lightblue"},
            # 設置 Tooltip 顯示欄位
            tooltip=leafmap.tooltip_initializer(gdf[[tooltip_col]]),
            highlight=True,
            # 添加 Legend (如果有分類的話，這裡先不加，保持簡潔)
        )

        m.add_layer_control()

        # 將地圖渲染到 Streamlit
        m.to_streamlit(height=700)

    except Exception as e:
        # 捕獲地圖繪製或數據格式化錯誤
        st.error(f"地圖繪製失敗，可能是 GeoDataFrame 結構問題。錯誤：`{e}`")
        st.warning("請確保 GeoDataFrame 的 'geometry' 列是有效的地理空間數據。")


# ----------------------------------------------------------------------------
# 4. 執行主函數
# ----------------------------------------------------------------------------
# 這是確保函數被呼叫並執行的關鍵步驟
load_and_display_map()