from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# List of all possible positions on the field
POSITIONS = ["GK", "LB", "RB", "LW", "RW", "CM", "Striker"]

# Basic inline CSS for styling the HTML templates
STYLE = '''
<style>
    body { font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }
    h1, h2 { color: #333; }
    a, input[type="submit"], button {
        display: inline-block; margin: 5px 5px 5px 0; padding: 10px 15px;
        background-color: #007BFF; color: white; border-radius: 5px; border: none; text-decoration: none;
    }
    a:hover, input[type="submit"]:hover, button:hover { background-color: #0056b3; }
    input, select { padding: 5px; margin: 5px 0; width: 100%; max-width: 400px; }
    form, ul {
        background-color: white; padding: 20px; border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); max-width: 500px;
    }
    .field-visual {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        margin-top: 20px;
        max-width: 800px;
    }
    .position-box {
        background-color: #e0e0e0;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        min-height: 60px;
    }
</style>
'''

# Database helper function to connect to SQLite
def get_db_connection():
    conn = sqlite3.connect('team.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Initialize the database schema if it doesn't exist
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

init_db()  # Initialize DB on app start

@app.route('/')
def index():
    # Homepage with navigation links
    return render_template_string(STYLE + '''
        <h1>Team Manager</h1>
        <a href="/add">Add Player</a>
        <a href="/roster">View Roster</a>
        <a href="/assign">Assign Positions</a>
    ''')

@app.route('/add', methods=['GET', 'POST'])
def add():
    # Add new player form
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        pos1 = request.form['preferred_pos1']
        pos2 = request.form['preferred_pos2']
        pos3 = request.form['preferred_pos3']
        # Ensure preferred positions are unique
        if len({pos1, pos2, pos3}) != 3:
            return "Position choices must be unique.", 400
        conn = get_db_connection()
        conn.execute('INSERT INTO players (name, gender, preferred_pos1, preferred_pos2, preferred_pos3) VALUES (?, ?, ?, ?, ?)',
                     (name, gender, pos1, pos2, pos3))
        conn.commit()
        conn.close()
        return redirect('/')

    # GET: show the form
    return render_template_string(STYLE + '''
        <h2>Add Player</h2>
        <form method="post">
            Name: <input name="name"><br>
            Gender:
            <select name="gender">
                <option value="M">M</option>
                <option value="F">F</option>
            </select><br>
            Preferred Position 1:
            <select name="preferred_pos1">
                {% for p in positions %}<option value="{{p}}">{{p}}</option>{% endfor %}
            </select><br>
            Preferred Position 2:
            <select name="preferred_pos2">
                {% for p in positions %}<option value="{{p}}">{{p}}</option>{% endfor %}
            </select><br>
            Preferred Position 3:
            <select name="preferred_pos3">
                {% for p in positions %}<option value="{{p}}">{{p}}</option>{% endfor %}
            </select><br>
            <input type="submit" value="Add Player">
        </form>
        <a href="/">Back</a>
    ''', positions=POSITIONS)

@app.route('/edit/<int:player_id>', methods=['GET', 'POST'])
def edit(player_id):
    # Edit player data
    conn = get_db_connection()
    player = conn.execute('SELECT * FROM players WHERE id = ?', (player_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        pos1 = request.form['preferred_pos1']
        pos2 = request.form['preferred_pos2']
        pos3 = request.form['preferred_pos3']
        if len({pos1, pos2, pos3}) != 3:
            return "Position choices must be unique.", 400
        conn.execute('UPDATE players SET name = ?, gender = ?, preferred_pos1 = ?, preferred_pos2 = ?, preferred_pos3 = ? WHERE id = ?',
                     (name, gender, pos1, pos2, pos3, player_id))
        conn.commit()
        conn.close()
        return redirect('/roster')
    conn.close()
    return render_template_string(STYLE + '''
        <h2>Edit Player</h2>
        <form method="post">
            Name: <input name="name" value="{{ player['name'] }}"><br>
            Gender:
            <select name="gender">
                <option value="M" {% if player['gender'] == 'M' %}selected{% endif %}>M</option>
                <option value="F" {% if player['gender'] == 'F' %}selected{% endif %}>F</option>
            </select><br>
            Preferred Position 1:
            <select name="preferred_pos1">
                {% for p in positions %}<option value="{{p}}" {% if player['preferred_pos1'] == p %}selected{% endif %}>{{p}}</option>{% endfor %}
            </select><br>
            Preferred Position 2:
            <select name="preferred_pos2">
                {% for p in positions %}<option value="{{p}}" {% if player['preferred_pos2'] == p %}selected{% endif %}>{{p}}</option>{% endfor %}
            </select><br>
            Preferred Position 3:
            <select name="preferred_pos3">
                {% for p in positions %}<option value="{{p}}" {% if player['preferred_pos3'] == p %}selected{% endif %}>{{p}}</option>{% endfor %}
            </select><br>
            <input type="submit" value="Save">
        </form>
        <a href="/roster">Back</a>
    ''', player=player, positions=POSITIONS)

@app.route('/delete/<int:player_id>')
def delete(player_id):
    # Delete a player from the roster
    conn = get_db_connection()
    conn.execute('DELETE FROM players WHERE id = ?', (player_id,))
    conn.commit()
    conn.close()
    return redirect('/roster')

@app.route('/roster')
def roster():
    # Show all registered players
    conn = get_db_connection()
    players = conn.execute('SELECT * FROM players').fetchall()
    conn.close()
    return render_template_string(STYLE + '''
        <h2>Roster</h2>
        <ul>
        {% for p in players %}
            <li>{{ p['name'] }} ({{ p['gender'] }}) - 
                <a href="/edit/{{ p['id'] }}">Edit</a> | 
                <a href="/delete/{{ p['id'] }}">Delete</a></li>
        {% endfor %}
        </ul>
        <a href="/">Back</a>
    ''', players=players)

@app.route('/assign', methods=['GET', 'POST'])
def assign():
    # Position assignment with gender and uniqueness constraints
    conn = get_db_connection()
    all_players = conn.execute('SELECT * FROM players').fetchall()
    conn.close()

    if request.method == 'POST':
        selected_ids = request.form.getlist('players')
        selected = [p for p in all_players if str(p['id']) in selected_ids]

        for _ in range(50):  # Max attempts to assign
            random.shuffle(selected)
            assigned = {}
            used_positions = set()
            males = [p for p in selected if p['gender'] == 'M']
            females = [p for p in selected if p['gender'] == 'F']
            team = []

            if len(males) < 3 or len(females) < 3:
                continue

            target_females = 3 if len(females) == 3 else random.choice([3, 4])
            target_males = 7 - target_females

            team = females[:target_females] + males[:target_males]
            if len(team) < 7:
                continue

            for priority in ['preferred_pos1', 'preferred_pos2', 'preferred_pos3']:
                for player in team:
                    if player['name'] not in assigned:
                        pos = player[priority]
                        if pos in POSITIONS and pos not in used_positions:
                            assigned[player['name']] = pos
                            used_positions.add(pos)

            if len(assigned) == 7:
                break

        # Format field layout
        bench = [p['name'] for p in selected if p['name'] not in assigned]
        field = {pos: '' for pos in POSITIONS}
        for name, pos in assigned.items():
            field[pos] = name

        return render_template_string(STYLE + '''
            <h2>Assigned Positions</h2>
            <div class="field-visual">
                <div class="position-box"><strong>GK</strong><br>{{ field['GK'] }}</div>
                <div class="position-box"><strong>LB</strong><br>{{ field['LB'] }}</div>
                <div class="position-box"><strong>RB</strong><br>{{ field['RB'] }}</div>
                <div class="position-box"><strong>CM</strong><br>{{ field['CM'] }}</div>
                <div class="position-box"><strong>Striker</strong><br>{{ field['Striker'] }}</div>
                <div class="position-box"><strong>LW</strong><br>{{ field['LW'] }}</div>
                <div class="position-box"><strong>RW</strong><br>{{ field['RW'] }}</div>
            </div>
            <h3>Bench</h3>
            <ul>{% for p in bench %}<li>{{ p }}</li>{% endfor %}</ul>
            <a href="/assign">Back</a> <a href="/">Home</a>
        ''', field=field, bench=bench)

    # Show selection form
    return render_template_string(STYLE + '''
        <h2>Select Players Present</h2>
        <form method="post">
        {% for p in all_players %}
            <label><input type="checkbox" name="players" value="{{ p['id'] }}"> {{ p['name'] }} ({{ p['gender'] }})</label><br>
        {% endfor %}
        <input type="submit" value="Assign">
        </form>
        <a href="/">Back</a>
    ''', all_players=all_players)

# Entry point when running the app locally
if __name__ == '__main__':
    init_db()  # Ensure DB is ready
    app.run(debug=True)  # Start Flask development server
