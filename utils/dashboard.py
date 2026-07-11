import streamlit as st


def executive_dashboard():

    st.subheader("📊 Executive Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "OEE",
        "91.8%",
        "+1.3%"
    )

    c2.metric(
        "Production",
        "128 MT",
        "+5 MT"
    )

    c3.metric(
        "Downtime",
        "38 min",
        "-12 min"
    )

    c4.metric(
        "AI Health",
        "96%",
        "+4%"
    )

    st.markdown("---")