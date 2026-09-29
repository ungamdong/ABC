import streamlit as st
from styles import apply_toss_style
from database import init_db, save_diagnosis_result, update_quiz_score
from logic import (
    SURVEY_QUESTIONS, QUIZ_QUESTIONS,
    validate_answers, calculate_risks, get_educational_contents, evaluate_quiz
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
if "page" not in st.session_state:
    st.session_state["page"] = "main"

if "survey_answers" not in st.session_state:
    st.session_state["survey_answers"] = {}

if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False

# =============================================================
# [3단계] 메인 화면
# =============================================================
if st.session_state["page"] == "main":
    
    st.markdown("""
        <div style="text-align: center; padding: 20px 0 10px 0;">
            <div style="font-size: 44px; margin-bottom: 12px;">🛡️</div>
            <span style="background-color: #E8EEF9; color: #1E4FA1; font-weight: 700; font-size: 13px; padding: 6px 14px; border-radius: 20px;">
                금융소비자 보호 AI 서비스
            </span>
            <h1 style="color: #222222; font-size: 26px; font-weight: 700; margin-top: 14px; margin-bottom: 8px;">
                금융소비자 AI 안전코치
            </h1>
            <p style="color: #6B7684; font-size: 15px; margin: 0; word-break: keep-all;">
                금융사기 예방을 위한 맞춤형 안전 교육
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="toss-card">
            <div style="font-size: 16px; font-weight: 700; color: #222222; margin-bottom: 14px;">
                💡 안전코치와 함께하는 3단계
            </div>
            <div style="display: flex; align-items: flex-start; margin-bottom: 12px;">
                <span style="margin-right: 12px; font-size: 20px;">🎯</span>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #222222;">1. 취약도 진단</div>
                    <div style="font-size: 13px; color: #6B7684; margin-top: 2px;">7가지 설문으로 나의 금융사기 위험도 확인</div>
                </div>
            </div>
            <div style="display: flex; align-items: flex-start; margin-bottom: 12px;">
                <span style="margin-right: 12px; font-size: 20px;">📚</span>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #222222;">2. 맞춤형 솔루션</div>
                    <div style="font-size: 13px; color: #6B7684; margin-top: 2px;">보이스피싱·스미싱 등 유형별 대응법 학습</div>
                </div>
            </div>
            <div style="display: flex; align-items: flex-start;">
                <span style="margin-right: 12px; font-size: 20px;">🧩</span>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #222222;">3. 실전 퀴즈 점검</div>
                    <div style="font-size: 13px; color: #6B7684; margin-top: 2px;">실제 예시 문제로 점검하고 안전점수 획득</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="toss-card" style="background-color: #E8EEF9; border: none; padding: 16px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 14px; color: #1E4FA1; font-weight: 600;">⏱️ 진단 소요 시간</span>
                <span style="font-size: 15px; color: #1E4FA1; font-weight: 700;">약 3분</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    if st.button("진단 시작하기 🚀"):
        if "diagnosis_id" in st.session_state:
            del st.session_state["diagnosis_id"]
        st.session_state["quiz_submitted"] = False
        st.session_state["page"] = "survey"
        st.rerun()

    st.markdown("""
        <p style="text-align: center; color: #8B95A1; font-size: 12px; margin-top: 14px;">
            🔒 별도의 회원가입 없이 누구나 바로 이용할 수 있습니다.
        </p>
    """, unsafe_allow_html=True)

# =============================================================
# [4단계] 금융사기 취약도 진단 설문 화면
# =============================================================
elif st.session_state["page"] == "survey":
    
    st.markdown("""
        <div style="margin-bottom: 16px;">
            <span style="color: #1E4FA1; font-weight: 700; font-size: 14px;">STEP 1 / 3</span>
            <h2 style="color: #222222; font-size: 22px; font-weight: 700; margin-top: 4px; margin-bottom: 4px;">
                금융사기 취약도 진단
            </h2>
            <p style="color: #6B7684; font-size: 14px; margin: 0;">
                정확한 진단을 위해 아래 7가지 항목에 답변해 주세요.
            </p>
        </div>
    """, unsafe_allow_html=True)

    current_answers = {}

    for q in SURVEY_QUESTIONS:
        st.markdown(f"""
            <div class="toss-card" style="padding-bottom: 12px;">
                <div style="font-size: 16px; font-weight: 700; color: #222222; margin-bottom: 4px;">
                    {q['title']}
                </div>
                <div style="font-size: 13px; color: #6B7684; margin-bottom: 12px;">
                    {q['subtitle']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        selected_option = st.radio(
            label=f"{q['id']}_label",
            options=q["options"],
            key=f"radio_{q['id']}",
            label_visibility="collapsed"
        )
        current_answers[q["id"]] = selected_option
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    if st.button("결과 확인하기 (위험도 분석) ➔"):
        if validate_answers(current_answers):
            st.session_state["survey_answers"] = current_answers
            st.session_state["page"] = "result"
            st.rerun()
        else:
            st.warning("모든 질문에 답변해 주세요.")

    if st.button("← 메인 화면으로 돌아가기"):
        st.session_state["page"] = "main"
        st.rerun()

# =============================================================
# [5단계 & 6단계] 위험도 분석 결과 및 맞춤 교육 화면
# =============================================================
elif st.session_state["page"] == "result":
    
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
            <span style="color: #1E4FA1; font-weight: 700; font-size: 14px;">STEP 2 / 3</span>
            <h2 style="color: #222222; font-size: 22px; font-weight: 700; margin-top: 4px; margin-bottom: 4px;">
                📊 맞춤 위험도 분석 리포트
            </h2>
            <p style="color: #6B7684; font-size: 14px; margin: 0;">
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
            <div style="font-size: 16px; font-weight: 700; color: #222222; margin-bottom: 16px;">
                🛡️ 유형별 사기 위험도
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span style="font-size: 15px; font-weight: 600; color: #222222;">📞 보이스피싱</span>
                {get_risk_badge(risk_results['voice_phishing'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span style="font-size: 15px; font-weight: 600; color: #222222;">📱 스미싱 (문자사기)</span>
                {get_risk_badge(risk_results['smishing'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span style="font-size: 15px; font-weight: 600; color: #222222;">💬 메신저피싱</span>
                {get_risk_badge(risk_results['messenger_phishing'])}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 15px; font-weight: 600; color: #222222;">📈 투자사기 / 리딩방</span>
                {get_risk_badge(risk_results['investment'])}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="margin: 24px 0 12px 0;">
            <h3 style="color: #222222; font-size: 18px; font-weight: 700; margin: 0;">
                🎓 사용자 맞춤 예방 교육
            </h3>
        </div>
    """, unsafe_allow_html=True)

    for edu in edu_contents:
        st.markdown(f"""
            <div class="toss-card" style="border-left: 4px solid #1E4FA1;">
                <div style="font-size: 15px; font-weight: 700; color: #1E4FA1; margin-bottom: 6px;">
                    {edu['title']}
                </div>
                <div style="font-size: 13px; color: #4E5968; line-height: 1.5; word-break: keep-all;">
                    {edu['desc']}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if st.button("실전 점검 퀴즈 풀러 가기 (STEP 3) 🧩"):
        st.session_state["page"] = "quiz"
        st.rerun()

    if st.button("← 다시 진단하기"):
        if "diagnosis_id" in st.session_state:
            del st.session_state["diagnosis_id"]
        st.session_state["quiz_submitted"] = False
        st.session_state["page"] = "survey"
        st.rerun()

# =============================================================
# [7단계] 사례 기반 퀴즈 풀이 및 결과 화면
# =============================================================
elif st.session_state["page"] == "quiz":

    st.markdown("""
        <div style="margin-bottom: 16px;">
            <span style="color: #1E4FA1; font-weight: 700; font-size: 14px;">STEP 3 / 3</span>
            <h2 style="color: #222222; font-size: 22px; font-weight: 700; margin-top: 4px; margin-bottom: 4px;">
                🧩 사례 기반 실전 퀴즈
            </h2>
            <p style="color: #6B7684; font-size: 14px; margin: 0;">
                실제 금융사기 상황 예시를 읽고 올바른 대처법을 선택해 보세요.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 퀴즈 제출 전 화면
    if not st.session_state["quiz_submitted"]:
        quiz_user_selections = {}

        for q in QUIZ_QUESTIONS:
            st.markdown(f"""
                <div class="toss-card" style="margin-bottom: 12px;">
                    <span style="background-color: #E8EEF9; color: #1E4FA1; font-weight: 700; font-size: 12px; padding: 4px 10px; border-radius: 10px;">
                        {q['category']}
                    </span>
                    <div style="font-size: 15px; font-weight: 700; color: #222222; margin-top: 10px; margin-bottom: 8px;">
                        {q['question']}
                    </div>
                    <div style="background-color: #F9FAFB; border: 1px solid #E5E8EB; border-radius: 8px; padding: 12px; font-size: 13px; color: #333D4B; line-height: 1.5; white-space: pre-line;">
                        {q['scenario']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 선택지 라디오 버튼
            chosen = st.radio(
                label=f"quiz_radio_{q['id']}",
                options=range(len(q["options"])),
                format_func=lambda idx, opts=q["options"]: opts[idx],
                key=f"q_radio_{q['id']}",
                label_visibility="collapsed"
            )
            quiz_user_selections[q["id"]] = chosen
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("퀴즈 제출 및 점수 확인하기 🎯"):
            st.session_state["quiz_selections"] = quiz_user_selections
            st.session_state["quiz_submitted"] = True
            st.rerun()

    # 퀴즈 제출 후 결과 및 해설 화면
    else:
        user_selections = st.session_state.get("quiz_selections", {})
        evaluation = evaluate_quiz(user_selections)

        # DB에 퀴즈 점수 업데이트
        diag_id = st.session_state.get("diagnosis_id")
        if diag_id:
            update_quiz_score(diag_id, evaluation["score"])

        # 최종 점수 카드
        st.markdown(f"""
            <div class="toss-card" style="text-align: center; background-color: #1E4FA1; color: white;">
                <div style="font-size: 14px; opacity: 0.9;">나의 금융안전 퀴즈 점수</div>
                <div style="font-size: 42px; font-weight: 800; margin: 8px 0;">
                    {evaluation['score']}점
                </div>
                <div style="font-size: 13px; opacity: 0.9;">
                    총 {evaluation['total_count']}문항 중 {evaluation['correct_count']}문항 정답
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # 문항별 정/오답 및 상세 해설 카드
        for idx, item in enumerate(evaluation["details"], 1):
            q = item["question"]
            is_correct = item["is_correct"]
            
            badge = '<span style="color: #27AE60; font-weight: 700;">⭕ 정답입니다!</span>' if is_correct else '<span style="color: #E74C3C; font-weight: 700;">❌ 오답입니다.</span>'

            st.markdown(f"""
                <div class="toss-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 13px; font-weight: 700; color: #6B7684;">문제 {idx} ({q['category']})</span>
                        <span style="font-size: 14px;">{badge}</span>
                    </div>
                    <div style="font-size: 15px; font-weight: 700; color: #222222; margin-bottom: 10px;">
                        {q['question']}
                    </div>
                    <div style="font-size: 13px; color: #4E5968; margin-bottom: 6px;">
                        <b>내가 선택한 답:</b> {q['options'][item['selected_idx']]}
                    </div>
                    <div style="font-size: 13px; color: #1E4FA1; margin-bottom: 10px;">
                        <b>정답:</b> {q['options'][q['answer_idx']]}
                    </div>
                    <div style="background-color: #E8EEF9; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #1E4FA1; line-height: 1.5;">
                        💡 <b>해설:</b> {q['explanation']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("메인 화면으로 돌아가기 🏠"):
            st.session_state["page"] = "main"
            st.session_state["quiz_submitted"] = False
            st.rerun()