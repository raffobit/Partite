#.venv\Scripts\activate
#python app.py
from flask import Flask, render_template, request, redirect
import mysql.connector # type: ignore

app = Flask(__name__)

# Configurazione della connessione al database
db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': '',  
    'database': 'calcio_db'
}

# Funzione per ottenere una connessione al database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    # Ottieni il nome della squadra dal parametro GET
    team = request.args.get('team')

    # Connessione al database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if team:
        # Query per filtrare le partite per squadra
        cursor.execute("""
            SELECT * FROM partite 
            WHERE team_a LIKE %s OR team_b LIKE %s
        """, (f"%{team}%", f"%{team}%"))
    else:
        # Query per ottenere tutte le partite
        cursor.execute("SELECT * FROM partite")

    matches = cursor.fetchall()

    # Chiude la connessione
    cursor.close()
    conn.close()

    return render_template('index.html', matches=matches, filter_team=team)

@app.route('/add', methods=['POST'])
def add_match():
    team_a = request.form['team_a']
    team_b = request.form['team_b']
    score_a = request.form['score_a']
    score_b = request.form['score_b']

    # Inserisce i dati nel database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO partite (team_a, team_b, score_a, score_b) VALUES (%s, %s, %s, %s)",
        (team_a, team_b, score_a, score_b)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:match_id>')
def delete_match(match_id):
    # Elimina la partita dal database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM partite WHERE id = %s", (match_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
