import streamlit as st

# st.set_page_config(layout="wide")
st.write("# Job Posting Analysis 📈")
st.write("")
st.markdown("""

    In my Advanced Python ESE-2 Assignment, 
            
    I have developed a Streamlit web application that scrapes job postings details from three different websites. Users can input their desired job role, location, and experience level, and the application presents relevant job postings in the form of cards. 

    Additionally, the application provides users with analysis charts based on the scraped data, allowing them to gain insights into trends and patterns in the job market. This project showcases both web scraping techniques and data visualization skills, providing users with a valuable tool for exploring job opportunities and market trends.
""")
st.write("")
st.write("")
st.write("###### Developer")
st.markdown("""
    Dubey Aarav Shailesh (2347114)
""")


st.write("")
st.write("")
st.write("")
st.write("###### Websites used for scrapping")
col1, col2, col3 = st.columns(3)
col3.write("") 
col3.write("") 
col3.image("https://static.timesjobs.com/images_cand/tj_images/personlisation/tj-logo-new.png", caption="www.freshersworld.com", width=150)
col2.write("")
col2.image("https://s3.amazonaws.com/static.freshersworld.com/adv_call_letter/fw-new-home-icon1661262022.png", caption="www.timesjobs.com", width=150)
st.write("")
col1.image("https://www.shine.com/next/static/images/shine-logo.png", caption="www.shine.com", width=120)