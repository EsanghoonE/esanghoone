import streamlit as st
import random 

# --- 1. 데이터 정의 (차종 대폭 확장) ---

# 대한민국 및 글로벌 주요 자동차 브랜드 및 대표 차종 (대폭 확장)
CAR_MODELS_EXTENDED = {
    '전기차': {
        '현대/제네시스': ['아이오닉 5', '아이오닉 6', '코나 EV', '넥쏘 (수소)', 'GV60', 'GV70 EV', 'G80 EV', '캐스퍼 EV'],
        '기아': ['EV6', 'EV9', '니로 EV', '레이 EV', '봉고 EV'],
        '테슬라': ['모델 3', '모델 Y', '모델 S', '모델 X', '사이버트럭'],
        'BMW': ['iX', 'i4', 'i5', 'i7', 'iX3'],
        '벤츠': ['EQA', 'EQB', 'EQC', 'EQE', 'EQS', 'EQV'],
        '폭스바겐/아우디': ['ID.4', 'ID.5', 'e-트론', 'e-트론 GT', 'Q4 e-트론'],
        '포르쉐': ['타이칸'],
        '기타 수입': ['쉐보레 볼트 EV', '폴스타 2', '리비안 R1S', '루시드 에어', 'BYD 씰']
    },
    '내연기관': {
        '현대/제네시스': ['아반떼', '쏘나타', '그랜저', '코나', '투싼', '싼타페', '팰리세이드', 'G70', 'G80', 'G90', 'GV80'],
        '기아': ['모닝', '레이', 'K3', 'K5', 'K8', '셀토스', '스포티지', '쏘렌토', '카니발', '스팅어'],
        'BMW': ['1시리즈', '3시리즈', '5시리즈', '7시리즈', 'M2/M3/M4/M5', 'X1~X7'],
        '벤츠': ['A클래스', 'C클래스', 'E클래스', 'S클래스', 'G바겐', 'AMG GT', 'GLA~GLS'],
        '아우디': ['A4', 'A6', 'A8', 'Q5', 'Q7', 'R8'],
        '포르쉐': ['911', '카이엔', '파나메라', '마칸'],
        '쉐보레/포드': ['트레일블레이저', '트래버스', '콜로라도', '머스탱', 'F-150', '브롱코'],
        '기타 수입': ['볼보 S60/XC90', '푸조 308', '지프 랭글러', '람보르기니 우루스', '페라리 로마']
    },
    '하이브리드': {
        '현대/제네시스': ['쏘나타 HEV', '그랜저 HEV', '투싼 HEV', '싼타페 HEV', '니로 HEV (PHEV 포함)'],
        '기아': ['K5 HEV', 'K8 HEV', '쏘렌토 HEV', '스포티지 HEV', '카니발 HEV'],
        '토요타/렉서스': ['프리우스', '캠리 HEV', '시에나 HEV', '라브4 HEV', 'ES 300h', 'RX 450h'],
        '기타 수입': ['혼다 어코드 HEV', '벤츠 C/E 클래스 PHEV', 'BMW 5시리즈 PHEV']
    }
}

# 1단계 최종: 선호 동인 분석 선택지 (유지)
DRIVING_FACTORS = {
    'A': '최고 수준의 가속력과 주행 성능',
    'B': '혁신적인 실내외 디자인',
    'C': '첨단 자율주행 및 인포테인먼트 옵션',
    'D': '탁월한 연비와 친환경성',
    'E': '안전성, 내구성, 잔고장이 적은 신뢰성',
    'F': '차량의 조립/정비 용이성'
}

# 2단계: 6가지 핵심 직무 설명 (유지)
JOB_ROLES = {
    '자동차 정비': "차량 기계, 전기/전자 시스템 고장 진단 및 수리. (EV 전문 정비 포함)",
    '자동차 차체수리': "사고 차량의 외형 복원, 판금 작업 및 차체 구조 안전성 확보.",
    '자동차 도장': "차량 외관 색상 복원, 표면 처리, 코팅 등 최종 외형 품질 담당.",
    '자동차 튜닝': "내/외장 드레스업 및 성능, 편의 기능 개선.",
    '서비스 어드바이저 (SA)': "고객 정비 상담, 고장 내용 파악, 작업 지시 및 결과 설명.",
    '자동차 딜러 (영업)': "고객에게 차량을 판매하고 계약, 출고, 사후 관리를 담당."
}

