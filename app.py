import streamlit as st
import google.generativeai as genai

# -----------------------------
# API KEY 불러오기
# -----------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API 키를 불러올 수 없습니다. secrets 설정을 확인하세요.")
    st.stop()

# -----------------------------
# 모델 설정
# -----------------------------
MODEL_NAME = "gemini-2.5-flash-lite"

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"모델 초기화 오류: {e}")
    st.stop()

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash-Lite 기반 AI 상담")

# -----------------------------
# 채팅 기록 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 채팅 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
prompt = st.chat_input("연애 고민을 입력하세요...")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        try:
            with st.spinner("답변 생성 중..."):

                # 이전 대화 기록 변환
                history = []

                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"

                    history.append({
                        "role": role,
                        "parts": [msg["content"]]
                    })

                # 채팅 세션 생성
                chat = model.start_chat(history=history)

                # 응답 생성
                response = chat.send_message(
                    f"""
                    너는 공감 능력이 좋은 연애상담 AI야.
                    사용자의 감정을 존중하며 현실적인 조언을 제공해.

                    사용자 질문:
                    {prompt}
                    """
                )

                reply = response.text

                st.markdown(reply)

                # 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

        except Exception as e:
            error_message = f"오류가 발생했습니다: {e}"

            st.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })
