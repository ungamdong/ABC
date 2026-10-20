import streamlit as st

def apply_toss_style():
    st.markdown("""
        <style>
        /* 메인 배경색 */
        html body .main {
            background-color: #F2F4F6 !important;
        }
        
        /* 토스 카드 기본 디자인 (개별 커스텀 배경색 허용) */
        html body .toss-card {
            background-color: #FFFFFF;
            border-radius: 18px !important;
            padding: 20px !important;
            margin-bottom: 14px !important;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.03) !important;
        }
        
        /* 일반 하단 버튼 디자인 */
        html body .stButton > button {
            width: 100% !important;
            background-color: #1E4FA1 !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 20px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            cursor: pointer !important;
        }

        /* ============================================================= */
        /* 🎨 상단 탭(st.tabs) 전용 스타일 */
        /* ============================================================= */
        
        /* 1. 상단 탭 바 전체 컨테이너 트랙 */
        html body div[data-testid="stTabs"] div[data-baseweb="tab-list"],
        html body div[data-baseweb="tab-list"] {
            background-color: #DCE5F2 !important;
            padding: 8px !important;
            border-radius: 18px !important;
            gap: 8px !important;
            margin-bottom: 24px !important;
            border: 2px solid #C0D1E8 !important;
            display: flex !important;
            justify-content: space-between !important;
        }

        /* 2. 각 탭 버튼 기본 상태 */
        html body div[data-testid="stTabs"] button[data-baseweb="tab"],
        html body button[data-baseweb="tab"] {
            height: 60px !important;
            background-color: #FFFFFF !important;
            border-radius: 14px !important;
            border: 1px solid #CDDBEE !important;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.06) !important;
            flex: 1 1 0% !important;
            justify-content: center !important;
            align-items: center !important;
            padding: 0px 4px !important;
        }

        /* 3. 탭 버튼 내부 글씨 */
        html body div[data-testid="stTabs"] button[data-baseweb="tab"] *,
        html body button[data-baseweb="tab"] * {
            font-size: 17px !important;
            font-weight: 800 !important;
            color: #333D4B !important;
            margin: 0 !important;
        }

        /* 4. 선택된 탭 (파란색 배경 + 흰색 글씨) */
        html body div[data-testid="stTabs"] button[aria-selected="true"],
        html body button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #1E4FA1 !important;
            border: none !important;
            box-shadow: 0px 4px 14px rgba(30, 79, 161, 0.4) !important;
        }

        html body div[data-testid="stTabs"] button[aria-selected="true"] *,
        html body button[data-baseweb="tab"][aria-selected="true"] * {
            color: #FFFFFF !important;
            font-size: 17px !important;
            font-weight: 800 !important;
        }

        /* 5. 기존 밑줄 제거 */
        html body div[data-testid="stTabs"] div[data-baseweb="tab-highlight"],
        html body div[data-testid="stTabs"] div[data-baseweb="tab-border-bar"] {
            display: none !important;
            visibility: hidden !important;
        }
        </style>
    """, unsafe_allow_html=True)