import streamlit as st
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="방구석 진로 탐색기",
    page_icon="🎓",
    layout="centered"
)

# 2. 20개로 확장된 학과 데이터베이스 (계열별 5개 학과씩 엄선)
DEPARTMENTS_DB = {
    # === 공학계열 (5개) ===
    "컴퓨터공학과": {
        "category": "공학계열",
        "summary": "현대 디지털 세상을 움직이는 소프트웨어 마법사를 양성하는 곳",
        "keywords": ["#개발자", "#AI", "#코딩노예", "#고연봉"],
        "pros": ["전 세계 어디서나 취업 기회가 많음", "원격 근무 및 자유로운 조직 문화"],
        "cons": ["트렌드가 너무 빨라 평생 공부해야 함", "거북목과 손목 통증의 위험"],
        "recommended_for": "논리적이고 퍼즐 풀기를 좋아하며 끈기 있는 사람",
        "mbti": "INTJ / INTP / ISTP"
    },
    "기계공학과": {
        "category": "공학계열",
        "summary": "자동차, 로봇, 우주선까지 움직이는 모든 기계를 설계하는 공학의 뿌리",
        "keywords": ["#역학지옥", "#로봇", "#취업깡패", "#설계"],
        "pros": ["제조업 기반 국가(한국)에서 매우 높은 취업률", "기계 구조를 이해하는 쾌감"],
        "cons": ["4대 역학의 무지막지한 수학/물리 폭격", "다소 딱딱하고 보수적인 조직 문화"],
        "recommended_for": "물건을 분해/조립하고 역학적 원리에 흥미가 있는 사람",
        "mbti": "ISTJ / ESTJ / ISTP"
    },
    "화학공학과": {
        "category": "공학계열",
        "summary": "신소재, 배터리, 석유화학 등 물질을 유용한 제품으로 대량 생산하는 학문",
        "keywords": ["#배터리", "#반도체", "#정유사", "#취업치트키"],
        "pros": ["전통적인 취업 치트키 라인 중 하나", "석유화학, 에너지, 바이오 등 넓은 진출 분야"],
        "cons": ["실제 화학 물질보다는 거대한 공정 설계(수학/물리) 중심", "지방 공장 근무 가능성"],
        "recommended_for": "수학적 계산과 스케일이 큰 공정 시스템에 관심이 있는 사람",
        "mbti": "ESTJ / ISTJ / INTJ"
    },
    "전자공학과": {
        "category": "공학계열",
        "summary": "반도체, 스마트폰, 자율주행 등 하드웨어 회로와 신호를 제어하는 핵심 공학",
        "keywords": ["#반도체", "#회로설계", "#대기업깡패", "#납땜"],
        "pros": ["대한민국 핵심 산업(반도체/디스플레이)의 중심이라 취업 시장이 매우 거대함", "기술 전문성 확보"],
        "cons": ["눈에 보이지 않는 전자와 신호를 다루어 개념 이해가 매우 추상적이고 어려움", "공부량이 압도적"],
        "recommended_for": "꼼꼼하고 분석적이며 전자기기의 작동 원리에 호기심이 많은 사람",
        "mbti": "ISTJ / INTJ / ESTP"
    },
    "건축학과": {
        "category": "공학계열",
        "summary": "인간이 살아가는 공간을 예술적으로 디자인하고 안전하게 설계하는 학문",
        "keywords": ["#설계도", "#모형제작", "#밤샘디자인", "#예술과공학사이"],
        "pros": ["내가 설계한 건축물이 세상에 남는 장기적인 보람", "예술적 감각과 기술적 능력을 동시에 발휘"],
        "cons": ["마감 직전 상상을 초월하는 밤샘 작업", "일반 공학 계열 대비 상대적으로 긴 5년제 교육과정"],
        "recommended_for": "미적 감각이 있고 공간에 대한 열정이 넘치며 야근을 견딜 체력이 있는 사람",
        "mbti": "INFP / ISFP / ENFP"
    },

    # === 인문/사회계열 (5개) ===
    "심리학과": {
        "category": "인문/사회계열",
        "summary": "인간의 마음과 행동의 비밀을 과학적인 실험과 통계로 파헤치는 학문",
        "keywords": ["#마음읽기", "#상담", "#독심술아님", "#통계학"],
        "pros": ["나 자신과 타인에 대한 깊은 이해 가능", "마케팅, UX, 인사 등 확장성 좋음"],
        "cons": ["의외로 수학(통계)을 엄청나게 많이 함", "상담사 등 전문직은 대학원 진학 필수"],
        "recommended_for": "사람에 대한 호기심이 많고, 타인의 고민을 잘 들어주는 사람",
        "mbti": "INFJ / INFP / ENFJ"
    },
    "경영학과": {
        "category": "인문/사회계열",
        "summary": "기업을 효율적으로 운영하고 돈의 흐름을 조율하는 비즈니스 리더의 요람",
        "keywords": ["#CEO", "#마케팅", "#팀플지옥", "#발표왕"],
        "pros": ["취업 선택의 폭이 가장 넓음(모든 회사엔 경영이 필요)", "커뮤니케이션 능력 향상"],
        "cons": ["넓게 배우지만 깊이가 애매해질 수 있음", "끊임없는 발표와 팀 프로젝트 스트레스"],
        "recommended_for": "리더십이 있고 트렌드에 민감하며 효율성을 중시하는 사람",
        "mbti": "ENTJ / ESTJ / ENFJ"
    },
    "미디어커뮤니케이션학과": {
        "category": "인문/사회계열",
        "summary": "방송, 신문, 유튜브부터 뉴미디어 콘텐츠까지 언론과 언어의 소통을 연구",
        "keywords": ["#PD", "#기자", "#콘텐츠기획", "#유튜브"],
        "pros": ["세상의 트렌드를 가장 먼저 읽는 힘이 생김", "영상, 글 등 크리에이티브한 활동 가능"],
        "cons": ["화려해 보이지만 실상은 야근과 마감 압박의 연속", "언론사 및 방송국 취업문이 좁음"],
        "recommended_for": "콘텐츠 소비를 좋아하고, 세상 돌아가는 이야기에 관심이 많은 사람",
        "mbti": "ENFP / ENTP / ENFJ"
    },
    "경제학과": {
        "category": "인문/사회계열",
        "summary": "사회 전체의 유한한 자원을 어떻게 효율적으로 분배할지 연구하는 사회과학의 꽃",
        "keywords": ["#주식", "#금융권", "#그래프지옥", "#수학적사회과학"],
        "pros": ["금융권, 국책연구소, 대기업 기획실 등 상위권 취업에 매우 유리", "세상을 보는 냉철한 눈을 가짐"],
        "cons": ["말만 문과지 실제로는 미적분과 통계학 공식으로 가득 찬 가짜 문과 학과"],
        "recommended_for": "숫자와 그래프에 강하고, 사회 현상의 인과관계를 논리적으로 분석하기 좋아하는 사람",
        "mbti": "INTJ / INTP / ESTJ"
    },
    "정치외교학과": {
        "category": "인문/사회계열",
        "summary": "권력의 역동성과 국가 간의 외교 전략을 배우며 글로벌 리더를 꿈꾸는 곳",
        "keywords": ["#외교관", "#정치인", "#토론", "#국제정세"],
        "pros": ["글로벌 이슈를 읽는 시야가 넓어지고 논리적 말하기 및 글쓰기 실력이 폭발함"],
        "cons": ["뚜렷한 기술을 배우는 게 아니라 기업 취업 시 스스로 직무 역량을 증명해야 함"],
        "recommended_for": "시사 뉴스 보는 것이 취미이고 비판적 사고와 토론을 즐기는 사람",
        "mbti": "ENTJ / ENTP / ENFJ"
    },

    # === 자연/과학계열 (5개) ===
    "생명공학과": {
        "category": "자연/과학계열",
        "summary": "바이오, 신약 개발 등 인류의 건강과 미래를 책임지는 첨단 과학 학문",
        "keywords": ["#바이오", "#DNA", "#백신", "#실험실"],
        "pros": ["고령화 시대에 가장 유망한 미래 성장 동력", "보람 있는 연구 가치"],
        "cons": ["실험 결과가 나올 때까지 무한 기다림(인내심 필수)", "학사 학위만으론 연구직 한계"],
        "recommended_for": "관찰력이 좋고 생물학적 신비로움에 가슴이 뛰는 사람",
        "mbti": "INTP / INTJ / ISTJ"
    },
    "통계학과": {
        "category": "자연/과학계열",
        "summary": "방대한 데이터 속에서 의미 있는 인사이트와 법칙을 찾아내는 학문",
        "keywords": ["#데이터사이언스", "#빅데이터", "#수학", "#알고리즘"],
        "pros": ["4차 산업혁명 시대(AI, 빅데이터) 최고의 블루칩 학과", "정보기술/금융권 취업 매우 유리"],
        "cons": ["순수 수학과 맞먹는 엄청난 수준의 수학적 증명과 코딩 스트레스"],
        "recommended_for": "숫자를 다루는 것을 좋아하고 데이터 분석에 흥미가 있는 사람",
        "mbti": "INTP / ISTJ / INTJ"
    },
    "수학과": {
        "category": "자연/과학계열",
        "summary": "자연과학의 근간이자 우주의 언어인 숫자와 기호의 논리적 순수성을 탐구",
        "keywords": ["#순수학문", "#증명지옥", "#천재들의놀이터", "#금융공학"],
        "pros": ["논리력의 끝판왕이 됨", "최근 AI 및 금융공학 발달로 몸값이 치솟는 중"],
        "cons": ["고등학교 수학은 수학이 아니었음을 깨달음", "숫자 대신 온통 영어와 기호로만 증명함"],
        "recommended_for": "문제가 풀릴 때까지 며칠 동안 한 문제만 붙잡고 있어도 행복한 사람",
        "mbti": "INTP / INTJ"
    },
    "물리학과": {
        "category": "자연/과학계열",
        "summary": "미시 세계의 양자역학부터 거시 세계의 우주까지 만물의 법칙을 연구하는 학문",
        "keywords": ["#아인슈타인", "#양자역학", "#우주론", "#이론물리"],
        "pros": ["세상의 모든 작동 원리를 근본적으로 이해할 수 있는 지적 쾌감", "공학 전반의 기초 체력 형성"],
        "cons": ["학문의 난이도가 인간 한계를 시험함", "마찬가지로 심도 깊은 연구를 위해 대학원 필수 성향"],
        "recommended_for": "호기심의 깊이가 끝이 없고 \"이건 왜 이렇지?\"라는 질문을 입에 달고 사는 사람",
        "mbti": "INTP / INTJ"
    },
    "천문우주학과": {
        "category": "자연/과학계열",
        "summary": "별, 은하, 블랙홀 등 미지의 우주 공간과 위성/우주선 탐사를 연구하는 낭만 학문",
        "keywords": ["#블랙홀", "#나사(NASA)", "#망원경", "#우주항공"],
        "pros": ["광활한 우주를 연구한다는 독보적인 낭만과 지적 충족감", "우주 항공 산업 발전으로 유망성 상승"],
        "cons": ["별을 보는 감성적인 곳이 아니라 하루 종일 프로그래밍과 데이터 코딩만 하는 반전 학과"],
        "recommended_for": "우주 다큐멘터리를 보면 밤에 잠이 안 올 정도로 가슴이 뛰는 사람",
        "mbti": "INTP / INFJ"
    },

    # === 예체능계열 (5개) ===
    "시각디자인학과": {
        "category": "예체능계열",
        "summary": "텍스트와 이미지를 활용해 세상과 시각적으로 소통하는 시각 크리에이터",
        "keywords": ["#포토샵", "#브랜딩", "#밤샘작업", "#컨셉"],
        "pros": ["내 아이디어가 멋진 결과물로 탄생하는 쾌감", "포트폴리오 중심의 확실한 실력 사회"],
        "cons": ["\"알아서 예쁘게 해주세요\"라는 클라이언트의 피드백 지옥", "잦은 밤샘과 마감 압박"],
        "recommended_for": "미적 감각이 뛰어나고, 시각적 요소로 표현하는 것을 좋아하는 사람",
        "mbti": "ISFP / INFP / ENFP"
    },
    "체육학과": {
        "category": "예체능계열",
        "summary": "신체 활동을 과학적으로 분석하고 스포츠 산업 및 건강 증진을 연구하는 학문",
        "keywords": ["#스포츠", "#운동선수", "#트레이너", "#활력"],
        "pros": ["활동적이고 건강한 대학 생활", "웰빙 시대 스포츠 마케팅 및 재활 등 유망 분야 존재"],
        "cons": ["강도 높은 신체 훈련으로 인한 부상 위험", "선후배 간의 다소 규율이 강한 문화"],
        "recommended_for": "운동을 사랑하고 활동적이며, 건강한 에너지를 전파하고 싶은 사람",
        "mbti": "ESTP / ESFP / ENFJ"
    },
    "작곡과": {
        "category": "예체능계열",
        "summary": "소리를 디자인하고 멜로디와 화성을 엮어 세상에 없는 음악을 창조하는 학문",
        "keywords": ["#플레이리스트", "#오케스트라", "#미디(MIDI)", "#저작권료"],
        "pros": ["내가 만든 음악을 사람들이 들을 때의 엄청난 희열", "클래식부터 대중음악까지 넓은 스펙트럼"],
        "cons": ["하얀 악보를 마주했을 때 찾아오는 창작의 고통", "치열한 프리랜서 시장 생존 경쟁"],
        "recommended_for": "감수성이 풍부하고 하루 종일 머릿속에서 멜로디가 맴도는 사람",
        "mbti": "INFP / ISFP / ENFP"
    },
    "연극영화학과": {
        "category": "예체능계열",
        "summary": "무대 위 연기부터 카메라 뒤 연출, 시나리오까지 영상 예술 전반을 배우는 곳",
        "keywords": ["#배우", "#영화감독", "#시나리오", "#오디션"],
        "pros": ["인간의 삶을 간접 체험하며 내면이 깊어짐", "끈끈한 동기들과의 공동체 의식 및 인맥"],
        "cons": ["불규칙한 촬영 스케줄로 인한 체력 방전", "인정받기 전까지의 긴 무명 시절 감내 필요"],
        "recommended_for": "표현력이 풍부하고 스포트라이트를 즐기거나 이야기 속에 빠져 살기 좋아하는 사람",
        "mbti": "ENFP / ENFJ / ESFP"
    },
    "웹툰만화콘텐츠학과": {
        "category": "예체능계열",
        "summary": "K-콘텐츠의 중심인 웹툰, 스토리보드, 캐릭터 디자인 전문 인력을 양성",
        "keywords": ["#타블렛", "#스토리텔링", "#K-웹툰", "#마감사수"],
        "pros": ["글과 그림을 동시에 다루는 종합 예술가로 성장", "플랫폼 다변화로 시장이 매우 활성화됨"],
        "cons": ["앉아서 하루에 10시간 이상 작화하느라 허리와 손목이 남아나질 않음", "독자들의 냉정한 평점 스트레스"],
        "recommended_for": "만화나 애니메이션을 매일 챙겨보고 상상한 스토리를 시각화하기 좋아하는 사람",
        "mbti": "INFP / ISFP / INTP"
    }
}

