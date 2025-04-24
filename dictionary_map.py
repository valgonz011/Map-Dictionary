import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
from math import radians, cos, sin, sqrt, atan2

st.set_page_config(layout="wide")
translator = Translator()

# Datos de ejemplo
countries = [
    {
        "name": "Germany 🇩🇪",
        "coordinates": [51.1657, 10.4515],
        "language": {"hochdeutsch": "de"},
        "dialects": {"bayern": "de", "berlin": "de"}
    },
    {
        "name": "India 🇮🇳",
        "coordinates": [20.5937, 78.9629],
        "language": {"hindi": "hi"},
        "dialects": {"bengali": "bn", "tamil": "ta"}
    },
    {
        "name": "Italy 🇮🇹",
        "coordinates": [41.8719, 12.5674],
        "language": {"italiano": "it"},
        "dialects": {"napolitano": "nap", "siciliano": "scn"}
    },
    {
        "name": "France 🇫🇷",
        "coordinates": [46.603354, 1.888334],
        "language": {"français": "fr"},
        "dialects": {}
    },
    {
        "name": "Japan 🇯🇵",
        "coordinates": [36.2048, 138.2529],
        "language": {"nihongo": "ja"},
        "dialects": {}
    },
]

def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def find_nearest_country(click_coords):
    distances = [haversine(click_coords, c["coordinates"]) for c in countries]
    return countries[distances.index(min(distances))]

def translate_and_speak(word, lang_code):
    try:
        translated = translator.translate(word, dest=lang_code)
        tts = gTTS(text=translated.text, lang=lang_code)
        audio = BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)
        romanized = translated.pronunciation or ""
        return translated.text, romanized, audio
    except Exception as e:
        return f"[ERROR] {str(e)}", "", None

st.sidebar.title("🗺️ Language Info")
word = st.text_input("Enter a word to translate into multiple languages:")

map_center = [20, 0]
world_map = folium.Map(location=map_center, zoom_start=2)

# Resultado del clic
click_data = st_folium(world_map, height=500, width=1000)

# Mostrar resultado si hay palabra y clic
if word and click_data and click_data.get("last_clicked"):
    latlng = click_data["last_clicked"]
    coords = [latlng["lat"], latlng["lng"]]
    selected = find_nearest_country(coords)

    st.sidebar.markdown(f"### 🌍 {selected['name']}")
    for label, code in selected["language"].items():
        trans, roman, audio = translate_and_speak(word, code)
        st.sidebar.markdown(f"**Idioma oficial ({label})**: {trans} {'('+roman+')' if roman else ''}")
        if audio:
            st.sidebar.audio(audio, format="audio/mp3")

    if selected["dialects"]:
        st.sidebar.markdown("#### 🗣️ Dialectos")
        for label, code in selected["dialects"].items():
            trans, roman, audio = translate_and_speak(word, code)
            st.sidebar.markdown(f"**{label}**: {trans} {'('+roman+')' if roman else ''}")
            if audio:
                st.sidebar.audio(audio, format="audio/mp3")
