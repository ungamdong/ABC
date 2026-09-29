import streamlit as st

def apply_toss_style():
    st.markdown(
        """
        <style>
        /* Pretendard 폰트 불러오기 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

        * {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
        }

        /* 지정 배경색 (#F5F7FA) 적용 */
        .stApp {
            background-color: #F5F7FA;
        }

        header[data-testid="stHeader"] {
            background-color: rgba(245, 247, 250, 0.8) !important;
        }
        footer {
            visibility: hidden;
        }

        /* 모바일 우선 반응형 폭 설정 (최대 500px) */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 500px !important;
        }

        /* 토스 스타일 카드 UI */
        .toss-card {
            background-color: #FFFFFF;
            border-radius: 20px;
            padding: 22px 20px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            border: 1px solid #E5E8EB;
        }

        /* 지정 Primary 색상 (#1E4FA1) 대형 버튼 */
        .stButton > button {
            width: 100%;
            background-color: #1E4FA1;
            color: #FFFFFF;
            border: none;
            border-radius: 16px;
            padding: 18px 20px;
            font-weight: 700;
            font-size: 18px;
            box-shadow: 0 4px 12px rgba(30, 79, 161, 0.2);
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background-color: #163B7A;
            color: #FFFFFF;
        }

        .stButton > button:active {
            background-color: #102B59;
            color: #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )