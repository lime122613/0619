import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="서울 기후변화 타임머신",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:48px;
    font-weight:bold;
}

.sub-title{
    text-align:center;
    font-size:22px;
    color:gray;
}

.metric-card{
    padding:15px;
    border-radius:10px;
    background-color:#f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv(
            "ta_20260619190504.csv",
            sep="\t"
        )
    except:
        df = pd.read_csv(
            "ta_20260619190504.csv"
        )

    df.columns = df.columns.str.strip()

    df["날짜"] = pd.to_datetime(df["날짜"])

    df["평균기온(℃)"] = pd.to_numeric(
        df["평균기온(℃)"],
        errors="coerce"
    )

    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"],
        errors="coerce"
    )

    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"],
        errors="coerce"
    )

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month

    return df


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러올 수 없습니다.\n\n{e}")
    st.stop()

# --------------------------------------------------
# 제목
# --------------------------------------------------
st.markdown(
    '<p class="main-title">🌍 서울 기후변화 타임머신</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">서울은 지난 100년 동안 얼마나 따뜻해졌을까요?</p>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# 연도별 평균기온 계산
# --------------------------------------------------
yearly = (
    df.groupby("연도")["평균기온(℃)"]
    .mean()
    .reset_index()
)

# --------------------------------------------------
# 주요 통계
# --------------------------------------------------
warmest = yearly.loc[
    yearly["평균기온(℃)"].idxmax()
]

coldest = yearly.loc[
    yearly["평균기온(℃)"].idxmin()
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📅 관측 시작",
    f"{int(df['연도'].min())}년"
)

col2.metric(
    "🔥 가장 더운 해",
    f"{int(warmest['연도'])}년",
    f"{warmest['평균기온(℃)']:.1f}℃"
)

col3.metric(
    "❄️ 가장 추운 해",
    f"{int(coldest['연도'])}년",
    f"{coldest['평균기온(℃)']:.1f}℃"
)

col4.metric(
    "📊 관측일수",
    f"{len(df):,}일"
)

st.divider()

# --------------------------------------------------
# 과거와 현재 비교
# --------------------------------------------------
st.subheader("🕰️ 과거와 현재 비교")

selected_year = st.selectbox(
    "비교할 연도를 선택하세요",
    sorted(yearly["연도"].unique())
)

selected_temp = yearly.loc[
    yearly["연도"] == selected_year,
    "평균기온(℃)"
].iloc[0]

latest_year = yearly["연도"].max()

latest_temp = yearly.loc[
    yearly["연도"] == latest_year,
    "평균기온(℃)"
].iloc[0]

change = latest_temp - selected_temp

a, b, c = st.columns(3)

a.metric(
    f"{selected_year}년",
    f"{selected_temp:.2f}℃"
)

b.metric(
    f"{latest_year}년",
    f"{latest_temp:.2f}℃"
)

c.metric(
    "기온 변화",
    f"{change:+.2f}℃"
)

if change > 0:
    st.success(
        f"🌡️ 서울은 {selected_year}년보다 현재 평균적으로 {change:.2f}℃ 더 따뜻해졌습니다."
    )
else:
    st.info(
        f"서울은 {selected_year}년보다 현재 평균적으로 {abs(change):.2f}℃ 낮습니다."
    )

st.divider()

# --------------------------------------------------
# 연평균 기온 변화
# --------------------------------------------------
st.subheader("📈 서울 연평균기온 변화")

fig = px.line(
    yearly,
    x="연도",
    y="평균기온(℃)",
    markers=True
)

z = np.polyfit(
    yearly["연도"],
    yearly["평균기온(℃)"],
    1
)

trend = np.poly1d(z)

fig.add_scatter(
    x=yearly["연도"],
    y=trend(yearly["연도"]),
    mode="lines",
    name="추세선"
)

fig.update_layout(height=600)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# 10년 단위 변화
# --------------------------------------------------
st.subheader("📊 10년 단위 평균기온")

yearly["10년단위"] = (
    yearly["연도"] // 10
) * 10

decade = (
    yearly.groupby("10년단위")["평균기온(℃)"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    decade,
    x="10년단위",
    y="평균기온(℃)",
    text_auto=".1f"
)

fig2.update_layout(height=500)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------------------------------------
# 최고기온 TOP10
# --------------------------------------------------
st.subheader("🔥 역대 최고기온 TOP10")

hot10 = (
    df.sort_values(
        "최고기온(℃)",
        ascending=False
    )
    .head(10)
)

fig3 = px.bar(
    hot10,
    x="날짜",
    y="최고기온(℃)",
    text="최고기온(℃)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# --------------------------------------------------
# 최저기온 TOP10
# --------------------------------------------------
st.subheader("❄️ 역대 최저기온 TOP10")

cold10 = (
    df.sort_values(
        "최저기온(℃)"
    )
    .head(10)
)

fig4 = px.bar(
    cold10,
    x="날짜",
    y="최저기온(℃)",
    text="최저기온(℃)"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# --------------------------------------------------
# 월별 평균기온
# --------------------------------------------------
st.subheader("📅 월별 평균기온")

monthly = (
    df.groupby("월")["평균기온(℃)"]
    .mean()
    .reset_index()
)

fig5 = px.line(
    monthly,
    x="월",
    y="평균기온(℃)",
    markers=True
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# --------------------------------------------------
# AI 분석
# --------------------------------------------------
st.subheader("🤖 기후변화 분석 결과")

first30 = yearly.head(30)["평균기온(℃)"].mean()
last30 = yearly.tail(30)["평균기온(℃)"].mean()

increase = last30 - first30

overall_change = (
    yearly.iloc[-1]["평균기온(℃)"]
    - yearly.iloc[0]["평균기온(℃)"]
)

st.info(
f"""
🌍 서울의 연평균기온은 관측 시작 이후 약 **{overall_change:.2f}℃** 변화했습니다.

🔥 가장 더운 해는 **{int(warmest['연도'])}년** 입니다.

❄️ 가장 추운 해는 **{int(coldest['연도'])}년** 입니다.

📈 최근 30년 평균기온은 초기 30년보다 **{increase:.2f}℃** 높습니다.
"""
)

st.caption("자료 : 서울 기온 관측자료 (1907~2026)")
