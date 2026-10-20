"""
logic.py
- 금융사기 취약도 진단을 위한 설문 문항 및 응답 처리 로직
- 위험도 산출 및 맞춤 교육 콘텐츠 추천 로직
- 사례 기반 퀴즈 데이터 및 채점 로직
- 최신 금융사기 주의보 데이터
- [신규] 생성형 AI(OpenAI) 기반 실시간 피싱 분석 함수
"""

import streamlit as st
from openai import OpenAI

# 1. 7가지 필수 설문 항목
SURVEY_QUESTIONS = [
    {
        "id": "age_group",
        "title": "1. 연령대를 선택해 주세요",
        "subtitle": "연령대에 따라 주로 발생하는 사기 유형이 다릅니다.",
        "options": ["20대 ~ 30대", "40대 ~ 50대", "60대 이상"]
    },
    {
        "id": "job",
        "title": "2. 현재 직업군을 선택해 주세요",
        "subtitle": "직업 및 경제 활동 형태별 맞춤 분석에 활용됩니다.",
        "options": ["직장인 / 자영업", "주부 / 무직", "은퇴자 / 연금수급자", "학생 / 기타"]
    },
    {
        "id": "financial_activity",
        "title": "3. 주요 금융활동 유형은 무엇인가요?",
        "subtitle": "자주 이용하시는 금융 서비스 유형을 선택해 주세요.",
        "options": ["예적금 및 원금보장형", "주식 / 코인 / 리딩방 등 투자", "대출 및 신용 거래", "금융 거래 거의 안 함"]
    },
    {
        "id": "digital_literacy",
        "title": "4. 스마트폰 및 디지털 활용 수준은 어느 정도인가요?",
        "subtitle": "문자 링크 클릭, 앱 설치 능숙도를 확인합니다.",
        "options": ["새로운 앱이나 웹사이트 이용이 매우 익숙함", "기본적인 카카오톡, 인터넷 정도만 사용", "스마트폰 조작이 서툴고 도움이 필요함"]
    },
    {
        "id": "investment_experience",
        "title": "5. 원금 고수익 투자 제안을 받아보신 적이 있나요?",
        "subtitle": "투자사기 및 리딩방 피싱 노출 가능성을 점검합니다.",
        "options": ["자주 받아보았거나 경험이 있음", "가끔 문자로 받아본 적 있음", "전혀 없음"]
    },
    {
        "id": "family_status",
        "title": "6. 현재 가구 구성 형태는 어떻게 되시나요?",
        "subtitle": "자녀 사칭 메신저피싱 취약도를 진단하는 항목입니다.",
        "options": ["독거 (1인 가구)", "배우자와 단둘이 거주", "자녀 또는 가족과 함께 거주"]
    },
    {
        "id": "mobile_banking",
        "title": "7. 모바일뱅킹(은행 앱)을 자주 사용하시나요?",
        "subtitle": "스미싱 악성 앱 설치 시 비대면 대출 위험도를 평가합니다.",
        "options": ["매일 또는 자주 사용함", "가끔 필요할 때만 사용함", "전혀 사용하지 않음"]
    }
]

