import streamlit as st
import random
import time

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="5등급제 대학 매칭 시뮬레이터",
    page_icon="🏫",
    layout="centered"
)

# 2. 데이터베이스 정의 (5등급제 기준 대학 & 학과 & 응원 문구)
GRADE_INFO = {
    1: {"percent": 10, "range": "상위 0% ~ 10%", "desc": "최상위권 (기존 9등급제의 1~2등급 수준)"},
    2: {"percent": 34, "range": "상위 10% ~ 34%", "desc": "상위권 (기존 9등급제의 3등급 수준)"},
    3: {"percent": 66, "range": "상위 34% ~ 66%", "desc": "중위권 (기존 9등급제의 4~5등급 수준)"},
    4: {"percent": 90, "range": "상위 66% ~ 90%", "desc": "중하위권 (기존 9등급제의 6~7등급 수준)"},
    5: {"percent": 100, "range": "상위 90% ~ 100%", "desc": "가능성 가득한 구간 (기존 9등급제의 8~9등급 수준)"}
}

UNI_DB = {
    1: ["서울대학교", "KAIST", "연세대학교", "고려대학교", "서강대학교", "성균관대학교", "한양대학교"],
    2: ["중앙대학교", "경희대학교", "한국외국어대학교", "서울시립대학교", "건국대학교", "동국대학교", "홍익대학교"],
    3: ["국민대학교", "숭실대학교", "세종대학교", "단국대학교", "광운대학교", "가천대학교", "경기대학교"],
    4: ["명지대학교", "상명대학교", "인천대학교", "가톨릭대학교", "주요 지역 거점 국립대"],
    5: ["전국 내신 5등급 전형 개설 대학", "가까운 지역 명문 전문대학교"]
}

DEPARTMENTS = [
    "컴퓨터공학과", "인공지능학과", "전자공학과", "생명공학과", "화학공학과",
    "경영학과", "경제학과", "미디어커뮤니케이션학과", "심리학과", "행정학과",
    "국어국문학과", "영어영문학과", "의류학과", "시각디자인학과", "자유전공학부"
]

CHEER_MESSAGES = [
    "🍀 찍는 것마다 정답이 되는 마법이 함께하길 바랍니다!",
    "✨ 지금 흘린 땀방울은 절대 배신하지 않을 거예요.",
    "합격 기운 팍팍! 당신의 잠재력은 등급 숫자가 전부 담지 못합니다.",
    "⏳ 묵묵히 걷는 당신의 발걸음 끝에 빛나는 합격증이 기다립니다.",
    "🦁 쫄지 마세요! 당신은 생각보다 훨씬 더 멋진 결과를 낼 사람입니다."
]

# 3. 앱 타이틀 및 소개
st.title("🏫 5등급제 대학 & 학과 무작위 매칭기")
st.caption("개편된 5등급제 컷 가이드라인과 당신의 운명의 대학을 재미로 확인해보세요!")
st.markdown("---")

# 4. 사이드바 - 성적 입력 창
st.sidebar.header("📊 성적 입력")
user_grade = st.sidebar.number_input(
    "자신의 평균 등급을 입력하세요 (1.0 ~ 5.0)",
    min_value=1.0,
    max_value=5.0,
    value=2.5,
    step=0.1,
    format="%.1f"
)

# 입력받은 등급 반올림하여 정수 키값으로 변환
rounded_grade = round(user_grade)
# 예외 처리: 혹시나 범위를 벗어날 경우 방어 코드
if rounded_grade < 1: rounded_grade = 1
if rounded_grade > 5: rounded_grade = 5

# 분석하기 버튼
start_button = st.sidebar.button("🔮 운명의 대학 추첨하기")

# 5. 메인 화면 로직
if start_button:
    # 로딩 애니메이션
    with st.spinner("⏳ 당신의 운명의 대학교를 분석 중..."):
        time.sleep(1.2) # 연출을 위한 약간의 대기시간
    
    # 데이터 가져오기
    info = GRADE_INFO[rounded_grade]
    chosen_uni = random.choice(UNI_DB[rounded_grade])
    chosen_dept = random.choice(DEPARTMENTS)
    chosen_cheer = random.choice(CHEER_MESSAGES)
    
    # 결과 섹션 1: 5등급제 분석 그래프
    st.subheader("📈 5등급제 기준 내 성적 위치")
    st.markdown(f"입력하신 등급은 **{user_grade}등급** (반올림 기준: **{rounded_grade}등급**) 입니다.")
    
    # 프로그레스 바를 이용한 누적 백분위 시각화
    # 상위 %가 낮을수록 스펙트럼이 좋은 것이므로, 반대로 채워지는 느낌 연출을 위해 100에서 뺌
    progress_val = max(0, min(100, 100 - info["percent"]))
    st.progress(progress_val / 100)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="예상 누적 위치", value=info["range"])
    with col2:
        st.metric(label="등급 가이드", value=f"{rounded_grade}등급 수준")
    st.caption(f"ℹ️ {info['desc']}")
    
    st.markdown("---")
    
    # 결과 섹션 2: 대학 및 학과 결과 카드
    st.subheader("🎉 무작위 매칭 결과")
    
    st.success(f"""
    ### 🏛️ **{chosen_uni}**
    ### 🧬 **{chosen_dept}**
    """)
    
    st.info(f"**💌 오늘의 합격 부적:**\n{chosen_cheer}")
    st.balloons() # 축하 풍선 효과

else:
    # 버튼을 누르기 전 초기 안내 화면
    st.info("👈 왼쪽 사이드바에 내신/수능 등급을 입력하고 **[운명의 대학 추첨하기]** 버튼을 눌러주세요!")
    st.image("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=1000&auto=format&fit=crop", caption="당신의 빛나는 미래를 응원합니다.")
