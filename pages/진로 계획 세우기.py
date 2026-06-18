import streamlit as st
import datetime

# 1. 페이지 설정 및 타이틀
st.set_page_config(page_title="진로 계획 세우기", layout="centered")
st.title("🎯 간단한 진로 계획 플래너")
st.write("원하는 직업을 선택하고 나만의 실천 계획을 입력해보세요.")
st.write("---")

# 2. 15개 직업 데이터베이스 (간결한 구조로 통합)
CAREER_DB = {
    "개발자": {
        "desc": "컴퓨터 프로그램이나 앱을 만드는 사람입니다.",
        "skills": "논리적 사고, 코딩 기초, 컴퓨터 이해, 꾸준한 학습",
        "activities": "간단한 앱 만들기, 코딩 사이트 활용, 웹사이트 제작"
    },
    "디자이너": {
        "desc": "보기 좋은 그림과 화면을 만드는 사람입니다.",
        "skills": "색감 이해, 창의력, 디자인 도구 사용, 그림 감각",
        "activities": "포스터 제작, UI 디자인 따라하기, 포트폴리오 만들기"
    },
    "마케터": {
        "desc": "상품이나 서비스를 세상에 알리는 사람입니다.",
        "skills": "기획력, 글쓰기, 트렌드 분석력, 소통 능력",
        "activities": "SNS 운영, 광고 카피 기획, 시장 트렌드 조사"
    },
    "공무원": {
        "desc": "국가와 지역을 위해 행정 업무를 하는 사람입니다.",
        "skills": "문제 해결력, 책임감, 행정 지식, 성실성",
        "activities": "공부 계획 수립, 시험 기출문제 풀이, 스터디 참여"
    },
    "의사": {
        "desc": "사람들의 건강을 진단하고 치료하는 사람입니다.",
        "skills": "생물학/의학 지식, 집중력, 책임감, 생명 존중",
        "activities": "과학 실험 참여, 병원 견학 및 체험, 생물 공부"
    },
    "간호사": {
        "desc": "환자를 돌보고 치료를 돕는 사람입니다.",
        "skills": "배려심, 의학 기초 지식, 책임감, 강한 체력",
        "activities": "병원 봉사활동, 응급처치 공부, 의료 분야 체험"
    },
    "교사": {
        "desc": "학생들에게 지식과 바른 길을 가르치는 사람입니다.",
        "skills": "설명 능력, 인내심, 전공 지식, 소통 능력",
        "activities": "학습 지도 봉사, 교육 실습 참여, 멘토링 활동"
    },
    "경찰": {
        "desc": "사람들의 안전을 지키고 사회 질서를 유지하는 사람입니다.",
        "skills": "강한 체력, 순간 판단력, 책임감, 정의감",
        "activities": "꾸준한 체력 운동, 기초 법률 공부, 무도 훈련"
    },
    "소방관": {
        "desc": "화재와 사고 현장에서 사람을 구하는 사람입니다.",
        "skills": "강한 체력, 용기, 상황 판단력, 협동심",
        "activities": "체력 단련 훈련, 응급 구조 공부, 안전 교육 이수"
    },
    "유튜버": {
        "desc": "영상 콘텐츠를 만들어 사람들과 소통하는 사람입니다.",
        "skills": "창의력, 영상 편집 기술, 대중 소통 능력, 기획력",
        "activities": "영상 촬영 및 편집 연습, 콘텐츠 기획, 개인 채널 운영"
    },
    "요리사": {
        "desc": "음식을 만들고 새로운 레시피를 요리하는 사람입니다.",
        "skills": "요리 기술, 창의력, 손재주, 철저한 위생 관리",
        "activities": "요리 실습 및 연습, 나만의 레시피 개발, 맛집 탐방"
    },
    "운동선수": {
        "desc": "스포츠 경기에서 좋은 성적을 내기 위해 활동하는 사람입니다.",
        "skills": "뛰어난 신체 능력, 경기 기술, 집중력, 인내심",
        "activities": "종목별 기술 훈련, 매일 체력 관리, 실전 경기 참가"
    },
    "회계사": {
        "desc": "회사의 돈 흐름을 관리하고 기록하는 사람입니다.",
        "skills": "수리 감각, 데이터 분석력, 꼼꼼함, 책임감",
        "activities": "회계 및 세무 공부, 엑셀 프로그램 연습, 경제 뉴스 보기"
    },
    "건축가": {
        "desc": "건물과 다양한 구조물을 멋지게 설계하는 사람입니다.",
        "skills": "공간 지각 능력, 수학적 사고, 디자인 감각, 설계 기술",
        "activities": "설계 도면 그리기 연습, 건축 모형 제작, 유명 건축물 탐방"
    },
    "항공승무원": {
        "desc": "비행기에서 승객의 안전과 서비스를 책임지는 사람입니다.",
        "skills": "서비스 정신, 뛰어난 외국어 능력, 친절함, 위기대처 능력",
        "activities": "외국어(영어 등) 회화 공부, 서비스 매너 연습, 체력 키우기"
    }
}

# 3. 사용자 입력 양식 (Form)
with st.form("career_planner_form"):
    st.subheader("📋 나의 정보 입력")
    name = st.text_input("이름", value="홍길동")
    age = st.number_input("나이", min_value=10, max_value=100, value=18)
    career = st.selectbox("희망 직업 선택", list(CAREER_DB.keys()))
    goal = st.text_input("최종 목표", value="멋진 전문가가 되기")
    
    st.subheader("🗓️ 기간별 나의 실행 계획")
    plan_short = st.text_input("단기 계획 (3개월 이내)", value="기초 책 1권 읽기")
    plan_mid = st.text_input("중기 계획 (6개월 이내)", value="관련 공부 및 경험 쌓기")
    plan_long = st.text_input("장기 계획 (1년 이내)", value="나만의 포트폴리오 완성하기")
    
    # 생성 버튼
    submitted = st.form_submit_button("🎯 진로 계획서 생성하기")

# 4. 결과 출력 및 다운로드 영역
if submitted:
    st.write("---")
    st.header("📊 완성된 나의 진로 로드맵")
    
    # 선택한 직업의 데이터 가져오기
    data = CAREER_DB[career]
    
    # 요약 카드
    st.info(f"👤 **{name}**({age}세)님의 목표 직업: **{career}**")
    st.markdown(f"**💡 직업 설명:** {data['desc']}")
    st.success(f"**🎯 최종 목표:** {goal}")
    
    # 가이드 및 실천 계획 (가독성을 위한 가벼운 이모지 사용)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧠 필요한 핵심 능력")
        st.write(data["skills"])
        
        st.markdown("### 🚀 추천 실천 활동")
        st.write(data["activities"])
        
    with col2:
        st.markdown("### 📝 내가 세운 기간별 계획")
        st.write(f"• **단기 목표:** {plan_short}")
        st.write(f"• **중기 목표:** {plan_mid}")
        st.write(f"• **장기 목표:** {plan_long}")
        
    st.write("---")
    
    # 다운로드용 텍스트 서식 준비
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
