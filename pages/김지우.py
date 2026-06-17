import streamlit as st

try:
    from google import genai
except ImportError:
    st.error("google-genai 라이브러리가 설치되지 않았습니다.")
    st.stop()

st.set_page_config(
    page_title="AI 진로 상담 챗봇",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI 진로 상담 챗봇")
st.caption("진로 고민을 입력하면 AI가 맞춤형 상담을 제공합니다.")

# API Key 확인
api_key = st.secrets.get("AIzaSyDP1JHuxE71oZBn2cguVDoCmI8s9SP3q1k", "")

if not api_key:
    st.warning("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# 채팅 기록
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 😊\n\n"
                "저는 AI 진로 상담사입니다.\n"
                "관심 분야, 성적, 적성, 고민 등을 편하게 이야기해 주세요."
            )
        }
    ]

# 예시 질문
with st.expander("💡 상담 예시"):
    st.write("- 공부를 잘 못하는데 어떤 직업이 좋을까요?")
    st.write("- 컴퓨터를 좋아하는데 어떤 학과를 가면 좋을까요?")
    st.write("- 진로를 아직 정하지 못했어요.")
    st.write("- 디자인 분야에 관심이 있어요.")

# 기존 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("진로 고민을 입력하세요")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("상담 중입니다..."):

            try:
                system_prompt = """
당신은 전문 진로 상담사입니다.

사용자의 고민을 듣고 다음 형식으로 답변하세요.

1. 고민 분석
2. 해결 방법
3. 추천 직업
4. 추천 학과
5. 추가로 생각해볼 질문

친절하고 이해하기 쉽게 설명하세요.
"""

                conversation = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "상담사"
                    conversation += f"{role}: {msg['content']}\n"

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=f"{system_prompt}\n\n{conversation}"
                )

                answer = response.text

            except Exception as e:
                answer = (
                    "AI 응답 중 오류가 발생했습니다.\n\n"
                    f"오류 내용: {e}"
                )

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
