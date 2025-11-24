import streamlit as st

st.set_page_config(page_title="Login", layout="centered")

# ---- LOGIN ---
def login_page():

    st.markdown(
        """
        <style>
            .centered-img {
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }
            .centered-img img {
                max-width: 300px;
                height: auto;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Wrap st.image inside a centered div
    st.markdown('<div class="centered-img">', unsafe_allow_html=True)
    st.image("logo2.png")
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Incorrect username or password")

# ---- MAIN APP ----
def app():
    st.title("Welcome to the Dashboard 🎉")
    st.write("You are now logged in!")

# ---- ROUTER ----
if "logged_in" not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    app()
else:
    login_page()
