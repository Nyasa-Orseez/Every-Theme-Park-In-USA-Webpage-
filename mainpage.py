import os
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium
from urllib.parse import unquote  # URLデコード用

# ページ設定
st.set_page_config(
    page_title="CS学科マッピング",
    page_icon=":world_map:",
    layout="wide",  # 幅広のレイアウトを使用
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        h1 {
            font-size: 36px !important;
        }
        h2 {
            font-size: 30px !important;
        }
        h3 {
            font-size: 24px !important;  /* st.subheader のサイズ */
        }
        p {
            font-size: 24px !important;
        }
    </style>
""", unsafe_allow_html=True)

# データの読み込み
@st.cache_data
def load_data():
    return pd.read_csv('university_data.csv')

data = load_data()

# サイドバーにメインページとリンク集ページのナビゲーションを追加
st.sidebar.title("Theme parks in US")
st.sidebar.markdown("Those are the theme parks in US with info")
st.sidebar.markdown("---")

# クエリパラメータを取得
params = st.query_params

# URLクエリパラメータからランキングを取得
selected_rank = params.get("rank", [None])[0]
if selected_rank:
    try:
        selected_rank = int(selected_rank)  # ランキングは整数型として扱う
    except ValueError:
        selected_rank = None  # 無効な値の場合はNoneに設定

# 地図の初期化
st.title("Theme Parks in the US (beta)")
st.write("Click on the park icon to see the info")
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)  # アメリカ全体を表示

# 各大学の位置を地図に追加
for _, row in data.iterrows():
    try:
        # アイコンパスを解決
        if "Icon_Path" in data.columns and pd.notna(row["Icon_Path"]):
            icon_path = os.path.join(os.getcwd(), row["Icon_Path"])

            # アイコンファイルの存在確認
            if not os.path.isfile(icon_path):
                st.write(f"File not found: {icon_path}")  # ファイルが存在しない場合
                raise FileNotFoundError(f"Icon file not found: {icon_path}")

            # アイコンを設定
            icon = folium.CustomIcon(icon_path, icon_size=(30, 30))
        else:
            icon = folium.Icon(color="blue", icon="info-sign")

        # ポップアップのスタイルをカスタマイズ
        popup_html = f"""
        <div style="border: 3px solid red; padding: 10px; font-size: 18px; max-width: 300px;">
            <b>{row['University']}</b><br>
            <strong>Rank:</strong> {row['Rank']}<br>
            <strong>Location:</strong> {row['Location']}<br>
        </div>
        """

        # ポップアップにスタイルを適用
        popup = folium.Popup(popup_html, max_width=300)

        # マーカーを地図に追加
        marker = folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup,
            tooltip=row["University"],
            icon=icon
        )

        # URLパラメータに一致する大学があれば、ハイライト
        # if selected_rank and row["Rank"] == selected_rank:
        #     marker.add_to(m)
        #     # 特定の大学が選ばれていれば、その位置を表示
        #     st.subheader(f"{row['University']}")
        #     st.write(f"ランキング（US News）: {row['Rank']}")
        #     st.write(f"Location: {row['Location']}")
        #     st.write(f"Info: {row['Info']}")

        marker.add_to(m)

    except Exception as e:
        st.warning(f"Error with {row['University']} icon: {e}")

# 状態を保持するために session_state を初期化
if "selected_university" not in st.session_state:
    st.session_state["selected_university"] = None

# 地図の表示
st_data = st_folium(m, width=1200, height=800)  # 地図のサイズ

# 地図上のアイコンがクリックされた場合
if st_data["last_object_clicked"]:
    clicked_location = st_data["last_object_clicked"]

    # 緯度経度が一致する大学を探す
    for _, row in data.iterrows():
        if (clicked_location["lat"] == row["Latitude"]) and (clicked_location["lng"] == row["Longitude"]):
            # クリックされた大学をセッション状態に保存
            st.session_state["selected_university"] = {
                "University": row["University"],
                "Rank": row["Rank"],
                "Location": row["Location"],
                "Info": row["Info"]
            }
            break

# アイコンがクリックされた場合の表示
if st.session_state["selected_university"]:
    selected_university = st.session_state["selected_university"]
    st.subheader(f"{selected_university['University']}")
    st.write(f"Number Added (if you got balls): {selected_university['Rank']}")
    st.write(f"Location: {selected_university['Location']}")
    st.write(f"Info: {selected_university['Info']}")

# URLパラメータのランクに一致する大学を表示（ただしアイコンが未クリックの場合のみ）
elif selected_rank:
    for _, row in data.iterrows():
        if row["Rank"] == selected_rank:
            st.subheader(f"{row['University']}")
            st.write(f"ランキング（US News）: {row['Rank']}")
            st.write(f"Location: {row['Location']}")
            st.write(f"Info: {row['Info']}")
            break