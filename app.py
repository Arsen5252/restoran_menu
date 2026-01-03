from flask import Flask, render_template, request, session, redirect, url_for
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


def search_menu(search):
    conn = sqlite3.connect("resto.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM menu_items
        WHERE title LIKE ? COLLATE NOCASE
           OR description LIKE ? COLLATE NOCASE
    """, (f"%{search}%", f"%{search}%"))

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

def search_categories(search):
    conn = sqlite3.connect('resto.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM categories
                   WHERE title LIKE ?
                   ''', ["%"+search+"%"])
    data = cursor.fetchall()
    conn.close()
    return data


@app.route("/")
def index():
    categories = get_categories()
    dishes = get_menu_items()
    likes = session.get('likes', [])
    return render_template("index.html", categories=categories, dishes=dishes, likes=likes)


@app.route("/search")
def search():
    categories = get_categories()
    search = request.args.get("search", "")
    dishes = search_menu(search)
    return render_template("index.html", categories=categories, dishes=dishes)


@app.route("/category/<int:id>")
def category_page(id):
    categories = get_categories()
    dishes = get_by_category(id)
    return render_template("index.html", categories=categories, dishes=dishes)

@app.route("/like/<int:dish_id>",methods=["POST"])
def like_dish(dish_id):
    likes = session.get('likes', [])

    if dish_id in likes:
        likes.remove(dish_id)
    else:
        likes.append(dish_id)

    session['likes'] = likes 

    return redirect(request.referrer or url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
