import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(
    page_title="AI 진로 상담 챗봇",
    page_icon="🎓",
    layout="centered"
)

# 2. API 키 설정 및 초기화
if "AIzaSyDP1JHuxE71oZBn2cguVDoCmI8s9SP3q1k" in st.secrets:
    api_key = st.secrets["AIzaSyDP1JHuxE71oZBn2cguVDoCmI8s9SP3q1k"]
else:
    # 로컬 테스트용 (Secrets가 없는 경우)
    api_key = st.sidebar.text_input("Gemini API Key를 입력하세요:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ API Key가 설정되지 않았습니다. Streamlit Secrets에 등록하거나 사이드바에 입력해주세요.")

# 3. 세션 상태(대화 내역) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 🎓 **AI 진로 상담소**에 오신 것을 환영합니다. 현재 어떤 진로 고민을 가지고 계신가요? 무엇이든 편하게 말씀해주세요!"
        }
    ]

# 4. UI 레이아웃 (헤더 및 안내)
st.title("🎓 AI 진로 상담 챗봇")
st.caption("당신의 꿈과 적성을 찾아가는 여정을 함께합니다. 심플하고 명확한 진로 솔루션을 받아보세요.")

# 추천 질문 칩 (사용자 편의성 기능)
st.markdown("💡 **이런 질문은 어떠세요?** (클릭 시 자동 입력)")
col1, col2, col3 = st.columns(3)
preset_question = None

with col1:
    if st.button("IT/AI 분야 직업 추천"):
        preset_question = "컴퓨터와 AI에 관심이 많은데, 앞으로 유망한 IT 직업과 필요한 학과를 추천해줘."
with col2:
    if st.button("문과/이과 진로 고민"):
        preset_question = "제가 문과 성향인지 이과 성향인지 잘 모르겠어요. 적성을 찾을 수 있는 방법을 알려주세요."
with col3:
    if st.button("이직 및 직무 변경"):
        preset_question = "현재 마케팅 일을 하고 있는데, 데이터 분석가로 직무를 전환하려면 뭐부터 준비해야 할까요?"

# 5. 기존 대화 내역 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 6. 사용자 입력 처리 (채팅창 또는 추천 질문 버튼)
user_input = st.chat_input("진로 고민을 입력하세요... (예: 전공이 적성에 안 맞아요)")

if preset_question:
    user_input = preset_question

if user_input:
    # 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not api_key:
            message_placeholder.error("API Key가 필요합니다.")
        else:
            try:
                with st.spinner("AI 상담사가 고민을 분석하고 있습니다..."):
                    # 모델 설정 (gemini-2.5-flash-lite 사용)
                    model = genai.GenerativeModel("gemini-2.5-flash-lite")
                    
                    # 진로 상담에 최적화된 시스템 프롬프트 부여
                    system_instruction = (
                        "당신은 친절하고 전문적인 AI 진로 상담 컨설턴트입니다. "
                        "사용자의 고민을 들으면 다음 규칙에 따라 답변하세요:\n"
                        "1. 사용자의 고민 유형을 공감하며 가볍게 요약해 줄 것.\n"
                        "2. 실질적이고 구체적인 해결 방법(Action Plan)을 제시할 것.\n"
                        "3. 관련된 적합한 직업 및 대학교 학과를 명확하게 추천할 것.\n"
                        "4. 가독성이 좋게 이
