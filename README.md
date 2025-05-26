# 🎬 LateFee_App

LateFee is a Flask-based movie collection web application where users can manage their personal libraries of films. Each movie entry includes details from the OMDb API, and there's even an AI-powered "Eye of the Duck" film analysis feature using OpenAI's GPT.

---

## 🚀 Features

- 📋 Manage users and their personal movie collections
- 🔍 Search and add movies with data from [OMDb API](https://www.omdbapi.com/)
- 🧠 AI-generated "Eye of the Duck" scene analysis using OpenAI
- ✏️ Update and delete movie entries
- 🌐 Friendly UI built with Flask templates
- 🪵 Rotating log system and robust error handling

---

## 🛠️ Tech Stack

- **Python 3**
- **Flask**
- **SQLAlchemy** with SQLite
- **Jinja2 Templates**
- **OMDb API**
- **OpenAI API**
- **dotenv** for environment management
- **RotatingFileHandler** for logging

---

## 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/stillpeyman/LateFee_App.git
cd LateFee_App
````

2. **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
````

3. **Install Dependencies**
```bash
pip install -r requirements.txt
````

4. **Set Up Environment Variables**

> Create a .env file in the root directory

```bash
SECRET_KEY=your_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
````

**5. Initialize the Database**

Create and run helper script `init_db.py`: 

```bash
from datamanager.models import db
from frontend_app import app

with app.app_context():
     db.create_all()
     exit()
````

## ▶️ Running the App

```bash
python3 app.py
````

Then open your browser to:
http://localhost:5000

## 📁 Project Structure

```
LateFee_App/
│
├── api/
│   ├── __init__.py
│   └── omdb_api.py
│
├── datamanager/
│   ├── __init__.py
│   ├── data_manager_interface.py
│   ├── models.py
│   └── sqlite_data_manager.py
│
├── templates/
│   ├── index.html
│   ├── users.html
│   ├── add_user.html
│   ├── user_movies.html
│   ├── add_movie.html
│   ├── update_movie.html
│   ├── eye_of_the_duck.html
│   └── error.html
│
├── static/
│   └── style.css
│
├── logs/
│   └── latefee_movies.log
│
├── data/
│   ├── latefee_movies.db
│   └── response.json
│
├── frontend_app.py
├── init_db.py
├── .env
├── requirements.txt
└── README.md
````

## ✨ Example Usage

1. Add a User – Navigate to /add_user, enter a name.

2. Add Movies – Visit the user's page and add movies via the OMDb API.

3. View AI Scene Analysis – Click "Eye of the Duck" on a movie to see GPT's take.

4. Edit/Delete – Update or delete movies from the user's library.

## 🧠 AI Integration
The Eye of the Duck feature uses OpenAI's GPT (via openai Python SDK) to generate interpretive analysis of a film's most essential scene.

## 🐞 Logging and Errors
All activity is logged to logs/latefee_movies.log. The app has handlers for:

- 404 – Resource not found

- 405 – Method not allowed

- 500 – Unhandled exceptions

## 🔐 Security Tips

- Always keep your .env secrets private.

- Use a strong SECRET_KEY in production.

- Avoid debug=True when deploying.

## 📜 License
This project is licensed under the MIT License.

## 🙌 Acknowledgments

- OMDb API for movie data

- OpenAI for GPT-based AI analysis

- Flask for the web framework

## 🧪 Tests and Future Enhancements
Planned improvements:

- Unit tests for routes and data manager

- Frontend enhancements (e.g., Bootstrap or Tailwind styling)

- Pagination for large movie collections

- User authentication

## 🔗 GitHub
Clone or star the repo:
👉 https://github.com/stillpeyman/LateFee_App













