import streamlit as st
import pandas as pd
import plotly.express as px
from googletrans import Translator

# Título de la app
st.title("🌍 Diccionario mundial interactivo")

# Entrada del usuario
palabra = st.text_input("Escribe una palabra para traducir:")

# Selección de idioma de traducción
idioma_seleccionado = st.selectbox("Selecciona el idioma de la traducción", ["en", "es", "fr", "de", "it", "pt", "ru", "zh-cn", "ar", "ja"])

if palabra:
    translator = Translator()

    # Diccionario de idiomas y países (más países, puedes agregar más si lo necesitas)
    idiomas_paises = {
        "es": "Spain",
        "en": "United States",
        "fr": "France",
        "de": "Germany",
        "it": "Italy",
        "pt": "Brazil",
        "ru": "Russia",
        "ja": "Japan",
        "zh-cn": "China",
        "ar": "Egypt",
        "ko": "South Korea",  # Agregar más países
        # Asegúrate de incluir más países si lo deseas
    }

    # Traducir la palabra
    datos = []
    for idioma, pais in idiomas_paises.items():
        try:
            traduccion = translator.translate(palabra, dest=idioma_seleccionado).text
            datos.append({"País": pais, "Traducción": traduccion})
        except Exception as e:
            print(f"Error en la traducción para {pais}: {e}")
            datos.append({"País": pais, "Traducción": "Error"})

    df = pd.DataFrame(datos)

    # Mostrar la tabla con traducciones
    st.subheader("Traducciones:")
    st.table(df)

    # Crear un mapa interactivo mejorado
    fig = px.choropleth(
        df,
        locations="País",
        locationmode="country names",
        color="Traducción",
        hover_name="País",
        hover_data={"Traducción": True},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(
        title=f"Traducción de '{palabra}' en {idioma_seleccionado.upper()}",
        geo=dict(showland=True, landcolor="lightgray", showcoastlines=True, coastlinecolor="black")
    )

    st.plotly_chart(fig)