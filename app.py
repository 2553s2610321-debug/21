import streamlit as st
from google import genai
from google.genai import types

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
st.markdown('<div class="sub-header">청소년 맞춤형 진로·직업 고민 상담실</div>', unsafe_allow_html=True)

# --- 2. API 인증 및 세션 초기화 ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 배포 설정 오류: 외부 Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_gemini_client()

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
        st.sidebar.success("대화가 초기화되었습니다.")
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
            당신은 청소년 진로 지도 자격증을 보유한 친절하고 유능한 학교 진로 상담 교사입니다.
            현재 상담 중인 학생은 [{school_level}]이며, 관심 분야는 [{interest}]입니다.
            
            [답변 규칙]
            1. 학생의 고민에 따뜻하게 공감해 주며 격려의 말을 건네세요.
            2. 대한민국 교육과정에 맞춰 이해하기 쉬운 단어로 직업, 학과 또는 고교학점제 선택 과목을 조언하세요.
            3. 가독성을 위해 이모지와 줄바꿈, 글머리 기호를 적극적으로 활용하여 답변을 구조화하세요.
            4. 글자 수 제한으로 인해 도중에 답변이 잘리지 않도록 핵심 위주로 명료하게 결론을 맺으세요.
            """
            
            try:
                # 최근 대화 문맥 유지 (최대 4개)
                chat_history = [system_instruction]
                for m in st.session_state.messages[-4:]:
                    chat_history.append(f"{m['role']}: {m['content']}")
                
                # 규칙에 명시된 gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents="\n".join(chat_history) + f"\nuser: {prompt}",
                    config=types.GenerateContentConfig(temperature=0.7)
                )
                
                # 안정적인 일괄 출력 방식
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            # 구글 서버 트래픽 초과(429) 및 일시적 과부하(503) 집중 방어 가이드
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    st.warning("⚠️ 현재 무료 제공량(분당/일일 요청 제한)을 초과했습니다. 약 30초~1분 뒤에 다시 입력해 주시면 정상 작동합니다.")
                elif "503" in error_str or "UNAVAILABLE" in error_str:
                    st.warning("⚠️ 구글 Gemini 서버에 일시적으로 많은 유저가 몰리고 있습니다. 잠시 후 전송 버튼을 다시 눌러주세요.")
                else:
                    st.error(f"⚠️ 대화 연결 중 오류가 발생했습니다. 다시 시도해 주세요. (상세: {error_str})")
