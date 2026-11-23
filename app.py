"""
🎮 내 PC 게임 프레임(FPS) 예측기
- 그래픽카드(GPU)와 그래픽 품질 옵션에 따른 게임별 예상 FPS 및 플레이 적합도 분석 웹앱
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
        max-width: 820px !important;
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
        box-shadow: 0 12px 28px rgba(
