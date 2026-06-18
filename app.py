import streamlit as st
from groq import Groq

# --- 1. 페이지 초기 설정 및 디자인 ---
st.set_page_config(
    page_title="하이틴 커리어 가이드 AI",
    page_icon="💬",
    layout="centered"
)

# 심플하고 정돈된 스타일을 위한 최소한의 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 25px;
    }
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💬 하이틴 커리어 가이드 AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">청소년 맞춤형 진로·직업 고민 상담실 (무제한 서버)</div>', unsafe_allow_html=True)

# --- 2. API 인증 및 세션 초기화 ---
# 기존 secrets에 등록된 키를 그대로 재활용하거나 새 탭에서 GROQ 키를 넣으시면 됩니다.
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 배포 설정 오류: 외부 Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

@st.cache_resource
def get_groq_client():
    # 호환성을 위해 기존 이름(GEMINI_API_KEY) 변수를 그대로 연동하되, 베이스 주소를 무료 대용량인 groq으로 전환합니다.
    return Groq(
        api_key=st.secrets["GEMINI_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )

try:
    client = get_groq_client()
except Exception as e:
    st.error("API 클라이언트 초기화 실패. 키를 확인해 주세요.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. [상단 제안 기능] 심플 프로필 입력 폼 ---
with st.expander("📊 정밀 진단을 위한 나의 프로필 설정 (클릭하여 열기)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        school_level = st.selectbox(
            "현재 학년",
            ["중학교 1~2학년", "중학교 3학년", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"]
        )
    with col2:
        interest = st.selectbox(
            "가장 관심 있는 분야",
            ["💻 IT / AI / 소프트웨어", "🎨 예술 / 디자인 / 콘텐츠", "🧬 의학 / 생명과학", "📊 경영 / 마케팅 / 창업", "⚖️ 인문 / 법률 / 사회과학", "🔍 아직 잘 모르겠어요"]
        )
    
    # 대화 리셋 기능 
    if st.button("🔄 대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 4. 대화 기록 내역 출력 ---
if not st.session_state.messages:
    st.info("👋 안녕하세요! 상단 프로필을 확인하신 후, 하단 입력창에 '나에게 맞는 직업 추천해줘' 또는 현재 지니고 있는 진로와 학업 고민을 편하게 적어주세요.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. 챗봇 대화 처리 및 예외 핸들링 ---
if prompt := st.chat_input("진로, 학과, 과목 선택 등 고민을 입력하세요..."):
    
    # 유저 입력창 즉시 반영
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("AI 상담 선생님이 고민을 분석하고 있습니다..."):
            
            # 구체적 페르소나 및 입력 조건 주입
            system_instruction = f"""
            당신은 청소년 진로 지도 자격증을 보유한 친절하고 유능한 대한민국 학교의 진로 상담 교사입니다.
            현재 상담 중인 학생은 [{school_level}]이며, 관심 분야는 [{interest}]입니다.
            
            [답변 규칙]
            1. 학생의 고민에 따뜻하게 공감해 주며 격려의 말을 건네세요.
            2. 대한민국 교육과정에 맞춰 이해하기 쉬운 한국어 단어로 직업, 학과 또는 고교학점제 선택 과목을 조언하세요.
            3. 가독성을 위해 이모지와 줄바꿈, 글머리 기호를 적극적으로 활용하여 답변을 구조화하세요.
            4. 결론까지 끊기지 않게 명료하고 체계적으로 완결성 있게 끝맺으세요.
            """
            
            try:
                # 대화 문맥 구축
                api_messages = [{"role": "system", "content": system_instruction}]
                for m in st.session_state.messages[-4:]:
                    api_messages.append({"role": m["role"], "content": m["content"]})
                
                # 무료 한도가 압도적으로 높은 대형 최신 모델 호출
                response = client.chat.completions.create(
                    model="llama-3.3-70b-specdec",  # 대량 호출에 특화된 초고속 70B 모델
                    messages=api_messages,
                    temperature=0.7,
                )
                
                ai_response = response.choices[0].message.content
                
                # 출력 및 세션 저장
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

            except Exception as e:
                st.error(f"⚠️ 대화 연결 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요. (에러: {str(e)})")
