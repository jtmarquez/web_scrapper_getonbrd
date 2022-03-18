import requests
import pandas as pd
from bs4 import BeautifulSoup

# Making get request to getonbrd@ dev jobs
url = 'https://www.getonbrd.com/empleos/programacion/'

response = requests.get(url)
response.raise_for_status()

# Using BeautifulSoup to parse html content and access it easily
soup = BeautifulSoup(response.content, 'html.parser')
dev_jobs = list()

# Selecting all featured title jobs
featured = soup.find_all("h4", class_ = "w900 size1 m0")
for featured_job in featured:

    #Saving to array

    dev_jobs.append(featured_job.get_text()) 

# Selecting all non-featured title jobs
non_featured = soup.find_all(attrs= {"class":"gb-results-list__title"})

for non_featured_job in non_featured:

    # Saving to array

    dev_jobs.append(non_featured_job.find(attrs={"class":"color-hierarchy1"}).get_text())

# Saving data from featured and non featured jobs saved on dev_jobs
pd_dev_jobs = pd.DataFrame(dev_jobs)
pd_dev_jobs.to_csv('dev_jobs@getonbrd')
