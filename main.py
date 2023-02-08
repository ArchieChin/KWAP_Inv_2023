# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 20:53:38 2023

@author: archi
"""

import requests
import json
import streamlit as st
from deta import Deta

def generate_entry(player, question, effort, carbon):
    return {
        "player": player,
        "question": question,
        "effort": effort,
        "carbon": carbon
    }


def clear_database():
    fetch_res = db.fetch()
    for item in fetch_res.items:
        db.delete(item["key"])


def is_entry_new(entry):
    fetch_res = db.fetch()
    unique_keys = []
    for item in fetch_res.items:
        unique_keys.append(item["question"]+item["player"])
    
    key = str(entry["question"])+entry["player"]
    
    if key in unique_keys:
        return False
    else:
        return True
        
        
def compute_score(choice):
    return 10, 10


deta = Deta("c0ky03c3_FeGypxDjVhTDCQU96cfUqLkstZLvo6Bb")
db = deta.Base("database")

st.title("KWAP 2023 Investment Retreat")
st.subheader("In Pursuit of Investment Returns and Portfolio Sustainability")

with st.form("my_form"):
    player = st.text_input('Enter your name')

    question = "1"
    choice = st.radio(
        "What\'s your favorite movie genre",
        ('Comedy', 'Drama', 'Documentary'))

    effort, carbon = compute_score(choice)
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        entry = generate_entry(player=player, question=question, effort=effort, carbon=carbon)
        if is_entry_new(entry):
            db.insert(entry)
            requests.post('https://api.powerbi.com/beta/6df17805-dab9-4c30-9af8-58a93885998a/datasets/061561f3-5c67-4a0a-a60a-4bf309306ceb/rows?language=en-gb&disableBranding=1&key=QLBQ6eTNPke9fPMU8C06Vv8IMHcabIos1wzEN1GD7tTSDdZH722Fvz6Pg0Gwd4b5lU0TQRmYqWsaj%2BVvamWGRg%3D%3D', 
                          data=json.dumps([entry]))
            st.write(f'Your answer has been submitted successfully')
    
