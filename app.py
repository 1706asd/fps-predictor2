"""
🎮 내 PC 게임 프레임(FPS) 예측기
- 그래픽카드(GPU)와 그래픽 품질 옵션에 따른 게임별 예상 FPS 및 플레이 적합도 분석 웹앱
"""
import streamlit as st
import pandas as pd

# =============================================
# 1. 시작: 페이지 설정 및 E-Sports Telemetry HUD 스타일
# =============================================
st.set_page_config(
    page_title="FPS TELEMETRY HUD // 내 PC 게임 프레임 예측기",
    page_icon="🎮",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&display=swap');

    /* 1. 다크 네이비 사이버 그리드 배경 */
    .stApp {
        background-color: #070B19;
        background-image:
            radial-gradient(circle at 15% 15%, rgba(0, 240, 255, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 85% 20%, rgba(139, 92, 246, 0.14) 0%, transparent 45%),
            linear-gradient(rgba(0, 240, 255, 0.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(139, 92, 246, 0.035) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 34px 34px, 34px 34px;
        color: #F8FAFC;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 780px;
    }

    /* 2. E-Sports HUD 키프레임 애니메이션 */
    @keyframes scanlineFlow {
        0% { top: -20%; opacity: 0; }
        20% { opacity: 0.75; }
        80% { opacity: 0.75; }
        100% { top: 120%; opacity: 0; }
    }

    @keyframes hudLogWipe {
        0% {
            opacity: 0;
            clip-path: inset(0 100% 0 0);
            transform: translateX(-10px);
        }
        100% {
            opacity: 1;
            clip-path: inset(0 0 0 0);
            transform: translateX(0);
        }
    }

    @keyframes hudPanelRise {
        0% {
            opacity: 0;
            transform: translateY(22px) scale(0.98);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes neonPulse {
        0%, 100% {
            box-shadow: 0 0 18px rgba(0, 240, 255, 0.28), inset 0 0 12px rgba(139, 92, 246, 0.2);
        }
        50% {
            box-shadow: 0 0 28px rgba(139, 92, 246, 0.45), inset 0 0 16px rgba(0, 240, 255, 0.3);
        }
    }

    /* 3. 상단 SF Telemetry HUD 배너 (각진 프레임 + 조준선 코너 + 스캔라인) */
    .hud-banner {
        position: relative;
        padding: 1.9rem 2.1rem;
        margin-bottom: 1.7rem;
        background: linear-gradient(135deg, rgba(11, 16, 33, 0.92) 0%, rgba(19, 26, 54, 0.88) 100%);
        border: 1px solid rgba(0, 240, 255, 0.35);
        clip-path: polygon(
            0 16px, 16px 0,
            calc(100% - 16px) 0, 100% 16px,
            100% calc(100% - 16px), calc(100% - 16px) 100%,
            16px 100%, 0 calc(100% - 16px)
        );
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.65);
        overflow: hidden;
        animation: hudPanelRise 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* 흐르는 스캔라인 */
    .hud-banner::before {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00F0FF, #8B5CF6, transparent);
        box-shadow: 0 0 12px #00F0FF;
        animation: scanlineFlow 3.8s linear infinite;
        pointer-events: none;
    }

    /* 좌상단·우하단 네온 포인트 바 */
    .hud-corner-tl {
        position: absolute;
        top: 0;
        left: 0;
        width: 56px;
        height: 3px;
        background: #00F0FF;
        box-shadow: 0 0 10px #00F0FF;
    }
    .hud-corner-br {
        position: absolute;
        bottom: 0;
        right: 0;
        width: 56px;
        height: 3px;
        background: #8B5CF6;
        box-shadow: 0 0 10px #8B5CF6;
    }

    .hud-tag {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #00F0FF;
        background: rgba(0, 240, 255, 0.1);
        border: 1px solid rgba(0, 240, 255, 0.4);
        padding: 0.28rem 0.8rem;
        border-radius: 4px;
        margin-bottom: 0.8rem;
    }

    .hud-banner h1 {
        margin: 0;
        font-size: 1.95rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.25);
    }

    .hud-banner h1 span {
        background: linear-gradient(90deg, #00F0FF 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hud-banner p {
        margin: 0.55rem 0 0;
        font-size: 0.95rem;
        color: #94A3B8;
    }

    /* 4. 하드웨어 입력 패널 (모서리 타겟 조준선 느낌) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(11, 16, 33, 0.78);
        border: 1px solid rgba(0, 240, 255, 0.22);
        border-radius: 12px;
        padding: 1rem 1.1rem 0.7rem;
        box-shadow: inset 0 0 18px rgba(0, 240, 255, 0.04);
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:hover {
        border-color: rgba(0, 240, 255, 0.55);
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.12);
    }

    div[data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    .stCaption {
        color: #38BDF8 !important;
        font-weight: 600 !important;
    }

    /* 5. E-Sports 실행 트리거 버튼 */
    div.stButton > button[kind="primary"] {
        margin-top: 0.8rem;
        background: linear-gradient(90deg, #00D2FF 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.28) !important;
        border-radius: 10px !important;
        padding: 0.78rem 1.4rem !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.02em;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.45);
        animation: neonPulse 3s infinite;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.01) !important;
        filter: brightness(1.12);
        box-shadow: 0 12px 30px rgba(0, 240, 255, 0.4) !important;
    }
    div.stButton > button[kind="primary"]:active {
        transform: scale(0.98) !important;
    }

    /* 6. 결과 구역 HUD 애니메이션 (1. 텍스트 메시지 -> 2. 테이블 -> 3. 강조 수치) */
    /* [출력 1] 시스템 로그 스윕 메시지 */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        border-left: 4px solid #00F0FF !important;
        background: rgba(15, 23, 42, 0.9) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        animation: hudLogWipe 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* [출력 2] 게이지 테이블 컨테이너 */
    div[data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(139, 92, 246, 0.45) !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.55), 0 0 20px rgba(139, 92, 246, 0.15) !important;
        animation: hudPanelRise 0.65s cubic-bezier(0.16, 1, 0.3, 1) 0.12s backwards;
    }

    /* [출력 3] 3D 입체 호버 계기판 카드 (Metric) */
    div[data-testid="stMetric"] {
        background: linear-gradient(155deg, rgba(15, 23, 42, 0.95) 0%, rgba(24, 20, 56, 0.92) 100%);
        border: 1px solid rgba(0, 240, 255, 0.32);
        border-radius: 14px;
        padding: 1.05rem 1.15rem;
        box-shadow: 0 10px 26px rgba(0, 0, 0, 0.5);
        transform-style: preserve-3d;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, box-shadow 0.3s ease;
        animation: hudPanelRise 0.75s cubic-bezier(0.16, 1, 0.3, 1) 0.24s backwards;
    }
    div[data-testid="stMetric"]:hover {
        transform: perspective(700px) rotateX(6deg) rotateY(-4deg) translateY(-6px) scale(1.03);
        border-color: #00F0FF;
        box-shadow: 0 18px 36px rgba(0, 240, 255, 0.25), 0 0 18px rgba(139, 92, 246, 0.35);
    }
    div[data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
        font-size: 0.84rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', 'Pretendard', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.6rem !important;
        background: linear-gradient(90deg, #00F0FF 0%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h3 {
        color: #F8FAFC !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        margin-top: 1.4rem !important;
    }
    </style>

    <div class="hud-banner">
        <div class="hud-corner-tl"></div>
        <div class="hud-corner-br"></div>
        <div class="hud-tag">TELEMETRY HUD // SYSTEM BENCHMARK v3.0</div>
        <h1>🎮 내 PC 게임 <span>프레임(FPS)</span> 예측기</h1>
        <p>그래픽카드와 그래픽 품질 옵션을 설정해 게임별 예상 FPS와 플레이 적합도를 스캔합니다</p>
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
        message = f"[{suitability}] {gpu_name} 시스템은 모든 게임에서 120 FPS 이상을 달성하여 매우 적합합니다!"
    elif fps >= 60:
        suitability = "보통"
        message = f"[{suitability}] {gpu_name} 시스템은 모든 게임에서 60 FPS 이상으로 무난하게 플레이 가능합니다."
    else:
        suitability = "미달"
        message = f"[{suitability}] {gpu_name} 시스템은 일부 고사양 게임이 60 FPS 미만으로 그래픽 옵션 조정이 필요합니다."

    return fps_list, message


# =============================================
# 3. 입력받기: 그래픽카드(selectbox) & 그래픽 옵션(slider)
# =============================================
col1, col2 = st.columns(2)
with col1:
    selected_gpu = st.selectbox("🖥️ 그래픽카드(GPU) 선택", gpu_list, index=1)
with col2:
    selected_option = st.slider("⚙️ 그래픽 품질 옵션", 1, 5, 2)
    st.caption(f"TARGET QUALITY : {option_names[selected_option - 1]} ({selected_option}단계)")

# =============================================
# 4. 버튼 클릭 시 함수 실행
# =============================================
if st.button("⚡ TELEMETRY 스캔 및 적합도 분석 실행", type="primary", use_container_width=True):
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
        st.success(message, icon="🔥")
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
    st.info("하드웨어와 그래픽 옵션을 설정한 뒤 **TELEMETRY 스캔 및 적합도 분석 실행** 버튼을 눌러 주세요.", icon="👆")
