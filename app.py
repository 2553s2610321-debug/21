import streamlit as st
from google import genai
from google.genai import types

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
    <p class="sub-title">청소년 맞춤형 AI 진로·직업 매핑 및 학업 가이드 시스템 (Ver 2.6)</p>
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
    st.markdown('<div class="section-title">📊 1. 학생 인적 정보 입력</div>', unsafe
