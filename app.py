import streamlit as st
from google import genai
from google.genai import types

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(
    page_title="하이틴 커리어 디자이너 AI",
    page_icon="💬",
    layout="centered"  # 챗봇에 가장 최적화된 중앙 집중형 레이아웃
)

# 직업 진단 솔루션 느낌의 세련된 모던 CSS
st.markdown("""
<style>
    /* 전체 배경: 깔끔한 소프트 그레이 */
    .stApp {
        background: #f8fafc;
        color: #0f172a;
    }
    
    /* 상단 통합 헤더 */
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 20px;
        text-align: center;
        border-bottom: 4px solid #10b981;
    }
    
    .main-title {
        font-size: 2rem !important;
        font-weight: 800;
        color: #ffffff !important;
        margin: 0;
    }

    /* 실시간 진단 프로필 대시보드 칩 */
    .status-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .status-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* 챗봇 대화창 레이아웃 최적화 */
    .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    
    /* 대화 입력창 고정 스타일 */
    div[data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid #cbd5e1 !important;
        background: white !important;
    }
    
    /* 초기화 버튼 스타일 */
    .stButton>button {
        border-radius: 20px !important;
        background: #ef4444 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 프로그램 헤더 ---
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🎯 High-Teen Career AI Bot</h1>
</div>
""", unsafe_allow_html=True)

# --- 3. API 연결 및 세션 관리 ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 시스템 연동 실패: Secrets에 'GEMINI_API_KEY'가 누락되었습니다.")
    st.stop()

@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. 상단 컨트롤러: 직업 진단을 위한 유저 조건 설정 ---
st.markdown('<div class="status-box">', unsafe_allow_html=True)
st.markdown('<div class="status-title">📊 실시간 분석 프로필 설정</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.2, 1.2])
with c1:
    school_level = st.selectbox(
        "현재 학년", 
        ["중학교 1~2학년", "중학교 3학년", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"]
    )
with c2:
    interests = st.multiselect(
        "관심 분야 (최대 2개)", 
        ["💻 AI·소프트웨어", "🎨 콘텐츠·디자인", "📝 웹소설·스토리", "🧬 생명과학·바이오", "🔭 로봇·우주공학", "📊 경제·스타트업", "⚖️ 법률·사회정의", "🧠 심리·교육"],
        max_selections=2
    )
with c3:
    user_strength = st.selectbox(
        "나의 핵심 강점",
        ["수학적/논리적 사고", "창의력과 아이디어", "말하기와 소통능력", "꼼꼼한 자료조사", "리더십과 실행력"]
    )

# 대화 초기화 버튼을 상단 우측에 배치
cc1, cc2 = st.columns([4, 1])
with cc2:
    if st.button("🔄 대화 비우기", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 정통 챗봇 대화 리스트 표시 ---
if not st.session_state.messages:
    st.info("👋 안녕하세요! 상단에서 나의 프로필과 관심사를 고른 뒤, 아래 입력창에 **'내 성향에 맞는 직업 추천해줘'** 혹은 진로 고민을 편하게 보내주세요!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. 실시간 챗봇 대화 처리 로직 ---
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 1. 유저 메시지 화면 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI 대답 생성 후 화면에 즉시 적재
    with st.chat_message("assistant"):
        with st.spinner("AI 상담 교사가 답변을 분석 중입니다..."):
            
            # AI에게 역할과 현재 유저 프로필 주입
            system_instruction = f"""
            당신은 대한민국 중고등학생 대상의 청소년 전문 진로·직업 상담 교사입니다.
            현재 대화 중인 학생 정보: 학년={school_level}, 관심분야={', '.join(interests) if interests else '탐색중'}, 강점={user_strength}.
            
            [답변 가이드]
            1. 친절하고 다정하게 존댓말로 답하되 문맥에 맞춰 학생에게 최적화된 직업과 학과, 고교학점제 과목을 추천하세요.
            2. 가독성을 위해 이모지와 불릿포인트를 다채롭게 활용하세요.
            3. 답변이 중간에 절대 끊기지 않도록 구조적이고 확실하게 마무리 지으세요.
            """
            
            try:
                # 대화 내역 누적 전송
                chat_history = [system_instruction]
                for m in st.session_state.messages[-6:]:
                    chat_history.append(f"{m['role']}: {m['content']}")
                
                # 글자 수 제한 없이 통째로 받아오기
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents="\n".join(chat_history) + f"\nuser: {prompt}",
                    config=types.GenerateContentConfig(temperature=0.7)
                )
                
                # 끊김 현상 없는 다이렉트 출력
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                st.error(f"⚠️ 답변을 가져오는 도중 문제가 발생했습니다: {str(e)}")
