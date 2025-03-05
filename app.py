from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ユーザー情報の仮データ
users = {
    "user1": {"password": "password1", "first_login": True},
    "user2": {"password": "password2", "first_login": True},
    "123": {"password": "123", "first_login": True},
    "456": {"password": "456", "first_login": True}
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username]['password'] == password:
        session['username'] = username
        if users[username]['first_login']:
            return redirect(url_for('health_questions'))
        else:
            return redirect(url_for('top'))
    else:
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = {"password": password, "first_login": True}
            session['username'] = username
            return redirect(url_for('health_questions'))
        else:
            return "ユーザー名は既に存在します"
    return render_template('register.html')

@app.route('/health_questions', methods=['GET', 'POST'])
def health_questions():
    if request.method == 'POST':
        score = 0
        answers = request.form
        for key, value in answers.items():
            score += int(value)
            users[session['username']][key] = int(value)
        users[session['username']]['first_login'] = False
        if score >= 11:
            group = "健康"
            return redirect(url_for('healthy'))
        elif 7 <= score < 11:
            group = "体調問題ない"
            return redirect(url_for('no_problem'))
        else:
            group = "注意が必要"
            return redirect(url_for('attention_needed'))
    return render_template('health_questions.html')

@app.route('/healthy')
def healthy():
    return render_template('result.html', group="健康")

@app.route('/no_problem')
def no_problem():
    return render_template('result2.html', group="体調問題ない")

@app.route('/attention_needed')
def attention_needed():
    return render_template('result3.html', group="注意が必要")

@app.route('/user_specific_advice')
def user_specific_advice():
    username = session.get('username')
    if not username:
        return redirect(url_for('home'))

    # 仮のデータとして、スコアが0だった質問に対するアドバイスを生成
    advice_list = []
    if users[username].get('q1') == 0:
        advice_list.append("最近よく眠れていないようです。規則正しい生活を心がけ、リラックスする時間を持ちましょう。")
    if users[username].get('q2') == 0:
        advice_list.append("食欲がないようです。バランスの取れた食事を心がけ、無理せず少しずつ食べるようにしましょう。")
    if users[username].get('q3') == 0:
        advice_list.append("バランスの取れた食事ができていないようです。栄養バランスを考えた食事を心がけましょう。")
    if users[username].get('q4') == 0:
        advice_list.append("最近運動していないようです。無理のない範囲で軽い運動を取り入れましょう。")
    if users[username].get('q5') == 0:
        advice_list.append("ストレスを感じているようです。リラックスする時間を持ち、ストレス解消法を見つけましょう。")
    if users[username].get('q6') == 0:
        advice_list.append("最近体調に変化があるようです。無理せず体を休め、必要なら医師の診察を受けましょう。")
    if users[username].get('q7') == 0:
        advice_list.append("社会的な交流が少ないようです。友人や家族との時間を大切にし、コミュニケーションを取りましょう。")

    return render_template('user_specific_advice.html', advice_list=advice_list)

@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/yoga')
def yoga():
    return render_template('yoga.html')

@app.route('/personal_health')
def personal_health():
    username = session.get('username', 'ゲスト')
    if username == 'ゲスト' or username not in users:
        health_score = 75  # デフォルト値
    else:
        # 質問の回答から健康スコアを計算
        total_score = 0
        questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7']
        answered_questions = 0
        
        for q in questions:
            if q in users[username]:
                total_score += users[username][q]
                answered_questions += 1
        
        if answered_questions > 0:
            # 質問の回答から100点満点のスコアに変換
            # 各質問は0-2点で、質問は7つあるので最大14点
            # (実際のスコア / 満点) * 100 で100点満点に換算
            health_score = int((total_score / (answered_questions * 2)) * 100)
        else:
            health_score = 75  # 回答がない場合のデフォルト値
    
    user = {
        'username': username,
        'health_score': health_score
    }
    
    context = {
        'user': user,
        'lifestyle_advice': generate_lifestyle_advice(health_score)
    }
    
    return render_template('personal_health.html', **context)

def generate_lifestyle_advice(health_score):
    if health_score >= 90:
        return '現在の健康的な生活習慣を維持しましょう！'
    elif health_score >= 75:
        return '概ね良好です。運動習慣をさらに増やすことをお勧めします。'
    elif health_score >= 60:
        return '生活習慣の見直しで、より健康的な毎日を目指しましょう。'
    else:
        return '専門家に相談し、健康管理のアドバイスを受けることをお勧めします。'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
