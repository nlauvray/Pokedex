from flask import Flask, render_template, request
import fight

app = Flask(__name__)
app.config['DEBUG'] = True

if __name__ == "__main__":
    app.run()