import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium
from folium import Tooltip
from googletrans import Translator
from gtts import gTTS
from io import BytesIO

# Lista de países con dialectos
countries = [
    {
        "name": "Germany",
        "coordinates": [51.1657, 10.4515],
        "dialects": {
            "hochdeutsch": "de",
            "bavarian": "de",
            "berlinerisch": "de"
        }
    },
    {
        "name": "India",
        "coordinates": [20.5937, 78.9629],
        "dialects": {
            "hindi": "hi",
            "punjabi": "pa",
            "bengali": "bn"
        }
    },
    {
        "name": "Italy",
        "coordinates": [41.8719, 12.5674],
        "dialects": {
            "italiano": "it",
            "sicilian": "it",
            "venetian": "it"
        }
    },
    {
        "name": "Japan",
        "coordinates": [36.2048, 138.2529],
        "dialects": {
            "japanese": "ja"
        }
    },
    {
        "name": "France",
        "coordinates": [46.6034, 1.8883],
        "dialects": {
            "français": "fr",
            "occitan": "fr"
        }
    }
    # Agrega más países si quieres
]

# Lenguajes que gTTS soporta para audio
SUPPORTED_LANGS = [
    'en', 'es', 'fr', 'de', 'it', 'pt', 'hi', 'ja', 'ru', 'zh-cn', 'ko',
    'ar', 'bn', 'pa'
]

# Instancia del traductor
translator = Translator()

# Crear mapa
world_map = folium.Map(location=[20, 0], zoom_start=2)

# Función para traducir palabra + romanización si existe
def translate_word(word, lang_code):
    try:
        result = translator.translate(word, dest=lang_code)
        translit = result.pronunciation if result.pronunciation else ''
        return result.text, translit
    except Exception as e:
        st.error(f"Error al traducir la palabra: {e}")
        return None, ''

# Función para crear audio
def create_audio_translation(word, lang_code):
    if lang_code not in SUPPORTED_LANGS:
        return None
    try:
        tts = gTTS(text=word, lang=lang_code)
        audio_file = BytesIO()
        tts.save(audio_file)
        audio_file.seek(0)
        return audio_file
    except Exception as e:
        st.error(f"Error al generar audio: {e}")
        return None

# Título de la app
st.title("🌍 Interactive World Map - Dictionary Explorer")

# Input
word = st.text_input("Enter a word to translate into multiple languages:")

# Procesar si hay palabra
if word:
    for country in countries:
        for dialect, lang_code in country["dialects"].items():
            translated, romanized = translate_word(word, lang_code)

            if not translated:
                continue

            hover_text = f"{country['name']} - {dialect}: {translated}"
            if romanized and romanized.lower() != translated.lower():
                hover_text += f" ({romanized})"

            marker = folium.Marker(
                location=country["coordinates"],
                tooltip=Tooltip(hover_text),
                popup=f"{hover_text}",
                icon=folium.Icon(color="blue", icon="info-sign")
            )
            marker.add_to(world_map)

    # Mostrar primer audio como ejemplo
    sample_lang = list(countries[0]["dialects"].values())[0]
    sample_translated, _ = translate_word(word, sample_lang)
    sample_audio = create_audio_translation(sample_translated, sample_lang)
    if sample_audio:
        st.audio(sample_audio, format="audio/mp3")

# Renderizar mapa
folium_static(world_map)
