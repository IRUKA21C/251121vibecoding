import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정 (탭 이름 등)
st.set_page_config(page_title="국가별 MBTI 통계", layout="wide")

# 제목
st.title("🌍 국가별 MBTI 비율 분석기")
st.markdown("각 나라별로 어떤 MBTI 유형이 많고 적은지 인터랙티브한 차트로 확인해보세요.")

# 데이터 로드 함수 (캐싱을 사용하여 성능 최적화)
@st.cache_data
def load_data():
    # 같은 폴더에 있는 csv 파일을 읽어옵니다.
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

try:
    df = load_data()
    
    # 사이드바 혹은 상단에 MBTI 선택 박스 배치
    # 첫 번째 컬럼(Country)을 제외한 나머지 컬럼(MBTI 유형들)을 리스트로 가져옴
    mbti_list = df.columns[1:].tolist()
    selected_mbti = st.selectbox("확인하고 싶은 MBTI 유형을 선택하세요:", mbti_list)

    # --- 데이터 처리 ---
    # 선택된 MBTI 비율을 기준으로 내림차순 정렬 (가장 높은 순)
    df_sorted_desc = df.sort_values(by=selected_mbti, ascending=False)
    top_10 = df_sorted_desc.head(10)

    # 선택된 MBTI 비율을 기준으로 오름차순 정렬 (가장 낮은 순)
    df_sorted_asc = df.sort_values(by=selected_mbti, ascending=True)
    bottom_10 = df_sorted_asc.head(10)

    # --- 시각화 (Plotly) ---
    
    # 1. 비율이 가장 높은 나라 Top 10
    st.subheader(f"📈 {selected_mbti} 비율이 가장 **높은** 나라 Top 10")
    fig_top = px.bar(
        top_10, 
        x='Country', 
        y=selected_mbti,
        color=selected_mbti,  # 비율에 따라 색상 농도 조절
        color_continuous_scale='Blues',
        text_auto='.3f',      # 막대 위에 수치 표시
        title=f"{selected_mbti} 비율 상위 10개국"
    )
    # 인터랙티브 요소 강화 (툴팁 등) 및 레이아웃 설정
    fig_top.update_layout(xaxis_title="국가", yaxis_title="비율")
    st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("---") # 구분선

    # 2. 비율이 가장 적은 나라 Top 10
    st.subheader(f"📉 {selected_mbti} 비율이 가장 **낮은** 나라 Top 10")
    fig_bottom = px.bar(
        bottom_10, 
        x='Country', 
        y=selected_mbti,
        color=selected_mbti,
        color_continuous_scale='Reds',
        text_auto='.3f',
        title=f"{selected_mbti} 비율 하위 10개국"
    )
    fig_bottom.update_layout(xaxis_title="국가", yaxis_title="비율")
    st.plotly_chart(fig_bottom, use_container_width=True)

except FileNotFoundError:
    st.error("데이터 파일(countriesMBTI_16types.csv)을 찾을 수 없습니다. 같은 폴더에 파일이 있는지 확인해주세요.")
