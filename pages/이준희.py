import streamlit as st
from datetime import datetime

st.set_page_config(page_title="진로 계획 세우기", layout="wide")

# -----------------------------
# 진로 데이터
# -----------------------------
CAREER_DB = {
    "개발자": {
        "skills": ["Python", "자료구조", "Git", "문제 해결 능력"],
        "certs": ["정보처리기사", "SQLD", "컴퓨터활용능력"],
        "activities": ["코딩 프로젝트", "GitHub 업로드", "해커톤 참여"]
    },
    "디자이너": {
        "skills": ["Figma", "Photoshop", "UI/UX 이해", "창의력"],
        "certs": ["GTQ", "컴퓨터그래픽스운용기능사"],
        "activities": ["포트폴리오 제작", "앱 리디자인", "공모전 참가"]
    },
    "마케터": {
        "skills": ["시장 분석", "SNS 운영", "기획력", "데이터 분석"],
        "certs": ["Google Analytics", "유통관리사"],
        "activities": ["SNS 운영", "캠페인 기획", "브랜드 분석"]
    },
    "공무원": {
        "skills": ["국어", "한국사", "행정학", "문제 해결력"],
        "certs": ["한국사능력검정시험", "컴퓨터활용능력"],
        "activities": ["기출문제 풀이", "스터디 참여", "모의고사"]
    }
}

# -----------------------------
# 함수
# -----------------------------
def get_data(career):
    if career in CAREER_DB:
        return CAREER_DB[career]
    return {
        "skills": ["기초 정보 부족"],
        "certs": ["관련 자격증 없음"],
        "activities": ["탐색 필요"]
    }


def make_roadmap():
    return [
        "1단계: 기초 역량 학습 (1~3개월)",
        "2단계: 자격증 준비 및 프로젝트 (3~12개월)",
        "3단계: 포트폴리오 및 실전 경험 (1년+)"
    ]


def make_checklist(items):
    result = []
    for item in items:
        result.append("☐ " + item)
    return result


# -----------------------------
# UI
# -----------------------------
st.title("🎯 진로 계획 세우기 앱")
st.write("희망 직업을 입력하면 맞춤 진로 계획을 만들어줍니다.")

with st.sidebar:
    st.header("📌 입력 정보")

    name = st.text_input("이름")
    age = st.number_input("나이", min_value=10, max_value=100, value=18)
    career = st.selectbox("희망 직업", ["개발자", "디자이너", "마케터", "공무원"])
    goal = st.text_input("최종 목표 (예: 취업, 합격 등)")

    run = st.button("📊 계획 생성")

# -----------------------------
# 결과 출력
# -----------------------------
if run:
    data = get_data(career)

    st.subheader("📍 목표 요약")

    if name == "":
        st.warning("이름을 입력하지 않았습니다.")
    else:
        st.success(name + "님의 진로 계획")

    if goal == "":
        st.info("목표가 비어 있습니다. 선택한 직업 기준으로 생성됩니다.")
    else:
        st.write("🎯 목표:", goal)

    st.subheader("🧠 필요 역량")
    st.write(data["skills"])

    st.subheader("📜 추천 자격증")
    st.write(data["certs"])

    st.subheader("🚀 추천 활동")
    st.write(data["activities"])

    st.subheader("🗺️ 진로 로드맵")
    roadmap = make_roadmap()
    for r in roadmap:
        st.write("- " + r)

    st.subheader("✅ 실행 체크리스트")
    checklist = make_checklist(data["activities"] + data["certs"])
    for c in checklist:
        st.write(c)

    # -----------------------------
    # 다운로드 기능
    # -----------------------------
    text = ""
    text += "진로 계획서\n\n"
    text += "이름: " + str(name) + "\n"
    text += "나이: " + str(age) + "\n"
    text += "희망 직업: " + career + "\n"
    text += "목표: " + str(goal) + "\n\n"

    text += "[필요 역량]\n" + ", ".join(data["skills"]) + "\n\n"
    text += "[자격증]\n" + ", ".join(data["certs"]) + "\n\n"
    text += "[활동]\n" + ", ".join(data["activities"]) + "\n\n"

    text += "[로드맵]\n"
    for r in roadmap:
        text += "- " + r + "\n"

    text += "\n생성일: " + str(datetime.now().strftime("%Y-%m-%d"))

    st.download_button(
        label="📥 계획 다운로드",
        data=text,
        file_name="career_plan.txt",
        mime="text/plain"
    )
