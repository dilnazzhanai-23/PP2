import psycopg2
import config

def get_connection():
    return psycopg2.connect(
        host=config.host,
        port=config.port,
        database=config.dbname,
        user=config.user,
        password=config.password
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_or_create_player(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE username = %s;", (username,))
    result = cursor.fetchone()
    if result:
        player_id = result[0]
    else:
        cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id;", (username,))
        player_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return player_id

def save_game_session(username, score, level):
    player_id = get_or_create_player(username)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached) 
        VALUES (%s, %s, %s);
    """, (player_id, score, level))
    conn.commit()
    cursor.close()
    conn.close()

def get_leaderboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.username, s.score, s.level_reached, s.played_at::date 
        FROM game_sessions s
        JOIN players p ON s.player_id = p.id
        ORDER BY s.score DESC LIMIT 10;
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_personal_best(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(s.score) FROM game_sessions s
        JOIN players p ON s.player_id = p.id
        WHERE p.username = %s;
    """, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result and result[0] else 0