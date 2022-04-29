@st.experimental_singleton
def get_session():
    engine = db.create_engine('sqlite:///survey.sqlite3'+'?check_same_thread=False')
    Session = sessionmaker(bind=engine)
    return Session()
