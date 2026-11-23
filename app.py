"""
🎮 내 PC 게임 프레임(FPS) 예측기
- 그래픽카드(GPU)와 그래픽 품질 옵션에 따른 게임별 예상 FPS 및 플레이 적합도 분석 웹앱
"""
import streamlit as st
import pandas as pd

# =============================================
# 1. 시작: 페이지 설정 및 밝은 하이엔드 애니메이션 UI 스타일
# =============================================
st.set_page_config(
    page_title="FPS STUDIO ✨ 내 PC 게임 프레임 예측기",
    page_icon="🎮",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* 깔끔하고 세련된 최신 한글·영문 폰트 임포트 (SUIT + Plus Jakarta Sans) */
    @import url('https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2/fonts/static/woff2/SUIT.css');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

    /* 1. 밝고 화사한 오로라 파스텔 배경 애니메이션 */
    @keyframes auroraMesh {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #F8FAFC, #EEF2FF, #F0F9FF, #FDF2F8, #F5F3FF);
        background-size: 300% 300%;
        animation: auroraMesh 12s ease infinite;
        color: #0F172A;
        font-family: 'SUIT', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.2rem;
        max-width: 820px;
    }

    /* 2. 다채로운 키프레임 애니메이션 모음 */
    @keyframes springPop {
        0% {
            opacity: 0;
            transform: translateY(26px) scale(0.95);
        }
        65% {
            opacity: 1;
            transform: translateY(-4px) scale(1.01);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes floatBob {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(1.5deg); }
    }

    @keyframes twinkleStar {
        0%, 100% { transform: scale(0.8) rotate(0deg); opacity: 0.45; }
        50% { transform: scale(1.25) rotate(18deg); opacity: 1; }
    }

    @keyframes orbitSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes shimmerGlide {
        0% { transform: translateX(-140%) skewX(-20deg); }
        60%, 100% { transform: translateX(260%) skewX(-20deg); }
    }

    @keyframes pulseRing {
        0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.45); }
        70% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
        100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
    }

    @keyframes slideReveal {
        0% {
            opacity: 0;
            transform: translateX(-18px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* 3. 상단 히어로 + 아일릿 원희 치어링 카드 레이아웃 */
    .hero-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.4rem;
        padding: 1.8rem 2rem;
        margin-bottom: 1.6rem;
        border-radius: 26px;
        background: rgba(255, 255, 255, 0.82);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        border: 1.5px solid rgba(255, 255, 255, 0.95);
        box-shadow:
            0 20px 45px rgba(99, 102, 241, 0.10),
            0 4px 12px rgba(15, 23, 42, 0.04);
        overflow: hidden;
        animation: springPop 0.75s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }

    /* 유리 카드 위를 스치는 빛 반사 애니메이션 */
    .hero-wrapper::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 40%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.75), transparent);
        animation: shimmerGlide 5.5s ease-in-out infinite;
        pointer-events: none;
    }

    /* 배경 장식 플로팅 버블 & 반짝이 */
    .deco-orb-1 {
        position: absolute;
        top: -30px;
        left: 35%;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(129, 140, 248, 0.22) 0%, transparent 70%);
        animation: floatBob 5s ease-in-out infinite;
        pointer-events: none;
    }
    .deco-orb-2 {
        position: absolute;
        bottom: -35px;
        right: 28%;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(244, 114, 182, 0.20) 0%, transparent 70%);
        animation: floatBob 6.5s ease-in-out infinite reverse;
        pointer-events: none;
    }

    .hero-left {
        flex: 1.35;
        z-index: 2;
    }

    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0.34rem 0.9rem;
        border-radius: 999px;
        font-family: 'Plus Jakarta Sans', 'SUIT', sans-serif;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        color: #4F46E5;
        background: linear-gradient(90deg, #EEF2FF 0%, #FCE7F3 100%);
        border: 1px solid rgba(99, 102, 241, 0.28);
        margin-bottom: 0.85rem;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #6366F1;
        animation: pulseRing 2s infinite;
    }

    .hero-left h1 {
        margin: 0;
        font-size: 1.95rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        line-height: 1.24;
        color: #0F172A;
    }

    .hero-left h1 .grad-text {
        background: linear-gradient(120deg, #4F46E5 0%, #EC4899 55%, #0EA5E9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-left p {
        margin: 0.6rem 0 0.9rem;
        font-size: 0.94rem;
        line-height: 1.5;
        color: #475569;
        font-weight: 500;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .mini-chip {
        font-size: 0.76rem;
        font-weight: 700;
        padding: 0.25rem 0.68rem;
        border-radius: 999px;
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
        transition: transform 0.2s ease, background 0.2s ease;
    }
    .mini-chip:hover {
        transform: translateY(-2px);
        background: #E0E7FF;
        color: #4338CA;
    }

    /* 우측 아일릿 원희 치어링 HUD 카드 */
    .wonhee-card {
        position: relative;
        flex: 0.85;
        min-width: 195px;
        padding: 0.95rem 0.85rem 0.85rem;
        border-radius: 22px;
        background: linear-gradient(155deg, #FFFFFF 0%, #FDF2F8 55%, #EEF2FF 100%);
        border: 1.5px solid rgba(244, 114, 182, 0.35);
        box-shadow: 0 12px 26px rgba(236, 72, 153, 0.12);
        text-align: center;
        z-index: 2;
        animation: floatBob 4.2s ease-in-out infinite;
        transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .wonhee-card:hover {
        transform: scale(1.05) rotate(-1deg);
    }

    .sparkle-1 {
        position: absolute;
        top: 8px;
        left: 12px;
        font-size: 0.95rem;
        animation: twinkleStar 2.2s infinite;
    }
    .sparkle-2 {
        position: absolute;
        top: 12px;
        right: 12px;
        font-size: 0.9rem;
        animation: twinkleStar 2.8s infinite 0.6s;
    }

    .wonhee-name-tag {
        display: inline-block;
        margin-top: 0.35rem;
        padding: 0.18rem 0.65rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 800;
        color: #DB2777;
        background: rgba(252, 231, 243, 0.9);
        border: 1px solid rgba(244, 114, 182, 0.4);
    }

    .wonhee-speech {
        margin-top: 0.4rem;
        padding: 0.38rem 0.55rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.92);
        font-size: 0.75rem;
        font-weight: 700;
        color: #334155;
        line-height: 1.35;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
    }

    /* 모바일 반응형 대응 */
    @media (max-width: 640px) {
        .hero-wrapper {
            flex-direction: column;
            text-align: center;
        }
        .chip-row {
            justify-content: center;
        }
    }

    /* 4. 입력 컨트롤 카드 스타일 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(14px);
        border: 1.5px solid rgba(226, 232, 240, 0.95);
        border-radius: 18px;
        padding: 1.05rem 1.2rem 0.8rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:hover {
        transform: translateY(-3px);
        border-color: #818CF8;
        box-shadow: 0 14px 30px rgba(99, 102, 241, 0.12);
    }

    div[data-testid="stWidgetLabel"] p {
        color: #1E293B !important;
        font-weight: 700 !important;
        font-size: 0.96rem !important;
    }
    .stCaption {
        color: #4F46E5 !important;
        font-weight: 700 !important;
    }

    /* 5. 실행 버튼 (스프링 바운스 + 그라데이션 광택) */
    div.stButton > button[kind="primary"] {
        margin-top: 0.7rem;
        background: linear-gradient(120deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%) !important;
        background-size: 200% auto !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.82rem 1.5rem !important;
        font-family: 'SUIT', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.06rem !important;
        letter-spacing: -0.01em;
        box-shadow: 0 10px 26px rgba(99, 102, 241, 0.32) !important;
        transition: all 0.32s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-position: right center !important;
        transform: translateY(-4px) scale(1.015) !important;
        box-shadow: 0 16px 34px rgba(236, 72, 153, 0.35) !important;
    }
    div.stButton > button[kind="primary"]:active {
        transform: scale(0.97) !important;
    }

    /* 6. 결과 출력 애니메이션 (1. 텍스트 메시지 -> 2. 테이블 -> 3. 강조 수치) */
    /* [출력 1] 텍스트 메시지 */
    div[data-testid="stAlert"] {
        border-radius: 16px !important;
        border: 1.5px solid rgba(99, 102, 241, 0.25) !important;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
        animation: slideReveal 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }

    /* [출력 2] 데이터프레임(테이블) */
    div[data-testid="stDataFrame"] {
        border-radius: 18px !important;
        overflow: hidden !important;
        border: 1.5px solid rgba(129, 140, 248, 0.32) !important;
        box-shadow: 0 14px 34px rgba(99, 102, 241, 0.09) !important;
        animation: springPop 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 0.14s backwards;
    }

    /* [출력 3] 강조 수치 (Metric) 카드 */
    div[data-testid="stMetric"] {
        background: linear-gradient(155deg, rgba(255, 255, 255, 0.95) 0%, rgba(238, 242, 255, 0.85) 100%);
        border: 1.5px solid rgba(129, 140, 248, 0.32);
        border-radius: 20px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 10px 26px rgba(99, 102, 241, 0.08);
        transition: all 0.32s cubic-bezier(0.34, 1.56, 0.64, 1);
        animation: springPop 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.28s backwards;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-7px) scale(1.03) rotate(0.6deg);
        border-color: #EC4899;
        box-shadow: 0 18px 36px rgba(236, 72, 153, 0.18);
    }
    div[data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-size: 0.86rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Plus Jakarta Sans', 'SUIT', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.7rem !important;
        background: linear-gradient(120deg, #4F46E5 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h3 {
        color: #0F172A !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        margin-top: 1.35rem !important;
    }
    </style>

    <div class="hero-wrapper">
        <div class="deco-orb-1"></div>
        <div class="deco-orb-2"></div>

        <div class="hero-left">
            <div class="live-badge">
                <span class="live-dot"></span>
                MAGNETIC FPS ANALYZER ✨
            </div>
            <h1>내 PC 게임 <span class="grad-text">프레임(FPS)</span> 예측기</h1>
            <p>그래픽카드와 그래픽 품질 옵션을 선택하면 게임별 예상 프레임과 플레이 적합도를 실시간으로 분석해 드려요!</p>
            <div class="chip-row">
                <span class="mini-chip">🟢 120+ FPS 적합</span>
                <span class="mini-chip">🟡 60+ FPS 보통</span>
                <span class="mini-chip">🔴 60 미만 미달</span>
            </div>
        </div>

        <div class="wonhee-card">
            <span class="sparkle-1">✨</span>
            <span class="sparkle-2">🧲</span>
            <svg width="86" height="86" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- 배경 후광 링 -->
                <circle cx="60" cy="60" r="52" fill="url(#bgGrad)" stroke="#F472B6" stroke-width="2" stroke-dasharray="6 4"/>
                <!-- 긴 생머리 뒷머리 -->
                <path d="M28 58C26 84 32 102 38 106H82C88 102 94 84 92 58C92 34 78 22 60 22C42 22 28 34 28 58Z" fill="#27272A"/>
                <!-- 교복/Y2K 상의 -->
                <path d="M36 105C38 92 48 86 60 86C72 86 82 92 84 105H36Z" fill="#FFFFFF"/>
                <path d="M47 88L60 101L73 88" stroke="#6366F1" stroke-width="3" stroke-linecap="round"/>
                <path d="M55 93L60 99L65 93L60 89L55 93Z" fill="#F472B6"/>
                <!-- 얼굴형 -->
                <path d="M38 55C38 71 47 82 60 82C73 82 82 71 82 55C82 40 72 31 60 31C48 31 38 40 38 55Z" fill="#FFE8D9"/>
                <!-- 앞머리 & 옆머리 -->
                <path d="M36 56C36 37 46 25 60 25C74 25 84 37 84 56C81 45 75 40 69 44C64 39 56 39 51 44C45 40 39 45 36 56Z" fill="#27272A"/>
                <!-- 별 모양 헤어핀 (원희 포인트) -->
                <path d="M77 35L79 39L83 39.5L80 42.5L80.8 46.5L77 44.5L73.2 46.5L74 42.5L71 39.5L75 39L77 35Z" fill="#FACC15"/>
                <!-- 초롱초롱 큰 눈 -->
                <ellipse cx="49" cy="58" rx="4.2" ry="5" fill="#1E1B4B"/>
                <ellipse cx="71" cy="58" rx="4.2" ry="5" fill="#1E1B4B"/>
                <circle cx="47.5" cy="56" r="1.7" fill="#FFFFFF"/>
                <circle cx="69.5" cy="56" r="1.7" fill="#FFFFFF"/>
                <circle cx="50.5" cy="59.5" r="0.9" fill="#F472B6"/>
                <circle cx="72.5" cy="59.5" r="0.9" fill="#F472B6"/>
                <!-- 발그레한 볼터치 -->
                <ellipse cx="43" cy="65" rx="4.5" ry="2.5" fill="#F472B6" fill-opacity="0.38"/>
                <ellipse cx="77" cy="65" rx="4.5" ry="2.5" fill="#F472B6" fill-opacity="0.38"/>
                <!-- 귀여운 미소 -->
                <path d="M55 69C57.5 72.5 62.5 72.5 65 69" stroke="#E11D48" stroke-width="2.4" stroke-linecap="round"/>
                <defs>
                    <linearGradient id="bgGrad" x1="15" y1="15" x2="105" y2="105" gradientUnits="userSpaceOnUse">
                        <stop stop-color="#FCE7F3"/>
                        <stop offset="1" stop-color="#E0E7FF"/>
                    </linearGradient>
                </defs>
            </svg>
            <div><span class="wonhee-name-tag">ILLIT 원희 CHEER</span></div>
            <div class="wonhee-speech">120 FPS 넘기면 완전 럭키잖아~ ✨</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================
# 2. 리스트 선언: 게임 목록, 기본 FPS, GPU 배율, 옵션명
# =============================================
games = ["리그 오브 레전드", "발로란트", "배틀그라운드"]
base_fps = [260, 240, 90]  # RTX 3060 · 옵션 1단계(낮음) 기준 기본 FPS

gpu_list = ["RTX 3060", "RTX 4060", "RTX 4070"]
gpu_rate = [1.0, 1.2, 1.7]  # 그래픽카드별 성능 배율
option_names = ["낮음", "보통", "높음", "매우 높음", "울트라"]


# =============================================
# 함수 정의 (def): GPU와 옵션을 받아 예상 FPS와 적합도 메시지 리턴
# =============================================
def predict_fps(gpu_name, option):
    """GPU 이름과 그래픽 옵션을 매개변수로 받아 예상 FPS 리스트와 적합도에 따른 텍스트 메시지를 리턴"""
    gpu_power = gpu_rate[gpu_list.index(gpu_name)]
    option_weight = 1 - 0.15 * (option - 1)  # 옵션 1단계 상승 시 프레임 15% 감소

    fps_list = []
    for base in base_fps:
        fps_list.append(int(base * gpu_power * option_weight))

    # 최저 프레임(fps) 기준 적합도 조건 판별 (120 / 60 프레임 기준)
    fps = min(fps_list)
    if fps >= 120:
        suitability = "적합"
        message = f"[{suitability}] {gpu_name} 환경에서는 모든 게임이 120 FPS 이상으로 매우 적합합니다!"
    elif fps >= 60:
        suitability = "보통"
        message = f"[{suitability}] {gpu_name} 환경에서는 모든 게임이 60 FPS 이상으로 무난하게 플레이 가능합니다."
    else:
        suitability = "미달"
        message = f"[{suitability}] {gpu_name} 환경에서는 일부 고사양 게임이 60 FPS 미만으로 그래픽 옵션 조정이 필요합니다."

    return fps_list, message


# =============================================
# 3. 입력받기: 그래픽카드(selectbox) & 그래픽 옵션(slider)
# =============================================
col1, col2 = st.columns(2)
with col1:
    selected_gpu = st.selectbox("🖥️ 그래픽카드(GPU) 선택", gpu_list, index=1)
with col2:
    selected_option = st.slider("⚙️ 그래픽 품질 옵션", 1, 5, 2)
    st.caption(f"✨ 현재 선택 옵션: {option_names[selected_option - 1]} ({selected_option}단계)")

# =============================================
# 4. 버튼 클릭 시 함수 실행
# =============================================
if st.button("✨ 예상 FPS 및 적합도 분석하기", type="primary", use_container_width=True):
    fps_list, message = predict_fps(selected_gpu, selected_option)

    # =============================================
    # 5. 조건 판단 (if-elif-else): 게임별 FPS에 따른 적합도 판정
    # =============================================
    suitability_list = []
    fit_count = 0

    for fps in fps_list:
        if fps >= 120:
            suitability = "🟢 적합"
            fit_count += 1
        elif fps >= 60:
            suitability = "🟡 보통"
        else:
            suitability = "🔴 미달"
        suitability_list.append(suitability)

    # =============================================
    # 6. 반복 출력 & 결과 화면 (1. 텍스트 메시지 -> 2. 테이블 -> 3. 강조 수치)
    # =============================================

    # [출력 1] 텍스트 메시지
    if min(fps_list) >= 120:
        st.success(message, icon="🎉")
        st.balloons()
    elif min(fps_list) >= 60:
        st.info(message, icon="✅")
    else:
        st.warning(message, icon="⚠️")

    # [출력 2] 테이블 (for문으로 게임별 FPS 및 적합도 리스트 순회하여 표 생성)
    table_data = []
    for i in range(len(games)):
        table_data.append(
            {
                "게임명": games[i],
                "예상 FPS": fps_list[i],
                "적합도": suitability_list[i],
            }
        )

    st.subheader("📊 게임별 예상 프레임 및 적합도")
    st.dataframe(
        pd.DataFrame(table_data),
        hide_index=True,
        use_container_width=True,
        column_config={
            "게임명": st.column_config.TextColumn("게임명", width="medium"),
            "예상 FPS": st.column_config.ProgressColumn(
                "예상 FPS",
                format="%d FPS",
                min_value=0,
                max_value=450,
            ),
            "적합도": st.column_config.TextColumn("적합도 (120 / 60 FPS 기준)"),
        },
    )

    # [출력 3] 강조 수치 (Metric)
    avg_fps = sum(fps_list) // len(fps_list)
    best_game = games[fps_list.index(max(fps_list))]

    st.subheader("🏆 핵심 성능 요약")
    m1, m2, m3 = st.columns(3)
    m1.metric("평균 예상 프레임", f"{avg_fps} FPS")
    m2.metric("최고 프레임 게임", best_game, f"{max(fps_list)} FPS")
    m3.metric("적합(120↑) 게임 수", f"{fit_count} / {len(games)}개")

    with st.expander("ℹ️ 프레임 산출 및 적합도 기준 보기"):
        st.markdown(
            f"""
            - **적합도 기준**: `120 FPS 이상` **적합** / `60 FPS 이상` **보통** / `60 FPS 미만` **미달**
            - **계산 공식**: `게임 기본 FPS × 그래픽카드 배율({gpu_rate[gpu_list.index(selected_gpu)]}배) × 옵션 가중치({int((1 - 0.15 * (selected_option - 1)) * 100)}%)`
            """
        )
else:
    st.info("위에서 그래픽카드와 옵션을 선택한 뒤 **예상 FPS 및 적합도 분석하기** 버튼을 눌러 주세요!", icon="👆")
