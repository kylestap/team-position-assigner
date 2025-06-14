Team Position Assigner

  A Flask web app to manage a team roster, assign players to soccer positions based on preferences and gender, and visualize those positions on a simplified half-field.

🔧 Features

  ✅ Add, edit, and delete players
  
  ✅ Each player has:
    Name
    Gender (M/F)
    Three unique preferred positions
    
  ✅ Position assignment logic:
    Fills all 7 field positions: GK, LB, RB, LW, RW, CM, Striker
    Ensures at least 3 female and 3 male players on the field
    Automatically re-tries assignment with shuffled player order if any positions are unfilled
    
  ✅ Displays:
    A visual half-field layout with assigned players
    A bench list for remaining players

  ☁️ Accessible online at https://team-position-assigner.onrender.com

🧪 Running the App Locally

  ✅ Clone the repository:
  
    bash
    Copy
    Edit
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    
  ✅ Create a virtual environment and activate it:
  
    bash
    Copy
    Edit
    python -m venv venv
    source venv/bin/activate (On Windows: venv\Scripts\activate)
    
  ✅ Install dependencies:
  
    bash
    Copy
    Edit
    pip install -r requirements.txt
    
  ✅ Run the app:
  
    bash
    Copy
    Edit
    python app.py
    
  ✅ Visit the local app:
    Open your browser to the local address displayed on the command line (example http://127.0.0.1:5000)

  ☁ Or simply access app online at https://team-position-assigner.onrender.com

☁️ Uploading files to GitHub

  ✅ Navigate to your project directory (if you’re not already there):
  
    bash
    Copy
    Edit
    cd path/to/your/project
    Create the README.md file

    You can create and open it in your text editor, or use the command below to quickly create it:

    bash
    Copy
    Edit
    nano README.md
    Then paste the full content of the file.
    
    After pasting:

    Press CTRL + O to write the file
    Press Enter to confirm the filename
    Press CTRL + X to exit

✅ Stage the README file for commit:

    bash
    Copy
    Edit
    git add README.md

✅ Commit the change:

    bash
    Copy
    Edit
    git commit -m "Add project README with deployment and troubleshooting steps"
    Push the update to GitHub:

    bash
    Copy
    Edit
    git push

⚠️ Troubleshooting & Roadblocks
            Problem	                                            Cause	                                                          Solution
404 Errors for /add and /roster	                    Missing route functions in app.py	                              Re-added the @app.route('/add') and @app.route('/roster') views
gunicorn: command not found on Render	              gunicorn not listed in requirements.txt	                        Added gunicorn to requirements.txt
Empty field positions after assignment	            Some positions weren’t filled due to preference conflicts	      Modified logic to shuffle and retry until all positions were filled with gender rules met
Missing players table	                              SQLite database wasn’t initialized	                            Ensured init_db() runs at the start of app.py
Flask app failed to bind port on Render	            Default Flask uses localhost	                                  Render expects 0.0.0.0, but this is handled automatically by Gunicorn
Login issues when pushing to GitHub from terminal	  Git tried to use wrong browser (Edge)	                          Used Chrome to authenticate via token login or used GitHub CLI
Failed test_position_uniqueness unit test	          Player preferences had duplicate values	                        Updated test to generate unique position preferences

📁 Project Structure
bash
Copy
Edit
team-position-assigner/
│
├── app.py              # Flask application with routing and logic
├── team.db             # SQLite database file
├── requirements.txt    # Dependencies for Flask & Gunicorn
├── Procfile            # Required by Render for deployment
├── venv/               # Virtual environment (ignored in Git)
└── __pycache__/        # Python cache files

🔧 Future Improvements and Features

  ✅ User login system

  ✅ Save multiple game lineups

  ✅ Export lineups to CSV or PDF

  ✅ Dynamic drag-and-drop field layout

