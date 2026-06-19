import streamlit as st
from openai import OpenAI

# 1. OpenAI 클라이언트 설정
# 스트림릿 클라우드의 Secrets에 저장된 API 키를 불러옵니다.
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. 웹 앱 화면 구성
st.set_page_config(page_title="감정 맞춤 응원봇", page_icon="🌈")
st.title("🌈 AI 감정 맞춤 위로 & 응원 메시지")
st.write("오늘 하루 어떤 기분인가요? 당신의 감정에 꼭 맞는 따뜻한 한마디를 건네드릴게요!")

# 3. 사용자 입력 받기
name = st.text_input("이름(또는 애칭)을 입력해주세요.", placeholder="예: 지민")
mood = st.text_input("지금 기분이 어떤가요? 편하게 적어주세요.", placeholder="예: 오늘 하루 너무 바빠서 지치고 우울해")

# 4. 버튼 클릭 시 동작
if st.button("응원 메시지 받기"):
    if name and mood:
        with st.spinner("AI가 진심을 담아 메시지를 작성하고 있습니다..."):
            try:
                # OpenAI API 호출 (GPT-4o-mini 모델 사용)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "당신은 사람들의 감정에 깊이 공감하고 따뜻하게 위로와 응원을 건네는 다정한 친구입니다. 3~4문장으로 상황에 맞는 힘이 되는 메시지를 작성해주세요. 이모지도 적절히 사용해주세요."},
                        {"role": "user", "content": f"{name}님이 현재 '{mood}'(이)라는 감정/상태를 느끼고 있습니다. 따뜻하게 공감하고 응원해주세요!"},
                    ],
                    temperature=0.8  # 창의성 조절 (0~2)
                )

                # 결과 출력
                message = response.choices[0].message.content
                st.success(message)
                st.balloons()  # 풍선 애니메이션 효과

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("이름과 현재 기분을 모두 입력해주세요!")
