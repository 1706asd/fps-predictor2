"""
🎮 내 PC 게임 프레임(FPS) 예측기
- 그래픽카드(GPU), 프로세서(CPU), 그래픽 품질 옵션에 따른 게임별 예상 FPS 및 플레이 적합도 분석 웹앱
"""
import streamlit as st
import pandas as pd

# =============================================
# 1. 시작: 페이지 설정 및 밝은 하이엔드 애니메이션 UI
# =============================================
st.set_page_config(
    page_title="FPS STUDIO ✨ 내 PC 게임 프레임 예측기",
    page_icon="🎮",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root {
        color-scheme: light !important;
    }
    @keyframes auroraShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes springEntrance {
        0% { opacity: 0; transform: translateY(28px) scale(0.95); }
        65% { opacity: 1; transform: translateY(-5px) scale(1.015); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    @keyframes slideMessage {
        0% { opacity: 0; transform: translateX(-24px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    @keyframes floatSlow {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-9px) rotate(1.5deg); }
    }
    @keyframes spinCW {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    @keyframes spinCCW {
        0% { transform: rotate(360deg); }
        100% { transform: rotate(0deg); }
    }
    @keyframes glassSweep {
        0% { transform: translateX(-150%) skewX(-22deg); }
        55%, 100% { transform: translateX(280%) skewX(-22deg); }
    }
    @keyframes pulseRing {
        0% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.55); }
        70% { box-shadow: 0 0 0 10px rgba(79, 70, 229, 0); }
        100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
    }
    @keyframes floatTag {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-3px); }
    }
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #F8FAFC, #E0E7FF, #E0F2FE, #FCE7F3, #EEF2FF) !important;
        background-size: 300% 300% !important;
        animation: auroraShift 10s ease infinite !important;
        color: #0F172A !important;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    [data-testid="stMain"], [data-testid="stHeader"], section.main {
        background: transparent !important;
    }
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label, .stApp button, .stApp input, .stApp td, .stApp th {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 850px !important;
    }
    .hero-card {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
        padding: 2rem 2.2rem;
        margin-bottom: 1.6rem;
        border-radius: 28px;
        background: rgba(255, 255, 255, 0.90);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 2px solid #FFFFFF;
        box-shadow: 0 20px 45px rgba(79, 70, 229, 0.12), 0 4px 14px rgba(15, 23, 42, 0.05);
        overflow: hidden;
        animation: springEntrance 0.75s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    .hero-card::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 38%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.9), transparent);
        animation: glassSweep 4.8s ease-in-out infinite;
        pointer-events: none;
    }
    .orb-blue {
        position: absolute;
        top: -25px;
        left: 38%;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.22) 0%, transparent 70%);
        animation: floatSlow 4.5s ease-in-out infinite;
        pointer-events: none;
    }
    .orb-pink {
        position: absolute;
        bottom: -30px;
        right: 26%;
        width: 145px;
        height: 145px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(236, 72, 153, 0.20) 0%, transparent 70%);
        animation: floatSlow 5.8s ease-in-out infinite reverse;
        pointer-events: none;
    }
    .hero-text {
        flex: 1.45;
        z-index: 2;
    }
    .top-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0.36rem 0.95rem;
        border-radius: 999px;
        font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif !important;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        color: #4338CA;
        background: linear-gradient(90deg, #EEF2FF 0%, #E0F2FE 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        margin-bottom: 0.85rem;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4F46E5;
        animation: pulseRing 1.8s infinite;
    }
    .hero-text h1 {
        margin: 0 !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.03em !important;
        line-height: 1.25 !important;
        color: #0F172A !important;
    }
    .hero-text h1 .accent {
        background: linear-gradient(120deg, #4F46E5 0%, #7C3AED 50%, #0284C7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-text p {
        margin: 0.6rem 0 1rem !important;
        font-size: 0.95rem !important;
        line-height: 1.55 !important;
        color: #475569 !important;
        font-weight: 500 !important;
    }
    .spec-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 7px;
    }
    .spec-chip {
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        background: #F1F5F9;
        color: #1E293B;
        border: 1px solid #CBD5E1;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .spec-chip:hover {
        transform: translateY(-3px) scale(1.04);
        background: #EEF2FF;
        border-color: #818CF8;
        color: #4338CA;
    }
    .gauge-widget {
        position: relative;
        flex: 0.75;
        min-width: 178px;
        padding: 1.05rem;
        border-radius: 24px;
        background: linear-gradient(155deg, #FFFFFF 0%, #EEF2FF 55%, #E0F2FE 100%);
        border: 1.5px solid rgba(99, 102, 241, 0.28);
        box-shadow: 0 12px 28px rgba(79, 70, 229, 0.12);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 2;
        animation: floatSlow 4s ease-in-out infinite;
        transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .gauge-widget:hover {
        transform: scale(1.06) rotate(-1.5deg);
    }
    .dual-ring {
        position: relative;
        width: 96px;
        height: 96px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .ring-outer {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 3px dashed #6366F1;
        animation: spinCW 12s linear infinite;
    }
    .ring-middle {
        position: absolute;
        inset: 7px;
        border-radius: 50%;
        border: 2px dotted #0EA5E9;
        animation: spinCCW 8s linear infinite;
    }
    .ring-core {
        width: 68px;
        height: 68px;
        border-radius: 50%;
        background: #FFFFFF;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.18);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .ring-value {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.15rem;
        font-weight: 800;
        color: #4F46E5;
        line-height: 1.1;
    }
    .ring-sub {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.62rem;
        font-weight: 800;
        color: #64748B;
    }
    .gauge-tag {
        margin-top: 0.6rem;
        font-size: 0.74rem;
        font-weight: 800;
        color: #4338CA;
        background: #E0E7FF;
        padding: 0.22rem 0.7rem;
        border-radius: 999px;
        animation: floatTag 2.5s ease-in-out infinite;
    }
    @media (max-width: 640px) {
        .hero-card { flex-direction: column; text-align: center; }
        .spec-chips { justify-content: center; }
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(14px);
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 20px !important;
        padding: 1.05rem 1.1rem 0.8rem !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05) !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:hover,
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:hover {
        transform: translateY(-4px) !important;
        border-color: #6366F1 !important;
        box-shadow: 0 14px 30px rgba(99, 102, 241, 0.14) !important;
    }
    div[data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 0.92rem !important;
    }
    .stCaption, .stCaption p {
        color: #4F46E5 !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 12px !important;
    }
    div.stButton > button[kind="primary"] {
        margin-top: 0.75rem !important;
        background: linear-gradient(120deg, #4F46E5 0%, #7C3AED 50%, #0284C7 100%) !important;
        background-size: 200% auto !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.85rem 1.5rem !important;
        font-weight: 800 !important;
        font-size: 1.08rem !important;
        box-shadow: 0 10px 26px rgba(79, 70, 229, 0.32) !important;
        transition: all 0.32s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div.stButton > button[kind="primary"] p {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-position: right center !important;
        transform: translateY(-4px) scale(1.015) !important;
        box-shadow: 0 16px 34px rgba(2, 132, 199, 0.36) !important;
    }
    div.stButton > button[kind="primary"]:active {
        transform: scale(0.97) !important;
    }
    div[data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.94) !important;
        color: #0F172A !important;
        border-radius: 16px !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06) !important;
        animation: slideMessage 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    div[data-testid="stAlert"] p {
        color: #0F172A !important;
        font-weight: 600 !important;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 18px !important;
        overflow: hidden !important;
        border: 1.5px solid rgba(99, 102, 241, 0.32) !important;
        box-shadow: 0 14px 34px rgba(79, 70, 229, 0.10) !important;
        animation: springEntrance 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 0.15s backwards;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(155deg, #FFFFFF 0%, #EEF2FF 100%) !important;
        border: 1.5px solid rgba(99, 102, 241, 0.32) !important;
        border-radius: 20px !important;
        padding: 1.15rem 1.25rem !important;
        box-shadow: 0 10px 26px rgba(79, 70, 229, 0.09) !important;
        transition: all 0.32s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        animation: springEntrance 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s backwards;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-7px) scale(1.03) rotate(0.6deg) !important;
        border-color: #4F46E5 !important;
        box-shadow: 0 18px 36px rgba(79, 70, 229, 0.22) !important;
    }
    div[data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-size: 0.86rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricValue"] div {
        font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.7rem !important;
        background: linear-gradient(120deg, #4F46E5 0%, #0284C7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.90) !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 16px !important;
    }
    div[data-testid="stExpander"] summary p {
        color: #1E293B !important;
        font-weight: 700 !important;
    }
    h3 {
        color: #0F172A !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        margin-top: 1.4rem !important;
    }
    </style>
    <div class="hero-card">
        <div class="orb-blue"></div>
        <div class="orb-pink"></div>
        <div class="hero-text">
            <div class="top-pill">
                <span class="pulse-dot"></span>
                FLAGSHIP CPU × GPU FPS ANALYZER ✨
            </div>
            <h1>내 PC 게임 <span class="accent">프레임(FPS)</span> 예측기</h1>
            <p>보급형부터 최상급 플래그십 GPU · CPU, 그래픽 품질 옵션을 조합해 게임별 예상 프레임과 플레이 적합도를 분석합니다.</p>
            <div class="spec-chips">
                <span class="spec-chip">🟢 120+ FPS 적합</span>
                <span class="spec-chip">🟡 60+ FPS 보통</span>
                <span class="spec-chip">🔴 60 미만 미달</span>
            </div>
        </div>
        <div class="gauge-widget">
            <div class="dual-ring">
                <div class="ring-outer"></div>
                <div class="ring-middle"></div>
                <div class="ring-core">
                    <span class="ring-value">120+</span>
                    <span class="ring-sub">TARGET FPS</span>
                </div>
            </div>
            <div class="gauge-tag">⚡ HIGH-END READY</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================
# 2. 리스트 선언: 게임 목록, 기본 FPS, GPU/CPU 배율, 옵션명
# =============================================
games = ["리그 오브 레전드", "발로란트", "배틀그라운드"]
base_fps = [260, 240, 90]  # RTX 3060 · i5-12400F · 옵션 1단계(낮음) 기준 기본 FPS

gpu_list = [
    "RTX 3060",
    "RTX 4060",
    "RTX 4070",
    "RTX 4080 SUPER",
    "RTX 4090",
    "RTX 5080",
    "RTX 5090",
]
gpu_rate = [1.0, 1.2, 1.7, 2.2, 2.6, 2.8, 3.4]  # 그래픽카드(GPU) 성능 배율

cpu_list = [
    "i5-12400F",
    "i5-14600K",
    "i7-14700K",
    "i9-14900K",
    "Ryzen 7 7800X3D",
    "Ryzen 7 9800X3D",
    "Ryzen 9 9950X3D",
]
cpu_rate = [1.0, 1.15, 1.23, 1.30, 1.32, 1.45, 1.48]  # 프로세서(CPU) 게이밍 연산 배율

option_names = ["낮음", "보통", "높음", "매우 높음", "울트라"]


# =============================================
# 함수 정의 (def): GPU, CPU, 옵션을 받아 예상 FPS와 적합도 메시지 리턴
# =============================================
def predict_fps(gpu_name, cpu_name, option):
    """GPU 이름, CPU 이름, 그래픽 옵션을 매개변수로 받아 예상 FPS 리스트와 적합도 텍스트 메시지를 리턴"""
    gpu_power = gpu_rate[gpu_list.index(gpu_name)]
    cpu_power = cpu_rate[cpu_list.index(cpu_name)]
    option_weight = 1 - 0.15 * (option - 1)  # 옵션 1단계 상승 시 프레임 15% 감소

    fps_list = []
    for base in base_fps:
        fps_list.append(int(base * gpu_power * cpu_power * option_weight))

    # 최저 프레임(fps) 기준 적합도 조건 판별 (120 / 60 프레임 기준)
    fps = min(fps_list)
    if fps >= 120:
        suitability = "적합"
        message = f"[{suitability}] {cpu_name} + {gpu_name} 조합은 모든 게임에서 120 FPS 이상으로 매우 적합합니다!"
    elif fps >= 60:
        suitability = "보통"
        message = f"[{suitability}] {cpu_name} + {gpu_name} 조합은 모든 게임에서 60 FPS 이상으로 무난하게 플레이 가능합니다."
    else:
        suitability = "미달"
        message = f"[{suitability}] {cpu_name} + {gpu_name} 조합은 일부 고사양 게임이 60 FPS 미만으로 그래픽 옵션 조정이 필요합니다."

    return fps_list, message


# =============================================
# 3. 입력받기: 그래픽카드(GPU), 프로세서(CPU), 그래픽 옵션
# =============================================
col1, col2, col3 = st.columns(3)
with col1:
    selected_gpu = st.selectbox("🖥️ 그래픽카드 (GPU)", gpu_list, index=2)
    st.caption(f"GPU 배율: {gpu_rate[gpu_list.index(selected_gpu)]}x")
with col2:
    selected_cpu = st.selectbox("🧠 프로세서 (CPU)", cpu_list, index=4)
    st.caption(f"CPU 배율: {cpu_rate[cpu_list.index(selected_cpu)]}x")
with col3:
    selected_option = st.slider("⚙️ 그래픽 품질 옵션", 1, 5, 3)
    st.caption(f"선택 옵션: {option_names[selected_option - 1]} ({selected_option}단계)")

# =============================================
# 4. 버튼 클릭 시 함수 실행
# =============================================
if st.button("✨ 예상 FPS 및 적합도 분석하기", type="primary", use_container_width=True):
    fps_list, message = predict_fps(selected_gpu, selected_cpu, selected_option)

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
                max_value=1400,
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
            - **계산 공식**: `게임 기본 FPS × GPU 배율({gpu_rate[gpu_list.index(selected_gpu)]}배) × CPU 배율({cpu_rate[cpu_list.index(selected_cpu)]}배) × 옵션 가중치({int((1 - 0.15 * (selected_option - 1)) * 100)}%)`
            """
        )
else:
    st.info("위에서 GPU, CPU, 그래픽 옵션을 선택한 뒤 **예상 FPS 및 적합도 분석하기** 버튼을 눌러 주세요!", icon="👆")
