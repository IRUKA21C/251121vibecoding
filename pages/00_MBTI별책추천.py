import streamlit as st

# 1. 페이지 기본 설정 (탭 이름, 아이콘, 레이아웃)
st.set_page_config(
    page_title="MBTI 고전 서재",
    page_icon="🕰️",
    layout="centered"
)

# 2. CSS 스타일링 (디자인 요소를 위해 HTML/CSS 주입)
# 외부 라이브러리 없이 기본 마크다운 기능을 활용한 커스텀 스타일
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(to right, #ece9e6, #ffffff);
        border-radius: 15px;
        margin-bottom: 30px;
    }
    .mbti-tag {
        background-color: #FF4B4B;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8em;
    }
    .book-card {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .quote-box {
        font-style: italic;
        color: #555;
        border-left: 5px solid #FF4B4B;
        padding-left: 15px;
        margin-top: 20px;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터베이스 (딕셔너리 활용)
# MBTI별 추천 도서, 저자, 설명, 명대사, 이모지 매핑
recommendations = {
    # 분석가형 (NT)
    "INTJ": {"book": "손자병법", "author": "손무", "desc": "전략적이고 용의주도한 당신에게, 천 년을 관통하는 지략의 정수를.", "icon": "♟️", "quote": "지피지기면 백전불태라."},
    "INTP": {"book": "소크라테스의 변명", "author": "플라톤", "desc": "끊임없이 탐구하는 사색가인 당신에게, 논리와 철학의 시작점을.", "icon": "🦉", "quote": "성찰하지 않는 삶은 살 가치가 없다."},
    "ENTJ": {"book": "군주론", "author": "니콜로 마키아벨리", "desc": "대담한 통솔자인 당신에게, 현실적이고 냉철한 리더십의 교본을.", "icon": "👑", "quote": "사랑받는 것보다 두려움의 대상이 되는 것이 안전하다."},
    "ENTP": {"book": "돈키호테", "author": "미겔 데 세르반테스", "desc": "뜨거운 논쟁과 모험을 즐기는 당신에게, 불가능에 도전하는 기사도를.", "icon": "⚔️", "quote": "이룩할 수 없는 꿈을 꾸고, 이루어질 수 없는 사랑을 하고..."},

    # 외교관형 (NF)
    "INFJ": {"book": "데미안", "author": "헤르만 헤세", "desc": "통찰력 있고 이상적인 당신에게, 자아를 찾아가는 깊은 내면의 여정을.", "icon": "🕊️", "quote": "새는 알을 깨고 나온다. 알은 세계다."},
    "INFP": {"book": "어린 왕자", "author": "앙투안 드 생텍쥐페리", "desc": "낭만적이고 섬세한 당신에게, 잃어버린 순수와 진정한 관계의 의미를.", "icon": "🌹", "quote": "가장 중요한 건 눈에 보이지 않아."},
    "ENFJ": {"book": "레 미제라블", "author": "빅토르 위고", "desc": "정의롭고 이타적인 당신에게, 인간애와 구원의 웅장한 서사를.", "icon": "🔥", "quote": "사랑하는 것은 신의 얼굴을 보는 것이다."},
    "ENFP": {"book": "빨강 머리 앤", "author": "루시 모드 몽고메리", "desc": "열정적이고 자유로운 당신에게, 일상을 마법처럼 바꾸는 상상력을.", "icon": "👒", "quote": "정말로 행복한 나날이란 멋지고 놀라운 일이 일어나는 날이 아니라..."},

    # 관리자형 (SJ)
    "ISTJ": {"book": "논어", "author": "공자", "desc": "사실적이고 책임감 강한 당신에게, 삶의 질서와 바른 길을 제시하는 지혜를.", "icon": "📜", "quote": "배우고 때때로 익히면 또한 기쁘지 아니한가."},
    "ISFJ": {"book": "제인 에어", "author": "샬롯 브론테", "desc": "헌신적이고 따뜻한 당신에게, 시련 속에서도 지키는 고결한 사랑을.", "icon": "🕯️", "quote": "나는 새가 아니에요. 어떤 그물도 나를 가둘 수 없어요."},
    "ESTJ": {"book": "동물농장", "author": "조지 오웰", "desc": "엄격하고 규칙을 중시하는 당신에게, 사회 시스템에 대한 날카로운 풍자를.", "icon": "🏗️", "quote": "모든 동물은 평등하다. 하지만 어떤 동물은 더 평등하다."},
    "ESFJ": {"book": "오만과 편견", "author": "제인 오스틴", "desc": "사교적이고 조화를 중시하는 당신에게, 관계 속에서 피어나는 이해와 사랑을.", "icon": "☕", "quote": "편견은 내가 다른 사람을 사랑하지 못하게 하고, 오만은 다른 사람이 나를 사랑할 수 없게 만든다."},

    # 탐험가형 (SP)
    "ISTP": {"book": "노인과 바다", "author": "어니스트 헤밍웨이", "desc": "만능 재주꾼이자 현실적인 당신에게, 묵묵히 운명과 맞서는 불굴의 의지를.", "icon": "🎣", "quote": "인간은 파괴될지언정 패배하지 않는다."},
    "ISFP": {"book": "월든", "author": "헨리 데이비드 소로", "desc": "예술적이고 온화한 당신에게, 자연 속에서 발견하는 소박한 삶의 미학을.", "icon": "🌿", "quote": "나는 의도적으로 살기 위해 숲으로 갔다."},
    "ESTP": {"book": "위대한 개츠비", "author": "F. 스콧 피츠제럴드", "desc": "대담하고 활동적인 당신에게, 화려한 불빛 뒤에 숨겨진 꿈과 욕망을.", "icon": "🥂", "quote": "우리는 조류를 거스르는 배처럼 끊임없이 과거로 떠밀려 가면서도 앞으로 나아가는 것이다."},
    "ESFP": {"book": "허클베리 핀의 모험", "author": "마크 트웨인", "desc": "자유로운 영혼의 연예인인 당신에게, 규율을 벗어난 짜릿한 자유와 모험을.", "icon": "🚣", "quote": "그래, 그렇다면 나는 지옥으로 가겠어."}
}

# 4. UI 구성

# [헤더 영역]
st.markdown("<div class='main-header'><h1>🕰️ 고전 문학 소믈리에</h1><p>당신의 MBTI 성향에 딱 맞는 고전 명작을 처방해 드립니다.</p></div>", unsafe_allow_html=True)

# [입력 영역]
st.write("### 당신의 MBTI를 선택해주세요 👇")
mbti_list = sorted(list(recommendations.keys()))
selected_mbti = st.selectbox("MBTI 유형 선택", mbti_list, index=None, placeholder="여기를 눌러 선택하세요...")

st.markdown("---")

# [결과 영역]
if selected_mbti:
    # 로딩 효과 (감성 더하기)
    with st.spinner(f"{selected_mbti} 유형의 영혼을 분석하여 책을 찾고 있습니다..."):
        import time
        time.sleep(1) # 1초 딜레이로 분석하는 느낌 주기
    
    data = recommendations[selected_mbti]
    
    # 결과를 카드 형태로 출력
    st.markdown(f"""
        <div class='book-card'>
            <div style='font-size: 80px; margin-bottom: 10px;'>{data['icon']}</div>
            <span class='mbti-tag'>{selected_mbti} 맞춤 추천</span>
            <h2 style='color: #333; margin-top: 10px;'>{data['book']}</h2>
            <h4 style='color: #666; font-weight: normal;'>저자: {data['author']}</h4>
            <p style='margin-top: 20px; font-size: 1.1em;'>{data['desc']}</p>
            <div class='quote-box'>
                "{data['quote']}"
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 추가 상호작용 버튼
    st.write("")
    st.write("")
    if st.button("✨ 다른 유형도 추천받기"):
        st.rerun()

else:
    # 선택 전 대기 화면
    st.info("👆 위 박스에서 MBTI를 선택하면, 인생 책을 추천해 드려요!")
    
    # 하단 장식
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🧐\n**나를 위한**\n깊이 있는 통찰")
    with col2:
        st.markdown("### 💖\n**마음을 울리는**\n따뜻한 위로")
    with col3:
        st.markdown("### 🚀\n**새로운 영감**\n대담한 모험")
