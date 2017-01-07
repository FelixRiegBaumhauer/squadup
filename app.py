from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'seizetheday'

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/main')
def main():
    return render_template("main.html")
    
if __name__ == '__main__':
    app.run(debug=True)
    app.run('0.0.0.0', port=8000)
