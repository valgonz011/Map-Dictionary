import streamlit as st
from streamlit_folium import folium_static  # Importar folium_static desde streamlit_folium
import pandas as pd
import folium
from folium import plugins
from googletrans import Translator
from gtts import gTTS
import os
from io import BytesIO

# Lista de países, coordenadas, y códigos de idioma
countries = [
    {"name": "Germany", "coordinates": [51.1657, 10.4515], "language": "de", "dialects": {"hochdeutsch": "de"}},
    {"name": "India", "coordinates": [20.5937, 78.9629], "language": "hi", "dialects": {"hindi": "hi", "punjabi": "pa"}},
    {"name": "Italy", "coordinates": [41.8719, 12.5674], "language": "it", "dialects": {"italiano": "it", "siciliano": "sc"}},
    # Agregar más países con sus dialectos
]

# Instancia del traductor de Google
translator = Translator()

# Crear el mapa base centrado en el mundo
world_map = folium.Map(location=[20, 0], zoom_start=2)

# Función para agregar marcador a los países
def add_markers_to_map(countries):
    for country in countries:
        # Usamos el nombre del país para mostrar la traducción de la palabra
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

# Función para crear el hover con traducción y audio
def create_hover_features():
    for country in countries:
        for dialect, lang_code in country["dialects"].items():
            # Traducir la palabra al idioma del dialecto
            translated_word = translate_word(word, lang_code)
            
            # Crear el marcador con un hover que cambie de color y agregue la traducción
            folium.Marker(
                location=country["coordinates"],
                popup=f"{country['name']} ({dialect}): {translated_word}",
                icon=folium.Icon(color="green"),
                tooltip=f"{country['name']} - {dialect}: {translated_word}",  # Mostrar la traducción al pasar el mouse
                icon_create_function='function() { return L.divIcon({className: "fa fa-map-marker", iconSize: [24, 24]}); }',
            ).add_to(world_map)

# Crear la interfaz de usuario de Streamlit
st.title("Interactive World Map - Translate and Listen")
word = st.text_input("Enter a word to translate:")

if word:
    # Traducir la palabra a los dialectos
    selected_country = countries[0]  # Usar el primer país solo como ejemplo
    st.write(f"Translated word in {selected_country['name']}: {word}")
    
    # Crear el audio para la traducción
    audio = create_audio_translation(word, selected_country["language"])
    
    # Mostrar el botón para reproducir el audio
    st.audio(audio, format="audio/mp3")

# Agregar los marcadores y los hover features
add_markers_to_map(countries)
create_hover_features()

# Mostrar el mapa interactivo
folium_static(world_map)
