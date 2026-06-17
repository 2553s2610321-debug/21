import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(
    page_title="AI 고교 선택과목 가이드",
    page_icon="📚",
    layout="centered"
)

# 2. API 키 설정 및 초기화
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # 로컬 테스트용
    api_key = st.sidebar.text_input("Gemini API Key를 입력하세요:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ API Key가 설정되지 않았습니다. Streamlit Secrets에 등록하거나 사이드바에 입력해주세요.")

# 3. 세션 상태(대화 내역) 초기화
if "subject_messages" not in st.session_state:
    st.session_state.subject_messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 📚 **AI 고교 선택과목 가이드**입니다. 희망하는 **대학 학과나 진로 분야**를 말씀해주시면, 고등학교에서 이수하면 좋은 추천 과목 디자인을 도와드릴게요!"
        }
    ]

# 4. UI 레이아웃
st.title("📚 AI 진로 맞춤 선택과목 가이드")
st.caption("희망 전공에 맞춰 고등학교에서 꼭 들어야 하는 필수 및 권장 과목을 확인하세요.")

# 빠른 학과 조회 칩 (자주 찾는 인기 학과)
st.markdown("💡 **인기 전공 바로 조회하기**")
col1, col2, col3, col4 = st.columns(4)
preset_department = None

with col1:
    if st.button("💻 컴퓨터공학과"):
        preset_department = "컴퓨터공학과/소프트웨어학과에 진학하고 싶어. 고등학교 때 들어야 하는 수학, 과학, 정보 관련 선택 과목을 알려줘."
with col2:
    if st.button("🩺 의예/간호학과"):
        preset_department = "의예과 및 간호학과 등 보건의료 계열을 희망해. 생명과학이나 화학 외에 어떤 과목을 이수하는 게 유리할까?"
with col3:
    if st.button("📊 경영/경제학과"):
        preset_department = "경영학과 또는 경제학과 진학이 목표야. 사회 선택 과목이랑 수학 과목(예: 미적분, 확률과 통계 등)을 어떻게 골라야 해?"
with col4:
    if st.button("🎨 미디어/디자인"):
        preset_department = "미디어커뮤니케이션이나 시각디자인학과를 가고 싶어. 예술이나 사회, 교양 과목 중에서 추천해줘."

# 5. 기존 대화 내역 출력
for message in st.session_state.subject_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 6. 사용자 입력 처리
user_input = st.chat_input("희망 학과나 진로를 입력하세요 (예: 기계공학과, 심리학과 등)")

if preset_department:
    user_input = preset_department

if user_input:
    # 사용자 메시지 화면 표시 및 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.subject_messages.append({"role": "user", "content": user_input})

    # AI 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not api_key:
            message_placeholder.error("API Key가 필요합니다.")
        else:
            try:
                with st.spinner("대학교 인재상과 교육과정을 분석하여 과목을 매칭 중입니다..."):
                    # 모델 설정
                    model = genai.GenerativeModel("gemini-2.5-flash-lite")
                    
                    # 교육과정 설계 전문가 페르소나 부여
                    system_instruction = (
                        "당신은 고등학교 교육과정 및 대학 입시 전형 전문가(입학사정관 및 학업설계사)입니다. "
                        "사용자가 희망 학과나 진로를 말하면 고등학교 선택 과목을 추천해야 합니다. 다음 구조를 엄격히 지켜 답변하세요:\n"
                        "1. [전공 핵심 역량]: 해당 학과에서 가장 중요하게 보는 핵심 능력 짧게 요약\n"
                        "2. [필수 이수 과목 (치명적으로 중요)]: 내신에서 반드시 선택해야 하는 핵심 과목 (수학, 과학, 사회 등 구분)\n"
                        "3. [권장 선택 과목 (가산점/학종 유리)]: 일반선택 및 진로선택 과목으로 나누어 추천\n"
                        "4. [전문가의 한마디]: 학생부종합전형(세특)을 채울 때 해당 과목들과 연계할 수 있는 탐구 주제 팁 1가지 제시\n"
                        "가독성을 위해 굵은 글씨(**)와 이모지, 깔끔한 리스트 구조를 적극 활용하세요."
                    )
                    
                    # 대화 맥락 포함
                    full_prompt = system_instruction + "\n\n"
                    for msg in st.session_state.subject_messages:
                        full_prompt += f"{msg['role']}: {msg['content']}\n"
                    
                    # API 호출
                    response = model.generate_content(full_prompt)
                    ai_response = response.text
                    
                    # 화면 표시 및 세션 저장
                    message_placeholder.write(ai_response)
                    st.session_state.subject_messages.append({"role": "assistant", "content": ai_response})
                    
            except Exception as e:
                message_placeholder.error(f"오류가 발생했습니다: {e}\nAPI 키를 확인하거나 잠시 후 다시 시도해주세요.")
