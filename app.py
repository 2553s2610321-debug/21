import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 테마
st.set_page_config(page_title="AI 진로 고민 상담소", page_icon="🎯", layout="wide")

# 2. API 키 설정 및 예외 처리
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API 키가 설정되지 않았습니다. 사이드바의 Secrets 설정 방법을 확인해주세요.")
    st.stop()

# 3. 세션 상태(Session State) 초기화 (대화 기록 저장용)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 화면 레이아웃 구성
st.title("🎯 AI 진로 고민 상담소: 캐리어 나침반")
st.caption("여러분의 꿈과 적성에 맞는 커리어 길잡이가 되어 드립니다.")
st.markdown("---")

# [사이드바] 사용자 성향 파악 및 초기화 버튼
with st.sidebar:
    st.header("📋 나의 성향 profile")
    interest = st.selectbox(
        "관심 있는 분야를 선택하세요:",
        ["IT / 개발", "경영 / 마케팅", "디자인 / 예술", "바이오 / 의학", "교육 / 연구", "기타 (대화로 입력)"]
    )
    
    value_priority = st.radio(
        "직업을 고를 때 가장 중요한 가치는?",
        ("연봉 및 보상", "워라밸 (일과 삶의 균형)", "자아실현 및 성장", "직업 안정성")
    )
    
    st.markdown("---")
    if st.button("🔄 대화 초기화하기", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. 페르소나 및 시스템 프롬프트 설정
system_instruction = f"""
당신은 친절하고 전문적인 AI 진로 상담 커리어 코치입니다.
사용자의 관심 분야는 [{interest}] 이며, 직업 선택 시 가장 중요하게 생각하는 가치는 [{value_priority}] 입니다.
이 정보를 바탕으로 사용자의 고민에 공감하고, 구체적이고 실현 가능한 진로 로드맵이나 조언을 제공해주세요.
답변은 친근하면서도 전문적인 어조(하십시요체 또는 해요체 혼용)로 작성하고, 가독성을 위해 이모지와 줄바꿈을 적절히 사용하세요.
"""

# 6. 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. 챗봇 입력 및 AI 답변 생성
if prompt := st.chat_input("진로에 대한 어떤 고민이든 편하게 말씀해주세요! (예: 비전공자인데 개발자가 되고 싶어요.)"):
    
    # 사용자 메시지 추가 및 화면 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # AI 답변 생성 프로세스
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # gemini-2.5-flash-lite 모델 호출
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction=system_instruction
            )
            
            # 이전 대화 맥락을 포함하여 API 요청 데이터 구성
            chat_history = []
            for msg in st.session_state.messages[:-1]: # 현재 프롬프트 제외한 이전 기록
                chat_history.append({"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]})
            
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt)
            full_response = response.text
            
            # 화면에 답변 출력 및 저장
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"⚠️ API 호출 중 오류가 발생했습니다: {e}")
            message_placeholder.markdown("죄송합니다. 잠시 후 다시 시도해주세요.")

# 8. 상담 리포트 다운로드 기능 (대화가 존재할 때만 표시)
if len(st.session_state.messages) > 0:
    st.markdown("---")
    report_text = f"=== 진로 상담 리포트 ===\n• 관심 분야: {interest}\n• 우선 가치: {value_priority}\n\n"
    for msg in st.session_state.messages:
        role_name = "나" if msg["role"] == "user" else "AI 코치"
        report_text += f"[{role_name}]: {msg['content']}\n\n"
        
    st.download_button(
        label="📥 현재까지의 상담 리of트 다운로드",
        data=report_text,
        file_name="career_consulting_report.txt",
        mime="text/plain",
    )
