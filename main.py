import streamlit as st
import pandas as pd
import requests as rq

st.set_page_config(page_title="Beerify", page_icon="🍻", layout="wide")

beer_df = pd.read_csv("assets/beers_clean_lean.csv")


@st.cache_data
def get_categories(df):
    beer_type = list(df["beer_type"].unique()) + ["All"]
    beer_type.sort()
    breweries = list(df["brewery"].unique()) + ["All"]
    breweries.sort()
    return beer_type, breweries


beers, breweries = get_categories(beer_df)

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
    st.slider("Overall Score", value=(1, 20), max_value=20, min_value=1, key="overall")


@st.cache_data
def get_filtered_df(df, min_abv, max_abv, types, breweries, min_overall, max_overall):
    df["abv"] = df["abv"].apply(lambda x: float(x[:-1]))
    df["favourite"] = False

    df = df.loc[
        (df["abv"] >= min_abv)
        & (df["abv"] <= max_abv)
        & (df["Overall"] >= min_overall)
        & (df["Overall"] <= max_overall)
    ]

    if "All" not in types:
        df = df.loc[df["beer_type"].isin(types)]

    if "All" not in breweries:
        df = df.loc[df["brewery"].isin(breweries)]

    df.drop_duplicates(subset=['beer_name'], inplace=True)

    return df


st.title("🍻 Beerify")
st.header("All beers")
edited_df = st.data_editor(
    get_filtered_df(
        beer_df,
        st.session_state["abv"][0],
        st.session_state["abv"][1],
        st.session_state["beer_types"],
        st.session_state["breweries"],
        st.session_state["overall"][0],
        st.session_state["overall"][1],
    ),
    use_container_width=True,
    hide_index=True,
    height=500,
    column_config={
        "beer_name": st.column_config.TextColumn("Beer", max_chars=100, disabled=True),
        "Unnamed: 0": None,
        "user": None,
        "user_id": None,
        "beer_id": None,
        "brewery_id": None,
        "beer_type_id": None,
        "brewery": st.column_config.TextColumn("Brewery", max_chars=100, disabled=True),
        "abv": st.column_config.NumberColumn("ABV", format="%f%%", disabled=True),
        "beer_type": st.column_config.TextColumn(
            "Beer Type", max_chars=100, disabled=True
        ),
        "calories": st.column_config.NumberColumn(
            "Calories per 355 ml", format="%f cal", disabled=True
        ),
        "Overall": st.column_config.NumberColumn("Overall", disabled=True),
        "Aroma": st.column_config.NumberColumn("Aroma", disabled=True),
        "Appearance": st.column_config.NumberColumn("Appearance", disabled=True),
        "Flavor": st.column_config.NumberColumn("Flavor", disabled=True),
        "Mouthfeel": st.column_config.NumberColumn("Mouthfeel", disabled=True),
        "favourite": st.column_config.CheckboxColumn("Favourite?", default=False),
        "rating": st.column_config.NumberColumn("Rating", disabled=True),
    },
    column_order=(
        "favourite",
        "beer_name",
        "beer_type",
        "abv",
        "rating",
        "Overall",
        "Aroma",
        "Appearance",
        "Flavor",
        "Mouthfeel",
        "calories",
        "brewery",
    ),
)

d = (
    edited_df[edited_df["favourite"] == True]["beer_type"]
    .apply(lambda s: s.split(" - ")[0])
    .value_counts()
)
d = d / d.sum()
s = ""
for hmm in dict(d):
    s += f"{hmm.replace(' ','').replace('/','').replace('-','')}={d[hmm]},"

response = None
if s[:-1]:
    api_request = f" https://3b63-104-154-24-77.ngrok-free.app/index/{s[:-1]}?k={10}"
    response = rq.get(api_request)
    response = response.json()

if response:
    st.header("Recommended for you :)")
    recom_df = beer_df.loc[beer_df["beer_name"].isin(response)].drop_duplicates(subset=["beer_name"])
    st.dataframe(
        recom_df,
        use_container_width=True,
        hide_index=True,
        height=387,
        column_config={
            "beer_name": st.column_config.TextColumn(
                "Beer", max_chars=100, disabled=True
            ),
            "Unnamed: 0": None,
            "user": None,
            "user_id": None,
            "beer_id": None,
            "brewery_id": None,
            "beer_type_id": None,
            "brewery": st.column_config.TextColumn(
                "Brewery", max_chars=100, disabled=True
            ),
            "abv": st.column_config.TextColumn("ABV", disabled=True),
            "beer_type": st.column_config.TextColumn(
                "Beer Type", max_chars=100, disabled=True
            ),
            "calories": st.column_config.NumberColumn(
                "Calories per 355 ml", format="%f cal", disabled=True
            ),
            "Overall": st.column_config.NumberColumn("Overall", disabled=True),
            "Aroma": st.column_config.NumberColumn("Aroma", disabled=True),
            "Appearance": st.column_config.NumberColumn("Appearance", disabled=True),
            "Flavor": st.column_config.NumberColumn("Flavor", disabled=True),
            "Mouthfeel": st.column_config.NumberColumn("Mouthfeel", disabled=True),
            "favourite": st.column_config.CheckboxColumn("Favourite?", default=False),
            "rating": st.column_config.NumberColumn("Rating", disabled=True),
        },
        column_order=(
            "favourite",
            "beer_name",
            "beer_type",
            "abv",
            "rating",
            "Overall",
            "Aroma",
            "Appearance",
            "Flavor",
            "Mouthfeel",
            "calories",
            "brewery",
        ),
    )

st.markdown(
    """ <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
    unsafe_allow_html=True,
)  # to hide menu in right upper corner with options for developers
