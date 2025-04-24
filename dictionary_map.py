import streamlit as st
from streamlit_folium import folium_static
import folium
from googletrans import Translator
from gtts import gTTS
from io import BytesIO

# 🌍 TITLE
st.set_page_config(layout="wide")
st.title("🌍 Welcome to the Interactive Language Map!")
st.markdown("Explore and listen to how different countries say a word in their own language.")

# 🌍 TRANSLATOR INSTANCE
translator = Translator()

# 🌍 WORD INPUT
word = st.text_input("Enter a word to translate:")

# 🌍 LANGUAGE DATA
countries = [
    {
        "name": "Germany", "flag": "🇩🇪", "coordinates": [51.1657, 10.4515],
        "language": {"name": "German", "code": "de"},
        "dialects": {
            "Bavarian": "bar",  # not supported
            "High German": "de"
        }
    },
    {
        "name": "Italy", "flag": "🇮🇹", "coordinates": [41.8719, 12.5674],
        "language": {"name": "Italian", "code": "it"},
        "dialects": {
            "Neapolitan": "nap",  # not supported
            "Sicilian": "scn"     # not supported
        }
    },
    {
        "name": "India", "flag": "🇮🇳", "coordinates": [20.5937, 78.9629],
        "language": {"name": "Hindi", "code": "hi"},
        "dialects": {
            "Marathi": "mr",
            "Bengali": "bn"
        }
    },
]

# 🌍 BASE MAP
world_map = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

# 🌍 PLACEHOLDER FOR SELECTION
selected_info = {}

# 🌍 HANDLE CLICK ON MAP
def on_click(e):
    lat, lng = e["latlng"]
    closest_country = min(countries, key=lambda c: (c["coordinates"][0] - lat) ** 2 + (c["coordinates"][1] - lng) ** 2)
    world_map.add_child(folium.Marker(
        location=closest_country["coordinates"],
        icon=folium.Icon(color="red", icon="map-marker", prefix="fa")
    ))
    return closest_country

# 🌍 HANDLE TRANSLATION
def safe_translate(word, lang_code):
    try:
        translated = translator.translate(word, dest=lang_code)
        return translated.text, getattr(translated, "pronunciation", "")
    except Exception:
        return "[ERROR]", ""

# 🌍 AUDIO
def create_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception:
        return None

# 🌍 ADD CLICK SUPPORT
click_js = """
function(e){
    var data = {latlng: [e.latlng.lat, e.latlng.lng]};
    fetch('/_stcore/streamlit/click', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}
"""

st.markdown("---")

# Create the hover layer
for country in countries:
    folium.CircleMarker(
        location=country["coordinates"],
        radius=10,
        fill=True,
        fill_color="blue",
        color="white",
        fill_opacity=0.6,
        popup=country["name"]
    ).add_to(world_map)

if word:
    st.sidebar.header("🗺️ Selected Country Details")
    click_placeholder = st.empty()
    for country in countries:
        # Official language
        try:
            translated, romanized = safe_translate(word, country["language"]["code"])
            audio = create_audio(translated, country["language"]["code"])
        except:
            translated, romanized, audio = "[ERROR]", "", None

        st.sidebar.markdown(f"### {country['flag']} {country['name']}")
        st.sidebar.markdown(f"**Official language**: {country['language']['name']}")
        st.sidebar.markdown(f"**Translation**: {translated}")
        if romanized:
            st.sidebar.markdown(f"**Romanized**: _{romanized}_")
        if audio:
            st.sidebar.audio(audio, format="audio/mp3")

        # Dialects
        valid_dialects = {
            name: code for name, code in country["dialects"].items()
            if code not in ["bar", "nap", "scn"]
        }
        if valid_dialects:
            st.sidebar.markdown(f"**Dialects:**")
        for name, code in valid_dialects.items():
            try:
                translated_d, roman_d = safe_translate(word, code)
                audio_d = create_audio(translated_d, code)
                st.sidebar.markdown(f"**{name}**: {translated_d}")
                if roman_d:
                    st.sidebar.markdown(f"_Romanized:_ {roman_d}")
                if audio_d:
                    st.sidebar.audio(audio_d, format="audio/mp3")
            except:
                pass

# 🌍 RENDER MAP
folium_static(world_map)
