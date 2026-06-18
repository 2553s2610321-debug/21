import streamlit as st
import datetime

# 1. 페이지 설정 및 타이틀
st.set_page_config(page_title="진로 계획 세우기", layout="centered")
st.title("🎯 간단한 진로 계획 플래너")
st.write("원하는 직업을 선택하고 나만의 실천 계획을 입력해보세요.")
st.write("---")

# 2. 핵심 직업 데이터베이스 (대표 직업 4개로 압축)
CAREER_DB = {
    "개발자": {
        "desc": "컴퓨터 프로그램이나 앱을 만드는 사람입니다.",
        "skills": "논리적 사고, 코딩 기초, 컴퓨터 이해",
        "activities": "간단한 앱 만들기, 코딩 사이트 활용"
    },
    "디자이너": {
        "desc": "보기 좋은 그림과 화면을 만드는 사람입니다.",
        "skills": "색감 이해, 창의력, 디자인 도구 사용",
        "activities": "포스터 제작, UI 디자인 따라하기"
    },
    "마케터": {
        "desc": "상품이나 서비스를 세상에 알리는 사람입니다.",
        "skills": "기획력, 글쓰기, 트렌드 분석력",
        "activities": "SNS 운영, 광고 카피 기획"
    },
    "교사": {
        "desc": "학생들에게 지식과 바른 길을 가르치는 사람입니다.",
        "skills": "설명 능력, 인내심, 전공 지식",
        "activities": "학습 지도 봉사, 교육 실습 참여"
    }
}

# 3. 사용자 입력 양식 (Form 하나로 통일)
with st.form("career_planner_form"):
    st.subheader("📋 나의 정보 입력")
    name = st.text_input("이름", value="홍길동")
    age = st.number_input("나이", min_value=10, max_value=100, value=18)
    career = st.selectbox("희망 직업", list(CAREER_DB.keys()))
    goal = st.text_input("최종 목표", value="멋진 전문가가 되기")
    
    st.subheader("🗓️ 기간별 나의 실행 계획")
    plan_short = st.text_input("단기 계획 (3개월 이내)", value="기초 책 1권 읽기")
    plan_mid = st.text_input("중기 계획 (6개월 이내)", value="관련 자격증 취득하기")
    plan_long = st.text_input("장기 계획 (1년 이내)", value="개인 포트폴리오 완성하기")
    
    # 생성 버튼
    submitted = st.form_submit_button("🎯 진로 계획서 생성하기")

# 4. 결과 출력 및 다운로드 영역
if submitted:
    st.write("---")
    st.header("📊 완성된 나의 진로 로드맵")
    
    # 선택한 직업의 기본 데이터 가져오기
    data = CAREER_DB[career]
    
    # 요약 카드
    st.info(f"👤 **{name}**({age}세)님의 목표: **{career}**")
    st.markdown(f"**직업 설명:** {data['desc']}")
    st.success(f"**최종 목표:** {goal}")
    
    # 가이드 및 실천 계획
    col1, col2 = st.columns(2)
    with col1:
        st.warning("🧠 필요한 핵심 능력")
        st.write(data["skills"])
        
        st.warning("🚀 추천 실천 활동")
        st.write(data["activities"])
        
    with col2:
        st.light_bulb("📝 내가 세운 기간별 계획")
        st.write(f"• **단기:** {plan_short}")
        st.write(f"• **중기:** {plan_mid}")
        st.write(f"• **장기:** {plan_long}")
        
    st.write("---")
    
    # 다운로드 텍스트 준비
    text = f"""===== 진로 계획서 =====
이름: {name} ({age}세)
희망 직업: {career}
최종 목표: {goal}

[직무 가이드]
- 필요 능력: {data['skills']}
- 추천 활동: {data['activities']}

[나의 계획]
- 단기: {plan_short}
- 중기: {plan_mid}
- 장기: {plan_long}

생성일: {datetime.datetime.now().strftime('%Y-%m-%d')}
"""

    # 다운로드 버튼
    st.download_button(
        label="📥 진로계획서 다운로드 (.txt)",
        data=text,
        file_name=f"진로계획서_{name}.txt",
        mime="text/plain"
    )
