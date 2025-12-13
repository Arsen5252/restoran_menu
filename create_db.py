import sqlite3

conn = sqlite3.connect('resto.db')
cursor = conn.cursor()

# Створення таблиці категорій
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Створення таблиці страв
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
''')

# Додавання тестових даних
cursor.execute("INSERT INTO categories (name) VALUES ('Гарячі страви')")
cursor.execute("INSERT INTO categories (name) VALUES ('Десерти')")
cursor.execute("INSERT INTO categories (name) VALUES ('Напої')")

cursor.execute(
    "INSERT INTO menu_items (title, price, description, image, category_id) VALUES (?, ?, ?, ?, ?)",
    ("Борщ український", 120, "Традиційний борщ зі сметаною", "images/borsh.jpg", 1)
)

cursor.execute(
    "INSERT INTO menu_items (title, price, description, image, category_id) VALUES (?, ?, ?, ?, ?)",
    ("Чізкейк", 95, "Ніжний сирний десерт", "images/cheesecake.jpg", 2)
)

cursor.execute(
    "INSERT INTO menu_items (title, price, description, image, category_id) VALUES (?, ?, ?, ?, ?)",
    ("Капучино", 65, "Кава з пінкою", "images/cappuccino.jpg", 3)
)

conn.commit()
conn.close()

print("Базу даних успішно створено!")
