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

# 화사하고 세련된 네온 파스텔톤 라이트 모드 CSS
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

# --- 2. 제목부 ---
st.markdown('<h1 class="main-title">하이틴 커리어 디자이너</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">꿈을 찾는 중고등학생을 위한 AI 진로 탐색 가이드</p>', unsafe_allow_html=True)

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

# --- 4. 사이드바: 중고등학생 맞춤 프로필 (괄호 명확히 마감) ---
with st.sidebar:
    st.markdown("### 🏫 나의 학교 정보")
    school_level = st.selectbox(
        "현재 학년", 
        ["중학교 1~2학년", "중학교 3학년", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"]
    )
    
    st.markdown("### 🧩 관심 있는 분야")
    interests = st.multiselect(
        "좋아하거나 관심 있는 것 (최대 3개)", 
        ["게임/컴퓨터", "그림/영상/디자인", "글쓰기/말하기", "과학 실험/수학", "음악/댄스/체육", "경영/경제/소비 트렌드", "사람 돕기/사회 문제"],
        max_selections=3
    )
    
    if st.button("💬 대화 초기화", use_container_width=True):
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
        3. 문과/이과 선택, 고교학점제 과목 선택, 관련 학과 추천 등 고등/중등 교육과정에 맞는 실질적인 조언을 제공하세요.
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
