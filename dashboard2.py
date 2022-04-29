from pypoll.data import *
import streamlit as st
from pypoll.data import * 
from streamlit import caching
import streamlit as st# Create a page dropdown 


#@st.cache(allow_output_mutation=True)
@st.experimental_singleton
def get_session():
    engine = db.create_engine('sqlite:///survey.sqlite3'+'?check_same_thread=False')
    Session = sessionmaker(bind=engine)
    return Session()

session = get_session()
q = get_one(session)


with st.sidebar:
    page = st.radio(
        "Choose your page", 
        ["Report", "Create Question"]
        ) 

if page == "Report":
    st.title(q.question)
    refresh = st.button("refresh")
    for o in q.options:
        st.write("{}: {}".format(o.text, o.votes))
    if refresh:
        get_session.clear()

if page == "Create Question":
    question = st.text_input("Question")
    options = st.text_area("Options (seperate by line-break)")
    save = st.button("Create")
    if save:
        add_question(session, question, options.split("\n"))