# 3. 세션 상태(Session State) 초기화
if "saved_departments" not in st.session_state:
    st.session_state.saved_departments = []

# 4. UI 구성
st.title("🎓 방구석 진로 탐색기 V3")
st.caption("어떤 학과를 갈지 모르겠나요? 4대 계열 20가지 다양한 학과 속에서 주사위를 굴려보세요!")

st.markdown("---")

# 5. 사용자 입력 (필터링 기능)
st.subheader("🎲 원하는 계열을 선택하고 버튼을 눌러보세요!")
category_list = ["전체"] + list(set(dept["category"] for dept in DEPARTMENTS_DB.values()))
selected_category = st.selectbox("관심 계열 선택", category_list)

# 버튼 디자인 및 클릭 이벤트 처리
if st.button("🔮 랜덤 학과 추천받기", type="primary", use_container_width=True):
    try:
        if selected_category == "전체":
            filtered_depts = list(DEPARTMENTS_DB.keys())
        else:
            filtered_depts = [name for name, info in DEPARTMENTS_DB.items() if info["category"] == selected_category]
        
        chosen_dept_name = random.choice(filtered_depts)
        chosen_dept_info = DEPARTMENTS_DB[chosen_dept_name]
        
        st.session_state.current_dept = (chosen_dept_name, chosen_dept_info)
    except Exception as e:
        st.error("학과를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")

# 6. 결과 출력 영역
if "current_dept" in st.session_state:
    name, info = st.session_state.current_dept
    
    st.success(f"🎉 오늘의 추천 학과: **[{info['category']}] {name}**")
    
    # 키워드 태그
    st.markdown(f"**{' '.join(info['keywords'])}**")
    
    # 한 줄 요약
    st.info(f"💡 **한 줄 요약:** {info['summary']}")
    
    # 장단점 비교 레이아웃
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
