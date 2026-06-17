import streamlit as st
from google import genai
from google.genai import types
import time

# --- 1. 페이지 설정 및 와이드 레이아웃 ---
st.set_page_config(
    page_title="하이틴 진로·직업 종합 진단 솔루션",
    page_icon="📊",
    layout="wide"
)

# 전문 진단 프로그램 느낌의 고급 커스텀 CSS
st.markdown("""
<style>
    /* 전체 배경: 신뢰감을 주는 차분하고 깨끗한 톤 */
    .stApp {
        background: #f8fafc;
        color: #0f172a;
    }
    
    /* 프로그램 상단 헤더 */
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #10b981;
    }
    
    .main-title {
        font-size: 2.2rem !important;
        font-weight: 800;
        color: #ffffff !important;
        margin: 0;
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 5px;
        margin-bottom: 0;
    }

    /* 좌우 섹션 카드화 */
    .program-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
        margin-bottom: 20px;
    }
    
    /* 서브 타이틀 강조 */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* 대화 아이템 커스텀 (프로그램 리포트 느낌) */
    div[data-testid="stVerticalBlock"] > div:has(div.stChatMessage) {
        background: #ffffff !important;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 15px !important;
        box-shadow: none !important;
    }
    
    /* 버튼 세련되게 변경 */
    .stButton>button {
        border-radius: 10px !important;
        background: #10b981 !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: background 0.2s ease;
    }
    .stButton>button:hover {
        background: #059669 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 최상단 프로그램 헤더 ---
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🎯 High-Teen Career Diagnostic Solution</h1>
    <p class="sub-title">청소년 맞춤형 AI 진로·직업 매핑 및 학업 가이드 시스템 (Ver 2.5)</p>
</div>
""", unsafe_allow_html=True)

# --- 3. API 키 검증 및 AI 세션 설정 ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 시스템 연동 실패: Secrets에 'GEMINI_API_KEY'가 누락되었습니다.")
    st.stop()

@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. 화면 분할 (직업 추천 프로그램 레이아웃) ---
left_col, right_col = st.columns([1, 1.8], gap="large")

# --- [좌측 섹션] 학생 기초 진단 정보 및 성향 입력 ---
with left_col:
    st.markdown('<div class="program-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 1. 학생 인적 정보 입력</div>', unsafe_allow_html=True)
    school_level = st.selectbox(
        "현재 소속/학년", 
        ["중학교 1~2학년", "중학교 3학년", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"]
    )
    
    st.markdown('<div class="section-title" style="margin-top:25px;">🧩 2. 흥미 및 핵심 관심사 (최대 4개)</div>', unsafe_allow_html=True)
    interests = st.multiselect(
        "본인의 흥미 분야를 선택하세요.", 
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
    
    st.markdown('<div class="section-title" style="margin-top:25px;">⚡ 3. 본인이 생각하는 강점</div>', unsafe_allow_html=True)
    user_strength = st.radio(
        "가장 자신 있는 능력을 하나 고르세요.",
        ["수학적/논리적 사고", "창의력과 아이디어", "말하기와 소통 능력", "꼼꼼함과 자료 조사", "리더십과 실행력"]
    )
    
    st.markdown("---")
    if st.button("🔄 진단 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [우측 섹션] 종합 분석 리포트 및 실시간 상담실 ---
with right_col:
    st.markdown('<div class="program-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 4. 맞춤형 직업 추천 및 상담실</div>', unsafe_allow_html=True)
    
    # 가이드 안내판
    if not st.session_state.messages:
        st.info("💡 좌측에서 정보를 입력한 후, 아래 입력창에 **'내 성향에 맞는 직업 추천해줘'** 또는 구체적인 고민을 적어주시면 전문적인 진단 리포트가 생성됩니다.")

    # 기존 진단 내역 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 질의 입력부
    if prompt := st.chat_input("진로 고민, 목표 대학/학과, 고교학점제 선택 과목 등을 질문하세요."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 추천 및 진단서 생성
        with st.chat_message("assistant"):
            msg_placeholder = st.empty()
            full_response = ""
            
            # 전문 직업 진단 솔루션 페르소나 주입
            system_instruction = f"""
            당신은 대한민국 최고 권위의 청소년 종합 진로·직업 진단 시스템입니다.
            사용자 정보(학년: {school_level}, 관심분야: {', '.join(interests) if interests else '미선택'}, 강점: {user_strength})를 바탕으로 결과 보고서 형식으로 답변하세요.
            
            [답변 프레임워크]
            1. [종합 분석]: 학생의 관심사와 강점을 조합하여 어떤 성향의 인재인지 2줄 요약 평가.
            2. [최적의 추천 직업 BEST 3]: 구체적인 직업명과 트렌드를 반영한 추천 이유 기술.
            3. [로드맵 제안]: 고교학점제 선택 과목 제안 혹은 추천 도서/동아리 활동 팁 제시.
            
            어조는 전문적이고 체계적이되, 학생이 용기를 얻을 수 있도록 친절하게 끝맺음하세요. 가독성을 극대화하기 위해 이모지와 표/불릿 형식을 적극 활용하세요.
            """
            
            try:
                chat_history = [system_instruction]
                for m in st.session_state.messages[-5:]:
                    chat_history.append(f"{m['role']}: {m['content']}")
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents="\n".join(chat_history) + f"\nuser: {prompt}",
                    config=types.GenerateContentConfig(
                        temperature=0.6,
                        max_output_tokens=1200,
                    )
                )
                
                # 리포트 출력용 타이핑 효과
                for chunk in response.text.split():
                    full_response += chunk + " "
                    time.sleep(0.02)
                    msg_placeholder.markdown(full_response + "▌")
                
                msg_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                error_msg = str(e)
                if "high demand" in error_msg.lower():
                    st.warning("📊 현재 진단 서버에 트래픽이 몰리고 있습니다. 잠시 후 질문을 다시 제출해 주세요.")
                else:
                    st.error(f"시스템 일시적 오류: {error_msg}")
    st.markdown('</div>', unsafe_allow_html=True)
