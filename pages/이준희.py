import streamlit as st
from datetime import datetime

st.set_page_config(page_title="진로 계획 세우기", layout="wide")

# -----------------------------
# 데이터베이스 (간단 추천 로직)
# -----------------------------
CAREER_DB = {
    "개발자": {
        "skills": ["Python", "알고리즘", "Git", "문제 해결 능력"],
        "certs": ["정보처리기사", "SQLD", "컴퓨터활용능력"],
        "activities": ["코딩 프로젝트", "오픈소스 참여", "해커톤 참가"]
    },
    "디자이너": {
        "skills": ["포토샵", "Figma", "UI/UX 이해", "창의력"],
        "certs": ["GTQ", "컴퓨터그래픽스운용기능사"],
        "activities": ["포트폴리오 제작", "앱 디자인 리디자인", "공모전 참가"]
    },
    "마케터": {
        "skills": ["시장 분석", "SNS 운영", "기획력", "데이터 분석"],
        "certs": ["Google Analytics", "유통관리사"],
        "activities": ["SNS 운영", "캠페인 기획", "브랜드 분석"]
    },
    "공무원": {
        "skills": ["국어", "한국사", "행정학", "문제 해결력"],
        "certs": ["한국사능력검정시험", "컴퓨터활용능력"],
        "activities": ["모의고사", "스터디 참여", "기출 분석"]
    }
}

# -----------------------------
# 함수
# -----------------------------
def generate_roadmap():
    return [
        "1단계: 기초 역량 학습 (3~6개월)",
        "2단계: 자격증 취득 및 프로젝트 (6~12개월)",
        "3단계: 실전 경험 및 포트폴리오 강화 (1년~)"
    ]

def make_checklist(items):
    return [f"☐ {item}" for item in items]

def safe_get_career_data(career):
    return CAREER_DB.get(career, {
        "skills": ["기초 역량 분석 필요"],
        "certs": ["관련 자격증 정보 없음"],
        "activities": ["탐색 활동 필요"]
    })

# -----------------------------
# UI
# -----------------------------
st.title("🎯 진로 계획 세우기 앱")
st.write("입력한 정보를 기반으로 맞춤형 진로 로드맵을 제공합니다.")

with st.sidebar:
    st.header("📌 기본 정보 입력")

    name = st.text_input("이름")
    age = st.number_input("나이", min_value=10, max_value=100, value=18)
    career = st.selectbox("희망 직업", ["개발자", "디자이너", "마케터", "공무원"])
    goal = st.text_input("최종 목표 (예: 네이버 취업, 공무원 합격 등)")

    generate = st.button("📊 계획 생성하기")

# -----------------------------
# 결과
# -----------------------------
if generate:
    data = safe_get_career_data(career)

    st.subheader("📍 목표 요약")
    st.success(f"{name}님의 목표: {goal if goal else career 진로 준비}")

    st.subheader("🧠 필요 역량")
    st.write(data["skills"])

    st.subheader("📜 추천 자격증")
    st.write(data["certs"])

    st.subheader("🚀 추천 활동")
    st.write(data["activities"])

    st.subheader("🗺️ 진로 로드맵")
    roadmap = generate_roadmap()
    for r in roadmap:
        st.write(r)

    st.subheader("✅ 실행 체크리스트")
    checklist = make_checklist(data["activities"] + data["certs"])
    for c in checklist:
        st.write(c)

    # -----------------------------
    # 다운로드
    # -----------------------------
    result_text = f"""
진로 계획서

이름: {name}
나이: {age}
희망 직업: {career}
최종 목표: {goal}

[필요 역량]
{data['skills']}

[자격증]
{data['certs']}

[추천 활동]
{data['activities']}

[로드맵]
{roadmap}

생성일: {datetime.now().strftime('%Y-%m-%d')}
"""

    st.download_button(
        label="📥 계획 다운로드",
        data=result_text,
        file_name="career_plan.txt",
        mime="text/plain"
    )
