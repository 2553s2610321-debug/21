import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 디자인
st.set_page_config(
    page_title="나의 AI 진로 나침반",
    page_icon="🧭",
    layout="wide"
)

# 커스텀 스타일 (부드러운 블루/네이비 톤의 신뢰감 있는 디자인)
st.markdown("""
    <style>
    .title-container {
        text-align: center;
        padding: 20px;
        background-color: #F0F4F8;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .bot-message {
        background-color: #EBF3FC;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #F1F1F1;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="title-container">
        <h2>🧭 AI 진로 나침반: 맞춤형 커리어 멘토</h2>
        <p>혼자 고민하던 진로, 취업, 전과, 이직 문제를 AI 멘토와 함께 풀어보세요.</p>
    </div>
""", unsafe_allow_html=True)

# 2. API 키 확인 및 클라이언트 초기화
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets에 'GEMINI_API_KEY'를 추가해주세요.")
    st.stop()

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_gemini_client()

# 3. 대화 세션 상태(Session State) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 당신의 진로 고민을 함께 나눌 AI 멘토입니다. 현재 어떤 고민(전공 선택, 이직, 직무 탐색 등)을 가지고 계시나요? 편하게 말씀해 주세요!"}
    ]

# 4. 사이드바: 사용자의 성향 및 상황 미리 정의 (챗봇의 정확도 향상용)
st.sidebar.header("📋 나의 프로필 (선택)")
current_status = st.sidebar.selectbox(
    "현재 신분/상황",
    ["선택 안 함", "중/고등학생", "대학생(취준생)", "재직자(이직 고민)", "기타"]
)

interest_tags = st.sidebar.multiselect(
    "나의 관심 키워드 (중복 가능)",
    ["IT/개발", "디자인/예술", "기획/마케팅", "연구/과학", "교육/상담", "경영/금융", "창업", "안정성 중심", "창의성 중심"],
    max_selections=3
)

if st.sidebar.button("🔄 대화 초기화"):
    st.session_state.messages = [
        {"role": "assistant", "content": "대화가 초기화되었습니다. 새로운 진로 고민을 말씀해 주세요!"}
    ]
    st.rerun()

# 5. 기존 대화 기록 출력
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])
    else:
        st.chat_message("user").write(msg["content"])

# 6. 사용자 입력 처리
if user_input := st.chat_input("진로 고민을 입력하세요... (예: 컴퓨터공학과를 졸업했는데 개발자가 맞는지 모르겠어요.)"):
    
    # 사용자 메시지 화면에 표시 및 세션 저장
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            
            # AI에게 역할과 맥락 부여 (System Instruction 역할 프롬프트 설계)
            context_prompt = f"""
            당신은 따뜻하고 전문적인 진로 및 커리어 컨설턴트입니다. 
            사용자의 고민에 공감해주고, 구체적이고 실현 가능한 조언이나 질문을 던져 스스로 답을 찾도록 도와주세요.
            
            [참고할 사용자 프로필]
            - 현재 상태: {current_status}
            - 관심사: {', '.join(interest_tags) if interest_tags else '미선택'}
            
            [대화 내용]
            """
            
            # 이전 대화 내용 누적하여 프롬프트 구성 (최근 6개 대화 유지로 안정성 확보)
            full_contents = [context_prompt]
            for m in st.session_state.messages[-6:]:
                full_contents.append(f"{'사용자' if m['role'] == 'user' else '멘토'}: {m['content']}")
            
            try:
                # gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents="\n".join(full_contents),
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=800
                    )
                )
                
                ai_response = response.text
                st.write(ai_response)
                
                # AI 메시지 세션 저장
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except APIError as e:
                st.error(f"❌ API 오류가 발생했습니다: {e.message}")
            except Exception as e:
                st.error(f"❌ 예기치 못한 오류가 발생했습니다: {str(e)}")
