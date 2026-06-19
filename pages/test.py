import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="🌎 Global Top10 Market Cap Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🌎 글로벌 시가총액 TOP10 주식 대시보드")
st.markdown("### 📈 최근 1년 주가 변화 비교")

# 글로벌 시총 상위 기업 (2026 기준 대표 종목)
companies = {
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Saudi Aramco": "2222.SR",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Berkshire Hathaway": "BRK-B"
}

@st.cache_data(ttl=3600)
def load_data():

    end = datetime.today()
    start = end - timedelta(days=365)

    all_data = []
    market_caps = []

    for name, ticker in companies.items():

        try:
            stock = yf.Ticker(ticker)

            hist = stock.history(start=start, end=end)

            if len(hist) == 0:
                continue

            base_price = hist["Close"].iloc[0]

            hist["Normalized"] = (
                hist["Close"] / base_price * 100
            )

            temp = pd.DataFrame({
                "Date": hist.index,
                "Company": name,
                "Performance": hist["Normalized"]
            })

            all_data.append(temp)

            info = stock.fast_info

            market_cap = info.get("market_cap", 0)

            market_caps.append({
                "Company": name,
                "Ticker": ticker,
                "Market Cap($)": market_cap
            })

        except:
            pass

    df = pd.concat(all_data)

    cap_df = pd.DataFrame(market_caps)
    cap_df = cap_df.sort_values(
        "Market Cap($)",
        ascending=False
    )

    return df, cap_df


df, cap_df = load_data()

# ------------------
# 시총 순위
# ------------------

st.subheader("🏆 시가총액 순위")

display_cap = cap_df.copy()

display_cap["Market Cap($)"] = (
    display_cap["Market Cap($)"] / 1_000_000_000
).round(1)

display_cap.columns = [
    "기업",
    "티커",
    "시가총액(십억달러)"
]

st.dataframe(
    display_cap,
    use_container_width=True
)

# ------------------
# 종목 선택
# ------------------

selected = st.multiselect(
    "📌 비교할 기업 선택",
    options=df["Company"].unique(),
    default=df["Company"].unique()
)

filtered = df[df["Company"].isin(selected)]

# ------------------
# Plotly 차트
# ------------------

fig = px.line(
    filtered,
    x="Date",
    y="Performance",
    color="Company",
    title="최근 1년 수익률 비교 (시작값=100)",
    labels={
        "Performance": "수익률 지수",
        "Date": "날짜"
    }
)

fig.update_layout(
    hovermode="x unified",
    height=700,
    legend_title="기업",
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------
# 현재 성과 랭킹
# ------------------

st.subheader("🚀 최근 1년 수익률 순위")

latest = (
    filtered
    .sort_values("Date")
    .groupby("Company")
    .tail(1)
)

latest["1년 수익률(%)"] = (
    latest["Performance"] - 100
).round(2)

ranking = latest[
    ["Company", "1년 수익률(%)"]
].sort_values(
    "1년 수익률(%)",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

st.markdown("---")
st.caption(
    "📊 데이터 출처 : Yahoo Finance (yfinance)"
)
