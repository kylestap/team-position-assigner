Project Progress Update: Team Position Assigner App

  What I’ve Completed
    I have made significant progress on my Flask web application designed to manage soccer team rosters and assign player positions fairly based on preferences and gender balance. 
    Specifically, I have:
      Set up the project environment using Flask and SQLite.
      Built a full CRUD interface (Create, Read, Update, Delete) for managing player data, including name, three preferred positions, and gender (M/F).
      Implemented a robust assignment algorithm that:
        Prioritizes position preferences.
        Ensures no duplicate assignments.
        Enforces gender balance (3–4 M and 3–4 F on the field).
        Retries with a shuffled roster if positions are left unfilled.
      Created a visual layout using CSS Grid to display players on the field.
      Successfully wrote and passed tests for roster logic and edge cases.
      Deployed the app live using Render with GitHub integration.
      Created a professional PLAN.md,  README.md, and project outline.

What I’m Currently Working On
  Final testing of the deployed app in a live environment to ensure it behaves identically to the local version.
  Evaluating possible UI/UX improvements for responsiveness or accessibility.
  Gathering feedback

What I’m Enjoying About the Project
  I’ve really enjoyed designing the assignment logic — it’s a fun blend of fairness, strategy, and technical problem-solving.
  I’m also enjoying the full-stack nature of the project: I get to work with Flask routes, backend logic, database structure, and frontend presentation.  
  Although I am only used to working with Python and some HTML CSS, I have enjoyed the practice of porting my work into other formats using LLMs such as Copilot and OpenAI.
  Seeing the live deployment working and shareable via a URL was very rewarding.

Lines of Code Written
  As of now, I have written approximately 200 lines of code and used LLMs to produce over 500 lines of code, considering the following:
    app.py (core logic, routes, styling)
    Embedded HTML templates (using render_template_string)
    Supporting files like README.md, requirements.txt, and the Procfile.

A Specific Success
  I successfully resolved a gender balance logic challenge: 
    I added a retry system that automatically shuffles the roster and reruns the assignment logic until all positions are filled with exactly 3–4 males and 3–4 females, which is a key functional and ethical goal of the app. 
    This ensures fairness and reliability — and it works smoothly even with varying roster sizes.

Challenges I Overcame 
  Unfilled Positions During Assignment
    The app couldn't fill all 7 field positions due to conflicts in player preferences or gender balance limits. This would previously result in an incomplete team. 
    To fix this, I implemented a retry loop with a maximum of 50 attempts. Each time the app fails to create a complete team, it:
      Randomly shuffles the selected player list.
      Re-runs the assignment logic.
      Stops once all positions are filled or 50 attempts are reached.
    This approach ensures that the app is resilient even when the roster is suboptimal, while avoiding infinite loops.

  Deployment on Render (Missing Dependencies & Port Binding)
    When deploying to Render, I encountered a failure due to the gunicorn package not being included in requirements.txt, and the app binding only to localhost. 
    I resolved this by:
      Adding gunicorn to requirements.txt
      Updating app.run() to bind to 0.0.0.0 and use the PORT environment variable from Render.

  Expanding from Pure Python to Full-Stack Web Development
    My original version of the project was purely written in Python — no interface, no database, and no web features. One of the biggest challenges was translating that logic into a full-stack web app. 
    I used ChatGPT to:
      Build Flask routes around my logic.
      Generate the HTML forms and field layout.
      Design a clean CSS layout using a responsive grid.
      Create and interact with a SQLite database.
      Prepare deployment tools like Procfile and requirements.txt.

    This transition taught me a lot about web development structure and how different layers of a full-stack app work together.
