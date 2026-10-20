import streamlit as st
import streamlit.components.v1 as components
from styles import apply_toss_style
from database import init_db, save_diagnosis_result, update_quiz_score
from logic import (
    SURVEY_QUESTIONS, QUIZ_QUESTIONS, LATEST_NEWS,
    validate_answers, calculate_risks, get_educational_contents, evaluate_quiz,
    ask_ai_coach
)

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="금융소비자 AI 안전코치",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 데이터베이스 자동 초기화
init_db()

# 토스 + 금융기관 스타일 디자인 적용
apply_toss_style()

# 세션 상태 변수 초기화
if "survey_answers" not in st.session_state:
    st.session_state["survey_answers"] = {}

if "tab2_state" not in st.session_state:
    st.session_state["tab2_state"] = "survey"

if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False

# 공통 클립보드 복사 JavaScript 컴포넌트
COPY_BUTTON_HTML = """
<div style="text-align: center; margin-bottom: 20px;">
    <button onclick="copyURL()" style="
        width: 100%;
        background-color: #1E4FA1;
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px 20px;
        font-weight: 700;
        font-size: 16px;
        cursor: pointer;
    ">
        🔗 서비스 링크 복사
    </button>
</div>

<script>
function copyURL() {
    var dummy = document.createElement('input');
    var text = window.parent.location.href;
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand('copy');
    document.body.removeChild(dummy);
    alert('서비스 주소가 클립보드에 복사되었습니다!\\n카카오톡이나 문자로 공유해 보세요.');
}
</script>
"""

# =============================================================
# 상단 타이틀 헤더
# =============================================================
st.markdown("""
    <div style="text-align: center; padding: 10px 0 15px 0;">
        <span style="background-color: #E8EEF9; color: #1E4FA1; font-weight: 700; font-size: 13px; padding: 6px 14px; border-radius: 20px;">
            금융소비자 보호 AI 서비스
        </span>
        <h1 style="color: #222222; font-size: 26px; font-weight: 700; margin-top: 12px; margin-bottom: 6px;">
            금융소비자 AI 안전코치
        </h1>
        <p style="color: #6B7684; font-size: 14px; margin: 0; word-break: keep-all;">
            피싱 진단부터 맞춤 예방 교육, 실전 퀴즈까지 한눈에
        </p>
    </div>
""", unsafe_allow_html=True)

# =============================================================
# 상단 탭(Tab) 메뉴 세션 (3가지 핵심 기능 배치)
# =============================================================
tab1, tab2, tab3 = st.tabs([
    "🤖 AI 즉시 분석",
    "🛡️ 3분 맞춤 진단",
    "🧩 실전 점검 퀴즈"
])

