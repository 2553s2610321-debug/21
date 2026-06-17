import streamlit as st
from datetime import datetime

st.set_page_config(page_title="진로 계획 세우기", layout="wide")

# -----------------------------
# 진로 데이터 (확장 버전)
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

# -----------------------------
# 함수
# -----------------------------
def roadmap():
    return [
        "1단계: 기초 공부 (1~3개월)",
        "2단계: 자격 준비 + 경험 쌓기 (3~6개월)",
        "3단계: 실전 경험 + 포트폴리오 (6개월~1년)"
    ]


def top_tasks(activities):
    return activities[:3]


# -----------------------------
# UI
# -----------------------------
st.title("🎯 진로 계획 세우기")
st.write("원하는 직업을 선택하면 맞춤 진로 계획을 만들어드립니다.")

with st.sidebar:
    name = st.text_input("이름")
    age = st.number_input("나이", 10, 100, 18)
    career = st.selectbox("희망 직업", list(CAREER_DB.keys()))
    goal = st.text_input("최종 목표")

    run = st.button("계획 생성")

# -----------------------------
# 결과
# -----------------------------
if run:
    data = CAREER_DB[career]

    st.subheader("📍 진로 요약")

    st.info(
        f"이름: {name if name else '미입력'}\n"
        f"직업: {career}\n"
        f"설명: {data['desc']}\n"
        f"목표: {goal if goal else '없음'}"
    )

    st.divider()

    st.subheader("🧠 필요한 능력")
    for s in data["skills"]:
        st.write("✔ " + s)

    st.subheader("📜 추천 자격")
    for c in data["certs"]:
        st.write("📌 " + c)

    st.subheader("🚀 추천 활동")
    for a in data["activities"]:
        st.write("🔥 " + a)

    st.subheader("🗺️ 진로 단계")
    for r in roadmap():
        st.write(r)

    st.subheader("⚡ 지금 할 일 TOP 3")
    for t in top_tasks(data["activities"]):
        st.success(t)

    st.divider()

    # 다운로드
    text = f"""
===== 진로 계획서 =====

이름: {name}
나이: {age}
희망 직업: {career}
직업 설명: {data['desc']}
목표: {goal}

[필요 능력]
- {'\n- '.join(data['skills'])}

[추천 자격]
- {'\n- '.join(data['certs'])}

[추천 활동]
- {'\n- '.join(data['activities'])}

[진로 단계]
- {'\n- '.join(roadmap())}

생성일: {datetime.now().strftime('%Y-%m-%d')}
"""

    st.download_button(
        "📥 진로 계획 다운로드",
        text,
        file_name="진로계획서.txt",
        mime="text/plain"
    )
