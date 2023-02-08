import streamlit as st
from deta import Deta

def insert_entry(player, question, effort, carbon):
    return db.insert({
        "player": player,
        "question": question,
        "effort": effort,
        "carbon": carbon
    })
    

st.title("KWAP 2023 ESG Game")
st.subheader("Achieving long-term sustainable investment outcomes")

if st.button("Click"):
    deta = Deta("c0ky03c3_FeGypxDjVhTDCQU96cfUqLkstZLvo6Bb")
    db = deta.Base("database")

    fetch_res = fb.fetch()

    for item in fetch_res.items:
        print(item)
        db.delete(item["key"])
