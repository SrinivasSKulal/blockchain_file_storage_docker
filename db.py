import psycopg2, os

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    # Create blockchain table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS blockchain (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        filename TEXT NOT NULL,
        filehash TEXT NOT NULL,
        prev_hash TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create users table - Fixed version
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


def register_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cur.close()
    conn.close()


def verify_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None


def add_block(username, filename, filehash, prev_hash):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO blockchain (username, filename, filehash, prev_hash) VALUES (%s, %s, %s, %s)",
        (username, filename, filehash, prev_hash)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_chain_db(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blockchain WHERE username=%s ORDER BY id", (username,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    chain = []
    for row in rows:
        chain.append({
            "id": row[0],
            "username": row[1],
            "filename": row[2],
            "filehash": row[3],
            "prev_hash": row[4],
            "timestamp": str(row[5])
        })
    return chain
