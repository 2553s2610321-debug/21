import streamlit as st
from groq import Groq

# --- 1. 페이지 초기 설정 및 디자인 ---
st.set_page_config(
    page_title="하이틴 커리어 가이드 AI",
    page_icon="💬",
    layout="centered"
)

st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1e293b; text-align: center; margin-bottom: 5px; }
    .sub-header { font-size: 1rem; color: #64748b; text-align: center; margin-bottom: 25px; }
    div[data-testid="stExpander"] { background-color: #ffffff; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💬 하이틴 커리어 가이드 AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">청소년 맞춤형 진로·직업 고민 상담실 (무제한 서버)</div>', unsafe_allow_html=True)

# --- 2. API 인증 및 세션 초기화 ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 배포 설정 오류: 외부 Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

@st.cache_resource
def get_groq_client():
    return Groq(api_key=st.secrets["GEMINI_API_KEY"], base_url="https://api.groq.com")

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
        school_level = st.selectbox("현재 학년", ["중학교 1~2학년", "중학교 3학년", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"])
    with col2:
        interest = st.selectbox("가장 관심 있는 분야", ["💻 IT / AI / 소프트웨어", "🎨 예술 / 디자인 / 콘텐츠", "🧬 의학 / 생명과학", "📊 경영 / 마케팅 / 창업", "⚖️ 인문 / 법률 / 사회과학", "🔍 아직 잘 모르겠어요"])
    
    if st.button("🔄 대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 4. 대화 기록 내역 출력 ---
if not st.session_state.messages:
    st.info("👋 안녕하세요! 상단 프로필을 확인하신 후, 하단 입력창에 진로와 학업 고민을 편하게 적어주세요.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. 챗봇 대화 처리 및 예외 핸들링 ---
if prompt := st.chat_input("진로, 학과, 과목 선택 등 고민을 입력하세요..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI 상담 선생님이 고민을 분석하고 있습니다..."):
            
            # 잘림 오류 원천 차단: 한 줄 형태의 프롬프트 구성
            sys_msg = f"당신은 친절한 진로상담 교사입니다. 학생은 {school_level}이며 관심사는 {interest}입니다. 학생의 고민에 따뜻하게 공감하며 한국 교육과정(직업, 학과, 고교학점제 과목)에 맞춰 가독성 좋게 이모지를 섞어 명확히 조언하세요."
            
            try:
                api_messages = [{"role": "system", "content": sys_msg}]
                for m in st.session_state.messages[-4:]:
                    api_messages.append({"role": m["role"], "content": m["content"]})
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-specdec",
                    messages=api_messages,
                    temperature=0.7,
                )
                
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

            except Exception as e:
                st.error(f"⚠️ 대화 연결 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요. (에러: {str(e)})")
