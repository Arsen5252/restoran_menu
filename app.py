from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)  # Створюємо веб–додаток Flask


@app.route('/')
def index():    
    return render_template('index.html')  # Відображаємо головну сторінку


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)