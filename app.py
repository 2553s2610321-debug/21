import streamlit as st
from google import genai
from google.genai import types
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="AI Career Architect",
    page_icon="💎",
    layout="wide"
)

# --- 고급스러운 커스텀 CSS 적용 ---
st.markdown("""
<style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: radial-gradient(circle at top right, #1a1b4b, #0a0a0a);
        color: #e0e0e0;
    }
    
    /* 메인 타이틀 스타일 */
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #9d50bb, #6e48aa, #2ebf91);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* 유리 느낌의 카드 (Glassmorphism) */
    div[data-testid="stVerticalBlock"] > div:has(div.stChatMessage) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
    }

    /* 사이드바 스타일 커스텀 */
    .stSidebar {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 챗 메시지 아이콘/텍스트 조정 */
    .stChatMessage {
        background-color: transparent !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 제목부 ---
st.markdown('<h1 class="main-title">CAREER ARCHITECT AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">미래의 가능성을 설계하는 프리미엄 진로 컨설팅</p>', unsafe_allow_html=True)

# --- API 연결 및 세션 관리 ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Secrets에 'GEMINI_API_KEY'를 설정해주세요.")
    st.stop()

@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 사이드바: 사용자의 Career DNA ---
with st.sidebar:
    st.markdown("### 🧬 Your Career DNA")
    status = st.selectbox("현재 상태", ["대학생", "취업 준비생", "주니어 직장인(1~3년)", "시니어 직장인(5년+)", "이직 희망자"])
    strengths = st.multiselect("보유 핵심 역량", ["논리적 분석", "창의적 기획", "기술적 전문성", "공감 및 소통", "리더십", "데이터 기반 의사결정"])
    
    if st.button("💬 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 대화 내용 표시 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 메인 로직 ---
if prompt := st.chat_input("당신의 진로 고민을 들려주세요..."):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        full_response = ""
        
        # 시스템 프롬프트 설정 (고급스러운 어조 및 맥락 반영)
        system_instruction = f"""
        당신은 상위 1% 커리어 전략가입니다. 사용자의 상태({status})와 역량({', '.join(strengths)})을 바탕으로
        매우 세련되고 통찰력 있는 진로 상담을 제공하십시오. 
        대답은 항상 따뜻하지만 전문적이어야 하며, 구체적인 액션 플랜을 제안하는 것이 좋습니다.
        대화 중간에 이모지를 적절히 섞어 고급스러운 느낌을 유지하세요.
        """
        
        try:
            # 대화 맥락 포함하여 전달
            chat_history = [system_instruction]
            for m in st.session_state.messages[-5:]: # 최근 5개 대화 맥락 유지
                chat_history.append(f"{m['role']}: {m['content']}")
            
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents="\n".join(chat_history) + f"\nuser: {prompt}",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
            )
            
            # 타이핑 효과 모사 (고급스러운 경험)
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                msg_placeholder.markdown(full_response + "▌")
            
            msg_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_msg = str(e)
            if "high demand" in error_msg.lower():
                st.warning("💎 현재 상담 대기자가 많습니다. 모델을 'gemini-2.5-flash'로 변경하거나 잠시 후 다시 시도해주세요.")
            else:
                st.error(f"상담 중 연결이 잠시 지연되었습니다. 다시 한번 말씀해주시겠어요? (Error: {error_msg})")
