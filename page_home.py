import streamlit as st

# 設定頁面配置 (Set page configuration - 可選，通常在主 app.py 中設定)
# st.set_page_config(layout="wide") 

# --- 1. 頁面標題 (st.title) ---
# st.title(): 你的名字
st.title("陳威齊")

# --- 2. 頁面標頭 (st.header) ---
# st.header(): (例如:"姓名的 GIS 專題")
st.header("陳威齊的 GIS 專題 - 大學生地圖作業")

# --- 3. 頁面內容 (st.write) ---
# st.write(): 一段簡短的自我介紹,以及這個 App 的用途
st.write("""
大家好，我是**王小明**，目前正在進行我的大學生 GIS 課程作業。

這個應用程式（App）的主要用途是**地理資訊視覺化 (GIS Visualization)**。
我利用 Streamlit、Leafmap 和 GeoPandas 等 Python 函式庫，
來讀取、處理並在互動式地圖上呈現地理資料，例如全球國家邊界。
本專題的目標是展示我對地理數據處理和地圖繪製的能力。
""")

# 可選：如果需要，您可以添加一個歡迎圖片或簡單的分隔線
st.markdown("---") 
st.info("請點選左側選單，前往下一頁查看地圖應用。")