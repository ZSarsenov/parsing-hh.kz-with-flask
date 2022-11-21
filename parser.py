import requests
from bs4 import BeautifulSoup

headers = {
    'Host': 'hh.kz',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}
items = 100

def extract_max_page(hh_url):
    hh_request = requests.get(hh_url, headers=headers) #request
    soup = BeautifulSoup(hh_request.text, 'html.parser') #BeautifulSoup

    paginator = soup.find_all('span', {'class': "pager-item-not-in-short-range"})
    paginator_pages = []

    for page in paginator:
        paginator_pages.append(int(page.find('a').text))

    return paginator_pages[-1]


def extract_job(html):
    title = html.find('a').text
    company = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text
    company = company.strip(' ')
    company_link = html.find('a')['href']
    location = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.partition(',')[0]
    solary = []
    if html.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}) is not None:
        solary = html.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
    else:
        solary = 'не узакана'
    return {'title': title, 'company': company, 'location': location, 'company_link': company_link, 'solary': solary}

def extract_hh_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f'парсинг страницы {page}')
        result = requests.get(f'{url}&page={page}', headers=headers) # requests
        soup = BeautifulSoup(result.text, 'html.parser')  # BeautifulSoup

        results = soup.find_all('div', {'class': 'serp-item'})

    for result in results:
        job = extract_job(result)
        jobs.append(job)

    return jobs

def getJobs(keyword):
    hh_url = f'https://hh.kz/search/vacancy?&text={keyword}&currency_code=KZT&items_on_page={items}'
    hh_max_page = extract_max_page(hh_url)
    jobs = extract_hh_jobs(hh_max_page, hh_url)
    return jobs