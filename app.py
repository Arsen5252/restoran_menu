from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'qwertyuhgfcdxsa')

def get_categories():
    conn = sqlite3.connect("resto.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories")
    data = cur.fetchall()
    conn.close()
    return data


def get_menu_items():
    conn = sqlite3.connect("resto.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT menu_items.*, categories.name as category 
        FROM menu_items 
        JOIN categories ON menu_items.category_id = categories.id
    """)
    data = cur.fetchall()
    conn.close()
    return data


def search_menu(query):
    conn = sqlite3.connect("resto.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT menu_items.*, categories.name as category
        FROM menu_items 
        JOIN categories ON menu_items.category_id = categories.id
        WHERE menu_items.title LIKE ?
    """, ('%' + query + '%',))
    data = cur.fetchall()
    conn.close()
    return data


def get_by_category(id):
    conn = sqlite3.connect("resto.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT menu_items.*, categories.name as category
        FROM menu_items 
        JOIN categories ON menu_items.category_id = categories.id
        WHERE category_id = ?
    """, (id,))
    data = cur.fetchall()
    conn.close()
    return data


@app.route("/")
def index():
    categories = get_categories()
    dishes = get_menu_items()
    return render_template("index.html", categories=categories, dishes=dishes)


@app.route("/search")
def search():
    categories = get_categories()
    query = request.args.get("search", "")
    dishes = search_menu(query)
    return render_template("index.html", categories=categories, dishes=dishes)


@app.route("/category/<int:id>")
def category_page(cat_id):
    categories = get_categories()
    dishes = get_by_category(cat_id)
    return render_template("index.html", categories=categories, dishes=dishes)


if __name__ == "__main__":
    app.run(debug=True)
