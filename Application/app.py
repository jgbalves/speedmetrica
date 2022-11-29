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
from speedmetrica import speedmetrica as sm


def main():
    '''Main function'''
    # --- General app configuration ---
    favicon = 'https://raw.githubusercontent.com/jgbalves/speedmetrica/master/Application/images/chapado%201.PNG'
    st.set_page_config(page_title='SpeedMetrica', page_icon=favicon, layout='wide')

    # --- Side Menu Configuration ---
    st.sidebar.title("Page")
    menu = ['Home', 'F1 Analysis', 'Data Analysis']
    # menu = ['Home', 'F1 Analysis', 'Blog', 'Data Analysis', 'Lap Time Simulation']
    selected_page = st.sidebar.selectbox(
        '',
        menu
    )


    # --- Home Page Configuration ---
    if selected_page == 'Home':

        def load_lottieurl(url):
            r = requests.get(url, timeout=2.50)
            if r.status_code != 200:
                return None
            return r.json()

        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        local_css("/style/style.css")

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
                    Already online:
                    - Formula 1 lap analysis
                    - Sim Racing Data Analysis

                    Coming up:
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

    # --- F1 Page ---
    elif selected_page == 'F1 Analysis':
        # --- Top Menu ---
        with st.container():    # fast lap filters
            year_column, event_column, session_column, driver_column = st.columns(4)
            with year_column:
                dropdown_year = st.selectbox('Year',f1.populate_year())
            with event_column:
                dropdown_event = st.selectbox('Event',f1.populate_event(dropdown_year), index=f1.populate_event(dropdown_year).index('Bahrain'))
            with session_column:
                dropdown_session = st.selectbox('Session',f1.populate_session(),  index=f1.populate_session().index('Qualifying'))
            with driver_column:
                selected_driver = st.multiselect('Driver',
                f1.populate_driver(dropdown_year, dropdown_event, dropdown_session), 
                default=['LEC', 'VER'])

        # --- Header section ---
        with st.container():
            st.plotly_chart(f1.resulting_plot(dropdown_year, dropdown_event, dropdown_session, selected_driver),
                use_container_width=True)

    # ---Data Analysis ---
    elif selected_page == 'Data Analysis':
        
        with st.container():
            outing_type = st.radio(
                "What is the outing type:",
                ('Automobilista 1', 'iRacing'))

        # --- File upload menu ---
        if outing_type == 'Automobilista 1':
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    uploaded_file_1 = st.file_uploader('Choose the first outing')
                    if (uploaded_file_1) is not None:
                        df1=sm.create_dataframe_ams1(uploaded_file_1)
                    else:
                        df1 = 'No csv uploaded'
                with col2:
                    uploaded_file_2 = st.file_uploader('Choose the second outing')
                    if (uploaded_file_2) is not None:
                        df2=sm.create_dataframe_ams1(uploaded_file_2)
                    else:
                        df2 = 'No csv uploaded'
            
            #Plot and dropdown
            with st.container():
                col1, col2 = st.columns([1, 6])
                with col1:    # Lap Dropdown
                    if (uploaded_file_1) is not None:
                        dropdown1 = st.selectbox('Outing 1 - Laps', sm.lap_counter_ams(df1))
                    else:
                        st.warning('you need to upload the first csv file.')
                    if (uploaded_file_2) is not None:
                        dropdown2 = st.selectbox('Outing 2 - Laps', sm.lap_counter_ams(df2))
                    else:
                        st.warning('you need to upload the second csv file.')
                with col2:    # Plot area
                    if (uploaded_file_1 and uploaded_file_2) is not None:
                        st.plotly_chart(
                            sm.plot_outing_ams1([
                                df1[df1['Lap Number'] == dropdown1[0]],
                                df2[df2['Lap Number'] == dropdown2[0]]]),
                                use_container_width=True)
                        st.plotly_chart(sm.plot_grip_factor_tire_pressure([df1,df2]),
                            use_container_width=True)
                        st.plotly_chart(sm.plot_grip_factor_aero([df1,df2]),
                            use_container_width=True)
                        st.plotly_chart(sm.plot_grip_factor_radar([df1,df2]),
                            use_container_width=True)

                    else:
                        st.warning('you need to upload both csv files.')

        else:
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    uploaded_file_1 = st.file_uploader('Choose the first outing')
                    if (uploaded_file_1) is not None:
                        df1=sm.create_dataframe_iracing(uploaded_file_1)
                    else:
                        df1 = 'No csv uploaded'
                        st.warning('you need to upload a csv file.')
                with col2:
                    uploaded_file_2 = st.file_uploader('Choose the second outing')
                    if (uploaded_file_2) is not None:
                        df2=sm.create_dataframe_iracing(uploaded_file_2)
                    else:
                        df2 = 'No csv uploaded'
                        st.warning('you need to upload a csv file.')
            
            #Plot and dropdown
            with st.container():
                col1, col2 = st.columns([1, 5])
                with col1:    # Lap Dropdown
                    if (uploaded_file_1) is not None:
                        dropdown1 = st.selectbox('Outing 1 - Laps', sm.lap_counter_iracing(df1))
                    else:
                        st.warning('you need to upload a csv file.')
                    if (uploaded_file_2) is not None:
                        dropdown2 = st.selectbox('Outing 2 - Laps', sm.lap_counter_iracing(df2))
                    else:
                        st.warning('you need to upload the second csv file.')
                with col2:    # Plot area
                    if (uploaded_file_1 and uploaded_file_2) is not None:
                        st.plotly_chart(sm.plot_outing_iracing([df1[df1['Lap'] == dropdown1[0]],df2[df2['Lap'] == dropdown2[0]]]), use_container_width=True)

                    else:
                        st.warning('you need to upload all csv files.')
if __name__ == '__main__':
    main()
