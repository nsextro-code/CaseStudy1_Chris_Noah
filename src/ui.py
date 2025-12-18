import streamlit as st

st.set_page_config(page_title="Case Study I – Mockup", layout="wide")

st.title("Case Study I – Geräteverwaltung")

menu = st.sidebar.selectbox(
    "Use Case auswählen",
    ["Nutzer anlegen"]
)

if menu == "Nutzer anlegen":
    st.header("Nutzer anlegen")

    email = st.text_input("E-Mail-Adresse")
    name = st.text_input("Name")

    if st.button("Speichern"):
        st.success("Nutzer wurde angelegt (Mockup)")