import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

titles = []
companies = []
locations = []
experiences = []
qualifications = []
descriptions = []
posted_dates = []
sources = []

progress_bar = st.progress(0)
progress_value = st.text("0% scrapping...")

st.write("")
st.write("")
st.write("# Job Postings 💼")
st.write("")
col1, col2 = st.columns(2)
role = col1.text_input("Enter Your Job Title", "")
location = col2.text_input("Enter Your Location", "")
exp = st.slider("Experience", min_value=0, max_value=15, step=1)
st.write("")

data = {
    'q': 'react', 
    'l': 'bangalore' 
}

if role == "" and location == "":
    url = "https://www.freshersworld.com/jobs/jobsearch"
    url2 = "https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35"
    url3 = "https://www.shine.com/job-search/all-jobs?q=all"
else: 
    url = f"https://www.freshersworld.com/jobs/jobsearch/{role}-jobs-in-{location}?experience={exp*12}"
    url2 = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=&txtKeywords={role}&txtLocation={location}&cboWorkExp1={exp}"
    url3 = f"https://www.shine.com/job-search/{role}-jobs-in-{location}?q={role}&loc={location}&minexp={exp}"

print(url)
st.markdown(
    """
    <style>
    .card {
        padding: 20px;
        border-radius: 10px;
        transition: 0.3s;
        background-color: #fff;
        margin-bottom: 20px;
        color: #333333;
    }
    .card h2 {
        margin-top: 0;
    }
    .card p {
        margin-bottom: 0;
    }
    .card a {
        color: #fff!important;
        background-color: #1a6a9d;
        border: none;
        margin-top: 1rem;
        padding: 5px 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }

    .card a:hover {
        background-color: #11476a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# left, right = st.columns(2)   

def card(title, company, location, experience, qualifications, description, posted, url, src):
    content = f"""
    <h4>{title}</h4>
    <p><strong>Company:</strong> {company}</p>
    <p><strong>Location:</strong> {location}</p>
    <p><strong>Experience:</strong> {experience}</p>
    <p><strong>Qualifications:</strong> {qualifications}</p>
    <p><strong>Description:</strong> {description}</p>
    <p><strong>Posted:</strong> {posted}</p>
    <p><strong>Source:</strong> {src}</p>
    <a type="button" href="{url}" target="_blank">Apply Now</a>
    """
    st.markdown(f"<div class='card'>{content}</div>", unsafe_allow_html=True)
    # if src == "www.freshersworld.com":
    #     left.markdown(f"<div class='card'>{content}</div>", unsafe_allow_html=True)
    # elif src == "www.timesjobs.com":
    #     right.markdown(f"<div class='card'>{content}</div>", unsafe_allow_html=True)

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find_all('div', class_='job-container')

    for job in jobs:
        title = job.find('span', class_='wrap-title').text.strip()
        company = job.find('h3', class_='company-name').text.strip()
        location = job.find('span', class_='job-location').text.strip()
        experience = job.find('span', class_='experience').text.strip()
        qualification = job.find('span', class_='qualifications').text.strip()
        description = job.find('span', class_='desc').text.strip()
        posted = job.find('span', class_='ago-text').text.strip()
        url = soup.find('div', class_='job-container')['job_display_url']

        titles.append(title)
        companies.append(company)
        locations.append(location)
        experiences.append(experience)
        qualifications.append(qualification)
        descriptions.append(description)
        posted_dates.append(posted)
        sources.append("Freshersworld")

        card(title.split(" at ")[0], company, location, experience, qualification, description, posted, url, "www.freshersworld.com")
else:
    print(response)
    print('Failed to retrieve Freshersworld.com')

for i in range(33):
    progress_bar.progress(i + 1)
progress_value.text("33% scraping...")

response2 = requests.get(url2)

if response2.status_code == 200:
    soup = BeautifulSoup(response2.text, 'html5lib')

    job_listings = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    print(len(job_listings))

    # Extract job details
    for job in job_listings:
        title = job.find('h2').text.strip()
        company = job.find('h3', class_='joblist-comp-name').text.strip()   
        experience = job.find('ul', class_='top-jd-dtl').find('li').text.strip().replace("card_travel", "")
        location = job.find('ul', class_='top-jd-dtl').find_all('li')[1].text.strip()
        description_label = job.find('label', text='Job Description:')
        description = description_label.find_next_sibling('li').text.strip() if description_label and description_label.find_next_sibling('li') else "Not available"
        
        # Check if the qualifications element exists
        qualifications_label = job.find('label', text='KeySkills:')
        qualification = qualifications_label.find_next_sibling('li').text.strip() if qualifications_label and qualifications_label.find_next_sibling('li') else "Not available"
        
        posted = job.find('span', class_='sim-posted').text.strip()

        titles.append(title)
        companies.append(company)
        locations.append(location)
        experiences.append(experience)
        qualifications.append(qualification)
        descriptions.append(description)
        posted_dates.append(posted)
        sources.append("Timesjobs")

        card(title, company, location.replace("location_on ", ""), experience, qualification, description, posted, url2, "www.timesjobs.com")

else:
    print(response2)
    print('Failed to retrieve Timesjobs.com')

for i in range(66):
    progress_bar.progress(i + 1)
progress_value.text("66% scraping...")

response2 = requests.get(url3)

if response2.status_code == 200:
    soup = BeautifulSoup(response2.text, 'html.parser')

    job_cards = soup.find_all('div', class_='jobCard_jobCard__jjUmu')

    for job_card in job_cards:
        title = job_card.find('strong', class_='jobCard_pReplaceH2__xWmHg').a.text.strip()
        company = job_card.find('div', class_='jobCard_jobCard_cName__mYnow').text.strip()
        experience = job_card.find('div', class_='jobCard_jobCard_lists__fdnsc').find('div').text.strip()
        location = job_card.find('div', class_='jobCard_jobCard_lists__fdnsc').find_all('div')[1].text.strip()
        
        job_details = job_card.find('ul', class_='jobCard_jobCard_jobDetail__jD82J')
        job_type = job_details.find_all('li')[0].text.strip() if job_details else "Not available"
        vacancies = job_details.find_all('li')[1].text.strip() if job_details and len(job_details.find_all('li')) > 1 else "Not available"
        posted = job_card.find('div', class_='jobCard_jobCard_features__wJid6').find_all('span')[1].text.strip()
        
        url = job_card.find('meta', itemprop='url')['content']

        titles.append(title)
        companies.append(company)
        locations.append(location)
        experiences.append(experience)
        qualifications.append(None)
        descriptions.append(None)
        posted_dates.append(posted)
        sources.append("Shine")

        card(title, company, location, experience, '---', vacancies, posted, url, "www.shine.com")
else:
    print(response2)
    print('Failed to retrieve Shine.com')

for i in range(100):
    progress_bar.progress(i + 1)
progress_value.text("100% scrapping completed.")

df = pd.DataFrame({
    "Title": titles,
    "Company": companies,
    "Location": locations,
    "Experience": experiences,
    "Qualifications": qualifications,
    "Description": descriptions,
    "Posted": posted_dates,
    "Source": sources
})
st.session_state['df'] = df
# st.write(df)