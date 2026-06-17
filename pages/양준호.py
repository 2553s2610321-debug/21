import random

# 1. 5등급제 누적 백분위 및 가이드라인 데이터
grade_info = {
    1: {"percent": "상위 0% ~ 10%", "desc": "최상위권 (기존 9등급제의 1~2등급 수준)"},
    2: {"percent": "상위 10% ~ 34%", "desc": "상위권 (기존 9등급제의 3등급 수준)"},
    3: {"percent": "상위 34% ~ 66%", "desc": "중위권 (기존 9등급제의 4~5등급 수준)"},
    4: {"percent": "상위 66% ~ 90%", "desc": "중하위권 (기존 9등급제의 6~7등급 수준)"},
    5: {"percent": "상위 90% ~ 100%", "desc": "잠재력 발휘 구간 (기존 9등급제의 8~9등급 수준)"}
}

# 2. 등급별 추천 대학 그룹
university_db = {
    1: ["서울대학교", "KAIST", "연세대학교", "고려대학교", "서강대학교", "성균관대학교", "한양대학교"],
    2: ["중앙대학교", "경희대학교", "한국외국어대학교", "서울시립대학교", "건국대학교", "동국대학교", "홍익대학교"],
    3: ["국민대학교", "숭실대학교", "세종대학교", "단국대학교", "광운대학교", "가천대학교", "경기대학교"],
    4: ["명지대학교", "상명대학교", "인천대학교", "가톨릭대학교", "주요 지역 거점 국립대"],
    5: ["전국 내신 5등급 전형 개설 대학 및 전문대학교"]
}

# 3. 무작위로 매칭될 학과 리스트
departments = [
    "컴퓨터공학과", "전자공학과", "기계공학과", "바이오메디컬공학과", "데이터사이언스학과",
    "경영학과", "경제학과", "미디어커뮤니케이션학과", "심리학과", "정치외교학과",
    "영어영문학과", "국어국문학과", "생명과학과", "화학공학과", "디자인학과"
]

def run_university_simulator():
    print("=" * 55)
    print(" 🏫 [5등급제 반영] 내 성적 맞춤 대학 & 학과 시뮬레이터 🏫 ")
    print("=" * 55)
    
    try:
        # 사용자 등급 입력
        grade_input = float(input("자신의 평균 등급을 입력하세요 (1 ~ 5): "))
        grade = round(grade_input)
        
        if grade < 1 or grade > 5:
            print("❌ 올바른 등급(1~5)을 입력해주세요.")
            return

        # 데이터 추출
        info = grade_info[grade]
        available_unis = university_db[grade]
        
        # 무작위 추첨 (대학 & 학과)
        chosen_uni = random.choice(available_unis)
        chosen_dept = random.choice(departments)
        
        # 결과 출력
        print("\n" + "✨" * 25)
        print(f"📊 [입력 등급] : {grade_input}등급 (반올림 기준 {grade}등급)")
        print(f"📈 [5등급제 컷] : 누적 {info['percent']} 이내 위치")
        print(f"💡 [등급 가이드] : {info['desc']}")
        print("-" * 50)
        print(f"🎉 당신의 운명이 이끄는 합격 대학은...")
        print(f"👉 **{chosen_uni} {chosen_dept}** 입니다!")
        print("✨" * 25 + "\n")
        
    except ValueError:
        print("❌ 숫자만 입력해주세요! (예: 1.8 또는 3)")

# 프로그램 실행
if __name__ == "__main__":
    run_university_simulator()
