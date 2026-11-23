"""
🎮 내 PC 게임 프레임(FPS) 예측기
- 그래픽카드(GPU)와 그래픽 품질 옵션에 따른 게임별 예상 FPS 및 플레이 적합도 분석 웹앱
"""
import streamlit as st
import pandas as pd

# =============================================
# 1. 시작: 페이지 설정 및 밝은 배경 · 폰트 · 애니메이션 스타일
# =============================================
st.set_page_config(
    page_title="FPS STUDIO ✨ 내 PC 게임 프레임 예측기",
    page_icon="🎮",
    layout="centered",
)

st.markdown(
    """
    <!-- Streamlit에서 정상 작동하는 외부 폰트 직접 로드 (Pretendard + Plus Jakarta Sans) -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet">

    <style>
    /* 1. Streamlit 다크모드 무력화 및 밝은 오로라 배경 강제 출력 */
    :root {
        color-scheme: light !important;
    }

    @keyframes auroraFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #F8FAFC, #E0E7FF, #E0F2FE, #FCE7F3, #EEF2FF) !important;
        background-size: 300% 300% !important;
        animation: auroraFlow 10s ease infinite !important;
        color: #0F172A !important;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    [data-testid="stMain"], [data-testid="stHeader"], section.main {
        background: transparent !important;
    }

    /* 아이콘 깨짐 없이 전체 텍스트에 Pretendard 폰트 강제 적용 */
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label, .stApp button, .stApp input, .stApp td, .stApp th {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 820px !important;
    }

    /* 2. 다채로운 키프레임 애니메이션 모음 */
    @keyframes popSpring {
        0% {
            opacity: 0;
            transform: translateY(28px) scale(0.94);
        }
        65% {
            opacity: 1;
            transform: translateY(-5px) scale(1.015);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes slideInLeft {
        0% {
            opacity: 0;
            transform: translateX(-24px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes floatSmooth {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-9px) rotate(1.5deg); }
    }

    @keyframes spinClockwise {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes spinCounter {
        0% { transform: rotate(360deg); }
        100% { transform: rotate(0deg); }
    }

    @keyframes shineSweep {
        0% { transform: translateX(-150%) skewX(-22deg); }
        55%, 100% { transform: translateX(280%) skewX(-22deg); }
    }

    @keyframes pulseHalo {
        0% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.55); }
        70% { box-shadow: 0 0 0 11px rgba(79, 70, 229, 0); }
        100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
    }

    @keyframes badgeFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }

    /* 3. 상단 히어로 배너 (글래스모피즘 + 광택 스윕 + 플로팅 오브) */
    .hero-card {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
        padding: 2rem 2.2rem;
        margin-bottom: 1.6rem;
        border-radius: 28px;
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 2px solid #FFFFFF;
        box-shadow:
            0 20px 45px rgba(79, 70, 229, 0.12),
            0 4px 14px rgba(15, 23, 42, 0.05);
        overflow: hidden;
        animation: popSpring 0.75s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }

    /* 유리 카드 광택 지나가는 효과 */
    .hero-card::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 38%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.85), transparent);
        animation: shineSweep 4.8s ease-in-out infinite;
        pointer-events: none;
    }

    /* 배경 플로팅 파스텔 구슬 */
    .orb-blue {
        position: absolute;
        top: -25px;
        left: 38%;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.22) 0%, transparent 70%);
        animation: floatSmooth 4.5s ease-in-out infinite;
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
        animation: floatSmooth 5.8s ease-in-out infinite reverse;
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
        animation: pulseHalo 1.8s infinite;
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

    /* 우측 듀얼 회전 FPS 게이지 위젯 */
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
        animation: floatSmooth 4s ease-in-out infinite;
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
        animation: spinClockwise 12s linear infinite;
    }

    .ring-middle {
        position: absolute;
        inset: 7px;
        border-radius: 50%;
        border: 2px dotted #0EA5E9;
        animation: spinCounter 8s linear infinite;
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
        animation: badgeFloat 2.5s ease-in-out infinite;
    }

    @media (max-width: 640px) {
        .hero-card {
            flex-direction: column;
            text-align: center;
        }
        .spec-chips {
            justify-content: center;
        }
    }

    /* 4. 입력 위젯 카드 (다크모드에서도 밝은 화이트 카드 유지) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.90) !important;
        backdrop-filter: blur(14px);
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 20px !important;
        padding: 1.1rem 1.25rem 0.85rem !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05) !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:hover {
        transform: translateY(-4px) !important;
        border-color: #6366F1 !important;
        box-shadow: 0 14px 30px rgba(99, 102, 241, 0.14) !important;
    }

    div[data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 0.96rem !important;
    }
    .stCaption, .stCaption p {
        color: #4F46E5 !important;
        font-weight: 700 !important;
    }

    /* 셀렉트박스 밝은 테마 강제 */
    div[data-baseweb="select"] > div {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 12px !important;
    }

    /* 5. 분석하기 버튼 (스프링 바운스 + 그라데이션 이동) */
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

    /* 6. 결과 화면 순차 애니메이션 (1. 텍스트 메시지 -> 2. 테이블 -> 3. 강조 수치) */
    /* [출력 1] 텍스트 메시지 */
    div[data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.92) !important;
        color: #0F172A !important;
        border-radius: 16px !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06) !important;
        animation: slideInLeft 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    div[data-testid="stAlert"] p {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    /* [출력 2] 테이블 */
    div[data-testid="stDataFrame"] {
        border-radius: 18px !important;
        overflow: hidden !important;
        border: 1.5px solid rgba(99, 102, 241, 0.32) !important;
        box-shadow: 0 14px 34px rgba(79, 70, 229, 0.10) !important;
        animation: popSpring 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 0.15s backwards;
    }

    /* [출력 3] 강조 수치 (Metric) 카드 */
    div[data-testid="stMetric"] {
        background: linear-gradient(155deg, #FFFFFF 0%, #EEF2FF 100%) !important;
        border: 1.5px solid rgba(99, 102, 241, 0.32) !important;
        border-radius: 20px !important;
        padding: 1.15rem 1.25rem !important;
        box-shadow: 0 10px 26px rgba(79, 70, 229, 0.09) !important;
        transition: all 0.32s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        animation: popSpring 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s backwards;
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

    /* Expander 밝은 테마 강제 */
    div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.88) !important;
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
                REAL-TIME FPS ANALYZER ✨
            </div>
            <h1>내 PC 게임 <span class="accent">프레임(FPS)</span> 예측기</h1>
            <p>그래픽카드와 그래픽 품질 옵션을 선택하면 게임별 예상 프레임과 플레이 적합도를 즉시 분석합니다.</p>
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
            <div class="gauge-tag">⚡ BENCHMARK READY</div>
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

gpu_list = ["RTX 3
