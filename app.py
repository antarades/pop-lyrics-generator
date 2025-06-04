import streamlit as st
import lyricsgenius
import os
import random
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()
GENIUS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
genius = lyricsgenius.Genius(GENIUS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])
genius.timeout = 15
st.set_page_config(page_title="🎤 Pop Artist Lyrics Viewer", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gloock&family=Poppins:wght@400;600&display=swap');
    
    body {
        background: linear-gradient(135deg, #ffe0f0 0%, #ffd1ec 100%) !important;
    }

    .title {
        font-family: 'Gloock', serif;
        font-size: 3em;
        color: #ff1694;
        text-align: center;
        margin-bottom: 0.5em;
    }

    .stRadio > div {
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }

    input[type="radio"] {
        display: none !important;
    }

    label[data-baseweb="radio"] {
        background-color: #ff5eaf;
        padding: 12px 24px;
        border-radius: 30px;
        margin: 5px;
        border: 2px solid #ffd6e7 ;
        transition: all 0.2s ease-in-out;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #000 !important;
        position: relative;
        box-shadow: none;
    }

    label[data-baseweb="radio"] > div:first-child {
        visibility: hidden;
        width: 0;
        height: 0;
        margin: 0;
        padding: 0;
    }

    
    label[data-baseweb="radio"]:hover {
        background-color: #ffc1dc;
        box-shadow: 0 0 8px #ffaad4;
        cursor: pointer;
    }
    div[data-baseweb="radio"] > div[aria-checked="true"]>label[data-baseweb="radio"] {
    background-color: #ffc1dc !important;
    color: #ffffff !important;
    border-color: #ff4fa2;
    box-shadow: 0 0 8px #ffaad4;
    transform: scale(1.02);
    font-weight: 700;
    transition: all 0.3s ease-in-out;
    }   

    div[data-baseweb="radio"][aria-checked="false"]:first-child:nth-last-child(n) label {
        opacity: 1;
        filter: none;
    }
     
    .stButton button {
    background-color: #ff1694;
    color: white;
    border: none;
    border-radius: 30px;
    padding: 0.6em 2em;
    font-weight: bold;
    transition: all 0.3s ease;
    font-family: 'Poppins', sans-serif;
    box-shadow: none;
}

.stButton button:hover {
    background-color: #ffc1dc;
    box-shadow: 0 0 8px #ffaad4;
    cursor: pointer;
    transform: scale(1.02);
}
    
    section[data-testid="stRadio"] > label {
    display: none !important;
            }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title"> Pop Lyrics Generator</div>', unsafe_allow_html=True)
st.subheader("Choose your favorite female artist ~")

artists = [
    "Taylor Swift", "Ariana Grande", "Billie Eilish", "Olivia Rodrigo",
    "Dua Lipa", "Gracie Abrams", "Selena Gomez", "Sabrina Carpenter",
    "Lana Del Rey", "Chappell Roan"]
artist = st.radio(" ", artists, horizontal=True)
st.markdown(f"""
<div style="text-align: center; margin-top: 1rem; font-family: 'Poppins', sans-serif; font-size: 1.2rem;">
  Selected: <b>💿 {artist}</b>
</div>
""", unsafe_allow_html=True)

# Cache artist lyrics
@st.cache_data(show_spinner=False, persist="disk")
def get_lyrics_for_artist(artist_name):
    try:
        result = genius.search_artist(artist_name, max_songs=30, sort="popularity", include_features=False)
    except Exception as e:
        st.error(f"❌ Genius API error: {e}")
        return []
    all_lines = []
    songs_data = []
    if result and result.songs:
        for song in result.songs:
            lyrics_lines = [line for line in song.lyrics.split('\n') if line.strip() and not line.startswith('[')]
            try:
                album_name = song._body["album"]["name"]
            except (KeyError, TypeError):
                album_name = "Unknown Album"

            for line in lyrics_lines:
                songs_data.append({
                    "lyric": line.strip(),
                    "song": song.title,
                    "album": album_name,
                    "art": song.song_art_image_url
                })
    return songs_data

if st.button("Generate Lyrics"):
    spinner = st.empty()
    spinner.markdown(f"""
    <div style="text-align: center; font-family: 'Poppins', sans-serif; font-size: 20px;">
        <div class="custom-spinner"></div>
        <p>Spinning the record for <b>{artist}</b>'s perfect lyrics ~ </p>
    </div>
    <style>
    .custom-spinner {{
        margin: 0 auto 20px auto;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 6px solid #ffaad4;
        border-top-color: #ff5eaf;
        animation: spin 1s linear infinite;
    }}
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    song_lines = get_lyrics_for_artist(artist)
    spinner.empty()

    if not song_lines:
        st.error("No lyrics found.")
    else:
        selected = random.choice(song_lines)
        st.markdown(f"""
        > *"{selected['lyric']}"*  
        — **{selected['song']}** | *{selected['album']}*
        """)
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="{selected['art']}" alt="Album Art" width="300">
            </div>
            """,
            unsafe_allow_html=True)
