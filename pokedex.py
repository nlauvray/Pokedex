from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def home_redirect():
    return render_template('home.html')

@app.route('/fight')
def fight():
    return render_template('fight.html')

if __name__ == "__main__":
    app.run(debug=True)