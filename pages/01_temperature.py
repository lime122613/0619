# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------------------------------------------

# 페이지 설정

# ---------------------------------------------------

st.set_page_config(
page_title="서울 기후변화 타임머신",
page_icon="🌍",
layout="wide"
)

# ---------------------------------------------------

# 데이터 로드

# ---------------------------------------------------

@st.cache_data
def load_data():
df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")

```
df["날짜"] = pd.to_datetime(df["날짜"])

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month

return df
```

try:
df = load_data()

except Exception as e:
st.error(f"데이터를 불러올 수 없습니다. 오류: {e}")
st.stop()

# ---------------------------------------------------

# 타이틀

# ---------------------------------------------------

st.title("🌍 서울 기후변화 타임머신")
st.markdown(
"""
## 서울은 지난 100년 동안 얼마나 따뜻해졌을까요?

```
과거의 서울과 현재의 서울을 비교해 보세요!
"""
```

)

# ---------------------------------------------------

# 사이드바

# ---------------------------------------------------

st.sidebar.header("⚙️ 분석 설정")

min_year = int(df["연도"].min())
max_year = int(df["연도"].max())

year_range = st.sidebar.slider(
"연도 범위 선택",
min_year,
max_year,
(min_year, max_year)
)

df_filtered = df[
(df["연도"] >= year_range[0]) &
(df["연도"] <= year_range[1])
]

# ---------------------------------------------------

# 연도별 평균기온

# ---------------------------------------------------

yearly_temp = (
df.groupby("연도")["평균기온"]
.mean()
.reset_index()
)

# ---------------------------------------------------

# 주요 지표

# ---------------------------------------------------

warmest_year = yearly_temp.loc[
yearly_temp["평균기온"].idxmax()
]

coldest_year = yearly_temp.loc[
yearly_temp["평균기온"].idxmin()
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
"📅 관측 시작",
f"{min_year}년"
)

col2.metric(
"🔥 가장 더운 해",
f"{int(warmest_year['연도'])}년",
f"{warmest_year['평균기온']:.1f}℃"
)

col3.metric(
"❄️ 가장 추운 해",
f"{int(coldest_year['연도'])}년",
f"{coldest_year['평균기온']:.1f}℃"
)

col4.metric(
"📊 데이터 수",
f"{len(df):,}"
)

st.divider()

# ---------------------------------------------------

# 출생연도 비교

# ---------------------------------------------------

st.subheader("🕰️ 과거와 현재 비교")

selected_year = st.selectbox(
"비교할 연도를 선택하세요",
sorted(df["연도"].unique())
)

selected_temp = yearly_temp[
yearly_temp["연도"] == selected_year
]["평균기온"].values[0]

latest_year = yearly_temp["연도"].max()

latest_temp = yearly_temp[
yearly_temp["연도"] == latest_year
]["평균기온"].values[0]

change = latest_temp - selected_temp

c1, c2, c3 = st.columns(3)

c1.metric(
f"📆 {selected_year}년",
f"{selected_temp:.2f}℃"
)

c2.metric(
f"🌡️ {int(latest_year)}년",
f"{latest_temp:.2f}℃"
)

c3.metric(
"📈 기온 변화",
f"{change:.2f}℃"
)

if change > 0:
st.success(
f"서울은 {selected_year}년보다 현재 약 {change:.2f}℃ 더 따뜻해졌습니다."
)
else:
st.info(
f"서울은 {selected_year}년보다 현재 약 {abs(change):.2f}℃ 낮습니다."
)

st.divider()

# ---------------------------------------------------

# 연도별 평균기온 그래프

# ---------------------------------------------------

st.subheader("📈 서울 연평균 기온 변화")

fig = px.line(
yearly_temp,
x="연도",
y="평균기온",
markers=True
)

# 추세선

z = np.polyfit(
yearly_temp["연도"],
yearly_temp["평균기온"],
1
)

p = np.poly1d(z)

fig.add_scatter(
x=yearly_temp["연도"],
y=p(yearly_temp["연도"]),
mode="lines",
name="추세선"
)

fig.update_layout(height=600)

st.plotly_chart(
fig,
use_container_width=True
)

# ---------------------------------------------------

# 10년 단위 분석

# ---------------------------------------------------

st.subheader("📊 10년 단위 평균기온 변화")

yearly_temp["10년단위"] = (
yearly_temp["연도"] // 10
) * 10

decade_temp = (
yearly_temp
.groupby("10년단위")["평균기온"]
.mean()
.reset_index()
)

fig2 = px.bar(
decade_temp,
x="10년단위",
y="평균기온",
text_auto=".1f"
)

fig2.update_layout(height=500)

st.plotly_chart(
fig2,
use_container_width=True
)

# ---------------------------------------------------

# 최고기온 TOP10

# ---------------------------------------------------

st.subheader("🔥 역대 최고기온 TOP10")

top_hot = (
df.sort_values("최고기온", ascending=False)
.head(10)
)

fig3 = px.bar(
top_hot,
x="날짜",
y="최고기온",
text="최고기온"
)

st.plotly_chart(
fig3,
use_container_width=True
)

# ---------------------------------------------------

# 최저기온 TOP10

# ---------------------------------------------------

st.subheader("❄️ 역대 최저기온 TOP10")

top_cold = (
df.sort_values("최저기온")
.head(10)
)

fig4 = px.bar(
top_cold,
x="날짜",
y="최저기온",
text="최저기온"
)

st.plotly_chart(
fig4,
use_container_width=True
)

# ---------------------------------------------------

# 월별 평균기온

# ---------------------------------------------------

st.subheader("📅 월별 평균기온")

monthly = (
df.groupby("월")["평균기온"]
.mean()
.reset_index()
)

fig5 = px.line(
monthly,
x="월",
y="평균기온",
markers=True
)

st.plotly_chart(
fig5,
use_container_width=True
)

# ---------------------------------------------------

# 기후변화 분석 결과

# ---------------------------------------------------

st.subheader("🤖 자동 기후 분석")

first30 = yearly_temp.head(30)["평균기온"].mean()
last30 = yearly_temp.tail(30)["평균기온"].mean()

increase = last30 - first30

overall_change = (
yearly_temp.iloc[-1]["평균기온"]
- yearly_temp.iloc[0]["평균기온"]
)

st.info(
f"""
🌍 서울의 연평균기온은 관측 시작 이후 약 **{overall_change:.2f}℃** 변화했습니다.

🔥 가장 더웠던 해는 **{int(warmest_year['연도'])}년** 입니다.

❄️ 가장 추웠던 해는 **{int(coldest_year['연도'])}년** 입니다.

📈 최근 30년 평균기온은 초기 30년보다 **{increase:.2f}℃** 높습니다.
"""
)

st.caption(
"자료: 서울 기온 관측 데이터 (1907~2026)"
)
