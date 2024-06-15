import sqlite3

DATABASE = 'database.db'


def ppl_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS xixia (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    surname TEXT NOT NULL,
                                    rating TEXT NOT NULL,
                                    comment TEXT NOT NULL
                                )''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    ppl_db()
