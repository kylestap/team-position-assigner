from flask import Flask, request, render_template_string, redirect
import sqlite3
import os
import random

app = Flask(__name__)

# Define the 7 field positions
POSITIONS = ["GK", "LB", "RB", "LW", "RW", "CM", "Striker"]

# Basic CSS styling for the HTML pages
STYLE = '''
<style>
    body { font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }
    h1, h2 { color: #333; }
    a, input[type="submit"], button {
        display: inline-block; margin: 5px 5px 5px 0; padding: 10px 15px;
        background-color: #007BFF; color: white; border-radius: 5px;
        border: none; text-decoration: none;
    }
    a:hover, input[type="submit"]:hover, button:hover { background-color: #0056b3; }
    input, select {
        padding: 5px; margin: 5px 0; width: 100%; max-width: 400px;
    }
    form, ul {
        background-color: white; padding: 20px;
        border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        max-width: 500px;
    }
    .field-visual {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;
        margin-top: 20px; max-width: 800px;
    }
    .position-box {
        background-color: #e0e0e0; padding: 10px;
        border-radius: 8px; text-align: center; min-height: 60px;
    }
</style>
'''

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('team.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database and table
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            preferred_pos1 TEXT,
            preferred_pos2 TEXT,
            preferred_pos3 TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template_string(STYLE + '''
        <h1>Team Manager</h1>
        <a href="/add">Add Player</a>
        <a href="/roster">View Roster</a>
        <a href="/assign">Assign Positions</a>
    ''')

# Add player form
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        pos1 = request.form['preferred_pos1']
        pos2 = request.form['preferred_pos2']
        pos3 = request.form['preferred_pos3']

        if len({pos1, pos2, pos3}) < 3:
            return "All preferred positions must be unique."

        conn = get_db_connection()
        conn.execute('INSERT INTO players (name, gender, preferred_pos1, preferred_pos2, preferred_pos3) VALUES (?, ?, ?, ?, ?)',
                     (name, gender, pos1, pos2, pos3))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template_string(STYLE + '''
        <h2>Add Player</h2>
        <form method="post">
            Name: <input type="text" name="name" required><br>
            Gender:
            <select name="gender">
                <option value="M">Male</option>
                <option value="F">Female</option>
            </select><br>
            Preferred Position 1: <select name="preferred_pos1">{% for p in positions %}<option value="{{p}}">{{p}}</option>{% endfor %}</select><br>
            Preferred Position 2: <select name="preferred_pos2">{% for p in positions %}<option value="{{p}}">{{p}}</option>{% endfor %}</select><br>
            Preferred Position 3: <select name="preferred_pos3">{% for p in positions %}<option value="{{p}}">{{p}}</option>{% endfor %}</select><br>
            <input type="submit" value="Add Player">
        </form>
        <a href="/">Back</a>
    ''', positions=POSITIONS)

# View roster
@app.route('/roster')
def roster():
    conn = get_db_connection()
    players = conn.execute('SELECT * FROM players').fetchall()
    conn.close()
    return render_template_string(STYLE + '''
        <h2>Roster</h2>
        <ul>
        {% for player in players %}
            <li>{{ player['name'] }} ({{ player['gender'] }}) - {{ player['preferred_pos1'] }}, {{ player['preferred_pos2'] }}, {{ player['preferred_pos3'] }}
                <a href="/edit/{{ player['id'] }}">Edit</a>
                <a href="/delete/{{ player['id'] }}">Delete</a>
            </li>
        {% endfor %}
        </ul>
        <a href="/">Back</a>
    ''', players=players)

# Edit player
@app.route('/edit/<int:player_id>', methods=['GET', 'POST'])
def edit(player_id):
    conn = get_db_connection()
    player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        pos1 = request.form['preferred_pos1']
        pos2 = request.form['preferred_pos2']
        pos3 = request.form['preferred_pos3']

        if len({pos1, pos2, pos3}) < 3:
            return "All preferred positions must be unique."

        conn.execute('UPDATE players SET name=?, gender=?, preferred_pos1=?, preferred_pos2=?, preferred_pos3=? WHERE id=?',
                     (name, gender, pos1, pos2, pos3, player_id))
        conn.commit()
        conn.close()
        return redirect('/roster')

    conn.close()
    return render_template_string(STYLE + '''
        <h2>Edit Player</h2>
        <form method="post">
            Name: <input type="text" name="name" value="{{ player['name'] }}" required><br>
            Gender:
            <select name="gender">
                <option value="M" {% if player['gender'] == 'M' %}selected{% endif %}>Male</option>
                <option value="F" {% if player['gender'] == 'F' %}selected{% endif %}>Female</option>
            </select><br>
            Preferred Position 1: <select name="preferred_pos1">{% for p in positions %}<option value="{{p}}" {% if player['preferred_pos1']==p %}selected{% endif %}>{{p}}</option>{% endfor %}</select><br>
            Preferred Position 2: <select name="preferred_pos2">{% for p in positions %}<option value="{{p}}" {% if player['preferred_pos2']==p %}selected{% endif %}>{{p}}</option>{% endfor %}</select><br>
            Preferred Position 3: <select name="preferred_pos3">{% for p in positions %}<option value="{{p}}" {% if player['preferred_pos3']==p %}selected{% endif %}>{{p}}</option>{% endfor %}</select><br>
            <input type="submit" value="Update Player">
        </form>
        <a href="/roster">Back</a>
    ''', player=player, positions=POSITIONS)

# Delete player
@app.route('/delete/<int:player_id>')
def delete(player_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM players WHERE id = ?', (player_id,))
    conn.commit()
    conn.close()
    return redirect('/roster')

# Assign positions
@app.route('/assign', methods=['GET', 'POST'])
def assign():
    conn = get_db_connection()
    all_players = conn.execute('SELECT * FROM players').fetchall()

    if request.method == 'POST':
        selected_ids = request.form.getlist('players')
        present_players = [p for p in all_players if str(p['id']) in selected_ids]

        # Retry logic to ensure all positions filled and gender balance
        for _ in range(100):  # Prevent infinite loops
            random.shuffle(present_players)
            assigned = {}
            bench = []
            used_positions = set()
            male_count = 0
            female_count = 0

            for priority in ['preferred_pos1', 'preferred_pos2', 'preferred_pos3']:
                for player in present_players:
                    if player['name'] not in assigned:
                        pos = player[priority]
                        if pos in POSITIONS and pos not in used_positions:
                            assigned[player['name']] = pos
                            used_positions.add(pos)
                            if player['gender'] == 'M':
                                male_count += 1
                            else:
                                female_count += 1

            for player in present_players:
                if player['name'] not in assigned:
                    bench.append(player['name'])

            if len(used_positions) == len(POSITIONS) and 3 <= female_count <= 4 and 3 <= male_count <= 4:
                break
        else:
            return "Could not assign positions while satisfying constraints."

        conn.close()
        field = {pos: '' for pos in POSITIONS}
        for player, pos in assigned.items():
            field[pos] = player

        return render_template_string(STYLE + '''
            <h2>Position Assignments</h2>
            <div class="field-visual">
                <div class="position-box"><strong>GK</strong><br>{{ field['GK'] }}</div>
                <div class="position-box"><strong>LB</strong><br>{{ field['LB'] }}</div>
                <div class="position-box"><strong>RB</strong><br>{{ field['RB'] }}</div>
                <div class="position-box"><strong>CM</strong><br>{{ field['CM'] }}</div>
                <div class="position-box"><strong>Striker</strong><br>{{ field['Striker'] }}</div>
                <div class="position-box"><strong>LW</strong><br>{{ field['LW'] }}</div>
                <div class="position-box"><strong>RW</strong><br>{{ field['RW'] }}</div>
            </div>
            <h3>Bench Players</h3>
            <ul>
            {% for p in bench %}
                <li>{{ p }}</li>
            {% endfor %}
            </ul>
            <a href="/assign">Back</a>
            <a href="/">Home</a>
        ''', field=field, bench=bench)

    return render_template_string(STYLE + '''
        <h2>Assign Positions</h2>
        <form method="post">
            <p>Select players present:</p>
            {% for player in all_players %}
                <label><input type="checkbox" name="players" value="{{ player['id'] }}"> {{ player['name'] }}</label><br>
            {% endfor %}
            <input type="submit" value="Assign">
        </form>
        <a href="/">Back</a>
    ''', all_players=all_players)

# Run app locally or on Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
