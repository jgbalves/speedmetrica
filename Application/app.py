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
''' StreamLit webapp main code '''

# # Importing Libraries random comment
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
from f1_analysis import f1_analysis as f1


def main():
    '''Main function'''
    # --- General app configuration ---
    favicon = Image.open("images/chapado 1.PNG")
    st.set_page_config(page_title='SpeedMetrica', page_icon=favicon, layout='wide')

    # --- Side Menu Configuration ---
    st.sidebar.title("Page")
    menu = ['Home', 'F1 Analysis']
    # menu = ['Home', 'F1 Analysis', 'Blog', 'Data Analysis', 'Lap Time Simulation']
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
        img_data_analysis = Image.open("images/data_analysis.jpg")


        # --- Header section ---
        with st.container():    # Optional
            st.subheader('Hi, I am Joao Alves, and this is:')
            st.title('SpeedMetrica')
            st.write('my project about Data Analysis in motorsport')

        # --- What I do ---
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with left_column:
                st.header("What I do")
                st.write("##")
                st.write(
                    """
                    - Data Analysis
                    - Race Engineering
                    - Amateur & Sim Racing
                    """
                )
                st.write(
                    "[Check it out!](https://www.youtube.com/channel/UCVb8NLqszxTuWQJCNJ7DSVQ)"
                )
            with right_column:
                st_lottie(lottie_coding, height=300, key='coding')

        # --- Projects ---
        with st.container():
            st.write('---')
            st.header('My Projects')
            st.write('##')
            image_column, text_column = st.columns((1, 2))
            with image_column:
                st.image(img_data_analysis)
            with text_column:
                st.subheader("Check it out the left menu a few projects!")
                st.write(
                    """
                    On going:
                    - Formula 1 lap analysis

                    Coming up:
                    - Driver KPIs
                    - Point Mass Lap Time Simulation
                    """
                )


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

    elif selected_page == 'F1 Analysis':
        # --- Top Menu ---
        years = [2022, 2021, 2020, 2019]
        event = ['Monza']
        session = ['FP1', 'FP2', 'FP3', 'Q', 'SQ', 'R']
        drivers = ['LEC', 'VER', 'HAM', 'SAI']

        with st.container():    # fast lap filters
            year_column, event_column, session_column, driver_column = st.columns(4)
            with year_column:
                dropdown_year = st.selectbox(
                    'Year',
                    years
                )
            with event_column:
                dropdown_event = st.selectbox(
                    'Event',
                    event
                )
            with session_column:
                dropdown_session = st.selectbox(
                    'Session',
                    session
                )
            with driver_column:
                selected_driver = st.multiselect(
                'Driver',
                drivers
                )


        # --- Header section ---
        speed = f1.speed_plot(dropdown_year, dropdown_event, dropdown_session, selected_driver)
        throttle = f1.throttle_plot(dropdown_year, dropdown_event, dropdown_session, selected_driver)
        delta = f1.delta_plot(dropdown_year, dropdown_event, dropdown_session, selected_driver)
        with st.container():
            st.plotly_chart(speed, use_container_width=True)
            st.plotly_chart(throttle, use_container_width=True)
            st.plotly_chart(delta, use_container_width=True)



if __name__ == '__main__':
    main()