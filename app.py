import streamlit as st
from google import genai
from google.genai import types

# --- 1. 페이지 설정 및 와이드 레이아웃 ---
st.set_page_config(
    page_title="하이틴 진로·직업 종합 진단 솔루션",
    page_icon="🎯",
    layout="wide"
)

# 화사한 네온 파스텔 톤 기반의 전문 진단 솔루션 시스템 CSS 커스텀
st.markdown("""
<style>
    /* 전체 배경: 은은하고 미래지향적인 파스텔 오로라 그라데이션 */
    .stApp {
        background: linear-gradient(125deg, #f3f4f6 0%, #eef2ff 50%, #f5f3ff 100%);
        color: #1e293b;
    }
    
    /* 프로그램 상단 헤더 폰트 및 배경 커스텀 */
    .header-container {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.2);
    }
    
    .main-title {
        font-size: 2.4rem !important;
        font-weight: 900;
        color: #ffffff !important;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .sub-title {
        color: #e0e7ff;
        font-size: 1.1rem;
        margin-top: 8px;
        margin-bottom: 0;
        font-weight: 500;
        opacity: 0.9;
    }

    /* 좌우 분할 구조용 글래스모피즘(Glassmorphism) 카드 디자인 */
    .program-card {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 20px 40px -15px rgba(99, 102, 241, 0.08);
        padding: 25px;
        margin-bottom: 20px;
    }
    
    /* 섹션 대타이틀 강조 */
    .section-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #4f46e5;
        margin-bottom: 15px;
    }

    /* 대화창 영역 투명화 및 테두리선 조절 */
    div[data-testid="stVerticalBlock"] > div:has(div.stChatMessage) {
        background: transparent !important;
        box-shadow: none !important;
        padding: 0px !important;
    }
    
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.08) !important;
        border-radius: 16px !important;
        margin-bottom: 12px !important;
        padding: 15px !important;
    }
    
    /* 하단 입력창 라운드형 스타일 */
    div[data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.1) !important;
        background: white !important;
    }
    
    /* 버튼 스타일 디자인 고도화 */
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 프로그램 헤더 ---
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🎯 High-Teen Career Diagnostic Solution</h1>
    <p class="sub-title">✨ 청소년 맞춤형 AI 진로·직업 매핑 및 학업 가이드 시스템 (Ver 3.0)</p>
</div>
""", unsafe_allow_html=True)

# --- 3. API 연결 및 세션 관리 ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 시스템 연동 실패: Secrets에 'GEMINI_API_KEY'를 설정해주세요.")
    st.stop()

@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. 화면 좌우 분할 (프로그램 전용 대시보드 구성) ---
left_col, right_col = st.columns([1, 1.7], gap="large")

