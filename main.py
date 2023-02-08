import streamlit as st
from deta import Deta

st.title("KWAP 2023 ESG Game")
st.subheader("Achieving long-term sustainable investment outcomes")

if st.button("Click"):
    deta = Deta("project key")
    users = deta.Base("users")

    users.insert({
        "name": "Geordi",
        "title": "Chief Engineer"
    })

    fetch_res = users.fetch({"name": "Geordi"})

    for item in fetch_res.items:
        users.delete(item["key"])
