import streamlit as st
# 1.使用 st.Page() ÿ¿¯
# 注意：st.Page() 會自動尋找.py 檔案
# Emoji Wÿhttps://tw.piliapp.com/emoji/list/
pages = [
st.Page("page_home.py", title="關於我"),
st.Page("page_map.py", title="地圖"),
st.Page("page_about.py", title="不確定")
]
# 2.使用 st.navigation() 建立導覽 (例如在側邊攔)
with st.sidebar:
    st.title("App 導覽")
# st.navigation() 會回傳被選擇的葉面
selected_page = st.navigation(pages)
#執行被選擇的葉面
selected_page.run()