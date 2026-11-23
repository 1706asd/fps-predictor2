"""
🎮 내 PC 게임 프레임(FPS) 예측기
- 그래픽카드(GPU)와 그래픽 품질 옵션에 따른 게임별 예상 FPS 및 플레이 적합도 분석 웹앱
"""
import streamlit as st
import pandas as pd

# =============================================
# 1. 시작: 페이지 설정 및 하이엔드 UI / 애니메이션 스타일
# =============================================
st.set_page_config(
    page_title="FPS STUDIO // 내 PC 게임 프레임 예측기",
    page_icon="🎮",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;800&display=swap');

    /* 1. 전체 배경 & 타이포그래피 (OpenAI / NVIDIA 다크 캔버스) */
    .stApp {
        background: radial-gradient(circle at 50% -10%, #162214 0%, #090C10 45%, #040507 100%);
        color: #F8FAFC;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 기본 헤더/여백 정리 */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 780px;
    }

    /* 2. Apple 스타일 물리 곡선 키프레임 애니메이션 */
    @keyframes appleEntrance {
        0% {
            opacity: 0;
            transform: translateY(24px) scale(0.97);
            filter: blur(6px);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
            filter: blur(0);
        }
    }

    @keyframes lightSweep {
        0% { transform: translateX(-150%) skewX(-25deg); }
        50%, 100% { transform: translateX(250%) skewX(-25deg); }
    }

    @keyframes pulseDot {
        0%, 100% { transform: scale(1); opacity: 1; box-shadow: 0 0 0 0 rgba(118, 185, 0, 0.7); }
        50% { transform: scale(1.25); opacity: 0.85; box-shadow: 0 0 0 8px rgba(118, 185, 0, 0); }
    }

    @keyframes borderGlow {
        0%, 100% { border-color: rgba(118, 185, 0, 0.35); }
        50% { border-color: rgba(163, 230, 53, 0.75); }
    }

    /* 3. 히어로 배너 (Apple Pro + NVIDIA 하이테크) */
    .pro-hero {
        position: relative;
        padding: 2.1rem 2.2rem;
        border-radius: 24px;
        margin-bottom: 1.8rem;
        background: linear-gradient(145deg, rgba(20, 26, 34, 0.85) 0%, rgba(10, 13, 18, 0.95) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 24px 50px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        overflow: hidden;
        animation: appleEntrance 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* 상단 네온 하이라이트 라인 */
    .pro-hero::before {
        content: "";
        position: absolute;
        top: 0;
        left: 10%;
        right: 10%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #76B900, #A3E635, transparent);
    }

    /* 유리 반사광 스윕 효과 */
    .pro-hero::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 45%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.045), transparent);
        animation: lightSweep 6s ease-in-out infinite;
        pointer-events: none;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0.32rem 0.85rem;
        border-radius: 999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #A3E635;
        background: rgba(118, 185, 0, 0.14);
        border: 1px solid rgba(118, 185, 0, 0.4);
        margin-bottom: 0.9rem;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #8CE000;
        animation: pulseDot 2s infinite;
    }

    .pro-hero h1 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2;
        background: linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .pro-hero h1 span {
        background: linear-gradient(90deg, #76B900 0%, #BEF264 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .pro-hero p {
        margin: 0.65rem 0 0;
        font-size: 0.98rem;
        color: #94A3B8;
        font-weight: 400;
    }

    /* 4. 입력 위젯 라벨 및 컨트롤 스타일링 */
    div[data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    .stCaption {
        color: #94A3B8 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 14px !important;
        color: #F8FAFC !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #76B900 !important;
        box-shadow: 0 0 0 3px rgba(118, 185, 0, 0.18) !important;
    }

    /* 5. 시그니처 실행 버튼 (NVIDIA Lime + Apple 스프링 인터랙션) */
    div.stButton > button[kind="primary"] {
        position: relative;
        overflow: hidden;
        margin-top: 0.6rem;
        background: linear-gradient(135deg, #76B900 0%, #95E000 100%) !important;
        color: #050801 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.78rem 1.4rem !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        letter-spacing: -0.01em;
        box-shadow: 0 8px 25px rgba(118, 185, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 14px 34px rgba(118, 185, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.7) !important;
    }
    div.stButton > button[kind="primary"]:active {
        transform: translateY(0) scale(0.98) !important;
    }

    /* 6. 결과 화면 순차 등장 애니메이션 (1. 텍스트 메시지 -> 2. 테이블 -> 3. 강조 수치) */
    /* [출력 1] 텍스트 메시지 카드 */
    div[data-testid="stAlert"] {
        border-radius: 16px !important;
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.4);
        animation: appleEntrance 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* [출력 2] 데이터프레임(테이블) 컨테이너 */
    div[data-testid="stDataFrame"] {
        border-radius: 18px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.55) !important;
        animation: appleEntrance 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.12s backwards;
    }

    /* [출력 3] Apple Bento 스타일 강조 수치 (Metric) 카드 */
    div[data-testid="stMetric"] {
        background: linear-gradient(160deg, rgba(22, 28, 38, 0.9) 0%, rgba(11, 15, 22, 0.96) 100%);
        border: 1px solid rgba(118, 185, 0, 0.3);
        border-radius: 20px;
        padding: 1.15rem 1.3rem;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        animation: appleEntrance 0.85s cubic-bezier(0.16, 1, 0.3, 1) 0.24s backwards, borderGlow 4s infinite;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: #8CE000;
        box-shadow: 0 20px 40px rgba(118, 185, 0, 0.22);
    }
    div[data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', 'Pretendard', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.75rem !important;
        color: #A3E635 !important;
        letter-spacing: -0.02em;
    }
    div[data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* 서브헤더 스타일 */
    h3 {
        color: #F1F5F9 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        margin-top: 1.4rem !important;
    }
    </style>

    <div class="pro-hero">
        <div class="status-pill">
            <span class="status-dot"></span>
            FPS ENGINE READY // REAL-TIME BENCHMARK
        </div>
        <h1>내 PC 게임 <span>프레임(FPS)</span> 예측기</h1>
        <p>그래픽카드와 그래픽 품질 옵션을 설정해 게임별 예상 프레임과 플레이 적합도를 정밀 분석합니다</p>
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
        message = f"[{suitability}] {gpu_name} 환경에서는 모든 게임이 120 FPS 이상으로 매우 쾌적하게 구동됩니다!"
    elif fps >= 60:
        suitability = "보통"
        message = f"[{suitability}] {gpu_name} 환경에서는 모든 게임이 60 FPS 이상으로 무난하게 플레이 가능합니다."
    else:
        suitability = "미달"
        message = f"[{suitability}] {gpu_name} 환경에서는 일부 고사양 게임이 60 FPS 미만으로 옵션 조정이 필요합니다."

    return fps_list, message


# =============================================
# 3. 입력받기: 그래픽카드(selectbox) & 그래픽 옵션(slider)
# =============================================
col1, col2 = st.columns(2)
with col1:
    selected_gpu = st.selectbox("🖥️ 그래픽카드(GPU) 선택", gpu_list, index=1)
with col2:
    selected_option = st.slider("⚙️ 그래픽 품질 옵션", 1, 5, 2)
    st.caption(f"현재 적용 옵션: **{option_names[selected_option - 1]} ({selected_option}단계)**")

# =============================================
# 4. 버튼 클릭 시 함수 실행
# =============================================
if st.button("⚡ 프레임 및 적합도 분석 실행", type="primary", use_container_width=True):
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
    st.info("그래픽카드와 옵션을 선택한 뒤 **프레임 및 적합도 분석 실행** 버튼을 눌러 주세요.", icon="👆")