# 2. 사례 기반 퀴즈 문항 데이터
QUIZ_QUESTIONS = [
    {
        "id": "q1",
        "category": "스미싱 (문자사기)",
        "scenario": "📨 [CJ대한통운] 택배 배송 주소 불명으로 미배송되었습니다. 아래 링크에서 주소를 확인 후 재요청하세요.\nhttp://bit.ly/3xX9Kz",
        "question": "Q1. 이러한 문자를 받았을 때 가장 안전하고 올바른 행동은 무엇일까요?",
        "options": [
            "1) 링크를 클릭하여 주소를 수정하고 재요청한다.",
            "2) 링크를 절대 누르지 않고 택배사 공식 앱이나 고객센터로 직접 확인한다.",
            "3) 문자 발신 번호로 전화하여 주소를 말해준다.",
            "4) 지인에게 이 문자를 전달하여 확인을 부탁한다."
        ],
        "answer_idx": 1,
        "explanation": "출처가 불분명한 문자 내 링크(URL)를 누르면 악성 앱이 설치되어 휴대폰의 개인정보와 금융정보가 유출될 수 있습니다. 반드시 공식 앱이나 전화로 직접 확인해야 합니다."
    },
    {
        "id": "q2",
        "category": "메신저피싱",
        "scenario": "💬 [카카오톡 메시지]\n'엄마! 나 핸드폰 액정이 깨져서 수리 맡겼어. 급하게 인증받아야 하니까 신분증 사진이랑 계좌 비밀번호 좀 보내줘!'",
        "question": "Q2. 자녀 이름으로 위와 같은 메시지가 왔을 때 어떻게 해야 할까요?",
        "options": [
            "1) 자녀가 급하다니 즉시 신분증 사진과 비밀번호를 보낸다.",
            "2) 카카오톡 메시지로 수리비 계좌번호를 알려달라고 한다.",
            "3) 메시지 응답을 멈추고, 반드시 자녀에게 직접 음성 통화를 걸어 본인 여부를 확인한다.",
            "4) 신용카드 앞뒷면 사진까지 추가로 전송해 준다."
        ],
        "answer_idx": 2,
        "explanation": "자녀나 지인을 사칭하는 메신저피싱의 전형적인 수법입니다. 신분증, 계좌/카드 비밀번호 요구 시 전송을 즉시 중단하고 전화로 직접 확인해야 합니다."
    },
    {
        "id": "q3",
        "category": "보이스피싱",
        "scenario": "📞 [전화 통화]\n'서울중앙지검 검사입니다. 귀하의 명의로 대포통장이 개설되어 범죄에 이용되었습니다. 자산 동결 조치를 피하려면 안내하는 안전계좌로 돈을 이체하세요.'",
        "question": "Q3. 검찰이나 금융감독원이라며 돈을 이체하라고 할 때 올바른 대처법은?",
        "options": [
            "1) 검찰이라니 놀라서 지정된 안전계좌로 돈을 바로 입금한다.",
            "2) 수사관의 소속과 이름을 메모한 후 안내에 따라 이체한다.",
            "3) 수사기관 및 금융기관은 어떠한 경우에도 '안전계좌 이체'를 요구하지 않으므로 즉시 전화를 끊고 112나 1332로 신고한다.",
            "4) 가족 몰래 은행 창구로 가서 대출을 받아 전달한다."
        ],
        "answer_idx": 2,
        "explanation": "검찰, 경찰, 금융감독원 등 국가기관은 절대로 전화로 '안전계좌 이체'나 현금 인출/전달을 요구하지 않습니다."
    }
]

# 3. 최신 금융사기 주의보 데이터
LATEST_NEWS = [
    {
        "tag": "🚨 금융감독원 주의보",
        "title": "모바일 부고장·청첩장 사칭 스미싱 기승",
        "desc": "부고나 결혼식 초대를 사칭한 문자 내 링크(URL) 클릭 시 악성 앱이 설치되어 휴대폰 소액결제 및 신분증 유출 피해가 발생하고 있습니다."
    },
    {
        "tag": "📢 금감원 핵심 안내",
        "title": "AI 딥보이스(목소리 합성) 자녀 사칭 주의",
        "desc": "실제 자녀의 목소리와 똑같이 음성을 합성하여 급전을 요구하더라도, 반드시 기존에 저장된 자녀 번호로 다시 전화해 본인 확인을 해야 합니다."
    }
]

def validate_answers(answers: dict) -> bool:
    if len(answers) < len(SURVEY_QUESTIONS):
        return False
    for q in SURVEY_QUESTIONS:
        if q["id"] not in answers or not answers[q["id"]]:
            return False
    return True

def calculate_risks(answers: dict) -> dict:
    age = answers.get("age_group", "")
    job = answers.get("job", "")
    fin = answers.get("financial_activity", "")
    digital = answers.get("digital_literacy", "")
    invest = answers.get("investment_experience", "")
    family = answers.get("family_status", "")
    banking = answers.get("mobile_banking", "")

    voice_score = 0
    if age == "60대 이상": voice_score += 2
    elif age == "40대 ~ 50대": voice_score += 1
    if "서툴고" in digital: voice_score += 2
    if job in ["주부 / 무직", "은퇴자 / 연금수급자"]: voice_score += 1

    voice_risk = "높음" if voice_score >= 3 else ("보통" if voice_score >= 1 else "낮음")

    smishing_score = 0
    if banking in ["매일 또는 자주 사용함", "가끔 필요할 때만 사용함"]: smishing_score += 1
    if "익숙함" not in digital: smishing_score += 2
    if invest == "가끔 문자로 받아본 적 있음": smishing_score += 1

    smishing_risk = "높음" if smishing_score >= 3 else ("보통" if smishing_score >= 1 else "낮음")

    messenger_score = 0
    if family in ["독거 (1인 가구)", "배우자와 단둘이 거주"]: messenger_score += 1
    if age == "60대 이상": messenger_score += 2
    if "서툴고" in digital: messenger_score += 1

    messenger_risk = "높음" if messenger_score >= 3 else ("보통" if messenger_score >= 1 else "낮음")

    invest_score = 0
    if invest == "자주 받아보았거나 경험이 있음": invest_score += 3
    elif invest == "가끔 문자로 받아본 적 있음": invest_score += 1
    if fin == "주식 / 코인 / 리딩방 등 투자": invest_score += 2

    invest_risk = "높음" if invest_score >= 3 else ("보통" if invest_score >= 1 else "낮음")

    return {
        "voice_phishing": voice_risk,
        "smishing": smishing_risk,
        "messenger_phishing": messenger_risk,
        "investment": invest_risk
    }