# -------------------------------------------------------------
# [탭 1] AI 실시간 피싱 분석 코너 (응급 대처)
# -------------------------------------------------------------
with tab1:
    st.markdown("""
        <div class="toss-card">
            <div style="font-size: 16px; font-weight: 700; color: #1E4FA1; margin-bottom: 6px;">
                🚨 의심스러운 문자나 전화를 받으셨나요?
            </div>
            <div style="font-size: 13px; color: #6B7684; margin-bottom: 12px; line-height: 1.5;">
                의심 내용이나 문자 텍스트를 그대로 복사하여 아래에 붙여넣으시면, AI 안전코치가 사기 가능성과 대처법을 즉시 분석해 드립니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    user_text = st.text_area(
        label="의심 문장 입력",
        placeholder="예: [국제발신] 해외결제 $980 승인 완료. 본인 요청 아닐 시 02-1234-5678 문의바랍니다.",
        height=120,
        label_visibility="collapsed",
        key="tab1_ai_input"
    )

    if st.button("AI 분석 받기 🔍", key="tab1_ai_btn"):
        if user_text.strip():
            with st.spinner("AI 안전코치가 의심 내용을 정밀 분석 중입니다..."):
                ai_reply = ask_ai_coach(user_text)
                st.markdown(f"""
                    <div class="toss-card" style="background-color: #E8EEF9; border-left: 4px solid #1E4FA1; margin-top: 12px;">
                        <div style="font-size: 15px; font-weight: 700; color: #1E4FA1; margin-bottom: 10px;">
                            💡 AI 코치의 피싱 분석 결과
                        </div>
                        <div style="font-size: 13px; color: #222222; line-height: 1.6; white-space: pre-line;">
                            {ai_reply}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("분석할 문자 또는 전화 내용을 입력해 주세요.")

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 최신 금융사기 예방 정보
    st.markdown("""
        <div style="margin: 10px 0 10px 0;">
            <h3 style="color: #222222; font-size: 16px; font-weight: 700; margin: 0;">
                📢 최신 금융사기 예방 정보
            </h3>
        </div>
    """, unsafe_allow_html=True)

    for news in LATEST_NEWS:
        st.markdown(f"""
            <div class="toss-card" style="background-color: #FFF9E6; border: 1px solid #FFE599; margin-bottom: 10px;">
                <span style="background-color: #D97706; color: white; font-weight: 700; font-size: 11px; padding: 3px 8px; border-radius: 8px;">
                    {news['tag']}
                </span>
                <div style="font-size: 14px; font-weight: 700; color: #222222; margin-top: 8px; margin-bottom: 4px;">
                    {news['title']}
                </div>
                <div style="font-size: 12px; color: #4E5968; line-height: 1.4;">
                    {news['desc']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# [탭 2] 3분 맞춤 안전진단 및 맞춤 교육 (예방 검진)
# -------------------------------------------------------------
with tab2:
    if st.session_state["tab2_state"] == "survey":
        st.markdown("""
            <div style="margin-bottom: 16px;">
                <h2 style="color: #222222; font-size: 20px; font-weight: 700; margin-bottom: 4px;">
                    🎯 금융사기 취약도 진단
                </h2>
                <p style="color: #6B7684; font-size: 13px; margin: 0;">
                    7가지 설문 항목을 작성해 주시면 개인별 위험도 리포트와 맞춤 교육을 제공합니다. (약 3분 소요)
                </p>
            </div>
        """, unsafe_allow_html=True)

        current_answers = {}
        for q in SURVEY_QUESTIONS:
            st.markdown(f"""
                <div class="toss-card" style="padding-bottom: 8px; margin-bottom: 8px;">
                    <div style="font-size: 15px; font-weight: 700; color: #222222; margin-bottom: 2px;">
                        {q['title']}
                    </div>
                    <div style="font-size: 12px; color: #6B7684; margin-bottom: 8px;">
                        {q['subtitle']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            selected_option = st.radio(
                label=f"tab2_{q['id']}_label",
                options=q["options"],
                key=f"tab2_radio_{q['id']}",
                label_visibility="collapsed"
            )
            current_answers[q["id"]] = selected_option
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        if st.button("결과 확인하기 (위험도 분석) ➔", key="tab2_submit_btn"):
            if validate_answers(current_answers):
                st.session_state["survey_answers"] = current_answers
                st.session_state["tab2_state"] = "result"
                st.rerun()
            else:
                st.warning("모든 질문에 답변해 주세요.")

    else:
        answers = st.session_state.get("survey_answers", {})
        risk_results = calculate_risks(answers)

        if "diagnosis_id" not in st.session_state:
            saved_id = save_diagnosis_result(
                age_group=answers.get("age_group", ""),
                job=answers.get("job", ""),
                voice=risk_results["voice_phishing"],
                smishing=risk_results["smishing"],
                messenger=risk_results["messenger_phishing"],
                investment=risk_results["investment"],
                quiz_score=0
            )
            st.session_state["diagnosis_id"] = saved_id

        edu_contents = get_educational_contents(risk_results)

        st.markdown("""
            <div style="margin-bottom: 16px;">
                <h2 style="color: #222222; font-size: 20px; font-weight: 700; margin-bottom: 4px;">
                    📊 맞춤 위험도 분석 리포트
                </h2>
                <p style="color: #6B7684; font-size: 13px; margin: 0;">
                    응답하신 내용을 기반으로 산출된 사기 취약도 결과입니다.
                </p>
            </div>
        """, unsafe_allow_html=True)

        def get_risk_badge(level):
            if level == "높음":
                return '<span style="background-color: #E74C3C; color: white; font-weight:700; padding:4px 10px; border-radius:12px; font-size:12px;">🚨 높음</span>'
            elif level == "보통":
                return '<span style="background-color: #F39C12; color: white; font-weight:700; padding:4px 10px; border-radius:12px; font-size:12px;">⚠️ 보통</span>'
            else:
                return '<span style="background-color: #27AE60; color: white; font-weight:700; padding:4px 10px; border-radius:12px; font-size:12px;">✅ 낮음</span>'

        st.markdown(f"""
            <div class="toss-card">
                <div style="font-size: 15px; font-weight: 700; color: #222222; margin-bottom: 14px;">
                    🛡️ 유형별 사기 위험도
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 600; color: #222222;">📞 보이스피싱</span>
                    {get_risk_badge(risk_results['voice_phishing'])}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 600; color: #222222;">📱 스미싱 (문자사기)</span>
                    {get_risk_badge(risk_results['smishing'])}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 600; color: #222222;">💬 메신저피싱</span>
                    {get_risk_badge(risk_results['messenger_phishing'])}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 14px; font-weight: 600; color: #222222;">📈 투자사기 / 리딩방</span>
                    {get_risk_badge(risk_results['investment'])}
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style="margin: 20px 0 10px 0;">
                <h3 style="color: #222222; font-size: 17px; font-weight: 700; margin: 0;">
                    🎓 사용자 맞춤 예방 교육
                </h3>
            </div>
        """, unsafe_allow_html=True)

        for edu in edu_contents:
            st.markdown(f"""
                <div class="toss-card" style="border-left: 4px solid #1E4FA1; margin-bottom: 10px;">
                    <div style="font-size: 14px; font-weight: 700; color: #1E4FA1; margin-bottom: 4px;">
                        {edu['title']}
                    </div>
                    <div style="font-size: 12px; color: #4E5968; line-height: 1.5; word-break: keep-all;">
                        {edu['desc']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # 🔗 [복구 완료] 가족 공유 카드 및 서비스 링크 복사 버튼
        st.markdown("""
            <div class="toss-card" style="background-color: #F2F4F6; border: none; text-align: center;">
                <div style="font-size: 14px; font-weight: 700; color: #191F28; margin-bottom: 4px;">
                    👨‍👩‍👧‍👦 소중한 가족에게 이 안전 지식을 알려주세요
                </div>
                <div style="font-size: 12px; color: #4E5968; margin-bottom: 8px;">
                    부모님이나 지인에게 금융사기 예방 가이드를 전달할 수 있습니다.
                </div>
            </div>
        """, unsafe_allow_html=True)

        components.html(COPY_BUTTON_HTML, height=65)

        if st.button("← 다시 진단하기", key="tab2_reset_btn"):
            if "diagnosis_id" in st.session_state:
                del st.session_state["diagnosis_id"]
            st.session_state["tab2_state"] = "survey"
            st.rerun()

# -------------------------------------------------------------
# [탭 3] 사례 기반 실전 퀴즈 및 공유 (학습 평가)
# -------------------------------------------------------------
with tab3:
    st.markdown("""
        <div style="margin-bottom: 16px;">
            <h2 style="color: #222222; font-size: 20px; font-weight: 700; margin-bottom: 4px;">
                🧩 사례 기반 실전 퀴즈
            </h2>
            <p style="color: #6B7684; font-size: 13px; margin: 0;">
                실제 금융사기 상황 예시를 읽고 올바른 대처법을 선택해 보세요.
            </p>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("quiz_submitted"):
        quiz_user_selections = {}

        for q in QUIZ_QUESTIONS:
            st.markdown(f"""
                <div class="toss-card" style="margin-bottom: 10px;">
                    <span style="background-color: #E8EEF9; color: #1E4FA1; font-weight: 700; font-size: 11px; padding: 3px 8px; border-radius: 8px;">
                        {q['category']}
                    </span>
                    <div style="font-size: 14px; font-weight: 700; color: #222222; margin-top: 8px; margin-bottom: 6px;">
                        {q['question']}
                    </div>
                    <div style="background-color: #F9FAFB; border: 1px solid #E5E8EB; border-radius: 8px; padding: 10px; font-size: 12px; color: #333D4B; line-height: 1.4; white-space: pre-line;">
                        {q['scenario']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            chosen = st.radio(
                label=f"tab3_quiz_radio_{q['id']}",
                options=range(len(q["options"])),
                format_func=lambda idx, opts=q["options"]: opts[idx],
                key=f"tab3_q_radio_{q['id']}",
                label_visibility="collapsed"
            )
            quiz_user_selections[q["id"]] = chosen
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        if st.button("퀴즈 제출 및 점수 확인하기 🎯", key="tab3_quiz_submit"):
            st.session_state["quiz_selections"] = quiz_user_selections
            st.session_state["quiz_submitted"] = True
            st.rerun()

    else:
        user_selections = st.session_state.get("quiz_selections", {})
        evaluation = evaluate_quiz(user_selections)

        diag_id = st.session_state.get("diagnosis_id")
        if diag_id:
            update_quiz_score(diag_id, evaluation["score"])

        # 퀴즈 점수 출력 카드
        st.markdown(f"""
            <div class="toss-card" style="text-align: center; background-color: #1E4FA1 !important; border: none;">
                <div style="font-size: 14px; color: #E8EEF9 !important; font-weight: 600;">나의 금융안전 퀴즈 점수</div>
                <div style="font-size: 42px; font-weight: 800; margin: 6px 0; color: #FFFFFF !important;">
                    {evaluation['score']}점
                </div>
                <div style="font-size: 13px; color: #E8EEF9 !important;">
                    총 {evaluation['total_count']}문항 중 {evaluation['correct_count']}문항 정답
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        for idx, item in enumerate(evaluation["details"], 1):
            q = item["question"]
            is_correct = item["is_correct"]
            badge = '<span style="color: #27AE60; font-weight: 700;">⭕ 정답입니다!</span>' if is_correct else '<span style="color: #E74C3C; font-weight: 700;">❌ 오답입니다.</span>'

            st.markdown(f"""
                <div class="toss-card" style="margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 12px; font-weight: 700; color: #6B7684;">문제 {idx} ({q['category']})</span>
                        <span style="font-size: 13px;">{badge}</span>
                    </div>
                    <div style="font-size: 14px; font-weight: 700; color: #222222; margin-bottom: 8px;">
                        {q['question']}
                    </div>
                    <div style="font-size: 12px; color: #4E5968; margin-bottom: 4px;">
                        <b>내가 선택한 답:</b> {q['options'][item['selected_idx']]}
                    </div>
                    <div style="font-size: 12px; color: #1E4FA1; margin-bottom: 8px;">
                        <b>정답:</b> {q['options'][q['answer_idx']]}
                    </div>
                    <div style="background-color: #E8EEF9; border-radius: 8px; padding: 8px 10px; font-size: 12px; color: #1E4FA1; line-height: 1.4;">
                        💡 <b>해설:</b> {q['explanation']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        st.markdown("""
            <div class="toss-card" style="background-color: #F2F4F6; border: none; text-align: center;">
                <div style="font-size: 14px; font-weight: 700; color: #191F28; margin-bottom: 4px;">
                    👨‍👩‍👧‍👦 소중한 가족에게 이 안내를 공유해 보세요
                </div>
                <div style="font-size: 12px; color: #4E5968; margin-bottom: 8px;">
                    버튼을 누르면 현재 서비스 링크가 클립보드에 바로 복사됩니다.
                </div>
            </div>
        """, unsafe_allow_html=True)

        components.html(COPY_BUTTON_HTML, height=65)

        if st.button("퀴즈 다시 풀기 🔄", key="tab3_quiz_reset"):
            st.session_state["quiz_submitted"] = False
            st.rerun()