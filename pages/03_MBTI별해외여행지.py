import streamlit as st
import folium
from streamlit.components.v1 import html

# --- 1. 페이지 설정 (가장 먼저 실행되어야 함) ---
st.set_page_config(
    page_title="MBTI 여행지 추천",
    page_icon="✈️",
    layout="centered"
)

# --- 2. 스타일 및 디자인 (CSS) ---
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #FF4B4B;
        font-weight: 700;
    }
    .sub-header {
        text-align: center;
        color: #333;
        margin-bottom: 20px;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .highlight {
        color: #FF4B4B;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 데이터 정의 (MBTI별 여행지 정보) ---
mbti_data = {
    "ISTJ": {"city": "독일, 베를린", "desc": "계획적이고 질서를 좋아하는 당신! 역사와 규칙, 효율성의 도시에서 편안함을 느껴보세요. 🏛️", "lat": 52.5200, "lon": 13.4050, "icon": "📝"},
    "ISFJ": {"city": "스위스, 인터라켄", "desc": "평화롭고 온화한 당신에게는 알프스의 대자연이 주는 힐링이 최고입니다. 🏔️", "lat": 46.6863, "lon": 7.8632, "icon": "☕"},
    "INFJ": {"city": "아이슬란드, 레이캬비크", "desc": "신비롭고 조용한 사색을 즐기는 당신, 오로라 아래에서 영감을 얻어보세요. 🌌", "lat": 64.1466, "lon": -21.9426, "icon": "🔮"},
    "INTJ": {"city": "영국, 런던", "desc": "지적 호기심이 넘치는 전략가! 박물관과 역사가 살아 숨 쉬는 런던이 딱입니다. 🇬🇧", "lat": 51.5074, "lon": -0.1278, "icon": "♟️"},
    "ISTP": {"city": "뉴질랜드, 퀸스타운", "desc": "모험과 스릴을 즐기는 만능 재주꾼! 번지점프와 액티비티의 천국으로 떠나세요. 🪂", "lat": -45.0312, "lon": 168.6626, "icon": "🛠️"},
    "ISFP": {"city": "프랑스, 파리", "desc": "예술적 감수성이 풍부한 당신, 낭만과 예술의 도시에서 감성을 채워보세요. 🎨", "lat": 48.8566, "lon": 2.3522, "icon": "🎨"},
    "INFP": {"city": "일본, 교토", "desc": "자신만의 세계와 몽상을 사랑하는 당신, 고즈넉한 사찰과 벚꽃 길을 걸어보세요. 🌸", "lat": 35.0116, "lon": 135.7681, "icon": "📖"},
    "INTP": {"city": "미국, 샌프란시스코", "desc": "논리적이고 창의적인 사색가! 혁신의 중심지 실리콘밸리에서 미래를 엿보세요. 💻", "lat": 37.7749, "lon": -122.4194, "icon": "🧪"},
    "ESTP": {"city": "스페인, 이비자", "desc": "에너지가 넘치는 당신! 뜨거운 태양과 멈추지 않는 파티가 있는 곳이 제격입니다. 🔥", "lat": 38.9067, "lon": 1.4206, "icon": "🕶️"},
    "ESFP": {"city": "브라질, 리우데자네이루", "desc": "자유로운 영혼의 연예인! 열정적인 삼바 축제와 해변이 당신을 기다립니다. 💃", "lat": -22.9068, "lon": -43.1729, "icon": "🎉"},
    "ENFP": {"city": "태국, 방콕", "desc": "열정적이고 새로운 관계를 좋아하는 당신! 활기찬 거리와 맛있는 음식이 가득합니다. 🍜", "lat": 13.7563, "lon": 100.5018, "icon": "✨"},
    "ENTP": {"city": "싱가포르", "desc": "논쟁과 새로운 도전을 즐기는 발명가! 현대적이고 빠르게 변하는 도시가 어울립니다. 🏙️", "lat": 1.3521, "lon": 103.8198, "icon": "💡"},
    "ESTJ": {"city": "미국, 뉴욕", "desc": "현실적이고 리더십 있는 당신! 세계 경제와 문화의 중심지에서 에너지를 느껴보세요. 🗽", "lat": 40.7128, "lon": -74.0060, "icon": "👔"},
    "ESFJ": {"city": "이탈리아, 로마", "desc": "사람을 좋아하고 사교적인 당신! 맛있는 음식과 따뜻한 사람들이 있는 로마로 가세요. 🍕", "lat": 41.9028, "lon": 12.4964, "icon": "🤝"},
    "ENFJ": {"city": "캐나다, 밴쿠버", "desc": "카리스마 있고 이타적인 당신! 자연과 도시가 조화를 이루는 곳이 평화를 줍니다. 🍁", "lat": 49.2827, "lon": -123.1207, "icon": "🌻"},
    "ENTJ": {"city": "아랍에미리트, 두바이", "desc": "대담한 통솔자! 사막 위에 세워진 기적의 도시에서 야망을 펼쳐보세요. 💎", "lat": 25.276987, "lon": 55.296249, "icon": "🏰"}
}

# --- 4. UI 구성 ---

# 헤더
st.markdown("<h1 class='main-header'>✈️ MBTI 맞춤 해외여행 추천</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>당신의 성격 유형을 선택하고, 운명의 여행지를 확인하세요!</p>", unsafe_allow_html=True)

st.write("---")

# 입력 섹션 (MBTI 선택)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    mbti_list = list(mbti_data.keys())
    selected_mbti = st.selectbox("당신의 MBTI는 무엇인가요?", mbti_list)

# 결과 섹션
if selected_mbti:
    info = mbti_data[selected_mbti]
    
    st.write("") # 여백
    
    # 결과 카드
    st.markdown(f"""
        <div class='card'>
            <h2 style='margin:0;'>{info['icon']} {selected_mbti} 유형에게 추천하는 곳</h2>
            <h3 class='highlight'>{info['city']}</h3>
            <p style='font-size: 1.1em;'>{info['desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Folium 지도 생성 (한글 구글 지도 적용)
    st.write("### 🗺️ 위치 미리보기")
    
    # tiles URL에 hl=ko 옵션을 넣어 한국어 라벨을 요청합니다.
    m = folium.Map(
        location=[info['lat'], info['lon']], 
        zoom_start=12,
        tiles='http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}',
        attr='Google'
    )
    
    # 마커 추가
    folium.Marker(
        [info['lat'], info['lon']],
        popup=info['city'],
        tooltip=f"{info['city']} - 여기야! 📍",
        icon=folium.Icon(color='red', icon='plane', prefix='fa')
    ).add_to(m)

    # Streamlit에서 지도 표시
    map_html = m._repr_html_()
    html(map_html, height=400)

st.write("---")
st.markdown("<p style='text-align: center; color: #888;'>Created with ❤️ by Streamlit</p>", unsafe_allow_html=True)
