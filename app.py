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

@app.route('/health_questions', methods=['GET', 'POST'])
def health_questions():
    if request.method == 'POST':
        score = 0
        answers = request.form
        for key, value in answers.items():
            score += int(value)
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

@app.route('/top')
def top():
    return render_template('top.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
