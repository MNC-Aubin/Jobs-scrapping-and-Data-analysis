import csv
import requests
from bs4 import BeautifulSoup

""" file = open('linkedin-jobs.csv', 'a')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'description', 'onsite_remote'
                'salary', 'Location', 'criteria', 'datetime', 'Apply'])
 """
links = {"onsite": "https://www.linkedin.com/jobs/search/?currentJobId=3351674810&f_WT=1&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=",
         "remote": "https://www.linkedin.com/jobs/search/?currentJobId=3205250146&f_WRA=true&f_WT=2&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=",
         "hybrid": "https://www.linkedin.com/jobs/search/?currentJobId=3343518868&f_WRA=true&f_WT=3&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start="}

with open('linkedin-jobs.csv', mode='w', encoding='UTF-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Company', 'description', 'onsite_remote',
                     'salary', 'Location', 'criteria', 'datetime', 'Apply'])

    def linkedin_scraper(webpage, page_number, onsite_remote):        
        count = 0
        next_page = webpage + str(page_number)
        # print(str(next_page))
        response = requests.get(str(next_page))
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(response.content)
        jobs = soup.find_all(
            'div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        for job in jobs:
            count += 1
            job_criteria = []
            job_title = job.find(
                'h3', class_='base-search-card__title').text.strip()
            job_company = job.find(
                'h4', class_='base-search-card__subtitle').text.strip()
            job_location = job.find(
                'span', class_='job-search-card__location').text.strip()
            job_datetime = job.find(
                'time', class_='job-search-card__listdate')['datetime'] if job.find(
                'time', class_='job-search-card__listdate') is not None else job.find(
                'time', class_='job-search-card__listdate--new')['datetime']
            job_salary = job.find('span', class_='job-search-card__salary-info').text.strip(
            ) if job.find('span', class_='job-search-card__salary-info') is not None else "NaN"

            job_link = job.find('a', class_='base-card__full-link')['href']
            resp = requests.get(job_link)
            sp = BeautifulSoup(resp.content, 'html.parser')

            job_desc = sp.find('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5').text.strip(
            ) if sp.find('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5') is not None else "Nan"

            criteria = sp.find_all(
                'li', class_='description__job-criteria-item')
            for criterion in criteria:
                feature = criterion.find(
                    'h3', class_='description__job-criteria-subheader').text.strip()
                value = criterion.find(
                    'span', class_='description__job-criteria-text description__job-criteria-text--criteria').text.strip()
                job_criteria.append({feature: value})

            writer.writerow([job_title, job_company, job_desc, onsite_remote, job_salary,
                            job_location, job_criteria, job_datetime, job_link])
            print(str(count) + ' Data updated')

        if page_number < 950:
            page_number = page_number + 25
            linkedin_scraper(webpage, page_number, onsite_remote)
            

    for work_type in links:
        linkedin_scraper(links[work_type], 0, work_type)
