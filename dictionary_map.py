import streamlit as st
import pandas as pd
import folium
from folium import plugins
from googletrans import Translator
from gtts import gTTS
import os
from io import BytesIO
from folium.plugins import HeatMap

# Cargar los datos de países y dialectos
# Se puede agregar más países y dialectos aquí
countries = [
    {"name": "Germany", "coordinates": [51.1657, 10.4515], "language": "de"},
    {"name": "India", "coordinates": [20.5937, 78.9629], "language": "hi"},
    {"name": "Italy", "coordinates": [41.8719, 12.5674], "language": "it"},
    # Agregar más países aquí
]

# Instancia del traductor de Google
translator = Translator()

# Crear el mapa base centrado en el mundo
world_map = folium.Map(location=[20, 0], zoom_start=2)

# Función para agregar marcador a los países
def add_markers_to_map(countries):
    for country in countries:
        folium.Marker(
            location=country["coordinates"],
            popup=country["name"],
            icon=folium.Icon(color="blue"),
        ).add_to(world_map)

# Función para traducir una palabra
def translate_word(word, lang_code):
    translated = translator.translate(word, dest=lang_code)
    return translated.text

# Función para crear el audio de la traducción
def create_audio_translation(word, lang_code):
    tts = gTTS(text=word, lang=lang_code)
    audio_file = BytesIO()
    tts.save(audio_file)
    audio_file.seek(0)
    return audio_file

# Agregar marcadores de países al mapa
add_markers_to_map(countries)

# Crear la interfaz de usuario de Streamlit
st.title("Interactive World Map - Translate and Listen")
word = st.text_input("Enter a word to translate:")

if word:
    # Traducir la palabra al idioma del país más cercano
    selected_country = countries[0]  # Aquí solo estamos tomando el primer país como ejemplo
    translated_word = translate_word(word, selected_country["language"])
    st.write(f"Translated word in {selected_country['name']}: {translated_word}")
    
    # Crear el audio para la traducción
    audio = create_audio_translation(translated_word, selected_country["language"])
    
    # Mostrar el botón para reproducir el audio
    st.audio(audio, format="audio/mp3")

# Mostrar el mapa interactivo
folium_static(world_map)
