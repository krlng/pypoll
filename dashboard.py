from pypoll.data import *
import streamlit as st
from pypoll.data import * 

import streamlit as st# Create a page dropdown 

@st.cache(allow_output_mutation=True)
def get_session():
    engine = db.create_engine('sqlite:///survey.sqlite3'+'?check_same_thread=False')
    Session = sessionmaker(bind=engine)
    return Session()

session = get_session()
q = get_one(session)

with st.sidebar:
    page = st.radio(
        "Choose your page", 
        ["Voting", "Report", "Create Question"]
    ) 

if page == "Voting":
    st.title(q.question)
    selected_option = st.radio("Optionen", [o.text for o in q.options])

    vote = st.button("Vote")
    if vote:
        option = [o for o in q.options if o.text == selected_option][0]
        option.votes += 1
        session.commit()
        st.write("voted for {}".format(selected_option))

if page == "Report":
    st.title(q.question)
    for o in q.options:
        st.write("{}: {}".format(o.text, o.votes))

if page == "Create Question":
    question = st.text_input("Question")
    options = st.text_area("Options (seperate by line-break)")
    save = st.button("Create")
    if save:
      add_question(session, question, options.split("\n"))