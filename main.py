import streamlit as st
import random

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🌟 MBTI 진로 추천 시스템",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# CSS 꾸미기
# -----------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
}

.title-box {
    background: linear-gradient(135deg,#667eea,#764ba2);
    padding:25px;
    border-radius:20px;
    text-align:center;
    color:white;
    margin-bottom:20px;
    box-shadow:0 5px 15px rgba(0,0,0,0.2);
}

.result-box{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0 5px 15px rgba(0,0,0,0.15);
    margin-top:20px;
}

.job-card{
    background:linear-gradient(135deg,#84fab0,#8fd3f4);
    padding:15px;
    border-radius:15px;
    margin:8px 0;
    font-size:20px;
    font-weight:bold;
}

.quote-box{
    background:#fff7d6;
    border-left:8px solid orange;
    padding:15px;
    border-radius:10px;
}

.stButton>button{
    background:linear-gradient(135deg,#667eea,#764ba2);
    color:white;
    font-size:20px;
    border:none;
    border-radius:15px;
    padding:10px 25px;
}

.stButton>button:hover{
    background:linear-gradient(135deg,#764ba2,#667eea);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# MBTI 데이터
# -----------------------------
mbti_jobs = {
    "INTJ": {
        "desc":"🧠 전략적 사고와 분석력이 뛰어난 혁신가",
        "jobs":["👨‍💻 AI 개발자","📊 데이터 과학자","🏗️ 건축가","🔬 연구원","📈 경영컨설턴트"]
    },
    "INTP": {
        "desc":"💡 호기심 많고 창의적인 아이디어 뱅크",
        "jobs":["🔬 과학자","💻 프로그래머","📚 교수","🎮 게임개발자","🧪 연구원"]
    },
    "ENTJ": {
        "desc":"👑 리더십이 강한 전략가",
        "jobs":["🏢 CEO","📈 경영컨설턴트","⚖️ 변호사","🏛️ 공무원","💰 투자전문가"]
    },
    "ENTP": {
        "desc":"🚀 창의적이고 도전적인 발명가",
        "jobs":["📢 마케터","🚀 스타트업 창업가","🎤 방송인","💻 IT기획자","🎬 PD"]
    },
    "INFJ": {
        "desc":"🌈 통찰력 있고 사람을 돕는 이상주의자",
        "jobs":["🧑‍🏫 교사","🧠 상담사","✍️ 작가","🌍 NGO활동가","👨‍⚕️ 심리상담사"]
    },
    "INFP": {
        "desc":"🎨 감수성이 풍부한 창작가",
        "jobs":["🎨 디자이너","✍️ 작가","🎵 작곡가","📷 사진작가","🎭 예술가"]
    },
    "ENFJ": {
        "desc":"🤝 사람을 이끄는 따뜻한 리더",
        "jobs":["🧑‍🏫 교사","🎤 강사","👩‍💼 인사담당자","🧠 상담사","🏛️ 정치인"]
    },
    "ENFP": {
        "desc":"🌟 열정적이고 창의적인 활동가",
        "jobs":["📢 광고기획자","🎤 유튜버","🎬 방송작가","🎭 배우","📚 강사"]
    },
    "ISTJ": {
        "desc":"📋 책임감 있고 체계적인 관리자",
        "jobs":["🏛️ 공무원","📊 회계사","⚖️ 법무사","👮 경찰관","🏦 은행원"]
    },
    "ISFJ": {
        "desc":"💖 성실하고 배려심 많은 수호자",
        "jobs":["👩‍⚕️ 간호사","🧑‍🏫 교사","🏥 의료기사","📚 사서","👶 사회복지사"]
    },
    "ESTJ": {
        "desc":"📢 조직을 이끄는 실무형 리더",
        "jobs":["👔 관리자","🏛️ 공무원","📈 경영자","👮 경찰간부","🏦 금융인"]
    },
    "ESFJ": {
        "desc":"😊 친절하고 협력적인 조정자",
        "jobs":["🧑‍🏫 교사","🏥 간호사","👩‍💼 HR전문가","🎉 행사기획자","🤝 사회복지사"]
    },
    "ISTP": {
        "desc":"🔧 문제 해결에 능한 실용가",
        "jobs":["✈️ 파일럿","🔧 엔지니어","🚗 자동차전문가","💻 개발자","🚒 소방관"]
    },
    "ISFP": {
        "desc":"🎨 감각적이고 자유로운 예술가",
        "jobs":["🎨 디자이너","📷 사진작가","🎵 음악가","💄 뷰티전문가","🎭 배우"]
    },
    "ESTP": {
        "desc":"⚡ 행동력이 뛰어난 모험가",
        "jobs":["💼 영업전문가","🎤 방송인","🚓 경찰관","🏆 스포츠선수","📢 마케터"]
    },
    "ESFP": {
        "desc":"🎉 에너지 넘치는 엔터테이너",
        "jobs":["🎤 가수","🎭 배우","🎬 방송인","🏆 스포츠선수","🎉 이벤트기획자"]
    }
}

quotes = [
    "🌟 꿈은 이루어지는 것이 아니라 이루어 가는 것이다.",
    "🚀 오늘의 작은 노력이 미래의 큰 성공을 만든다.",
    "💪 실패는 성공으로 가는 과정이다.",
    "🌈 자신을 믿는 순간 가능성이 시작된다.",
    "🏆 가장 큰 경쟁자는 어제의 나 자신이다."
]

# -----------------------------
# 제목
# -----------------------------
st.markdown("""
<div class='title-box'>
<h1>🚀 MBTI 진로 탐험대 🌈</h1>
<h3>나의 성격유형으로 알아보는 미래 직업 찾기 💼</h3>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# MBTI 선택
# -----------------------------
st.subheader("📝 나의 MBTI를 선택해 보세요!")

mbti = st.selectbox(
    "👇 MBTI 선택",
    list(mbti_jobs.keys())
)

# -----------------------------
# 결과 버튼
# -----------------------------
if st.button("🔍 추천 직업 보기"):
    info = mbti_jobs[mbti]

    st.markdown(
        f"""
        <div class='result-box'>
        <h2>🎉 당신의 MBTI는 {mbti} 입니다!</h2>
        <h4>{info['desc']}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🌟 추천 직업 TOP 5")

    for job in info["jobs"]:
        st.markdown(
            f"<div class='job-card'>{job}</div>",
            unsafe_allow_html=True
        )

    st.balloons()

    st.markdown("---")

    st.markdown(
        f"""
        <div class='quote-box'>
        <h4>💡 오늘의 진로 명언</h4>
        <p>{random.choice(quotes)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# 하단
# -----------------------------
st.markdown("---")
st.markdown(
    """
    <center>
    <h4>🎓 미래를 준비하는 여러분을 응원합니다! 🚀🌈✨</h4>
    <p>MBTI는 참고 자료일 뿐, 진로는 여러분의 꿈과 노력으로 만들어집니다. 💖</p>
    </center>
    """,
    unsafe_allow_html=True
)
