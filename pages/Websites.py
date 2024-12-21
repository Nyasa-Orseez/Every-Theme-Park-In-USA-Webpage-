import pandas as pd
import streamlit as st
from urllib.parse import unquote

# ページ設定
st.set_page_config(
    page_title="Websites",
    page_icon=":world_map:",
    layout="wide",  # 幅広のレイアウトを使用
    initial_sidebar_state="expanded",
)

# サイドバーにメインページとリンク集ページのナビゲーションを追加
st.sidebar.title("websites and wikis of theme parks")
st.sidebar.markdown("Websites and wikis of all American themeparks that are operating")

# データの読み込み
@st.cache_data
def load_data():
    return pd.read_csv('university_data.csv')

data = load_data()

# ランキング順に大学を表示
st.title("Websites of Parks")
st.write("Shows All websites and wikis of USA Parks")

# ランキング順でデータをソート
data_sorted = data.sort_values(by="Rank")

# 表形式ではなく、ランキング順に情報を表示
for _, row in data_sorted.iterrows():
    # 大学名リンクを作成（遷移先を/mainpageに変更）
    university_link = f"<a href='/mainpage?rank={row['Rank']}&university={row['University']}&lat={row['Latitude']}&lng={row['Longitude']}'>{row['University']}</a>"

    # 大学名、ランキング、情報、URLの表示
    st.markdown(f"**Rank {row['Rank']}:** {university_link}", unsafe_allow_html=True)
    st.write(f"**Info:** {row['Info']}")
    st.write(f"[Website of park]({row['URL-department']})")
    st.write(f"[Wiki of park]({row['URL-Application1']})")
    st.write("---")