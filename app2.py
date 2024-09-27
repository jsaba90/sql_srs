import duckdb
import streamlit as st
import pandas as pd


st.write("Hello")

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    sql_query = st.text_area(label="Entrez votre input")
    st.write(f"Vous avez entré la query suivante: {sql_query}")

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
