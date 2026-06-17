import streamlit as st
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="방구석 진로 탐색기",
    page_icon="🎓",
    layout="centered"
)

# 2. 학과 데이터베이스 (확장 및 유지보수가 쉬운 딕셔너리 구조)
DEPARTMENTS_DB = {
    "컴퓨터공학과": {
        "category": "공학계열",
        "summary": "현대 디지털 세상을 움직이는 소프트웨어 마법사들을 양성하는 곳",
        "keywords": ["#개발자", "#AI", "#코딩", "#코딩노예", "#고연봉"],
        "pros": ["전 세계 어디서나 취업 기회가 많음", "원격 근무 및 자유로운 조직 문화", "스스로 무언가를 창조하는 희열"],
        "cons": ["트렌드가 너무 빨라 평생 공부해야 함", "거북목, 손목 터널 증후군과의 사투", "에러 잡다가 밤새기 일쑤"],
        "recommended_for": "논리적이고 퍼즐 풀기를 좋아하며, 끈기 하나는 자신 있는 사람",
        "mbti": "INTJ / INTP / ISTP"
    },
    "심리학과": {
        "category": "인문/사회계열",
        "summary": "인간의 마음과 행동의 비밀을 과학적으로 파헤치는 학문",
        "keywords": ["#마음읽기", "#상담", "#독심술아님", "#통계학", "#인간이해"],
        "pros": ["나 자신과 타인에 대한 깊은 이해 가능", "마케팅, UX, 인사 등 다양한 산업군으로 진출 가능", "들을 귀가 넓어짐"],
        "cons": [" 주변에서 \"내 마음 읽어봐\"라는 소리를 귀에 딱지 앉도록 들음", "의외로 수학(통계)을 엄청나게 많이 함", "대학원 진학이 거의 필수적임"],
        "recommended_for": "사람에 대한 호기심이 많고, 타인의 고민을 잘 들어주는 따뜻한 사람",
        "mbti": "INFJ / INFP / ENFJ"
    },
    "경영학과": {
        "category": "인문/사회계열",
        "summary": "기업을 효율적으로 운영하고 돈의 흐름을 조율하는 비즈니스 리더의 요람",
        "keywords": ["#CEO", "#마케팅", "#스타트업", "#팀플지옥", "#발표"],
        "pros": ["취업 선택의 폭이 가장 넓음(모든 회사엔 경영이 필요)", "팀 프로젝트를 통해 커뮤니케이션 능력 극대화"],
        "cons": ["무엇이든 배우지만 깊이가 애매해질 수 있음", "끊임없는 발표와 인맥 관리 스트레스"],
        "recommended_for": "리더십이 있고, 트렌드에 민감하며, 효율성을 중시하는 사람",
        "mbti": "ENTJ / ESTJ / ENFJ"
    },
    "생명공학과": {
        "category": "자연/과학계열",
        "summary": "바이오, 신약 개발 등 인류의 건강과 미래를 책임지는 첨단 과학",
        "keywords": ["#바이오", "#DNA", "#백신", "#실험실", "#하얀가운"],
        "pros": ["고령화 시대에 가장 유망한 미래 성장 동력", "인류의 질병 퇴치에 기여한다는 엄청난 보람"],
        "cons": ["실험 결과가 나올 때까지 기다림의 연속(인내심 폭발)", "학사 학위만으로는 연구직 취업이 다소 어려움"],
        "recommended_for": "관찰력이 좋고 생물학적 신비로움에 가슴이 뛰는 사람",
        "mbti": "INTP / INTJ / ISTJ"
    },
    "시각디자인학과": {
        "category": "예체능계열",
        "summary": "텍스트와 이미지를 활용해 세상과 시각적으로 소통하는 크리에이터",
        "keywords": ["#포토샵", "#브랜딩", "#예술", "#야근", "#컨셉"],
        "pros": ["내 아이디어가 눈앞의 멋진 결과물로 탄생함", "포트폴리오만 확실하면 학벌 상관없이 실력으로 인정받음"],
        "cons": ["\"알아서 예쁘게 해주세요\"라는 클라이언트의 요청 지옥", "끊임없는 수정 작업과 마감 압박"],
        "recommended_for": "미적 감각이 뛰어나고, 시각적 요소로 표현하는 것을 좋아하는 사람",
        "mbti": "ISFP / INFP / ENFP"
    },
    "기계공학과": {
        "category": "공학계열",
        "summary": "자동차, 로봇, 우주선까지 움직이는 모든 기계를 설계하는 공학의 뿌리",
        "keywords": ["#역학지옥", "#로봇", "#자동차", "#취업깡패", "#설계"],
        "pros": ["제조업 기반 국가(한국)에서 취업률 깡패", "기계 구조를 완벽히 이해했을 때의 쾌감"],
        "cons": ["4대 역학(열, 유체, 재료, 동역학)의 무지막지한 수학/물리 폭격", "남초 성향이 강한 다소 딱딱한 문화"],
        "recommended_for": "물건을 분해하고 조립하는 것을 좋아하며, 수학/물리에 거부감이 없는 사람",
        "mbti": "ISTJ / ESTJ / ISTP"
    }
}

