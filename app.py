import streamlit as st
# 1. o st.Page() ÿ¿¯
# ÿst.Page() ¯×~ .py þ
# Emoji Wÿhttps://tw.piliapp.com/emoji/list/
pages = [
st.Page("page_home.py", title="\¿¿", icon="🐼"),
st.Page("page_map.py", title="×W½", icon="🦘"),
st.Page("page_about.py", title="sQ", icon="🌵")
]
# 2. o st.navigation() ½ (Ït)
with st.sidebar:
st.title("App ½")
# st.navigation() Þóö¿¯
selected_page = st.navigation(pages)
# 3. ¯ö¿¯
selected_page.run()