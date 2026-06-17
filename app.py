import streamlit as st
from google import genai
from google.genai import types
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="하이틴 커리어 디자이너",
    page_icon="🎨",
    layout="wide"
)

# --- 화사하고 세련된 네온 파스텔톤 라이트 모드 CSS ---
st.markdown("""
<style>
    /* 전체 배경: 밝고 트렌디한 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        color: #2c3e50;
    }
    
    /* 메인 타이틀: 청량한 블루-퍼플 그라데이션 */
    .main-title {
        font-size: 2.8rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        font-weight: 500;
    }

    /* 화사한 유리 느낌의 카드 (Glassmorphism Light) */
    div[data-testid="stVerticalBlock"] > div:has(div.stChatMessage) {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        padding: 25px;
    }

    /* 사이드바 스타일 스타일리시하게 변경 */
    .stSidebar {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }

    /* 채팅 메시지 구분선 및 스타일 */
    .stChatMessage {
        background-color: transparent !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.03) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 제목부 ---
st.markdown('<h1 class="main-title">하이틴 커리어 디자이너</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">꿈을 찾는 중고등학생을 위한 AI 진로 탐색 가이드</p>', unsafe_allow_html=True)

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

# --- 사이드바: 중고등학생 맞춤 프로필 ---
with st.sidebar:
    st.markdown("### 🏫 나의 학교 정보")
    school_level = st.selectbox("현재 학년", ["중학교 1~2학년", "중학교 3학년", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"])
    
    st.markdown("### 🧩 관심 있는 분야")
    interests = st.multiselect(
        "좋아하거나 관심 있는 것 (최대 3개)",
