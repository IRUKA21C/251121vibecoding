import streamlit as st
import pandas as pd
import altair as alt

# 페이지 기본 설정
st.set_page_config(
    page_title="국가별 MBTI 비율 분석",
    layout="wide"
)

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    # 같은 폴더에 있는 csv 파일을 읽어옵니다.
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

def main():
    st.title("🌏 국가별 MBTI 분포 비율 분석")
    st.markdown("데이터 출처: `countriesMBTI_16types.csv`")

    # 데이터 불러오기
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일이 같은 폴더에 있는지 확인해주세요.")
        return

    # MBTI 유형 선택 (첫 번째 컬럼인 Country를 제외한 나머지 컬럼)
    mbti_list = df.columns[1:].tolist()
    selected_mbti = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_list)

    # 데이터 처리
    # 선택된 MBTI를 기준으로 내림차순 정렬 (상위 10개)
    top_10 = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)
    
    # 선택된 MBTI를 기준으로 오름차순 정렬 (하위 10개)
    bottom_10 = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=True).head(10)

    # 레이아웃 구성
    col1, col2 = st.columns(2)

    # --- 상위 10개 국가 그래프 ---
    with col1:
        st.subheader(f"📈 {selected_mbti} 비율이 가장 높은 국가 Top 10")
        
        # Altair 차트 생성
        chart_top = alt.Chart(top_10).mark_bar().encode(
            x=alt.X('Country', sort='-y', title='국가'), # y축 값 기준 내림차순 정렬
            y=alt.Y(selected_mbti, title='비율'),
            color=alt.value('#FF6B6B'), # 막대 색상 (빨간 계열)
            tooltip=['Country', alt.Tooltip(selected_mbti, format='.4f')] # 마우스 오버 시 정보 표시
        ).properties(
            height=400
        ).interactive() # 줌, 팬 기능 활성화

        st.altair_chart(chart_top, use_container_width=True)

    # --- 하위 10개 국가 그래프 ---
    with col2:
        st.subheader(f"📉 {selected_mbti} 비율이 가장 낮은 국가 Top 10")
        
        # Altair 차트 생성
        chart_bottom = alt.Chart(bottom_10).mark_bar().encode(
            x=alt.X('Country', sort='y', title='국가'), # y축 값 기준 오름차순 정렬
            y=alt.Y(selected_mbti, title='비율'),
            color=alt.value('#4D96FF'), # 막대 색상 (파란 계열)
            tooltip=['Country', alt.Tooltip(selected_mbti, format='.4f')]
        ).properties(
            height=400
        ).interactive()

        st.altair_chart(chart_bottom, use_container_width=True)

    # 전체 데이터 보기 (옵션)
    with st.expander("전체 데이터 보기"):
        st.dataframe(df)

if __name__ == '__main__':
    main()