# --- [좌측 섹션] 기초 진단 정보 조건 설계 ---
with left_col:
    st.markdown('<div class="program-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 1. 학생 인적 정보 입력</div>', unsafe_allow_html=True)
    school_level = st.selectbox(
        "현재 소속 / 학년", 
        ["중학교 1~2학년", "중학교 3학년", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"]
    )
    
    st.markdown('<div class="section-title" style="margin-top:25px;">🧩 2. 흥미 및 관심사 분석 (최대 4개)</div>', unsafe_allow_html=True)
    interests = st.multiselect(
        "좋아하는 테마를 선택해 주세요.", 
        [
            "💻 AI·SW·소프트웨어 개발", "🎨 일러스트·영상 콘텐츠·디자인",
            "📝 웹소설·방송 대본·스토리텔링", "🧬 의학·생명과학·바이오",
            "🔭 우주·항공·첨단 로봇공학", "🧪 신소재·화학·에너지 환경",
            "📊 경제·경영·스타트업 창업", "⚖️ 법률·정치·외교·사회 정의",
            "🧠 심리학·상담·아동 교육", "🎬 미디어 엔터테인먼트·K-POP 콘텐츠",
            "📈 금융 투자·빅데이터 분석", "🌍 어학·글로벌 문화·관광"
        ],
        max_selections=4
    )
    
    st.markdown('<div class="section-title" style="margin-top:25px;">⚡ 3. 주력 직업 강점 인자</div>', unsafe_allow_html=True)
    user_strength = st.radio(
        "본인에게 가장 가깝다고 느끼는 강점을 선택하세요.",
        ["수학적/논리적 문제 해결", "풍부한 상상력과 창의력", "말하기와 소통/공감 능력", "집요한 데이터 수집과 꼼꼼함", "강한 리더십과 팀 지휘력"]
    )
    
    st.markdown("---")
    if st.button("🔄 진단 세션 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [우측 섹션] 종합 매핑 분석 및 결과실 리포트 ---
with right_col:
    st.markdown('<div class="program-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 4. 맞춤형 직업 추천 결과 리포트</div>', unsafe_allow_html=True)
    
    # 초깃값 상태의 안내 카드 (텍스트를 짧게 수정하여 누락 차단)
    if not st.session_state.messages:
        st.info("💡 좌측 정보를 기입한 뒤 아래에 질문을 입력하시면 진단 리포트가 생성됩니다.")

    # 기존 리포트 내역 디스플레이
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 분석 요청 입력창
    if prompt := st.chat_input("진로 질문, 학과 문의, 고교학점제 이수 과목 고민을 입력하세요."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 분석 및 답변 도출 엔진 가동
        with st.chat_message("assistant"):
            with st.spinner("학생의 커리어 스펙트럼 데이터를 분석하여 정밀 보고서를 작성 중입니다..."):
                
                # 정밀 진단 시스템 전용 특화 프롬프트 설계
                system_instruction = f"""
                당신은 대한민국 고등/중등 교육과정을 마스터한 청소년 종합 진로·직업 정밀 진단 시스템입니다.
                사용자 데이터(소속 학년: {school_level}, 핵심 관심사: {', '.join(interests) if interests else '종합 탐색 중'}, 메인 역량: {user_strength})를 고도 분석한 뒤 문서 결과 리포트 체계로 출력하세요.
                
                [결과 리포트 출력 규격]
                1. 📊 [종합 다차원 분석]: 관심사와 역량을 크로스 매핑하여 어떠한 유망 잠재력을 가진 학생 인재인지 2줄 명확 요약.
                2. 🎯 [최적 매핑 직업 BEST 3]: 시장 가치 및 트렌드를 포함한 구체적 명칭과 명확한 선정이유 도출.
                3. 🚀 [미래 교육과정 로드맵]: 고교학점제 선택 과목 가이드 혹은 추천 진로 동아리/관련 학과 목록 제안.
                
                텍스트는 정돈된 구조적 어조로 작성하되, 학생이 주도적 자신감을 키우도록 이모지와 마크다운 형식을 다채롭게 변형 적용해 아름답게 끝맺으십시오.
                """
                
                try:
                    chat_history = [system_instruction]
                    for m in st.session_state.messages[-5:]:
                        chat_history.append(f"{m['role']}: {m['content']}")
                    
                    # 안정적인 고성능 gemini-2.5-flash 모델 사용 및 config 내 토큰 제한 완전 제거
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents="\n".join(chat_history) + f"\nuser: {prompt}",
                        config=types.GenerateContentConfig(
                            temperature=0.65
                        )
                    )
                    
                    # 도중 뚝 끊기는 버퍼 현상을 원천 방지하기 위한 통짜 즉시 출력 메커니즘
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

                except Exception as e:
                    error_msg = str(e)
                    if "high demand" in error_msg.lower():
                        st.warning("📊 현재 전용 진단 서버 사용자가 많아 혼잡합니다. 잠시 후 재입력 부탁드립니다.")
                    else:
                        st.error(f"시스템 진단 도중 일시 지연 에러가 포착되었습니다: {error_msg}")
    st.markdown('</div>', unsafe_allow_html=True)
