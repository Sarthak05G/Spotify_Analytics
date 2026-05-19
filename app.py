import streamlit as st
import spotipy
import pandas as pd
import plotly.express as px
from spotipy.oauth2 import SpotifyClientCredentials


client_id = "Your_client_id"
client_secret = "Your_client_secret"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
)


st.set_page_config(
    page_title="Spotify Dashboard",
    layout="wide"
)

st.title("Spotify Analytics Dashboard")


artist_name = st.sidebar.text_input(
    "Enter Artist Name"
)


if artist_name:

    try:



        results = sp.search(
            q=artist_name,
            type="track",
            limit=10
        )

        tracks = []


        for item in results['tracks']['items']:

            tracks.append({

                "song": item.get(
                    'name',
                    'Unknown'
                ),

                "artist": item['artists'][0].get(
                    'name',
                    'Unknown'
                ),

                "album": item['album'].get(
                    'name',
                    'Unknown'
                ),

                "release_date": item['album'].get(
                    'release_date',
                    'Unknown'
                ),

                "popularity": item.get(
                    'popularity',
                    50
                )

            })



        df = pd.DataFrame(tracks)

        if df.empty:

            st.warning(
                "No songs found"
            )

            st.stop()



        df = df.drop_duplicates(
            subset="song"
        )



        df.to_csv(
            "spotify_data.csv",
            index=False
        )



        st.subheader(
            "Track Dataset"
        )

        st.dataframe(df)


        col1, col2 = st.columns(2)

        col1.metric(
            "Total Songs",
            len(df)
        )

        col2.metric(
            "Average Popularity",
            round(
                df['popularity'].mean(),
                2
            )
        )



        st.subheader(
            "Popularity Analysis"
        )

        fig = px.bar(
            df,
            x="song",
            y="popularity",
            color="song",
            text="popularity"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.subheader(
            "Artist Distribution"
        )

        pie_fig = px.pie(
            df,
            names="artist",
            values="popularity"
        )

        st.plotly_chart(
            pie_fig,
            width="stretch"
        )


        st.subheader(
            "Release Timeline"
        )

        timeline_fig = px.line(
            df,
            x="release_date",
            y="popularity",
            markers=True
        )

        st.plotly_chart(
            timeline_fig,
            width="stretch"
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="⬇ Download Dataset",
            data=csv,
            file_name="spotify_data.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

else:

    st.info(
        "Enter artist name"
    )