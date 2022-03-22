import requests
import pandas as pd
from bs4 import BeautifulSoup
import argparse



# Returns Soup object w/ request get response
def get_jobs_from_getonbrd(programacion=True, dataScience=False):

    if (programacion):
        url = 'https://www.getonbrd.com/empleos/programacion/'
    elif (dataScience):
        url = 'https://www.getonbrd.cl/jobs/data-science-analytics'
    else:
        raise Exception("You didn't assing neither developer nor data science jobs")

    # Making get request to getonbrd@ dev jobs

    response = requests.get(url)
    response.raise_for_status()

    # Using BeautifulSoup to parse html content and access it easily
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

# To-do: verify this function works for DS jobs.
def find_jobs_from_soup(soup):
    dev_jobs = list()

    # Selecting all featured title jobs
    #featured = soup.find_all("h4", class_ = "w900 size1 m0")
    #for featured_job in featured:
    #
    #    #Saving to array
    #
    #    dev_jobs.append(featured_job.get_text()) 
    #
    ## Selecting all non-featured title jobs
    non_featured = soup.find_all(attrs= {"class":"color-hierarchy2 gb-results-list__item"})

    for non_featured_job in non_featured:

        # Saving to array
        job = non_featured_job.find(attrs={"class":"color-hierarchy1"}).get_text()
        job_listing_date = non_featured_job.find(attrs={"class": "gb-results-list__date color-hierarchy3"}).get_text()
        jobs_and_date = [job.strip(), job_listing_date.strip()]
        dev_jobs.append(",".join(jobs_and_date))
    return None, dev_jobs

def save_job_data_to_file(jobs, dev, ds):
    if (dev):
        file_name = "dev_jobs@getonbrd"
    elif ds:
        file_name = "ds_jobs@getonbrd"
    else:
        raise Exception("Can't process both jobs. Select only one")
    # Saving data from featured and non featured jobs saved on dev_jobs
    pd_dev_jobs = pd.DataFrame(jobs)
    pd_dev_jobs.to_csv(file_name)
    pass

def validate_inputs():
    parser = argparse.ArgumentParser(description='A simple web scrapper for jobs listed on getonbrd.cl')

    parser.add_argument("-p", "--job", help="Select which kind of job would you like to scrape: dev (developer) or ds (as in data science )", default="dev", type = str)

    args = parser.parse_args()

    if (args.job == 'dev'):
        dev = True
        ds = False
    elif (args.job == 'ds'):
        ds = True
        dev = False
    else:
        raise Exception("Wrong input.")

    return dev, ds
if __name__ == "__main__":

    dev, ds = validate_inputs()

    job_soup = get_jobs_from_getonbrd(dev, ds)

    _, non_feat_jobs = find_jobs_from_soup(job_soup)

    save_job_data_to_file(non_feat_jobs, dev, ds)
