import streamlit as st
import random

# 음식 리스트
foods = [
    "김치찌개",
    "된장찌개",
    "비빔밥",
    "치킨",
    "피자",
    "햄버거",
    "초밥",
    "떡볶이",
    "라면",
    "삼겹살"
]

# 제목
st.title("🍚 음식 추천 앱")

st.write("버튼을 누르면 오늘 먹을 음식을 추천해드립니다.")

# 버튼
if st.button("추천 받기"):
    food = random.choice(foods)
    st.success(f"오늘의 추천 음식은 👉 {food}")
