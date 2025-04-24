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
    world_map = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodb positron')

    # Crear una lista para almacenar las traducciones
    traducciones = []

    # Recorrer el diccionario de países y traducir
    for pais, idioma in paises_idiomas.items():
        try:
            # Traducir la palabra
            traduccion = translator.translate(palabra, dest=idioma).text
            traducciones.append({"Pais": pais, "Idioma": idioma, "Traducción": traduccion})

            # Agregar marcador en el mapa para cada país con un popup
            # Usamos coordenadas aproximadas de los países
            if pais == "España":
                lat, lon = 40.4637, -3.7492
            elif pais == "United States":
                lat, lon = 37.0902, -95.7129
            elif pais == "Francia":
                lat, lon = 46.6034, 1.8883
            elif pais == "Alemania":
                lat, lon = 51.1657, 10.4515
            elif pais == "Italia":
                lat, lon = 41.9028, 12.4964
            elif pais == "Brasil":
                lat, lon = -14.2350, -51.9253
            elif pais == "Rusia":
                lat, lon = 55.7558, 37.6173
            elif pais == "China":
                lat, lon = 35.8617, 104.1954
            elif pais == "Japón":
                lat, lon = 36.2048, 138.2529
            elif pais == "Egipto":
                lat, lon = 26.8206, 30.8025

            # Crear un marcador en el mapa para este país con la traducción como popup
            folium.Marker([lat, lon], popup=f"{pais}: {traduccion}").add_to(world_map)

        except Exception as e:
            print(f"Error al traducir para {pais}: {e}")
            traducciones.append({"Pais": pais, "Idioma": idioma, "Traducción": "Error"})

    # Mostrar la tabla con traducciones
    df = pd.DataFrame(traducciones)
    st.subheader("Traducciones:")
    st.table(df)

    # Mostrar el mapa interactivo
    st.subheader("Mapa interactivo:")
    folium_static(world_map)
