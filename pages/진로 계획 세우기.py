import streamlit as st
import datetime

# 페이지 설정 (가장 상단에 위치해야 합니다)
st.set_page_config(
    page_title="🎯 나만의 진로 계획 플래너",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# 1. 진로 데이터베이스 (제공된 데이터 완벽 반영)
# -----------------------------
CAREER_DB = {
    "개발자": {
        "desc": "컴퓨터 프로그램이나 앱을 만드는 사람입니다.",
        "skills": ["논리적 사고", "컴퓨터 이해", "코딩 기초", "꾸준한 학습"],
        "certs": ["컴퓨터 활용 능력", "정보 기술 기초 자격", "코딩 기초 인증"],
        "activities": ["간단한 앱 만들기", "코딩 공부 사이트 활용", "웹사이트 제작"]
    },
    "디자이너": {
        "desc": "보기 좋은 그림과 화면을 만드는 사람입니다.",
        "skills": ["색감 이해", "그림 감각", "디자인 도구 사용", "창의력"],
        "certs": ["그래픽 디자인 자격", "디지털 그림 능력 인증"],
        "activities": ["포스터 제작", "UI 디자인 따라하기", "포트폴리오 만들기"]
    },
    "마케터": {
        "desc": "상품이나 서비스를 알리는 사람입니다.",
        "skills": ["기획력", "글쓰기", "분석력", "트렌드 이해"],
        "certs": ["기초 마케팅 이해", "데이터 분석 기초"],
        "activities": ["SNS 운영", "광고 기획", "트렌드 분석"]
    },
    "공무원": {
        "desc": "국가와 지역을 위해 행정 업무를 하는 사람입니다.",
        "skills": ["국어", "한국사", "문제 해결력", "책임감"],
        "certs": ["한국사 능력 시험", "컴퓨터 활용 능력"],
        "activities": ["기출 문제 풀이", "공부 계획", "스터디"]
    },
    "의사": {
        "desc": "사람들의 건강을 진단하고 치료하는 사람입니다.",
        "skills": ["생물 이해", "집중력", "책임감", "공부 능력"],
        "certs": ["의과대학 진학", "의사 국가고시"],
        "activities": ["생물 공부", "병원 체험", "과학 실험"]
    },
    "간호사": {
        "desc": "환자를 돌보고 치료를 돕는 사람입니다.",
        "skills": ["배려심", "생물 지식", "책임감", "체력"],
        "certs": ["간호학과 졸업", "간호사 국가시험"],
        "activities": ["병원 봉사", "응급처치 공부", "의료 체험"]
    },
    "교사": {
        "desc": "학생들에게 지식을 가르치는 사람입니다.",
        "skills": ["설명 능력", "책임감", "인내심", "전공 지식"],
        "certs": ["교원 자격증"],
        "activities": ["학습 지도", "봉사 활동", "교육 실습"]
    },
    "경찰": {
        "desc": "사람들의 안전을 지키는 사람입니다.",
        "skills": ["체력", "판단력", "책임감", "정의감"],
        "certs": ["경찰 시험"],
        "activities": ["체력 운동", "법 공부", "훈련 참여"]
    },
    "소방관": {
        "desc": "화재와 사고에서 사람을 구하는 사람입니다.",
        "skills": ["체력", "용기", "판단력", "협동심"],
        "certs": ["소방 공무원 시험"],
        "activities": ["체력 훈련", "응급 구조 공부", "안전 교육"]
    },
    "유튜버": {
        "desc": "영상 콘텐츠를 만들어 사람들과 소통하는 사람입니다.",
        "skills": ["창의력", "영상 편집", "소통 능력", "기획력"],
        "certs": ["없음 (실력 중심)"],
        "activities": ["영상 촬영", "편집 연습", "채널 운영"]
    },
    "요리사": {
        "desc": "음식을 만들고 요리하는 사람입니다.",
        "skills": ["요리 기술", "창의력", "손재주", "위생 관리"],
        "certs": ["조리 기능사"],
        "activities": ["요리 연습", "레시피 개발", "식당 체험"]
    },
    "운동선수": {
        "desc": "스포츠 경기에서 활동하는 사람입니다.",
        "skills": ["체력", "기술", "집중력", "인내심"],
        "certs": ["종목별 자격 없음"],
        "activities": ["운동 훈련", "경기 참가", "체력 관리"]
    },
    "회계사": {
        "desc": "회사의 돈을 관리하고 기록하는 사람입니다.",
        "skills": ["수학", "분석력", "꼼꼼함", "책임감"],
        "certs": ["회계 관련 자격증"],
        "activities": ["회계 공부", "엑셀 연습", "경제 공부"]
    },
    "건축가": {
        "desc": "건물과 구조물을 설계하는 사람입니다.",
        "skills": ["공간 이해", "수학", "창의력", "설계 능력"],
        "certs": ["건축사 자격증"],
        "activities": ["설계 연습", "모형 제작", "도면 공부"]
    },
    "항공승무원": {
        "desc": "비행기에서 승객을 안전하게 돕는 사람입니다.",
        "skills": ["서비스 정신", "외국어", "친절함", "대처 능력"],
        "certs": ["항공 관련 교육 과정"],
        "activities": ["외국어 공부", "서비스 연습", "면접 준비"]
    }
}

# 기본 로드맵 가이드 함수
def roadmap():
    return [
        "1단계: 기초 공부 (1~3개월)",
        "2단계: 자격 준비 + 경험 쌓기 (3~6개월)",
        "3단계: 실전 경험 + 포트폴리오 (6개월~1년)"
    ]

# -----------------------------
# 2. 세션 상태 초기화 및 데이터 로딩
# -----------------------------
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []
if "selected_career" not in st.session_state:
    st.session_state.selected_career = list(CAREER_DB.keys())[0]

# 상단 타이틀
st.title("🎯 맞춤형 진로 계획 로드맵 플래너")
st.markdown("""
원하는 직업을 선택하면 표준 가이드 라인이 제공되며, 이를 바탕으로 **나만의 세부 계획 설정 및 실시간 실천 체크리스트 기능**을 이용할 수 있습니다.
""")
st.write("---")

# 화면 구성 분할 (좌측: 입력 및 제어, 우측: 실시간 시각화 대시보드)
col1, col2 = st.columns([1, 1.2])

# -----------------------------
# 3. 좌측 영역: 데이터 및 계획 입력 서식
# -----------------------------
with col1:
    st.header("📋 기본 정보 및 목표 설정")
    
    with st.form("career_form"):
        name = st.text_input("이름 또는 닉네임", value="홍길동")
        age = st.number_input("나이", min_value=10, max_value=100, value=18)
        career = st.selectbox("희망 직업 선택", list(CAREER_DB.keys()), index=list(CAREER_DB.keys()).index(st.session_state.selected_career))
        goal = st.text_input("최종 도달 목표", value="해당 분야 최고의 전문가가 되어 선한 영향력 펼치기")
        
        st.subheader("🗓️ 기간별 나만의 상세 계획 설계")
        st.caption("아래 가이드를 바탕으로 자신만의 실천 목표를 자유롭게 다듬어주세요.")
        
        plan_short = st.text_area("단기 계획 (1~3개월 목표)", 
                                  value="- 직무 관련 기본 이론 도서 2권 완독하기\n- 추천 기초 스킬 학습 및 기초 인강 수강")
        
        plan_mid = st.text_area("중기 계획 (3~6개월 목표)", 
                                 value="- 하단 대시보드에 추천된 '추천 자격증' 접수 및 취득 공부\n- 관련 분야 동아리 혹은 학습 스터디 구하기")
        
        plan_long = st.text_area("장기 계획 (6개월~1년 목표)", 
                                 value="- 추천 활동 내용들을 바탕으로 개인 포트폴리오 사이트 제작\n- 실제 인턴십 기회 탐색 또는 실전 공모전 도전")
        
        submitted = st.form_submit_button("🎯 맞춤형 로드맵 생성 및 반영")
        
        if submitted:
            st.session_state.selected_career = career
            # 신규 로드맵 생성 시 데이터베이스 내 추천 활동들을 체크리스트에 자동 매핑 등록
            base_activities = CAREER_DB[career]["activities"]
            base_skills = CAREER_DB[career]["skills"]
            
            # 초기화 및 기본 추천 과제 탑재
            st.session_state.todo_list = [{"task": f"[{career} 추천과제] {act}", "done": False} for act in base_activities]
            st.session_state.todo_list.append({"task": f"[{career} 핵심역량] {base_skills[0]} 기르기", "done": False})
            st.rerun()

    # 동적 체크리스트 관리 시스템
    st.write("---")
    st.subheader("🛠️ 실천 체크리스트 & 역량 캘린더")
    st.caption("위에서 직업을 바꾸고 버튼을 누르면 추천 활동이 자동 세팅되며, 수동으로 나만의 과제를 더 추가할 수 있습니다.")
    
    new_todo = st.text_input("나만의 커스텀 실천 과제 추가:", placeholder="예: 매일 관련 뉴스 스크랩하기, 자격증 기출 풀기")
    if st.button("➕ 과제 추가"):
        if new_todo.strip():
            st.session_state.todo_list.append({"task": new_todo.strip(), "done": False})
            st.rerun()
        else:
            st.warning("내용을 입력한 뒤 추가 버튼을 눌러주세요.")

    if st.session_state.todo_list:
        st.write("**현재 나의 미션 목록:**")
        updated_todos = []
        for i, item in enumerate(st.session_state.todo_list):
            is_done = st.checkbox(item["task"], value=item["done"], key=f"todo_item_{i}")
            updated_todos.append({"task": item["task"], "done": is_done})
        st.session_state.todo_list = updated_todos
        
        if st.button("🧹 완료된 항목 목록에서 청소"):
            st.session_state.todo_list = [item for item in st.session_state.todo_list if not item["done"]]
            st.rerun()
    else:
        st.info("현재 관리 중인 실천 체크리스트가 비어있습니다.")

# -----------------------------
# 4. 우측 영역: 대시보드 시각화 및 다운로드
# -----------------------------
with col2:
    st.header("📊 마이 커리어 대시보드")
    
    # 세션에 저장된 현재 타겟 직업 정보 추출
    current_career = st.session_state.selected_career
    data = CAREER_DB[current_career]
    
    # 상단 메인 프로필 요약 카드
    st.info(f"👤 **작성자**: {name if name else '미입력'} ({age}세)  |  🎯 **희망 직업**: {current_career}")
    
    # 직업 설명 및 핵심 비전
    st.subheader("💡 직업 설명")
    st.markdown(f"> {data['desc']}")
    
    st.subheader("🎯 나의 최종 비전")
    st.success(f"“ {goal if goal else '설정된 최종 비전이 없습니다.'} ”")
    
    st.write("---")
    
    # 데이터를 구조화하여 탭 분할 배치
    tab1, tab2, tab3 = st.tabs(["🧠 역량 및 추천정보", "🗺️ 진로 단계 및 세부계획", "⚡ 지금 할 일 TOP 3"])
    
    with tab1:
        c_sub1, c_sub2 = st.columns(2)
        with c_sub1:
            st.markdown("#### 🧠 필요한 능력")
            for s in data["skills"]:
                st.markdown(f"✔ {s}")
        with c_sub2:
            st.markdown("#### 📜 추천 자격")
            for c in data["certs"]:
                st.markdown(f"📌 {c}")
                
        st.write("---")
        st.markdown("#### 🚀 추천 활동 목록")
        for a in data["activities"]:
            st.markdown(f"🔥 {a}")
            
    with tab2:
        st.markdown("#### 🧭 시스템 표준 진로 단계")
        for r in roadmap():
            st.markdown(f"📍 {r}")
            
        st.write("---")
        st.markdown("#### 📝 내가 설계한 세부 실천 과제")
        with st.expander("⏱️ 1단계: 단기 계획 (1~3개월)", expanded=True):
            st.write(plan_short)
        with st.expander("⌛ 2단계: 중기 계획 (3~6개월)", expanded=True):
            st.write(plan_mid)
        with st.expander("🔮 3단계: 장기 계획 (6개월~1년)", expanded=True):
            st.write(plan_long)
            
    with tab3:
        st.markdown("#### ⚡ 우선적으로 실천해야 할 핵심 TOP 3 활동")
        # 데이터베이스 내 activities의 상위 3개 자동 바인딩
        for i, t in enumerate(data["activities"][:3]):
            st.success(f"**TOP {i+1}** : {t}")

    # 실시간 달성률 분석 시스템
    st.write("---")
    st.subheader("📈 실천 과제 달성률 리포트")
    
    if st.session_state.todo_list:
        total_tasks = len(st.session_state.todo_list)
        completed_tasks = sum(1 for item in st.session_state.todo_list if item["done"])
        progress_percentage = completed_tasks / total_tasks
        
        st.write(f"현재 총 {total_tasks}개의 계획 미션 중 **{completed_tasks}개 체크 완료**")
        st.progress(progress_percentage)
        st.metric(label="목표 도달 스코어", value=f"{int(progress_percentage * 100)}%")
    else:
        st.warning("왼쪽 서식에서 '🎯 맞춤형 로드맵 생성 및 반영' 버튼을 누르시면 실시간 달성률 계측기가 작동합니다.")

    # 저장 및 파일 다운로드 가속화
    st.write("---")
    st.subheader("💾 완성된 진로 계획서 저장")
    
    # 텍스트 파일 포맷 빌드
    report_text = f"""=========================================
[{name}]님의 커리어 맞춤형 진로 계획 리포트
생성일자: {datetime.date.today()}
=========================================

[1. 기본 프로필]
- 이름: {name}
- 나이: {age}세
- 희망 직업: {current_career}
- 직업 정의: {data['desc']}
- 나의 비전: {goal}

-----------------------------------------
[2. 데이터 기반 매칭 가이드라인]
■ 요구 역량: {', '.join(data['skills'])}
■ 추천 자격증: {', '.join(data['certs'])}
■ 추천 핵심활동: {', '.join(data['activities'])}

-----------------------------------------
[3. 수립한 기간별 상세 계획 목록]
■ 단기 계획 (1~3개월):
{plan_short}

■ 중기 계획 (3~6개월):
{plan_mid}

■ 장기 계획 (6개월~1년):
{plan_long}

-----------------------------------------
[4. 시스템 추천 진로 프로세스 기본형]
{'- ' + '\\n- '.join(roadmap())}
========================================="""

    st.download_button(
        label="📥 완벽 통합 진로계획서(.txt) 다운로드",
        data=report_text,
        file_name=f"진로계획서_{name}_{current_career}.txt",
        mime="text/plain"
    )
