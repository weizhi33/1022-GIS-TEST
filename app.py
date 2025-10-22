import streamlit as st

# 最佳实践：统一设置页面配置
st.set_page_config(
    page_title="我的 GIS 專題",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. 使用 st.Page() 定义页面 (确保这些文件存在于您的项目根目录或 pages/ 文件夹)
# 注意：文件名应与您实际的文件名一致，例如 page_home.py
pages = [
    st.Page("page_home.py", title="關於我", icon="🏠"),
    st.Page("page_map.py", title="地圖", icon="🗺️"),
    st.Page("page_about.py", title="不確定", icon="🤔")
]

# 2. 使用 st.navigation() 建立導覽 (在侧边栏中)
# 修复 IndentationError，使用 4 个空格缩进
with st.sidebar:
    st.title("App 導覽") # 确保这里是 4 个空格缩进

    # st.navigation() 会回传被选择的页面
    selected_page = st.navigation(pages)

# **重要修正：删除 selected_page.run()**
# 在使用 st.navigation() 时，Streamlit 会自动运行选中的页面。
# 删除手动调用可以避免 SyntaxError。
# selected_page.run() # <--- 移除这一行！

# 可以在主页面添加一个引导信息
if selected_page.title == "關於我":
    st.markdown("## 歡迎來到 GIS 專題應用")
    st.write("請使用左側導航欄切換頁面。")