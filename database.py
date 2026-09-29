"""
database.py
- SQLite DB 생성 및 진단/퀴즈 결과 저장 관리
"""
import sqlite3

DB_NAME = "financial_coach.db"

def init_db():
    """데이터베이스 및 테이블 초기화"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age_group TEXT,
            job TEXT,
            voice_risk TEXT,
            smishing_risk TEXT,
            messenger_risk TEXT,
            investment_risk TEXT,
            quiz_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_diagnosis_result(age_group, job, voice, smishing, messenger, investment, quiz_score=0):
    """진단 결과 1차 저장"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO diagnosis_results (age_group, job, voice_risk, smishing_risk, messenger_risk, investment_risk, quiz_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (age_group, job, voice, smishing, messenger, investment, quiz_score))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def update_quiz_score(diagnosis_id: int, quiz_score: int):
    """[7단계] 퀴즈 완료 시 최종 점수 업데이트"""
    if not diagnosis_id:
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE diagnosis_results 
        SET quiz_score = ? 
        WHERE id = ?
    """, (quiz_score, diagnosis_id))
    conn.commit()
    conn.close()