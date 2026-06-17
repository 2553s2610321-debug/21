import streamlit as st
from datetime import datetime

st.set_page_config(page_title="진로 계획 세우기", layout="wide")

# -----------------------------
# 데이터
# -----------------------------
CAREER_DB = {
    "개발자": {
        "desc": "앱, 웹, 시스템을 만드는 소프트웨어 전문가",
        "skills": ["Python", "알고리즘", "Git", "논리적 사고"],
        "certs": ["정보처리기사", "SQLD", "컴활 1급"],
        "activities": ["GitHub 프로젝트", "코딩테스트", "해커톤 참여"]
    },
    "디자이너": {
        "desc": "사용자 경험과 시각 디자인을 설계하는 전문가",
        "skills": ["Figma", "Photoshop", "UI/UX", "창의력"],
        "certs": ["GTQ", "컴퓨터그래픽스운용기능사"],
        "activities": ["포트폴리오 제작", "앱 리디자인", "공모전"]
    },
    "마케터": {
        "desc": "제품과 브랜드를 알리고 전략을 설계하는 전문가",
        "skills": ["시장 분석", "기획력", "SNS", "데이터 분석"],
        "certs": ["Google Analytics", "유통관리사"],
        "activities": ["SNS 운영", "캠페인 기획", "트렌드 분석"]
    },
    "공무원": {
        "desc": "국가 및 지방 행정 업무를 수행하는 직업",
        "skills": ["국어", "한국사", "행정학", "문제 해결"],
        "certs": ["한국사능력검정시험", "컴퓨터활용능력"],
        "activities": ["기출 문제 풀이", "스터디", "모의고사"]
    }
}

# -----------------------------
# 함수
# -----------------------------
def roadmap():
    return [
        "📘 1단계: 기초 개념 학습 (1~3개월)",
        "🧪 2단계: 자격증 + 미니 프로젝트 (3~6개월)",
        "🚀 3단계: 포트폴리오 + 실전 경험 (6개월~1년)"
    ]


def top_actions(activities):
    return activities[:3]


# -----------------------------
# UI
# -----------------------------
st.title("🎯 진로 계획 세우기")
st.write("당신의 목표에 맞는 현실적인 진로 로드맵을 만들어드립니다.")

with st.sidebar:
    st.header("📌 입력")
    name = st.text_input("이름")
    age = st.number_input("나이", 10, 100, 18)
    career = st.selectbox("희망 직업", list(CAREER_DB.keys()))
    goal = st.text_input("최종 목표")

    run = st.button("📊 계획 생성")

# -----------------------------
# 결과
# -----------------------------
if run:

    data = CAREER_DB.get(career)

    st.subheader("📍 1. 진로 요약")

    st.info(f"""
👤 이름: {name if name else '미입력'}  
🎯 직업: {career}  
📌 설명: {data['desc']}  
🏁 목표: {goal if goal else '미설정'}
""")

    st.divider()

    st.subheader("🧠 2. 필요 역량")
    for s in data["skills"]:
        st.write("✔ " + s)

    st.subheader("📜 3. 추천 자격증")
    for c in data["certs"]:
        st.write("🎓 " + c)

    st.subheader("🚀 4. 추천 활동")
    for a in data["activities"]:
        st.write("🔥 " + a)

    st.subheader("🗺️ 5. 진로 로드맵")
    for r in roadmap():
        st.write(r)

    st.subheader("⚡ 6. 지금 당장 할 일 TOP 3")
    for t in top_actions(data["activities"]):
        st.success(t)

    st.divider()

    # -----------------------------
    # 다운로드
    # -----------------------------
    text = f"""
===== 진로 계획서 =====

이름: {name}
나이: {age}
희망 직업: {career}
직업 설명: {data['desc']}
목표: {goal}

[필요 역량]
- {'\n- '.join(data['skills'])}

[자격증]
- {'\n- '.join(data['certs'])}

[추천 활동]
- {'\n- '.join(data['activities'])}

[로드맵]
- {'\n- '.join(roadmap())}

생성일: {datetime.now().strftime('%Y-%m-%d')}
"""

    st.download_button(
        "📥 진로 계획 다운로드",
        text,
        file_name="career_plan.txt",
        mime="text/plain"
    )
