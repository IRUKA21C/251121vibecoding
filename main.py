import streamlit as st

# 1. 페이지 기본 설정 (탭 이름, 아이콘, 레이아웃)
st.set_page_config(
    page_title="MBTI 진로 나침반",
    page_icon="🧭",
    layout="centered"
)

# 2. CSS를 활용한 간단한 스타일링 (폰트 및 여백 조정)
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MBTI 데이터 (별도 파일 없이 딕셔너리로 내장)
mbti_data = {
    "ISTJ": {"name": "현실주의자", "emoji": "🧐", "traits": "책임감, 현실적, 논리적, 질서정연", 
             "jobs": ["회계사/세무사 📊", "공무원/행정가 🏛️", "웹 개발자 💻"]},
    "ISFJ": {"name": "수호자", "emoji": "🛡️", "traits": "헌신, 인내심, 성실, 협조적", 
             "jobs": ["간호사/의료계열 🏥", "초등교사 🏫", "인사 담당자(HR) 🤝"]},
    "INFJ": {"name": "옹호자", "emoji": "🧙‍♂️", "traits": "통찰력, 직관, 영감, 이상주의", 
             "jobs": ["심리 상담가 🛋️", "작가/시나리오 작가 ✍️", "사회복지사 ❤️"]},
    "INTJ": {"name": "전략가", "emoji": "♟️", "traits": "독창성, 비판적 분석, 독립적, 결단력", 
             "jobs": ["데이터 과학자 🧬", "투자 분석가 📈", "건축가 🏛️"]},
    "ISTP": {"name": "장인", "emoji": "🔧", "traits": "관찰력, 융통성, 효율성, 도구 사용", 
             "jobs": ["소프트웨어 엔지니어 🖥️", "파일럿/항공 정비 ✈️", "응급 구조사 🚑"]},
    "ISFP": {"name": "모험가", "emoji": "🎨", "traits": "온화, 겸손, 예술적 감각, 현재 충실", 
             "jobs": ["그래픽 디자이너 🎨", "패션 MD 👗", "수의사/사육사 🐾"]},
    "INFP": {"name": "중재자", "emoji": "🧚", "traits": "성실, 이해심, 개방적, 낭만적", 
             "jobs": ["일러스트레이터 🖌️", "크리에이터/유튜버 📹", "예술 치료사 🎨"]},
    "INTP": {"name": "논리술사", "emoji": "🧪", "traits": "지적 호기심, 잠재력, 분석, 아이디어", 
             "jobs": ["프로그래머 ⌨️", "경제학자 📉", "물리학자/연구원 🔬"]},
    "ESTP": {"name": "사업가", "emoji": "🕶️", "traits": "활동적, 문제해결, 적응력, 유머", 
             "jobs": ["창업가/CEO 💼", "스포츠 에이전트 ⚽", "마케터 📣"]},
    "ESFP": {"name": "연예인", "emoji": "🎉", "traits": "사교적, 에너지, 긍정, 즉흥적", 
             "jobs": ["이벤트 기획자 🎈", "승무원 ✈️", "엔터테이너 🎤"]},
    "ENFP": {"name": "활동가", "emoji": "✨", "traits": "열정, 상상력, 순발력, 인간관계", 
             "jobs": ["PD/방송 연출 🎬", "광고 기획자 💡", "홍보 전문가(PR) 📢"]},
    "ENTP": {"name": "변론가", "emoji": "🗣️", "traits": "박식, 독창성, 다방면 관심, 도전", 
             "jobs": ["벤처 투자자 💰", "정치인/변호사 ⚖️", "발명가 🔭"]},
    "ESTJ": {"name": "경영자", "emoji": "👔", "traits": "체계적, 규칙 준수, 사실적, 리더십", 
             "jobs": ["프로젝트 매니저(PM) 📅", "경영 컨설턴트 📑", "약사 💊"]},
    "ESFJ": {"name": "집정관", "emoji": "🍰", "traits": "친절, 동정심, 협동, 사교성", 
             "jobs": ["승무원/서비스직 ✈️", "영양사 🥦", "유치원 교사 🐥"]},
    "ENFJ": {"name": "선도자", "emoji": "🌟", "traits": "카리스마, 설득력, 언변, 이타주의", 
             "jobs": ["아나운서/리포터 🎤", "기업 교육 강사 👩‍🏫", "세일즈 매니저 🤝"]},
    "ENTJ": {"name": "통솔자", "emoji": "🦁", "traits": "철저한 준비, 활동적, 통솔력, 논리", 
             "jobs": ["기업 임원/CEO 🏢", "변호사/검사 ⚖️", "경영 컨설턴트 📊"]},
}

# 4. 헤더 섹션
st.title("🧭 학생 진로 나침반")
st.write("당신의 **MBTI**를 선택하면, 미래의 **멋진 진로**를 추천해 드려요!")
st.divider()

# 5. 입력 섹션 (MBTI 선택)
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/7486/7486242.png", width=100) # 무료 아이콘 예시
    
with col2:
    mbti_list = sorted(mbti_data.keys())
    selected_mbti = st.selectbox(
        "자신의 MBTI 유형을 선택하세요 👇",
        mbti_list,
        index=None,
        placeholder="여기를 눌러 선택하세요!"
    )

# 6. 결과 출력 섹션
if selected_mbti:
    data = mbti_data[selected_mbti]
    
    st.divider()
    
    # 유형 소개 (애니메이션 효과 느낌의 컨테이너)
    with st.container():
        st.subheader(f"{data['emoji']} 당신은 **[{selected_mbti}] {data['name']}** 유형이군요!")
        st.info(f"✨ **핵심 성격:** {data['traits']}")
        
    st.markdown("### 🚀 추천 진로 Top 3")
    st.write("당신의 성향에 딱 맞는 직업들을 찾아봤어요.")
    
    # 카드 형태로 진로 3가지 보여주기
    c1, c2, c3 = st.columns(3)
    
    jobs = data['jobs']
    
    # 각 컬럼에 카드 디자인 적용
    with c1:
        st.markdown(f"""
        <div class="card">
            <h3>🥇 1순위</h3>
            <p>{jobs[0]}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="card">
            <h3>🥈 2순위</h3>
            <p>{jobs[1]}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="card">
            <h3>🥉 3순위</h3>
            <p>{jobs[2]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("💡 *이 결과는 참고용입니다. 당신의 가능성은 무한하다는 걸 잊지 마세요!*")

else:
    # 선택하지 않았을 때 보이는 대기 화면
    st.info("👆 위 상자에서 MBTI를 선택하면 결과가 나타납니다!")
