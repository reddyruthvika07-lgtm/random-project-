import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Smart Networking")

users = pd.read_csv("users.csv")
connections = pd.read_csv("connections.csv")

VISIBILITY = {
    "Recruiter": [
        "name",
        "email",
        "linkedin",
        "resume",
        "portfolio"
    ],
    "Investor": [
        "name",
        "email",
        "portfolio",
        "pitch_deck"
    ],
    "Professional": [
        "name",
        "email",
        "linkedin",
        "portfolio"
    ],
    "Friend": [
        "name",
        "instagram",
        "email"
    ]
}

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Menu",
    [
        "Profile",
        "Connect",
        "Connections",
        "Analytics"
    ]
)

current_user = st.sidebar.selectbox(
    "Login As",
    users["user_id"]
)

# PROFILE

if page == "Profile":

    profile = users[
        users["user_id"] == current_user
    ].iloc[0]

    st.title("My Profile")

    st.write(profile)

# CONNECT

elif page == "Connect":

    st.title("Connect")

    scanned_user = st.selectbox(
        "Select User To Connect",
        users["user_id"]
    )

    mode = st.radio(
        "Connection Mode",
        [
            "Recruiter",
            "Investor",
            "Professional",
            "Friend"
        ]
    )

    event = st.text_input(
        "Event Name"
    )

    notes = st.text_area(
        "Notes"
    )

    if st.button("Create Connection"):

        new_row = {
            "owner_id": current_user,
            "connected_user": scanned_user,
            "mode": mode,
            "event": event,
            "notes": notes,
            "date": datetime.now()
        }

        connections.loc[
            len(connections)
        ] = new_row

        connections.to_csv(
            "connections.csv",
            index=False
        )

        profile = users[
            users["user_id"] == scanned_user
        ].iloc[0]

        visible_fields = VISIBILITY[mode]

        st.success("Connection Created")

        st.subheader(
            "Visible Profile"
        )

        for field in visible_fields:
            st.write(
                f"{field}: {profile[field]}"
            )

# CONNECTIONS

elif page == "Connections":

    st.title("My Connections")

    my_connections = connections[
        connections["owner_id"]
        == current_user
    ]

    filter_mode = st.selectbox(
        "Filter By Mode",
        ["All"]
        + list(
            my_connections["mode"]
            .dropna()
            .unique()
        )
    )

    if filter_mode != "All":
        my_connections = my_connections[
            my_connections["mode"]
            == filter_mode
        ]

    st.dataframe(my_connections)

# ANALYTICS

elif page == "Analytics":

    st.title("Networking Analytics")

    my_connections = connections[
        connections["owner_id"]
        == current_user
    ]

    st.metric(
        "Total Connections",
        len(my_connections)
    )

    if len(my_connections) > 0:

        mode_chart = px.pie(
            my_connections,
            names="mode",
            title="Connections by Mode"
        )

        st.plotly_chart(
            mode_chart,
            use_container_width=True
        )

        event_chart = px.bar(
            my_connections["event"]
            .value_counts()
            .reset_index(),
            x="event",
            y="count",
            title="Connections by Event"
        )

        st.plotly_chart(
            event_chart,
            use_container_width=True
        )