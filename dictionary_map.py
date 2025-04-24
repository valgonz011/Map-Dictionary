import streamlit as st
import pandas as pd
import folium
from folium import plugins
from googletrans import Translator
from folium.plugins import HeatMap

# Título de la app
st.title("🌍 Diccionario mundial interactivo")

# Entrada del usuario
palabra = st.text_input("Escribe una palabra para traducir:")

# Diccionario de países y sus idiomas principales
paises_idiomas = {
    "España": "es",
    "United States": "en",
    "Francia": "fr",
    "Alemania": "de",
    "Italia": "it",
    "Brasil": "pt",
    "Rusia": "ru",
    "China": "zh-cn",
    "Japón": "ja",
    "Egipto": "ar"
    # Puedes agregar más países aquí
}

# Si hay una palabra escrita
if palabra:
    translator = Translator()

    # Crear un mapa base de folium centrado en el mundo
    world_map = folium_
