import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 1 - 시간")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 진짜 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 컬럼 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


df = load_data()


# --------------------------------------------------
# 그래프 1
# --------------------------------------------------

st.header("그래프 1. 영화별 날짜별 일관객")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list,
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie}의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
    },
)

fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    hovermode="x unified",
    xaxis=dict(
        tickformat="%Y-%m-%d",
    ),
    yaxis=dict(
        tickformat=",",
    ),
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.markdown(
    "### 이 그래프로 알 수 있는 것"
)
st.text_area(
    "내용을 입력하세요.",
    key="graph1_description",
    height=100,
    label_visibility="collapsed",
)


# --------------------------------------------------
# 그래프 2
# --------------------------------------------------

st.divider()
st.header("그래프 2. 기간 내 일관객 합계가 가장 큰 5편")

st.info(
    "이 구역부터 다음 그래프들을 계속 추가할 수 있습니다."
)


# 기간 내 일관객 합계 기준으로 영화 Top 5 선정
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
    .tolist()
)

top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .groupby(["날짜", "영화명"], as_index=False)["일관객"]
    .sum()
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=False,
    title="기간 내 일관객 합계 Top 5 영화의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
        "영화명": "영화",
    },
)

fig2.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis=dict(
        tickformat="%Y-%m-%d",
    ),
    yaxis=dict(
        tickformat=",",
    ),
    legend=dict(
        title="영화",
        groupclick="toggleitem",
    ),
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

st.markdown(
    "### 이 그래프로 알 수 있는 것"
)
st.text_area(
    "내용을 입력하세요.",
    key="graph2_description",
    height=100,
    label_visibility="collapsed",
)


# --------------------------------------------------
# 앞으로 추가할 그래프 영역
# --------------------------------------------------

st.divider()
st.header("그래프 3")

st.caption(
    "다음 그래프를 이 구역에 추가하세요."
)

st.markdown(
    "### 이 그래프로 알 수 있는 것"
)
st.text_area(
    "내용을 입력하세요.",
    key="graph3_description",
    height=100,
    label_visibility="collapsed",
)
# --------------------------------------------------
# 그래프 2
# --------------------------------------------------

st.divider()
st.header("그래프 2. 기간 내 일관객 합계 Top 5")

# 전체 기간의 일관객 합계를 영화별로 계산한 뒤
# 합계가 가장 큰 5편을 선택
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)

# Top 5 영화의 날짜별 일관객 데이터만 추출
top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .groupby(["날짜", "영화명"], as_index=False)["일관객"]
    .sum()
    .sort_values(["날짜", "영화명"])
)

# 다섯 영화를 하나의 선 그래프로 표시
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="일관객 합계 Top 5 영화의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
        "영화명": "영화",
    },
)

# 마우스를 올렸을 때 날짜와 관객 수 표시
fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis=dict(
        tickformat="%Y-%m-%d",
    ),
    yaxis=dict(
        tickformat=",",
    ),
    legend=dict(
        title="영화",
        itemclick="toggle",
        itemdoubleclick="toggleothers",
    ),
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

# --------------------------------------------------
# 그래프 2 설명 입력 영역
# --------------------------------------------------

st.markdown("### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요.",
    key="graph2_description",
    height=100,
    label_visibility="collapsed",
)
