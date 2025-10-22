# pages/map_viewer.py

import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

st.title("第 2 頁 (map_viewer.py): 互動地圖瀏覽器 - 台灣地圖")
st.markdown("---")

# **新的数据源：台湾行政区划 GeoJSON (示例)**
# 注意：这是一个示例URL，实际使用中您可能需要替换为自己的或官方的 GeoJSON 文件
# 这个示例数据通常包含 'COUNTYNAME'（县市名称）等字段。
VECTOR_URL = "https://raw.githubusercontent.com/g0v/tw-map/master/json/county/taiwan_county_2010.topojson"
# 🚨 注意：这个 URL 是一个 TopoJSON 文件。GeoPandas 可以直接读取，但如果遇到问题，
# 建议换成纯 GeoJSON。这里假设它可以正常读取。
VECTOR_NAME = "台灣縣市邊界"

# 台湾的中心坐标和合适的缩放级别
TAIWAN_CENTER = [23.8, 120.96]
TAIWAN_ZOOM = 7


def load_and_display_map():
    """載入 GeoData 並使用 Leafmap 繪製地圖。"""
    
    st.info(f"正在載入向量數據: {VECTOR_NAME}...")

    try:
        # 使用 GeoPandas 从 URL 读取数据
        gdf = gpd.read_file(VECTOR_URL)

        # **修正错误：动态检查列名**
        # 假设新的台湾数据包含 'COUNTYNAME' (县市名称)
        # 如果没有，我们会尝试使用其他列，避免程序崩溃。
        display_cols = ['COUNTYNAME', 'geometry'] if 'COUNTYNAME' in gdf.columns else gdf.columns.tolist()
        if 'geometry' in display_cols:
             display_cols.remove('geometry')
        display_cols = ['geometry'] + display_cols[:2] # 确保 geometry 在最后，只显示少数几列
        
        st.subheader("數據概覽 (前 5 行)")
        # 使用存在的列进行显示
        st.dataframe(gdf[display_cols].head(), use_container_width=True)

        # --- 建立 Leafmap 地圖 ---
        m = leafmap.Map(center=TAIWAN_CENTER, zoom=TAIWAN_ZOOM) 
        
        # --- GeoDataFrame 加入地圖 ---
        # Tooltip 使用 'COUNTYNAME' 或第一个可用列
        tooltip_col = 'COUNTYNAME' if 'COUNTYNAME' in gdf.columns else gdf.columns[0]
        
        m.add_gdf(
            gdf,
            layer_name=VECTOR_NAME,
            # 自定义样式：灰色填充，黑色边框
            style={"fillOpacity": 0.5, "color": "black", "weight": 1.0, "fillColor": "lightgray"},
            # 开启 Tooltip 和 Highlight
            tooltip=leafmap.tooltip_initializer(gdf[[tooltip_col]]),
            highlight=True
        )

        m.add_layer_control()

        st.subheader("Leafmap 互動地圖顯示 - 台灣")
        m.to_streamlit(height=700)
        
    except Exception as e:
        # **捕获并显示具体的列名错误或网络错误**
        st.error(f"地圖或數據載入失敗。請確認網路連接或依賴庫：錯誤：`{e}`")
        st.warning("如果錯誤包含 'No such file' 或 'HTTP Error'，請檢查上面的數據源 URL 是否有效。")


# 执行地图加载