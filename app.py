import streamlit as st
from web_pages import AppPages

def main():
    # Page configuration
    st.set_page_config(
    page_title = "PDFs Chatbot",
    page_icon = "🤖",
    layout = "wide",
    initial_sidebar_state="expanded"
    )

    # Sidebar navigation
    st.sidebar.title("Navigate")
    page_option = ["Home", "Chat"]
    selected_page = st.sidebar.radio("Go to",page_option)

    # Take an instabce from the class 
    pages = AppPages()

    # Display selected page
    if selected_page == "Home":
       pages.home_page()
    elif selected_page == "Chat":
        pages.chat_page()



if __name__ == '__main__':
    main()