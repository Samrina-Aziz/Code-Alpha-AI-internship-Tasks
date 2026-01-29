import streamlit as st
from deep_translator import GoogleTranslator

st.title("🌍 Language Translation Tool")

text = st.text_area("Enter text to translate")

source_lang = st.selectbox(
    "Select Source Language",
    ["auto", "en", "es", "fr", "de", "hi"]
)

target_lang = st.selectbox(
    "Select Target Language",
    ["en", "es", "fr", "de", "hi"]
)

if st.button("Translate"):
    if text == "":
        st.warning("Please enter some text")
    else:
        translated = GoogleTranslator(
            source=source_lang,
            target=target_lang
        ).translate(text)

        st.success("Translated Text:")
        st.write(translated)

        st.code(translated)  # makes copying easy
