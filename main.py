import streamlit as st

st.set_page_config(page_title="Beerify", page_icon="🍻", layout="wide")

with st.sidebar:
    st.image("assets\logo.png", width=256)
    st.title("🍻 Beerify")
    st.divider()
    st.header("Filters")
    min_abv, max_abv = st.slider(
        "ABV - Alcohol by volume", value=(0, 10), max_value=10, format='%d%%'
    )
    beer_types = st.multiselect(
        "Beer Types",
        options=["All", "Pilsner", "Pale Lager", "IPA - White", "Stout - Imperial"],
        default="All",
    )
    breweries = st.multiselect(
        "Breweries",
        options=["All", "Browar Sady", "Browar Fortuna", "Browar Bojanowo"],
        default="All",
    )
    countries = st.multiselect(
        "Countries", options=["All", "Poland", "Germany", "Czechia"], default="All"
    )
    if st.button("Filter", type="primary"):
        pass  # refresh beer view

st.title("🍻 Beerify")


st.markdown(
    """ <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
    unsafe_allow_html=True,
)  # to hide menu in right upper corner with options for developers
