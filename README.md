# 🎬 Movie Recommender System

A content-based movie recommendation web application built with **Python, Machine Learning, and Streamlit**. Discover movies based on your preferences and explore recommendations with movie posters, ratings, genres, and descriptions.

## 📌 Project Overview

The Movie Recommender System helps users discover movies similar to the ones they already enjoy.

It uses **Content-Based Filtering** to calculate similarities between movies based on their metadata, including genres, keywords, cast, and director.

The application provides an interactive interface where users can log in, search movies by genre, actor, or director, find similar movies, and manage their personal watchlists.

## ✨ Features

- **Movie Recommendations:** Get recommendations based on movie similarity.
- **Content-Based Filtering:** Uses CountVectorizer and Cosine Similarity to identify similar movies.
- **Variable Search:** Search movies by **genre**, **actor**, or **director**.
- **Similar Movie Finder:** Pick any movie and find the most similar titles using cosine similarity.
- **Movie Search:** Search through a collection of approximately 4,800 movies.
- **Movie Posters:** Fetches movie posters dynamically using the TMDB API.
- **Movie Information:** Displays movie descriptions, ratings, release years, and genres.
- **User Authentication:** Login system with password hashing using Streamlit Authenticator, giving each user a personalized recommender experience.
- **Personal Watchlists:** Add movies to your watchlist and remove them at any time.
- **Interactive Interface:** Built using Streamlit for a simple and user-friendly experience.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | CountVectorizer and Cosine Similarity |
| Streamlit | Web application interface |
| Streamlit Authenticator | User authentication |
| TMDB API | Movie posters and movie information |
| Pickle | Saving and loading trained model artifacts |
| Git & GitHub | Version control |

## 🧠 How the Recommendation System Works

The recommendation engine follows these steps:

1. **Data Collection:** Uses movie metadata such as genres, keywords, cast, and director.
2. **Feature Engineering:** Combines relevant movie attributes into a single text-based feature.
3. **Text Vectorization:** Applies CountVectorizer to convert movie descriptions and metadata into numerical vectors.
4. **Similarity Calculation:** Uses Cosine Similarity to measure how similar movies are.
5. **Recommendation:** Finds the movies with the highest similarity scores and recommends them to the user.

### Recommendation Pipeline

```text
Movie Dataset
      |
      v
Data Preprocessing
      |
      v
Feature Engineering
      |
      v
CountVectorizer
      |
      v
Cosine Similarity
      |
      v
Similarity Matrix
      |
      v
Movie Recommendations
```

## 📸 Screenshots

Screenshots of the application:

### Login Page
Users authenticate before accessing the recommender.

![Login Page](https://raw.githubusercontent.com/nischal-027/Movie-Recommender-System/main/Screenshots/login-page.png)

### Home Page
The main landing page after logging in.

![Home Page](https://raw.githubusercontent.com/nischal-027/Movie-Recommender-System/main/Screenshots/home-page.png)

### Sidebar
Navigation and search options.

![Sidebar](https://raw.githubusercontent.com/nischal-027/Movie-Recommender-System/main/Screenshots/sidebar.png)

### Movie by Genre
Browse and discover movies by genre.

![Movie by Genre](https://raw.githubusercontent.com/nischal-027/Movie-Recommender-System/main/Screenshots/movie-by-genre.png)

### Movie by Actor, Director and Similarity
Search by actor or director, and find movies similar to one you like.

![Movie by Actor, Director and Similarity](https://raw.githubusercontent.com/nischal-027/Movie-Recommender-System/main/Screenshots/movie-by-actor-director-similarity.png)

## 📂 Project Structure

```text
MovieRecommender/
│
├── model/
│   ├── actor_list.pkl
│   ├── director_list.pkl
│   ├── movies.pkl
│   └── similarity.pkl
│
├── Screenshots/
│   ├── login-page.png
│   ├── home-page.png
│   ├── sidebar.png
│   ├── movie-by-genre.png
│   └── movie-by-actor-director-similarity.png
│
├── app.py
├── main.py
├── config.example.yaml
├── requirements.txt
├── pyproject.toml
├── setup.sh
├── Procfile
├── .gitignore
├── .gitattributes
└── README.md
```

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/nischal-027/Movie-Recommender-System.git
```

Navigate to the project directory:

```bash
cd Movie-Recommender-System
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
TMDB_API_KEY=your_tmdb_api_key
```

Obtain an API key from [The Movie Database (TMDB)](https://www.themoviedb.org/).

Keep your `.env` file private. Never upload your API key to GitHub.

### 5. Configure User Authentication

Copy `config.example.yaml` to `config.yaml`:

```powershell
Copy-Item config.example.yaml config.yaml
```

Update `config.yaml` with your own usernames, bcrypt password hashes, and authentication configuration.

Do not upload `config.yaml` to GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

The application should open in your browser at:

```text
http://localhost:8501
```

## 🔐 Security

- API credentials are stored in environment variables.
- Authentication passwords are stored as bcrypt hashes.
- Sensitive configuration files are excluded through `.gitignore`.

## 🚀 Future Improvements

- Add collaborative filtering for more personalized recommendations.
- Integrate a hybrid recommendation approach.
- Improve recommendation ranking using additional movie features.
- Add user ratings and feedback to improve recommendations.
- Deploy the application for public access.

## 👨‍💻 Author

**Nischal Acharya**

Computer Engineering Student | AI/ML Enthusiast

- GitHub: [@nischal-027](https://github.com/nischal-027)
- Project Repository: [Movie Recommender System](https://github.com/nischal-027/Movie-Recommender-System)

---

⭐ If you find this project interesting, consider giving the repository a star!
