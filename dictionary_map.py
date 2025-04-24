
import streamlit as st
import pandas as pd
import folium
from folium import Marker
from streamlit_folium import folium_static
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
from math import radians, cos, sin, sqrt, atan2

# ------------------------- CONFIGURACIÓN INICIAL ------------------------- #
st.set_page_config(layout="wide")
translator = Translator()

# ----------------------------- DATOS BASE ----------------------------- #
# Se puede extender este diccionario con más países, idiomas y dialectos
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

# ----------------------------- FUNCIONES AUXILIARES ----------------------------- #
def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
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
        return translated.text, audio
    except Exception as e:
        return f"[ERROR] {str(e)}", None

# ----------------------------- INTERFAZ STREAMLIT ----------------------------- #
st.sidebar.title("🗺️ Language Info")
word = st.text_input("Enter a word to translate into multiple languages:")

selected_info = None

map_center = [20, 0]
world_map = folium.Map(location=map_center, zoom_start=2)

# Este marcador se actualizará dinámicamente con el clic
def handle_click(**kwargs):
    global selected_info
    click_coords = kwargs.get("latlng")
    if click_coords and word:
        nearest_country = find_nearest_country(click_coords)
        translations = []

        for label, lang_code in nearest_country["language"].items():
            t, audio = translate_and_speak(word, lang_code)
            translations.append((f"Oficial ({label})", t, audio))

        for dialect, lang_code in nearest_country["dialects"].items():
            t, audio = translate_and_speak(word, lang_code)
            translations.append((f"Dialecto ({dialect})", t, audio))

        selected_info = {"country": nearest_country["name"], "translations": translations}

world_map.add_child(folium.LatLngPopup())  # permite capturar el clic
folium_static(world_map)

# Mostrar resultado al hacer clic y escribir palabra
if selected_info:
    st.sidebar.markdown(f"### {selected_info['country']}")
    for label, t, audio in selected_info["translations"]:
        st.sidebar.markdown(f"**{label}:** {t}")
        if audio:
            st.sidebar.audio(audio, format="audio/mp3")
