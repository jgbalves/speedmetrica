# # ==============================================================================
# #
# #   _____ ____  ________________     __  ___________________  _____________
# #  / ___// __ \/ ____/ ____/ __ \   /  |/  / ____/_  __/ __ \/  _/ ____/   |
# #  \__ \/ /_/ / __/ / __/ / / / /  / /|_/ / __/   / / / /_/ // // /   / /| |
# # ___/ / ____/ /___/ /___/ /_/ /  / /  / / /___  / / / _, _// // /___/ ___ |
# #/____/_/   /_____/_____/_____/  /_/  /_/_____/ /_/ /_/ |_/___/\____/_/  |_|
# #
# #                           www.speedmetrica.com
# #
# # ==============================================================================
''' StreamLit Website main code '''

# # Importing Libraries
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import requests
import sqlite3

# Connector DB Functions
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Blog DB Functions

def create_table():
    '''Creating a db table inside the sqlite'''
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,text TEXT,postdate DATE)')

def add_data(author,title,text,postdate):
    '''Add data to the db table'''
    c.execute('INSERT INTO blogtable(author,title,text,postdate) VALUES (?,?,?,?)',(author,title,text,postdate))
    conn.commit()

def view_all_notes():
    '''To view all blog notes'''
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data

def view_all_titles():
    c.execute('SELECT DISTINCT title FROM blogtable')
    data = c.fetchall()
    return data

# Blog Layout Templates

html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">Simple Blog </h1>
</div>
"""
title_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
<h6>Author:{}</h6>
<br/>
<br/> 
<p style="text-align:justify">{}</p>
</div>
"""
article_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>Author:{}</h6> 
<h6>Post Date: {}</h6>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
head_message_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
<h6>Author:{}</h6> 
<h6>Post Date: {}</h6> 
</div>
"""
full_message_temp ="""
<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""


def main():
    '''Main function'''
    # --- General app configuration ---
    st.set_page_config(page_title='SpeedMetrica', page_icon=':chart:', layout='wide')

    # --- Side Menu Configuration ---
    st.sidebar.title("Menu")
    menu = ['Home', 'Blog', 'Add Post', 'Search', 'Manage']
    selected_page = st.sidebar.selectbox(
        '',
        menu
    )

    # --- Home Page Configuration ---
    if selected_page == 'Home':

        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        local_css("style/style.css")

        # --- Load Assets ---
        lottie_coding = load_lottieurl(
            "https://assets9.lottiefiles.com/private_files/lf30_kmn9juoo.json"
        )
        img_contact_form = Image.open("images/ayrton cena - Copia (2).jfif")
        img_lottie_animation = Image.open("images/ilxl00419yv51.jpg")

        # --- Header section ---
        with st.container():    # Optional
            st.subheader('Hi, I am Joao Alves')
            st.title('A Brazilian Data analyst')
            st.write('I am passionate about motorsport and metrics')
            st.write('[Learn More](https://speedmetrica.com/)')

        # --- What I do ---
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with left_column:
                st.header("What I do")
                st.write("##")
                st.write(
                    """
                    Some lines to test:
                    - Topic structures and how we see them in the website
                    - Topic structures and how we see them in the website
                    - Topic structures and how we see them in the website
                    """
                )
                st.write("[youtube](https://www.youtube.com/channel/UCVb8NLqszxTuWQJCNJ7DSVQ)")
            with right_column:
                st_lottie(lottie_coding, height=300, key='coding')

        # --- Projects ---
        with st.container():
            st.write('---')
            st.header('My Projects')
            st.write('##')
            image_column, text_column = st.columns((1, 2))
            with image_column:
                st.image(img_lottie_animation)
            with text_column:
                st.subheader("Watch a some sim laps and karting laps")
                st.write(
                    """
                    Watch and learn how to guarantee a basic lap in some popular circuits
                    """
                )
                st.markdown("[Watch Video](https://www.youtube.com/watch?v=a7k0BnQnw90)")

        with st.container():
            image_column, text_column = st.columns((1, 2))
            with image_column:
                st.image(img_contact_form)
            with text_column:
                st.subheader("Lets test some diff image formats")
                st.write(
                    """
                    We will se if jlif format can work on
                    """
                )
                st.markdown("[Watch Video](https://www.youtube.com/watch?v=a7k0BnQnw90)")

        # --- Contact Us ---
        with st.container():
            st.write("---")
            st.header("Get in touch through those channels:")
            st.write("##")

            # Documentation https://formsubmit.co/

            contact_form = """
            <form action="https://formsubmit.co/jgbalves.23@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
            </form>
            """
            left_column, right_column = st.columns(2)
            with left_column:
                st.markdown(contact_form, unsafe_allow_html=True)
            with right_column:
                st.empty()
        # --- Blog Test --- (ERASE LATER)
        with st.container():
            st.write("---")
            st.header("Blog Results:")
            st.write("##")
            result = view_all_notes()
            # st.write(result)
            for i in result:
                b_author = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                st.markdown(title_temp.format(b_title, b_author, b_article, b_post_date), unsafe_allow_html=True)





    # --- Blog Page ---
    elif selected_page == 'Blog':
        st.subheader('Blog')

        postlist = st.sidebar.selectbox('View posts',['Post 1', 'Post 2'])

    # --- Add Post ---
    elif selected_page == 'Add Post':
        st.subheader('Add Post')
        create_table()
        blog_author = st.text_input('Enter Author Name', max_chars=50)
        blog_title = st.text_input('Enter Post Title')
        blog_text = st.text_area('Post Article Here', height=200)
        blog_post_date = st.date_input('Date')
        if st.button('Add'):
            add_data(blog_author, blog_title, blog_text, blog_post_date)
            st.success('Post:{} saved'.format(blog_title))


    # --- Search ---
    elif selected_page == 'Search':
        st.subheader('Search')

    # --- Manage ---
    elif selected_page == 'Manage':
        st.subheader('Manage')

if __name__ == '__main__':
    main()
