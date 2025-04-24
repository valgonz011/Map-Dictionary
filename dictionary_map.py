import streamlit as st
import pandas as pd
import plotly.express as px
from googletrans import Translator

# Título de la app
st.title("🌍 Diccionario mundial interactivo")

# Entrada del usuario
palabra = st.text_input("Escribe una palabra para traducir:")

if palabra:
    translator = Translator()

    # Idiomas y sus países representativos
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
        "ar": "Egypt"
    }

    # Traducir la palabra
    datos = []
    for idioma, pais in idiomas_paises.items():
        try:
            traduccion = translator.translate(palabra, dest=idioma).text
            datos.append({"País": pais, "Traducción": traduccion})
        except:
            datos.append({"País": pais, "Traducción": "Error"})

    df = pd.DataFrame(datos)

    # Mostrar tabla
    st.subheader("Traducciones:")
    st.table(df)

    # Mostrar mapa
    fig = px.choropleth(
        df,
        locations="País",
        locationmode="country names",
        color="Traducción",
        hover_name="País",
        hover_data={"Traducción": True},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(title=f"Traducción de '{palabra}' en distintos países")
    st.plotly_chart(fig)