import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Beerify", page_icon="🍻", layout="wide")

beer_df = pd.read_csv("assets/clean.csv")

@st.cache_data
def get_categories(df):
    beer_type = list(beer_df["beer_type"].unique()) + ["All"]
    beer_type.sort()
    breweries = list(beer_df["brewery"].unique()) + ["All"]
    breweries.sort()
    countries = list(beer_df["country"].unique()) + ["All"]
    countries.remove(np.nan)
    countries.sort()
    return beer_type, breweries, countries

beers, breweries, countries = get_categories(beer_df)

with st.sidebar:
    st.image("assets/logo.png", width=256)
    st.title("🍻 Beerify")
    st.divider()
    st.header("Filters")
    st.slider(
        "ABV - Alcohol by volume", value=(0, 25), max_value=25, format="%d%%", key="abv"
    )
    st.multiselect(
        "Beer Types",
        options=beers,
        default="All",
        key="beer_types",
    )
    st.multiselect(
        "Breweries",
        options=breweries,
        default="All",
        key="breweries",
    )
    st.multiselect(
        "Countries",
        options=countries,
        default="All",
        key="countries",
    )
    # if st.button("Filter", type="primary"):
    #     pass  # refresh beer view

@st.cache_data
def filtered_df(df):
    df['abv'] = df['abv'].apply(lambda x: float(x[:-1]))
    df['calories'] = df['calories'].apply(lambda x: x.rstrip("cal per 355ml"))
    df['calories'] = df['calories'].apply(lambda x: float(x) if x else None)
    df['favourite'] = False
    return df


st.title("🍻 Beerify")
st.data_editor(
    filtered_df(beer_df),
    use_container_width=True,
    hide_index=True,
    height=720,
    column_config={
        "beer_name": st.column_config.TextColumn("Beer", max_chars=100, disabled=True),
        "Unnamed: 0": None,
        "brewery": st.column_config.TextColumn("Brewery", max_chars=100, disabled=True),
        "abv": st.column_config.NumberColumn("ABV", format="%f%%", disabled=True),
        "beer_type": st.column_config.TextColumn("Beer Type", max_chars=100, disabled=True),
        "country": st.column_config.TextColumn("Country", max_chars=50, disabled=True),
        "city": st.column_config.TextColumn("City", max_chars=50, disabled=True),
        "land": st.column_config.TextColumn("Land", max_chars=50, disabled=True),
        "style_score": st.column_config.NumberColumn("Style Score", disabled=True),
        "overall_score": st.column_config.NumberColumn("Overall Score", disabled=True),
        "calories": st.column_config.NumberColumn("Calories per 355 ml",format="%d cal", disabled=True),
        "average_rating": st.column_config.NumberColumn("Average Rating", disabled=True),
        "review_average": st.column_config.NumberColumn("Average Review", disabled=True),
        "weighted_average": st.column_config.NumberColumn("Weighted Average", disabled=True),
        "description": st.column_config.TextColumn("Description", max_chars=100, disabled=True),
        "served_in": st.column_config.TextColumn("Best served in", max_chars=50, disabled=True),
        "favourite": st.column_config.CheckboxColumn("Favourite?", default=False)
    },
    column_order=("favourite", "beer_name", "beer_type", "abv", "overall_score", "description", "served_in", "calories", "brewery", "country", "land", "city", "style_score", "average_rating", "review_average", "weighted_average")
)

st.markdown(
    """ <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
    unsafe_allow_html=True,
)  # to hide menu in right upper corner with options for developers
