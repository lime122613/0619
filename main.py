# main.py
import streamlit as st
from openai import OpenAI

# 1. OpenAI 클라이언트 설정
# 스트림릿 클라우드의 Secrets에 저장된 API 키를 불러옵니다.
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. 웹 앱 화면 구성
st.set_page_config(page_title="시험 응원봇", page_icon="🍀")
st.title("🍀 AI 시험 응원 메시지 생성기")
st.write("중간고사, 기말고사, 수능 등 중요한 시험을 앞둔 분들께 따뜻한 응원을 전해드려요!")

# 3. 사용자 입력 받기
name = st.text_input("응원받을 사람의 이름(또는 애칭)을 입력해주세요.", placeholder="예: 지민")
exam_name = st.text_input("어떤 시험을 준비하고 있나요?", placeholder="예: 1학기 정보 기말고사")

# 4. 버튼 클릭 시 동작
if st.button("응원 메시지 받기"):
	if name and exam_name:
		with st.spinner("AI가 진심을 담아 메시지를 작성하고 있습니다..."):
			try:
				# OpenAI API 호출 (GPT-4o-mini 모델 사용)
				response = client.chat.completions.create(
					model="gpt-4o-mini",
					messages=\[
						{"role": "system", "content": "당신은 학생들을 진심으로 아끼고 다정하게 격려하는 멘토입니다. 3\~4문장으로 힘이 되는 응원 메시지를 작성해주세요. 이모지도 적절히 사용해주세요."},
						{"role": "user", "content": f"\{name\} 학생이 \{exam_name\}을(를) 준비하고 있습니다. 응원해주세요!"},
					\],
					temperature=0.7  # 창의성 조절 (0\~2)
				)

				# 결과 출력
				message = response.choices\[0\].message.content
				st.success(message)
				st.balloons()  # 풍선 애니메이션 효과

			except Exception as e:
				st.error(f"오류가 발생했습니다: {e}")
	else:
		st.warning("이름과 시험 종류를 모두 입력해주세요!")