# 드림카 색상 옵션 (유지)
COLOR_OPTIONS = ['화이트', '블랙', '실버', '블루', '레드', '커스텀 색상']

# --- 2. Streamlit 앱 페이지 구성 함수 ---

def page_header():
    """앱 제목 및 상태 초기화"""
    st.title("🚗 너는 왜 자동차과에 왔니?")
    st.subheader("고등학교 1학년, 나의 꿈을 찾는 진로 탐색 앱")
    st.divider()

    # Session State 초기화 (페이지 전환 및 데이터 저장용)
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = 1
        st.session_state.car_data = {}
        st.session_state.selected_job = None
        st.session_state.final_color = None

def stage_1_dreamcar():
    """1단계: 드림카 비전보드 및 선호 동인 분석"""
    st.header("✨ 1단계: 나의 드림카 비전보드 만들기")

    # 1-1. 동력원 선택
    st.markdown("##### 1. 당신이 꿈꾸는 자동차의 핵심 동력원을 선택해주세요.")
    st.session_state.car_data['engine'] = st.radio(
        "동력원 선택", list(CAR_MODELS_EXTENDED.keys()), index=None, horizontal=True, label_visibility="collapsed"
    )

    if st.session_state.car_data['engine']:
        engine_type = st.session_state.car_data['engine']
        
        # 1-2. 브랜드 및 모델 선택
        st.markdown(f"##### 2. {engine_type} 분야에서 가장 관심 있는 브랜드와 모델을 선택해주세요.")
        
        brands = list(CAR_MODELS_EXTENDED.get(engine_type, {}).keys())
        brand_col, model_col = st.columns(2)
        
        with brand_col:
            st.session_state.car_data['brand'] = st.selectbox("브랜드 선택", brands, index=None, placeholder="브랜드 선택", key="brand_select")
        
        if st.session_state.car_data['brand']:
            brand = st.session_state.car_data['brand']
            models = CAR_MODELS_EXTENDED[engine_type][brand]
            
            with model_col:
                st.session_state.car_data['model'] = st.selectbox("모델 선택 (다양한 차종 포함)", models, index=None, placeholder="모델 선택", key="model_select")

            # 1-2-1. 색상 선택 (추가)
            if st.session_state.car_data['model']:
                st.markdown("##### 3. 나의 드림카 색상을 선택해주세요.")
                st.session_state.final_color = st.selectbox(
                    "색상 선택", COLOR_OPTIONS, index=0, key="color_select"
                )
                
                model = st.session_state.car_data['model']
                
                # 1-3. 드림카 비전보드 최종 화면 (이미지 문제 해결을 위해 텍스트 대체)
                st.markdown("---")
                st.markdown("### 🏆 나의 드림카 비전보드 완성!")
                
                # 이미지 플레이스홀더 영역 (실제 운영 시 이미지 URL로 대체 필수)
                st.markdown(f"""
                <div style="background-color: #f0f2f6; height: 300px; border-radius: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: 5px solid {st.session_state.final_color.lower() if st.session_state.final_color else '#ccc'};">
                    <h3 style="color:#333;">선택된 드림카 이미지 영역</h3>
                    <p style="color:#555;">[모델: {brand} {model} / 색상: {st.session_state.final_color}]</p>
                    <p style="color:red; font-weight:bold;">🚨 실제 앱에서는 고품질 이미지를 URL로 연결해야 합니다.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 1-4. 나의 드림카 코멘트
                st.session_state.car_data['comment'] = st.text_area(
                    "나의 드림카 코멘트 (이 차에 대한 나의 꿈이나 생각)", 
                    placeholder="예: '이 차를 언젠가 직접 튜닝해보고 싶어요!'",
                    key="comment_area"
                )
                
                # 1-5. 선호 동인 분석 (2단계 직무 매칭의 기초 자료)
                st.markdown("---")
                st.markdown("### 🔍 4. 이 차를 선택한 가장 결정적인 이유는 무엇인가요? (최대 3가지)")
                
                selected_factors = []
                cols = st.columns(2)
                for i, (key, desc) in enumerate(DRIVING_FACTORS.items()):
                    if cols[i % 2].checkbox(f'{key}. {desc}', key=f'factor_{key}'):
                        selected_factors.append(key)
                
                st.session_state.car_data['factors'] = selected_factors
                
                if st.button("2단계: 미래 직무 연결하기"):
                    if len(selected_factors) > 0:
                        st.session_state.current_stage = 2
                        st.rerun()
                    else:
                        st.error("결정적인 이유(선호 동인)를 최소 1가지 선택해주세요.")

def stage_2_job_matching():
    """2단계: 산업 수요 브리핑 및 6가지 직무 선택"""
    st.header("🔗 2단계: 현장 실무 중심 직무 연결")
    
    # 2-1. 산업 수요 브리핑
    st.markdown("### 💡 미래 자동차 산업, 왜 유망할까요? **(당신의 직업이 안정적인 이유)**")
    st.info("""
    **1. 지금 당장 밖에서 보이는 모든 차들이 일거리!**
    자동차는 소모품이 많고, **하루에도 수많은 사고가 시시각각 발생**합니다. 정비, 차체수리, 도장 등은 기계로 대체 불가능한 **사람의 숙련된 손기술**이 필요하며, 꾸준하고 안정적인 수요가 보장됩니다.

    **2. 자동차 정비/수리의 불변의 가치:**
    모든 사고와 고장 부위가 다르므로, **기계가 대체할 수 없는 당신의 섬세한 진단과 손길**이 필요합니다. 미래에도 인간의 기술력은 핵심 경쟁력입니다.

    **3. 시대 변화에 적응하는 기술의 연속성:**
    내연기관 경험은 미래 EV/수소차 정비의 탄탄한 기초가 됩니다. 앞으로도 당신의 기술은 계속 **진화 가능한 유망한 직업**으로 이어질 것입니다.
    """)
    
    st.markdown("---")
    
    # 2-2. 6가지 핵심 직무 카드 제시
    st.markdown("### 🎯 6가지 핵심 직무 카드")
    st.markdown("##### 당신의 드림카와 선호 동인을 바탕으로 가장 적합한 직무를 선택하세요.")
    
    # 직무 카드 배치
    cols = st.columns(3)
    job_choices = list(JOB_ROLES.keys())
    
    for i, job_name in enumerate(job_choices):
        with cols[i % 3]:
            # 카드 디자인 (마크다운 활용)
            st.markdown(f"""
            <div style="border: 2px solid #0078D4; border-radius: 10px; padding: 10px; margin-bottom: 10px; height: 160px;">
                <h4 style="color:#0078D4; margin-top:0;">{job_name}</h4>
                <p style="font-size:14px;">{JOB_ROLES[job_name]}</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")

    # 2-3. 최종 직무 선택
    st.markdown("### ✅ 1. 이 6가지 직무 중, 당신의 꿈에 가장 가까운 직무를 최종 선택해주세요.")
    st.session_state.selected_job = st.selectbox(
        "최종 선택 직무", job_choices, index=None, placeholder="직무 선택", key="final_job_select"
    )
    
    if st.session_state.selected_job:
        st.success(f"최종 목표 직무: **{st.session_state.selected_job}**")
        if st.button("3단계: 3년 학습 로드맵 설계하기"):
            st.session_state.current_stage = 3
            st.rerun()
    
    if st.button("이전 단계 (1단계)로 돌아가기", key="back_to_stage1"):
        st.session_state.current_stage = 1
        st.rerun()

def stage_3_roadmap():
    """3단계: 3년 학습 로드맵 설계 (다음 단계에서 구체화 예정)"""
    st.header("🗓️ 3단계: 나만의 3년 학습 로드맵 만들기")
    
    if st.session_state.selected_job:
        st.info(f"선택하신 직무는 **{st.session_state.selected_job}** 입니다.")
        st.markdown("---")
        st.markdown("##### 이제 이 직무를 달성하기 위한 고등학교 3년간의 구체적인 계획(교과, 방과후, 자격증 등)을 설계해 봅시다.")
        
        # 여기에 3단계 로드맵 구체화 내용이 들어갑니다.
        st.warning("🚨 3단계 로드맵 내용은 다음 논의에서 구체적으로 채워집니다.")
        
    else:
        st.warning("직무 선택이 필요합니다. 2단계로 돌아가서 직무를 선택해주세요.")
        if st.button("2단계로 돌아가기"):
            st.session_state.current_stage = 2
            st.rerun()
        

# --- 3. 메인 앱 실행 로직 ---

page_header()

if st.session_state.current_stage == 1:
    stage_1_dreamcar()
elif st.session_state.current_stage == 2:
    stage_2_job_matching()
elif st.session_state.current_stage == 3:
    stage_3_roadmap()