def get_educational_contents(risk_results: dict) -> list:
    contents = []
    if risk_results["voice_phishing"] in ["높음", "보통"]:
        contents.append({
            "type": "보이스피싱",
            "title": "🏛️ 기관사칭 및 딥보이스(AI 음성) 피싱 대응법",
            "desc": "검찰·금감원·은행이라며 '안전계좌 이체'를 요구하거나, 자녀 목소리로 급전을 요구하면 일단 끊고 해당 기관 및 자녀에게 직접 확인하세요!"
        })

    if risk_results["smishing"] in ["높음", "보통"]:
        contents.append({
            "type": "스미싱",
            "title": "📱 택배/부고 문자 속 링크(URL) 절대 클릭 금지",
            "desc": "출처가 불분명한 문자 속 링크를 클릭하면 악성 앱이 설치되어 휴대폰이 원격 제어됩니다. '시티즌코난' 앱을 통해 악성 앱을 점검하세요."
        })

    if risk_results["messenger_phishing"] in ["높음", "보통"]:
        contents.append({
            "type": "메신저피싱",
            "title": "💬 자녀 사칭 '액정 파손/상품권 구매' 카톡 대처법",
            "desc": "'엄마 핸드폰 고장 났어' 하며 신분증 사진이나 상품권 핀번호를 요구하면, 절대로 전송하지 말고 반드시 음성 통화로 본인 여부를 확인하세요."
        })

    if risk_results["investment"] in ["높음", "보통"]:
        contents.append({
            "type": "투자사기",
            "title": "📈 원금보장 고수익 리딩방 사기 피하는 법",
            "desc": "세상에 '원금이 보장되는 고수익 투자'는 없습니다. 가짜 거래소 앱 화면 및 리딩방 바람잡이에 속아 입금하지 않도록 각별히 주의하세요."
        })

    if not contents:
        contents.append({
            "type": "기초안전",
            "title": "🛡️ 금융소비자 필수 3대 안전 수칙",
            "desc": "1. 의심스러운 전화는 먼저 끊기 / 2. 문자 속 링크(URL) 누르지 않기 / 3. 비밀번호와 OTP 번호는 절대 타인에게 알려주지 않기"
        })

    return contents

def evaluate_quiz(user_selections: dict) -> dict:
    correct_count = 0
    details = []

    for q in QUIZ_QUESTIONS:
        selected_idx = user_selections.get(q["id"])
        is_correct = (selected_idx == q["answer_idx"])
        if is_correct:
            correct_count += 1
            
        details.append({
            "question": q,
            "selected_idx": selected_idx,
            "is_correct": is_correct
        })

    score = int((correct_count / len(QUIZ_QUESTIONS)) * 100)
    return {
        "score": score,
        "correct_count": correct_count,
        "total_count": len(QUIZ_QUESTIONS),
        "details": details
    }

def ask_ai_coach(user_message: str) -> str:
    """
    [생성형 AI 연동] 의심 문자/전화 내용을 GPT 모델로 분석
    """
    try:
        if "OPENAI_API_KEY" not in st.secrets:
            return "⚠️ OpenAI API 키가 설정되지 않았습니다. (.streamlit/secrets.toml 파일을 확인해 주세요)"

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "당신은 금융소비자를 보호하는 '금융사기 예방 전문 AI 안전코치'입니다. "
                        "사용자가 입력한 의심스러운 문자나 전화 내용을 분석하여 답변하세요:\n"
                        "1. 🚨 위험도 판정 (위험 / 주의 / 안전)\n"
                        "2. 🔍 주요 의심 사유 (2~3문장으로 간결하게 설명)\n"
                        "3. 🛡️ 지금 당장 취해야 할 행동 수칙 (2가지 안내)\n"
                        "쉬운 한국어와 다정한 말투를 사용하세요."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI 분석 중 에러가 발생했습니다: {str(e)}"