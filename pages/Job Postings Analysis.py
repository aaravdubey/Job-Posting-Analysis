import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.write("# Job Postings Analysis 📊")
st.write("")
st.write("")
st.write("")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
df = st.session_state.df
st.subheader("Data scrapped")
st.write(df)

if not df.empty:
    time_units = {
        'hour': 1 / 24,
        'hours': 1 / 24,
        'day': 1,
        'days': 1,
        'week': 7,
        'weeks': 7,
        'month': 30, 
        'months': 30,
        'today': 0,
    }

    def convert_to_days(time_string):
        parts = time_string.split()
        if len(parts) < 2:
            return None
        if parts[0] == 'Posted' or parts[0] == 'Just':
            return 0
        value = int(parts[0])
        unit = parts[1].lower()
        if unit not in time_units:
            return None
        return value * time_units[unit]

    if not pd.api.types.is_numeric_dtype(df['Posted']):
        df['Posted'] = df['Posted'].apply(convert_to_days)

    hist_values = df['Posted'].dropna().astype(int)
    hist, bins = np.histogram(hist_values, bins=30)
    hist_df = pd.DataFrame({
        "Days Ago": bins[:-1], 
        "Frequency": hist
    })

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Posting frequency on daily basis")
    st.write("")
    # st.bar_chart(hist_df, x="Days Ago", y="Frequency", use_container_width=True)
    st.line_chart(hist_df, x="Days Ago", y="Frequency", use_container_width=True)


    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Job Postings Per Company")
    st.write("")
    company_counts = df['Company'].value_counts().reset_index()
    company_counts.columns = ['Company', 'Count']

    chart = alt.Chart(company_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Company", type="nominal"),
    )

    st.altair_chart(chart, use_container_width=True)




    def categorize_experience(experience):
        if 'Years' in experience:
            years = int(experience.split()[0])
            if years <= 2.5 or experience.strip() == '1 - 6 yrs':
                return '0 - 2.5 Years'
            elif years <= 5:
                return '2.5 - 5 Years'
            elif years <= 7:
                return '5 - 7 Years'
            elif years <= 10:
                return '7 - 10 Years'
            else:
                return 'More than 10 Years'
        elif 'to' in experience:
            return experience
        elif 'yrs' in experience:
            return experience
        else:
            print(experience)
            return 'Other'

    experience_categories = [categorize_experience(exp) for exp in df['Experience']]
    experience_counts = pd.Series(experience_categories).value_counts()

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Experience Level Frequency Distribution")
    st.write("")

    st.bar_chart(experience_counts)

else:
    st.info("Analysis charts will be displayed once the data is scrapped 100%.")

    # Get the entire HTML text
    # html_text = soup.prettify()

    # # Write the HTML text to a file
    # with open('html_content.html', 'w', encoding='utf-8') as file:
    #     file.write(html_text)

    # print("HTML content has been saved to 'html_content.html' file.")