import streamlit as st
from google import genai
from google.genai import types
import time

# --- 1. 페이지 설정 및 테마 ---
st.set_page_config(
    page_title="하이틴 커리어 디자이너",
    page_icon="🎨",
    layout="wide"
)

# 고급스러운 네온 파스텔 스타일시트 초정밀 커스텀
st.markdown("""
<style>
    /* 전체 웹 페이지 배경: 은은하고 미래지향적인 파스텔 오로라 그라데이션 */
    .stApp {
        background: linear-gradient(125deg, #f3f4f6 0%, #eef2ff 50%, #f5f3ff 100%);
        color: #1e293b;
    }
    
    /* 사이드바 영역 스타일리시 디자인 */
    .stSidebar {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    
    /* 메인 타이틀: 입체감 있는 네온 그라데이션 효과 */
    .main-title {
        font-size: 3.2rem !important;
        font-weight: 900;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #4f46e5 10%, #9333ea 50%, #06b6d4 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        text-align: center;
        color: #475569;
        font-size: 1.2rem;
        margin-bottom: 3.5rem;
        font-weight: 600;
        opacity: 0.9;
    }

    /* 챗봇 대화창 영역: 프리미엄 글래스모피즘(Glassmorphism)과 쉐도우 효과 */
    div[data-testid="stVerticalBlock"] > div:has(div.stChatMessage) {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 20px 40px -15px rgba(99, 102, 241, 0.12), 
                    0 0 0 1px rgba(99, 102, 241, 0.05);
        padding: 30px !important;
        margin-bottom: 20px;
    }

    /* 대화창 내부 테두리선 부드럽게 지우기 */
    .stChatMessage {
        background-color: transparent !important;
        border-bottom: 1px solid rgba(99, 102, 241, 0.06) !important;
        padding: 15px 10px !important;
    }
    
    /* 입력창 디자인 커스텀 (입력바가 둥글고 예쁘게 돋보이도록 함) */
    div[data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.1) !important;
        background: white !important;
    }
    
    /* 사이드바 내부의 버튼 디자인 고도화 */
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 제목부 ---
st.markdown('<h1 class="main-title">하이틴 커리어 디자이너</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ 나만의 빛나는 스토리를 디자인하는 프리미엄 AI 진로 상담실</p>', unsafe_allow_html=True)

# --- 3. API 연결 및 세션 관리 ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Secrets에 'GEMINI_API_KEY'를 설정해주세요.")
    st.stop()

@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. 사이드바: 중고등학생 맞춤 프로필 ---
with st.sidebar:
    st.markdown("### 🏫 나의 학교 정보")
    school_level = st.selectbox(
        "현재 학년", 
        ["중학교 1~2학년", "중학교 3학년", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"]
    )
    
    st.markdown("### 🧩 관심 있는 분야")
    interests = st.multiselect(
        "좋아하거나 관심 있는 것 (최대 4개)", 
        [
            "💻 AI·SW·소프트웨어 개발",
            "🎨 일러스트·영상 콘텐츠·디자인",
            "📝 웹소설·방송 대본·스토리텔링",
            "🧬 의학·생명과학·바이오",
            "🔭 우주·항공·첨단 로봇공학",
            "🧪 신소재·화학·에너지 환경",
            "📊 경제·경영·스타트업 창업",
            "⚖️ 법률·정치·외교·사회 정의",
            "🧠 심리학·상담·아동 교육",
            "🎬 미디어 엔터테인먼트·K-POP 콘텐츠",
            "📈 금융 투자·빅데이터 분석",
            "🌍 어학·글로벌 문화·관광"
        ],
        max_selections=4
    )
    
    st.markdown("---")
    if st.button("🔄 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. 기존 대화 내용 표시 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. 메인 챗봇 대화 로직 ---
if prompt := st.chat_input("진로, 학과 선택, 공부 방법 등 고민을 편하게 적어보세요!"):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        full_response = ""
        
        # 청소년 대상 눈높이 가이드 프롬프트
        system_instruction = f"""
        당신은 청소년 전문 친절하고 유능한 진로 상담 교사입니다. 
        사용자는 {school_level} 학생이며, 관심 분야는 [{', '.join(interests) if interests else '탐색 중'}]입니다.
        
        [답변 규칙]
        1. 지나치게 딱딱한 직장인용 전문 용어는 피하고, 학생이 이해하기 쉽게 설명하세요.
        2. 학생의 고민에 깊이 공감해주고 칭찬과 격려를 아끼지 마세요.
        3. 문과/이과 선택, 고교학점제 과목 선택, 관련 학과 추천 등 대한민국 고등/중등 교육과정에 맞는 실질적인 조언을 제공하세요.
        4. 가독성이 좋게 이모지와 불릿포인트를 적극적으로 사용해 화사하게 작성하세요.
        """
        
        try:
            # 대화 맥락 유지 (최근 5개 대화)
            chat_history = [system_instruction]
            for m in st.session_state.messages[-5:]:
                chat_history.append(f"{m['role']}: {m['content']}")
            
            # 안정적인 gemini-2.5-flash 모델 호출
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents="\n".join(chat_history) + f"\nuser: {prompt}",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
            )
            
            # 고급스러운 글자 타이핑 효과
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.03)
                msg_placeholder.markdown(full_response + "▌")
            
            msg_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_msg = str(e)
            if "high demand" in error_msg.lower():
                st.warning("🌈 현재 상담실에 친구들이 많이 몰려있어요! 잠시 후 다시 질문을 입력해 주세요.")
            else:
                st.error(f"앗, 잠시 대화 연결이 불안정해요. 다시 한번 말해줄래요? (Error: {error_msg})")
