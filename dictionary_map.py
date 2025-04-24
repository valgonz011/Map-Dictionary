import streamlit as st
import folium
from streamlit_folium import folium_static
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import base64

# --- Supported langs for gTTS (idiomas soportados para audio)
SUPPORTED_LANGS = ["de", "it", "hi", "bn", "fr", "es", "en", "ja"]

translator = Translator()

# --- Example countries with dialects
countries = [
    {
        "name": "Germany",
        "coordinates": [51.1657, 10.4515],
        "dialects": {
            "hochdeutsch": "de",
            "bavarian": "de"
        }
    },
    {
        "name": "India",
        "coordinates": [20.5937, 78.9629],
        "dialects": {
            "hindi": "hi",
            "bengali": "bn"
        }
    },
    {
        "name": "Italy",
        "coordinates": [41.8719, 12.5674],
        "dialects": {
            "standard italian": "it",
            "sicilian": "it"
        }
    },
    {
        "name": "France",
        "coordinates": [46.6034, 1.8883],
        "dialects": {
            "standard french": "fr"
        }
    },
    {
        "name": "Japan",
        "coordinates": [36.2048, 138.2529],
        "dialects": {
            "standard japanese": "ja"
        }
    }
]

# --- Translate word
def translate_word(word, lang_code):
    try:
        result = translator.translate(word, dest=lang_code)
        return result.text, result.pronunciation if result.pronunciation else ""
    except Exception as e:
        return f"[Error: {str(e)}]", ""

# --- Generate audio
def generate_audio(text, lang_code):
    if lang_code not in SUPPORTED_LANGS:
        return None
    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        return audio_file
    except Exception:
        return None

# --- Streamlit UI
st.set_page_config(layout="wide")
st.title("🌍 Interactive Language Map")

word = st.text_input("Enter a word to translate into multiple languages:")

# --- Create Map
world_map = folium.Map(location=[20, 0], zoom_start=2)

# --- Sidebar info panel
st.sidebar.title("🗺 Translations & Audio")

# --- Markers
if word:
    for country in countries:
        for dialect, lang_code in country["dialects"].items():
            translated, romanized = translate_word(word, lang_code)

            tooltip_text = f"{country['name']} - {dialect}: {translated}"

            folium.Marker(
                location=country["coordinates"],
                tooltip=tooltip_text,
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(world_map)

            st.sidebar.subheader(f"{country['name']} - {dialect}")
            st.sidebar.write(f"**Translated:** {translated}")
            if romanized:
                st.sidebar.write(f"**Romanized:** {romanized}")

            audio_file = generate_audio(translated, lang_code)
            if audio_file:
                st.sidebar.audio(audio_file, format="audio/mp3")

# --- Show map
folium_static(world_map)
