import pickle
import streamlit as st
import requests
import yaml
import json
import os
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# ---------- Page Config ----------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --bg-deep: #0a0908;
        --bg-panel: rgba(255, 255, 255, 0.035);
        --gold: #cda349;
        --gold-bright: #f0c860;
        --crimson: #7a1f2b;
        --crimson-bright: #c8102e;
        --text-main: #f2ede1;
        --text-muted: #9a9184;
    }

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse 60% 40% at 50% 0%, rgba(205, 163, 73, 0.10) 0%, transparent 60%),
            radial-gradient(ellipse 80% 60% at 50% 100%, rgba(122, 31, 43, 0.14) 0%, transparent 65%),
            var(--bg-deep);
    }

    /* ---- Hero Section ---- */
    .hero {
        text-align: center;
        padding: 2.6rem 1rem 0.5rem 1rem;
    }
    .hero-eyebrow {
        font-family: 'Space Mono', monospace;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        font-size: 0.7rem;
        color: var(--gold);
        opacity: 0.85;
    }
    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4.4rem;
        letter-spacing: 0.06em;
        font-weight: 400;
        line-height: 1;
        margin: 0.35rem 0 0 0;
        background: linear-gradient(180deg, var(--gold-bright) 0%, var(--gold) 55%, var(--crimson-bright) 130%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 46px rgba(240, 200, 96, 0.18);
    }
    .hero-subtitle {
        color: var(--text-muted);
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* ---- Marquee bulb divider (signature element) ---- */
    .marquee-bulbs {
        display: flex;
        justify-content: center;
        gap: 14px;
        margin: 1.4rem 0 0.4rem 0;
    }
    .marquee-bulbs span {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--gold);
        box-shadow: 0 0 6px 1px rgba(240, 200, 96, 0.5);
        animation: bulb-glow 2.4s ease-in-out infinite;
    }
    .marquee-bulbs span:nth-child(odd) { animation-delay: 0s; }
    .marquee-bulbs span:nth-child(even) { animation-delay: 1.2s; }
    @keyframes bulb-glow {
        0%, 100% { opacity: 0.35; box-shadow: 0 0 4px 0px rgba(240, 200, 96, 0.25); }
        50% { opacity: 1; box-shadow: 0 0 10px 2px rgba(240, 200, 96, 0.65); }
    }

    /* ---- Subsection heading (Discover Movies, Find Your Next Watch) ---- */
    .subsection-wrap {
        text-align: center;
        margin: 1.6rem 0 1.1rem 0;
    }
    .subsection-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.3rem;
        letter-spacing: 0.04em;
        color: var(--gold-bright);
        margin-top: 0.15rem;
    }

    /* ---- Selectbox ---- */
    div[data-baseweb="select"] {
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: var(--bg-panel) !important;
        border-color: rgba(205, 163, 73, 0.35) !important;
    }

    /* ---- Search mode radio (Movie / Director / Actor) ---- */
    div[role="radiogroup"] {
        gap: 0.6rem;
        justify-content: center;
    }
    div[role="radiogroup"] label {
        padding: 0.45rem 1.1rem !important;
        border: 1px solid rgba(205, 163, 73, 0.3);
        border-radius: 999px;
        background: var(--bg-panel);
        transition: all 0.2s ease;
    }
    div[role="radiogroup"] label:hover {
        border-color: rgba(240, 200, 96, 0.6);
    }
    div[role="radiogroup"] label p {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em;
    }

    /* ---- Primary Button ---- */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, var(--crimson-bright), var(--crimson));
        color: var(--text-main);
        font-family: 'Bebas Neue', sans-serif;
        letter-spacing: 0.08em;
        font-weight: 400;
        font-size: 1.15rem;
        border: 1px solid rgba(240, 200, 96, 0.4);
        border-radius: 8px;
        padding: 0.65rem 1rem;
        box-shadow: 0 4px 18px rgba(200, 16, 46, 0.35);
        transition: all 0.25s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        border-color: var(--gold-bright);
        box-shadow: 0 8px 24px rgba(200, 16, 46, 0.5);
    }

    /* ---- Movie Card (ticket-stub styling) ---- */
    .movie-card {
        position: relative;
        background: var(--bg-panel);
        backdrop-filter: blur(6px);
        border: 1px solid rgba(205, 163, 73, 0.18);
        border-radius: 14px;
        padding: 12px 12px 14px 12px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        animation: fadeInUp 0.6s ease both;
    }
    .movie-card:hover {
        transform: translateY(-8px) scale(1.015);
        border-color: rgba(240, 200, 96, 0.55);
        box-shadow: 0 18px 36px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(240, 200, 96, 0.15);
    }
    .poster-wrap {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        /* Fixed 2:3 poster ratio so Discover cards and Recommended cards always match,
           regardless of the source image's actual dimensions. */
        aspect-ratio: 2 / 3;
        background: rgba(255,255,255,0.03);
    }
    .poster-wrap img {
        border-radius: 10px;
        transition: transform 0.4s ease;
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .movie-card:hover .poster-wrap img {
        transform: scale(1.05);
    }
    .rating-badge {
        position: absolute;
        top: 8px;
        right: 8px;
        padding: 3px 9px;
        border-radius: 4px;
        font-family: 'Space Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        color: #0a0908;
        background: var(--gold-bright);
        transform: rotate(-3deg);
        box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        z-index: 2;
    }
    /* perforated tear-line, like a ticket stub */
    .ticket-perf {
        height: 1px;
        margin: 10px -12px 0 -12px;
        background-image: repeating-linear-gradient(90deg, rgba(205,163,73,0.45) 0 6px, transparent 6px 12px);
    }
    .movie-title {
    font-weight: 600;
    font-size: 0.98rem;
    margin-top: 10px;
    color: var(--text-main);
    height: 48px;
    line-height: 1.3;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    }
    .movie-meta {
    font-family: 'Space Mono', monospace;
    color: var(--gold);
    opacity: 0.75;
    font-size: 0.75rem;
    margin-top: 2px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    }
    .similarity-score {
    font-family: 'Space Mono', monospace;
    color: var(--gold-bright);
    font-size: 0.75rem;
    font-weight: 700;
    margin-top: 6px;
    letter-spacing: 0.03em;
}
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(25px); }
        to { opacity: 1; transform: translateY(0); }
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14120f 0%, var(--bg-deep) 100%);
        border-right: 1px solid rgba(205, 163, 73, 0.12);
    }

    /* ---- Sidebar section headings ---- */
    section[data-testid="stSidebar"] h3 {
        color: var(--gold-bright) !important;
        font-family: 'Bebas Neue', sans-serif;
        letter-spacing: 0.04em;
    }

    /* ---- Section label (used above "Because you liked...") ---- */
    .section-eyebrow {
        font-family: 'Space Mono', monospace;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        font-size: 0.7rem;
        color: var(--gold);
        opacity: 0.8;
        margin-bottom: 0.2rem;
    }

    /* ---- Login form (streamlit-authenticator) ---- */
    div[data-testid="stForm"] {
        background: var(--bg-panel);
        border: 1px solid rgba(205, 163, 73, 0.28);
        border-radius: 16px;
        padding: 2rem 2rem 1.4rem 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    div[data-testid="stForm"] h1 {
        font-family: 'Bebas Neue', sans-serif;
        letter-spacing: 0.05em;
        color: var(--gold-bright);
    }
    div[data-testid="stForm"] label p {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted) !important;
    }
    div[data-testid="stForm"] input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(205, 163, 73, 0.3) !important;
        border-radius: 8px !important;
        color: var(--text-main) !important;
    }
    div[data-testid="stForm"] button {
        background: linear-gradient(90deg, var(--crimson-bright), var(--crimson)) !important;
        border: 1px solid rgba(240, 200, 96, 0.4) !important;
        border-radius: 8px !important;
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 0.08em !important;
        font-size: 1.05rem !important;
    }
    </style>