# 3. 세션 상태(Session State) 초기화 (저장된 학과 리스트 보관용)
if "saved_departments" not in st.session_state:
    st.session_state.saved_departments = []

# 4. UI 구성
st.title("🎓 방구석 진로 탐색기")
st.caption("어떤 학과를 갈지 모르겠나요? 주저하지 말고 주사위를 굴려보세요!")

st.markdown("---")

# 5. 사용자 입력 (필터링 기능)
st.subheader("🎲 원하는 계열을 선택하고 버튼을 눌러보세요!")
category_list = ["전체"] + list(set(dept["category"] for dept in DEPARTMENTS_DB.values()))
selected_category = st.selectbox("관심 계열 선택", category_list)

# 버튼 디자인 및 클릭 이벤트 처리
if st.button("🔮 랜덤 학과 추천받기", type="primary", use_container_width=True):
    try:
        # 필터링된 학과 목록 생성
        if selected_category == "전체":
            filtered_depts = list(DEPARTMENTS_DB.keys())
        else:
            filtered_depts = [name for name, info in DEPARTMENTS_DB.items() if info["category"] == selected_category]
        
        # 무작위 추출
        chosen_dept_name = random.choice(filtered_depts)
        chosen_dept_info = DEPARTMENTS_DB[chosen_dept_name]
        
        # 현재 추천된 학과를 임시 저장 (화면 리프레시 대응)
        st.session_state.current_dept = (chosen_dept_name, chosen_dept_info)
    except Exception as e:
        st.error("학과를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")

# 6. 결과 출력 영역
if "current_dept" in st.session_state:
    name, info = st.session_state.current_dept
    
    st.success(f"🎉 오늘의 추천 학과: **[{info['category']}] {name}**")
    
    # 키워드 태그 예쁘게 출력
    st.markdown(f"**{' '.join(info['keywords'])}**")
    
    # 한 줄 요약
    st.info(f"💡 **한 줄 요약:** {info['summary']}")
    
    # 장단점 비교 레이아웃 (Column 분할)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 이런 장점이 있어요")
        for pro in info["pros"]:
            st.markdown(f"- {pro}")
            
    with col2:
        st.markdown("### 🔴 이런 단점은 각오해야 해요")
        for con in info["cons"]:
            st.markdown(f"- {con}")
            
    st.markdown("---")
    
    # 추가 꿀팁 정보
    st.markdown(f"🎯 **이런 사람에게 찰떡:** {info['recommended_for']}")
    st.markdown(f"🧬 **이 학과에 많은 MBTI:** `{info['mbti']}`")
    
    # 찜하기 버튼
    if st.button("⭐ 이 학과 관심 목록에 찜하기"):
        if name not in st.session_state.saved_departments:
            st.session_state.saved_departments.append(name)
            st.toast(f"'{name}' 학과가 관심 목록에 저장되었습니다!", icon="💾")
        else:
            st.toast("이미 저장된 학과입니다.", icon="⚠️")

# 7. 사이드바 - 찜한 목록 대시보드
st.sidebar.title("💾 나의 관심 학과")
if st.session_state.saved_departments:
    for saved in st.session_state.saved_departments:
        st.sidebar.markdown(f"- **{saved}** ({DEPARTMENTS_DB[saved]['category']})")
    if st.sidebar.button("목록 비우기"):
        st.session_state.saved_departments = []
        st.rerun()
else:
    st.sidebar.info("추천받은 학과 중 마음에 드는 학과를 찜해보세요!")
