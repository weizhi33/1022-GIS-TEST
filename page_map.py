# pages/map_viewer.py

import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd

st.title("第 2 頁 (map_viewer.py): 互動地圖瀏覽器")
st.markdown("---")

# 向量圖層數據源 (使用一个可靠的全球城市 GeoJSON 示例)
VECTOR_URL = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
VECTOR_NAME = "全球國家邊界 (GeoJSON)"


def load_and_display_map():
    """載入 GeoData 並使用 Leafmap 繪製地圖。"""
    
    st.info(f"正在使用 GeoPandas 載入向量數據: {VECTOR_NAME}...")

    try:
        # 使用 GeoPandas 从 URL 读取数据
        gdf = gpd.read_file(VECTOR_URL)
        
        st.subheader("數據概覽 (前 5 行)")
        # 只显示重要的列，避免表格过长
        st.dataframe(gdf[['ADMIN', 'ISO_A3', 'geometry']].head(), use_container_width=True)

        # --- 建立 Leafmap 地圖 ---
        # Leafmap 建立全宽地图 (layout="wide" 已在 app.py 中设置)
        m = leafmap.Map(center=[0, 0], zoom=1) 
        
        # --- GeoDataFrame 加入地圖 ---
        m.add_gdf(
            gdf,
            layer_name=VECTOR_NAME,
            # 自定义样式：透明填充，黑色边框
            style={"fillOpacity": 0, "color": "black", "weight": 0.5},
            # 开启 Tooltip 和 Highlight，提供交互性
            tooltip=leafmap.tooltip_initializer(gdf[["ADMIN", "ISO_A3"]]),
            highlight=True
        )

        # 添加图层控制
        m.add_layer_control()

        st.subheader("Leafmap 互動地圖顯示")
        # 将地图渲染到 Streamlit 页面
        m.to_streamlit(height=700)
        
    except Exception as e:
        st.error(f"地圖或數據載入失敗。請確認網路連接或依賴庫：`{e}`")
        st.code("pip install geopandas leafmap")


# 执行地图加载函数
load_and_display_map()