""", unsafe_allow_html=True)

## ---------- Authentication ----------

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

if st.session_state.get('authentication_status') is not True:

    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Now Showing</div>
        <div class="hero-title">Movie Recommender</div>
        <div class="hero-subtitle">
            Sign in to step up to the box office
        </div>
    </div>
    """, unsafe_allow_html=True)
    col_l, col_mid, col_r = st.columns([1, 1.1, 1])

    with col_mid:
        authenticator.login()

        if st.session_state.get('authentication_status') is False:
            st.error('Username/password is incorrect')

        elif st.session_state.get('authentication_status') is None:
            st.warning('Please enter your username and password')

    st.stop()

# ---------- Persistent Watchlist ----------

WATCHLIST_FILE = "watchlists.json"


def load_watchlists():
    if not os.path.exists(WATCHLIST_FILE):
        return {}

    try:
        with open(WATCHLIST_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_watchlists(watchlists):
    with open(WATCHLIST_FILE, "w", encoding="utf-8") as file:
        json.dump(watchlists, file, indent=4)


# ---------- Load Current User's Watchlist ----------

username = st.session_state.get("username")

watchlists = load_watchlists()

if username not in watchlists:
    watchlists[username] = []
    save_watchlists(watchlists)

st.session_state.watchlist = watchlists[username]


# ---------- If we reach here, the user is authenticated ----------

# ---------- Data Loading (cached) ----------
@st.cache_data
def load_data():
    movies = pickle.load(open('model/movies.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
    director_list = pickle.load(open('model/director_list.pkl', 'rb'))
    actor_list = pickle.load(open('model/actor_list.pkl', 'rb'))
    return movies, similarity, director_list, actor_list

movies, similarity, director_list, actor_list = load_data()

# ---------- Watchlist + Recommendation Session State ----------

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "recommended_movie_names" not in st.session_state:
    st.session_state.recommended_movie_names = []

if "recommended_details" not in st.session_state:
    st.session_state.recommended_details = []

if "recommended_similarities" not in st.session_state:
    st.session_state.recommended_similarities = []

if "recommended_selected" not in st.session_state:
    st.session_state.recommended_selected = ""

if "recommended_search_mode" not in st.session_state:
    st.session_state.recommended_search_mode = ""

if "eyebrow_label" not in st.session_state:
    st.session_state.eyebrow_label = ""

# ---------- Genre List ----------
genre_list = sorted(
    set(genre for genres in movies['genres'] for genre in genres)
)

genre_list.insert(0, "All Genres")

# ---------- Poster + Details Fetching (cached + safer) ----------


# ---------- Poster + Details Fetching (cached + safer) ----------

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:
        response = requests.get(
            url,
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US"
            },
            timeout=5
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException:
        data = {}

    # Fetch poster
    poster_path = data.get("poster_path")

    full_path = (
        f"https://image.tmdb.org/t/p/w500{poster_path}"
        if poster_path
        else "https://via.placeholder.com/500x750?text=No+Image"
    )

    # Fetch genres (maximum 2)
    genres = ", ".join(
        [g["name"] for g in data.get("genres", [])][:2]
    ) or "—"

    # Return all movie details together
    return {
        "poster": full_path,
        "overview": data.get("overview") or "No overview available.",
        "rating": data.get("vote_average", 0) or 0,
        "release_date": (data.get("release_date") or "N/A")[:4],
        "genres": genres
    }


def add_to_watchlist(movie_title):
    if movie_title not in st.session_state.watchlist:
        st.session_state.watchlist.append(movie_title)

        watchlists = load_watchlists()
        username = st.session_state.get("username")

        watchlists[username] = st.session_state.watchlist
        save_watchlists(watchlists)

        st.toast(f"❤️ {movie_title} added to your watchlist!")
    else:
        st.toast(f"⚠️ {movie_title} is already in your watchlist.")


def remove_from_watchlist(movie_title):
    if movie_title in st.session_state.watchlist:
        st.session_state.watchlist.remove(movie_title)

    watchlists = load_watchlists()
    username = st.session_state.get("username")

    watchlists[username] = st.session_state.watchlist
    save_watchlists(watchlists)

# ---------- Hero ----------
st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Now Showing</div>
        <div class="hero-title">Movie Recommender</div>
        <div class="hero-subtitle">Discover your next favorite movie in seconds</div>
    </div>
    <div class="marquee-bulbs">
        <span></span><span></span><span></span><span></span><span></span>
    </div>
""", unsafe_allow_html=True)

def rating_color(score):
    if score >= 7.5:
        return "#2ecc71"   # green
    elif score >= 5.5:
        return "#f1c40f"   # yellow
    elif score > 0:
        return "#e74c3c"   # red
    else:
        return "#7f8c8d"   # gray for N/A

# ---------- Random Movies ----------

st.markdown("""
    <div class="subsection-wrap">
        <div class="section-eyebrow">Curated For You</div>
        <div class="subsection-title">🎲 Discover Movies</div>
    </div>
""", unsafe_allow_html=True)

if "random_movies" not in st.session_state:
    st.session_state.random_movies = movies.sample(n=10)

random_movies = st.session_state.random_movies

cols = st.columns(5)

for i, (_, row) in enumerate(random_movies.iterrows()):
    with cols[i % 5]:
        info = fetch_movie_details(row['movie_id'])
        color = rating_color(info["rating"])

        # Same .movie-card / .poster-wrap markup as the recommendation cards below,
        # so poster size and framing stay identical across both sections.
        st.markdown(f"""
            <div class="movie-card">
                <div class="poster-wrap">
                    <span class="rating-badge" style="background:{color};">
                        ⭐ {info['rating']:.1f}
                    </span>
                    <img src="{info['poster']}" style="width:100%;">
                </div>
                <div class="ticket-perf"></div>
                <div class="movie-title">{row['title']}</div>
                <div class="movie-meta">{info['release_date']} · {info['genres']}</div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("📖 Overview"):
            st.write(info["overview"])

        if row['title'] in st.session_state.watchlist:
            st.button(
                "❤️ In Watchlist",
                key=f"random_watchlisted_{row['movie_id']}",
                disabled=True
            )
        else:
            st.button(
                "❤️ Add to Watchlist",
                key=f"random_add_watchlist_{row['movie_id']}",
                on_click=add_to_watchlist,
                args=(row['title'],)
            )

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    names, details, similarities = [], [], []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        info = fetch_movie_details(movie_id)

        names.append(movies.iloc[i[0]].title)
        details.append(info)

        # Store cosine similarity
        similarities.append(float(i[1]))

    return names, details, similarities

# ---------- Why This Movie ----------

def explain_recommendation(selected_movie, recommended_movie):

    selected_row = movies[movies['title'] == selected_movie].iloc[0]
    recommended_row = movies[movies['title'] == recommended_movie].iloc[0]

    explanation = {}

    # Similar Genres
    selected_genres = set(selected_row['genres'])
    recommended_genres = set(recommended_row['genres'])

    explanation['genres'] = list(
        selected_genres.intersection(recommended_genres)
    )

    # Similar Keywords
    selected_keywords = set(selected_row['keywords'])
    recommended_keywords = set(recommended_row['keywords'])

    explanation['keywords'] = list(
        selected_keywords.intersection(recommended_keywords)
    )

    # Similar Cast
    selected_cast = set(selected_row['cast_list'])
    recommended_cast = set(recommended_row['cast_list'])

    explanation['cast'] = list(
        selected_cast.intersection(recommended_cast)
    )

    # Same Director
    if selected_row['director'] == recommended_row['director']:
        explanation['director'] = selected_row['director']
    else:
        explanation['director'] = None

    return explanation

def recommend_by_director(director_name, genre="All Genres", n=5):
    df = movies[movies['director'] == director_name]

    if genre != "All Genres":
        df = df[df['genres'].apply(lambda genres: genre in genres)]

    df = df.sort_values(
        by='vote_average',
        ascending=False
    ).head(n)

    names, details = [], []

    for _, row in df.iterrows():
        info = fetch_movie_details(row['movie_id'])
        names.append(row['title'])
        details.append(info)

    return names, details

def recommend_by_actor(actor_name, genre="All Genres", n=5):
    df = movies[
        movies['cast_list'].apply(lambda cast: actor_name in cast)
    ]

    if genre != "All Genres":
        df = df[df['genres'].apply(lambda genres: genre in genres)]

    df = df.sort_values(
        by='vote_average',
        ascending=False
    ).head(n)

    names, details = [], []

    for _, row in df.iterrows():
        info = fetch_movie_details(row['movie_id'])
        names.append(row['title'])
        details.append(info)

    return names, details

# ---------- Top Rated Movies by Genre ----------

def get_top_rated_by_genre(genre):

    # Filter movies belonging to the selected genre
    genre_movies = movies[
        movies['genres'].apply(lambda genres: genre in genres)
    ].copy()

    # Remove movies that don't have a valid rating
    genre_movies = genre_movies[
        genre_movies['vote_average'].notna() &
        (genre_movies['vote_average'] > 0)
    ]

    # Sort by highest rating
    genre_movies = genre_movies.sort_values(
        by='vote_average',
        ascending=False
    )

    # Get top 5
    genre_movies = genre_movies.head(5)

    names = []
    details = []

    for _, row in genre_movies.iterrows():

        info = fetch_movie_details(row['movie_id'])

        # IMPORTANT:
        # Use the dataset rating that we sorted by
        info["rating"] = float(row["vote_average"])

        names.append(row['title'])
        details.append(info)

    return names, details
# ---------- Sidebar ----------

with st.sidebar:
    st.markdown("### 🎬 Movie Recommender")
    st.write(f"Welcome, **{st.session_state.get('name')}** 👋")
    authenticator.logout('Logout', 'sidebar')

    st.markdown("---")

    st.write(
        "A content-based movie recommender powered by machine learning and TMDB data."
    )

    st.markdown("---")

    st.markdown("**How it works:**")
    st.write(
        "Pick a movie → the model finds titles with similar features → "
        "you get 5 tailored picks. Pick a director or actor → "
        "we pull their top-rated titles instead."
    )

    st.markdown("---")

    # ---------- Watchlist ----------

    st.markdown("### ❤️ My Watchlist")

    if st.session_state.watchlist:
        for i, movie in enumerate(st.session_state.watchlist):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"🎬 {movie}")

            with col2:
                st.button(
                    "❌",
                    key=f"remove_watchlist_{i}",
                    on_click=remove_from_watchlist,
                    args=(movie,)
                )
    else:
        st.caption("Your watchlist is empty.")

    st.markdown("---")

    st.caption("Built with Streamlit + TMDB API")

# ---------- Top Rated by Genre ----------

st.markdown("""
    <div class="subsection-wrap">
        <div class="section-eyebrow">Genre Spotlight</div>
        <div class="subsection-title">🏆 Top Rated by Genre</div>
    </div>
""", unsafe_allow_html=True)

genre_col_l, genre_col_mid, genre_col_r = st.columns([1, 2, 1])

with genre_col_mid:

    selected_top_genre = st.selectbox(
        "Select a genre",
        genre_list,
        key="top_rated_genre"
    )

    show_genre_movies = st.button(
        "🏆 Show Top Rated Movies",
        key="show_genre_movies"
    )

# ---------- Display Genre Movies ----------

if show_genre_movies:

    with st.spinner("Finding the top-rated movies..."):

        genre_movie_names, genre_movie_details = get_top_rated_by_genre(
            selected_top_genre
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-eyebrow">Highest Rated</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"#### 🏆 Top Rated {selected_top_genre} Movies"
    )

    st.write("")

    cols = st.columns(5)

    for i, (name, info) in enumerate(
        zip(genre_movie_names, genre_movie_details)
    ):

        with cols[i % 5]:

            color = rating_color(info["rating"])

            st.html(f"""
            <div class="movie-card">

                <div class="poster-wrap">

                    <span class="rating-badge"
                          style="background:{color};">
                        ⭐ {info['rating']:.1f}
                    </span>

                    <img src="{info['poster']}"
                         style="width:100%;">

                </div>

                <div class="ticket-perf"></div>

                <div class="movie-title">
                    {name}
                </div>

                <div class="movie-meta">
                    {info['release_date']} · {info['genres']}
                </div>

            </div>
            """)

            with st.expander("📖 Overview"):
                st.write(info["overview"])

# ---------- Search Mode + Selection ----------
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

st.markdown("""
    <div class="subsection-wrap">
        <div class="section-eyebrow">Start Exploring</div>
        <div class="subsection-title">🔍 Find Your Next Watch</div>
    </div>
""", unsafe_allow_html=True)

col_l, col_mid, col_r = st.columns([1, 2, 1])
with col_mid:
    search_mode = st.radio(
        "Search by",
        ["🎬 Movie", "🎥 Director", "🎭 Actor"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if search_mode == "🎬 Movie":
        selected = st.selectbox(
            "Type or select a movie you love",
            movies['title'].values
        )
    elif search_mode == "🎥 Director":
        selected = st.selectbox(
            "Type or select a director",
            director_list
        )
        selected_genre = st.selectbox(
            "Filter by Genre",
            genre_list
        )
    else:
        selected = st.selectbox(
            "Type or select an actor",
            actor_list
        )
        selected_genre = st.selectbox(
            "Filter by Genre",
            genre_list
        )

    show_button = st.button('✨ Show Recommendations')

# ---------- Recommendations ----------

if show_button:
    with st.spinner('Curating your recommendations...'):

        if search_mode == "🎬 Movie":
            recommended_movie_names, recommended_details, recommended_similarities = recommend(selected)
            eyebrow_label = "Because you liked"

        elif search_mode == "🎥 Director":
            recommended_movie_names, recommended_details = recommend_by_director(
                selected, selected_genre
            )
            recommended_similarities = []
            eyebrow_label = "Top-rated films directed by"

        else:
            recommended_movie_names, recommended_details = recommend_by_actor(
                selected, selected_genre
            )
            recommended_similarities = []
            eyebrow_label = "Top-rated films starring"

        # Save recommendation results in Session State
        st.session_state.recommended_movie_names = recommended_movie_names
        st.session_state.recommended_details = recommended_details
        st.session_state.recommended_similarities = recommended_similarities
        st.session_state.recommended_selected = selected
        st.session_state.recommended_search_mode = search_mode
        st.session_state.eyebrow_label = eyebrow_label


# ---------- Display Saved Recommendations ----------

recommended_movie_names = st.session_state.recommended_movie_names
recommended_details = st.session_state.recommended_details
recommended_similarities = st.session_state.recommended_similarities
display_selected = st.session_state.recommended_selected
display_search_mode = st.session_state.recommended_search_mode
display_eyebrow_label = st.session_state.eyebrow_label


if recommended_movie_names:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f'<div class="section-eyebrow">{display_eyebrow_label}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "#### 🎟️ *{}*".format(display_selected)
    )

    st.write("")

    cols = st.columns(5)

    for i, (col, name, info) in enumerate(
            zip(cols, recommended_movie_names, recommended_details)
    ):
        with col:
            color = rating_color(info["rating"])

            # Similarity is shown ONLY for Movie search
            similarity_html = ""

            if display_search_mode == "🎬 Movie":
                similarity_score = recommended_similarities[i]

                similarity_html = f"""
                    <div class="similarity-score">
                        🎯 Similarity: {similarity_score:.2f}
                    </div>
                """

            st.html(f"""
            <div class="movie-card">
                <div class="poster-wrap">
                    <span class="rating-badge" style="background:{color};">
                        ⭐ {info['rating']:.1f}
                    </span>

                    <img src="{info['poster']}" style="width:100%;">
                </div>

                <div class="ticket-perf"></div>

                <div class="movie-title">{name}</div>

                <div class="movie-meta">
                    {info['release_date']} · {info['genres']}
                </div>

                {similarity_html}

            </div>
            """)

            with st.expander("📖 Overview"):
                st.write(info["overview"])

            if search_mode == "🎬 Movie":

                with st.expander("💡 Why this movie?"):

                    explanation = explain_recommendation(
                        selected,
                        name
                    )

                    if explanation["genres"]:
                        st.write(
                            "🎭 **Similar genres:** "
                            + ", ".join(explanation["genres"])
                        )

                    if explanation["keywords"]:
                        st.write(
                            "🔑 **Similar keywords:** "
                            + ", ".join(explanation["keywords"][:5])
                        )

                    if explanation["cast"]:
                        st.write(
                            "👤 **Similar cast:** "
                            + ", ".join(explanation["cast"][:3])
                        )

                    if explanation["director"]:
                        st.write(
                            "🎥 **Same director:** "
                            + explanation["director"]
                        )

                    if not any([
                        explanation["genres"],
                        explanation["keywords"],
                        explanation["cast"],
                        explanation["director"]
                    ]):
                        st.write(
                            "Similar content features were found in the recommendation."
                        )

            if name in st.session_state.watchlist:
                st.button(
                    "❤️ In Watchlist",
                    key=f"watchlisted_{i}_{name}",
                    disabled=True
                )
            else:
                st.button(
                    "❤️ Add to Watchlist",
                    key=f"add_watchlist_{i}_{name}",
                    on_click=add_to_watchlist,
                    args=(name,)
                )