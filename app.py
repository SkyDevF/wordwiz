from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # เปลี่ยนเป็นคีย์ที่คุณต้องการ

# ฟังก์ชันสำหรับโหลดคำศัพท์จากไฟล์ JSON
def load_vocab():
    try:
        with open("vocab.json", "r", encoding="utf-8") as file:
            vocab = json.load(file)
            if isinstance(vocab, list):
                vocab = {item['word']: item['meaning'] for item in vocab}
            return vocab
    except FileNotFoundError:
        return {}

# ฟังก์ชันสำหรับบันทึกคะแนนสูงสุด
def save_high_score(score):
    try:
        with open("high_score.json", "r", encoding="utf-8") as file:
            high_score = json.load(file)
    except FileNotFoundError:
        high_score = 0

    if score > high_score:
        with open("high_score.json", "w", encoding="utf-8") as file:
            json.dump(score, file, ensure_ascii=False, indent=4)
        return score
    return high_score

# หน้าแรก - เมนู
@app.route('/')
def index():
    try:
        with open("high_score.json", "r", encoding="utf-8") as file:
            high_score = json.load(file)
    except FileNotFoundError:
        high_score = 0

    return render_template('index.html', high_score=high_score)

# เริ่มเล่นเกม
@app.route('/start_quiz', methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'POST':
        session['score'] = 0  # รีเซ็ตคะแนนเมื่อเริ่มเกมใหม่

    vocab = load_vocab()
    if not vocab:
        return "No vocabulary found. Please add some words to vocab.json."

    total_questions = len(vocab)
    score = session.get('score', 0)  # ดึงคะแนนจาก session

    # สุ่มคำถาม
    word, meaning = random.choice(list(vocab.items()))

    return render_template('quiz.html', word=word, meaning=meaning, score=score, total_questions=total_questions)

# ตรวจสอบคำตอบ
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    score = session.get('score', 0)  # ดึงคะแนนจาก session

    if answer.lower() == correct_answer.lower():
        score += 1  # เพิ่มคะแนน
    else:
        score = 0  # รีเซ็ตคะแนนเมื่อผู้ใช้ตอบผิด

    session['score'] = score
    high_score = save_high_score(score)  # บันทึกคะแนนสูงสุด
    session['high_score'] = high_score

    return redirect(url_for('start_quiz'))

if __name__ == '__main__':
    app.run(debug=True)
