# page_map.py (或您的地圖檔案名稱)

import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
# 引入 warnings 用於處理可能的 geopandas 警告
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)


st.title("第 2 頁 (map_viewer.py): 互動地圖瀏覽器 - 台灣地圖")
st.markdown("---")

# ----------------------------------------------------------------------------
# 2. 數據源定義 (已修正為您的本地 Shapefile 路徑)
# ----------------------------------------------------------------------------
# *** 根據您的檔案結構，使用本地 data 資料夾和正確的檔案名 ***
VECTOR_URL = "data/COUNTY_MOI_1140318.shp" 
VECTOR_NAME = "台灣縣市邊界１ (內政部數據)"

# 台灣的中心坐標和合適的縮放級別
TAIWAN_CENTER = [23.8, 120.96]
TAIWAN_ZOOM = 7


# ----------------------------------------------------------------------------
# 3. 核心地圖載入與顯示函數
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner="正在載入地理空間數據...")
def load_geodata(path):
    """
    使用 Streamlit 緩存從本地路徑讀取數據，並處理台灣 Shapefile 常見的編碼問題。
    """
    st.info(f"正在從本地路徑讀取數據: {path}")
    
    # 嘗試預設讀取 (通常是 utf-8)
    try:
        gdf = gpd.read_file(path)
        st.success("數據成功載入 (使用預設編碼)。")
        return gdf
    
    except Exception as e_default:
        # 如果預設編碼失敗，通常是 Big5 (cp950) 的問題
        st.warning(f"預設編碼讀取失敗: {e_default}。嘗試使用 'big5' 編碼...")
        
        try:
            # 嘗試使用 Big5 編碼 (台灣常見的編碼)
            gdf = gpd.read_file(path, encoding='big5')
            st.success("數據成功載入 (使用 big5 編碼)。")
            return gdf
        except Exception as e_big5:
            # 如果 Big5 也失敗，則拋出最原始的錯誤
            st.error(f"Big5 編碼讀取再次失敗。請檢查您的 Shapefile 文件是否完整。")
            raise e_big5

def load_and_display_map():
    """載入 GeoData 並使用 Leafmap 繪製地圖。"""
    
    # 嘗試載入數據
    try:
        gdf = load_geodata(VECTOR_URL)
        
    except Exception as e:
        # 捕獲最上層的數據載入錯誤
        st.error(f"數據載入失敗！請確認：1. {VECTOR_URL} 路徑正確；2. Shapefile 文件完整。錯誤：`{e}`")
        return 

    # --- 數據概覽顯示 ---
    st.subheader("數據概覽 (前 5 行)")
    
    # 動態檢查 GeoDataFrame 的欄位 (內政部資料可能用中文欄位名)
    potential_cols = ['COUNTYNAME', 'TOWNNAME', 'NAME', '縣市名稱', '縣市名', 'C_NAME']
    primary_col = next((col for col in potential_cols if col in gdf.columns), gdf.columns[0])
    
    # 確保只顯示少數幾列 (不顯示 geometry)
    cols_to_display = [col for col in gdf.columns if col != 'geometry'][:5]
    if primary_col not in cols_to_display:
        cols_to_display.insert(0, primary_col)
    cols_to_display = [col for col in cols_to_display if col != 'geometry']
    
    st.dataframe(gdf[cols_to_display].head(), use_container_width=True)

    # --- 建立 Leafmap 地圖 ---
    st.subheader("Leafmap 互動地圖顯示 - 台灣")
    
    # 使用 foliumap 模組
    m = leafmap.Map(
        center=TAIWAN_CENTER, 
        zoom=TAIWAN_ZOOM,
        tiles='OpenStreetMap' 
    ) 
    
    # --- GeoDataFrame 加入地圖 ---
    tooltip_col = primary_col # 繼續使用找到的第一個欄位作為 Tooltip 
    
    try:
        m.add_gdf(
            gdf,
            layer_name=VECTOR_NAME,
            # 自定义样式：輕微填充，黑色邊框
            style={"fillOpacity": 0.5, "color": "black", "weight": 1.0, "fillColor": "lightblue"},
            # 設置 Tooltip 顯示欄位
            tooltip=leafmap.tooltip_initializer(gdf[[tooltip_col]]),
            highlight=True,
        )

        m.add_layer_control()

        # 將地圖渲染到 Streamlit
        m.to_streamlit(height=700)

    except Exception as e:
        # 捕獲地圖繪製或數據格式化錯誤
        st.error(f"地圖繪製失敗。錯誤：`{e}`")
        st.warning("如果 Shapefile 載入成功但繪製失敗，可能是投影系統 (CRS) 不兼容。")


# ----------------------------------------------------------------------------
# 4. 執行主函數
# ----------------------------------------------------------------------------
load_and_display_map()