import random

# 1. 개편된 5등급제 기준 대학 데이터베이스 (예시 데이터)
university_db = {
    1: ["서울대학교", "KAIST", "연세대학교", "고려대학교", "서강대학교", "성균관대학교", "한양대학교"],
    2: ["중앙대학교", "경희대학교", "한국외국어대학교", "서울시립대학교", "건국대학교", "동국대학교", "홍익대학교"],
    3: ["국민대학교", "숭실대학교", "세종대학교", "단국대학교", "광운대학교", "가천대학교", "경기대학교"],
    4: ["명지대학교", "상명대학교", "인천대학교", "가톨릭대학교", "주요 지역 거점 국립대"],
    5: ["전국 각지의 잠재력 넘치는 대학들! (어디서든 치열하게 하면 성공합니다)"]
}

def recommend_university_5grades():
    print("=" * 45)
    print("   🏫 [신교육과정] 내 성적 맞춤 대학 무작위 추천 🏫   ")
    print("=" * 45)
    
    try:
        # 사용자로부터 개편된 5등급제 기준 입력 받기
        grade_input = float(input("자신의 평균 등급을 입력하세요 (1 ~ 5): "))
        
        # 소수점 입력 시 반올림하여 정수 등급으로 변환 (예: 1.3등급 -> 1등급)
        grade = round(grade_input)
        
        # 5등급제 범위 예외 처리
        if grade < 1 or grade > 5:
            print("❌ 올바른 등급(1~5)을 입력해주세요.")
            return

        # 해당 등급의 대학 리스트 가져오기
        available_unis = university_db[grade]
        
        # 무작위로 하나 선택
        chosen_uni = random.choice(available_unis)
        
        # 결과 출력
        print("\n" + "-" * 45)
        print(f"📊 입력하신 등급: {grade_input} (반올림 기준: {grade}등급)")
        print(f"✨ 변경된 5등급제 기준, 당신의 추천 대학은... \n    👉 **[{chosen_uni}]** 입니다!")
        print("-" * 45)
        
    except ValueError:
        print("❌ 숫자만 입력해주세요! (예: 1.5 또는 3)")

# 프로그램 실행
if __name__ == "__main__":
    recommend_university_5grades()
