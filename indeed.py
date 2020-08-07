#URL 요청/html가져오기
import requests
#정보(페이지) 추출 by BeautifulSoup
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"

#마지막 페이지 가져오는 첫번째 단계
def get_last_page():
    result = requests.get(URL)
#soup is object that extract data
    soup = BeautifulSoup(result.text, "html.parser")
#class는 attribute
    pagination = soup.find("div", {"class": "pagination"})
#find_all 은 모든 리스트 반환
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]

    return max_page

#2-1함수 각각의 페이지에서 구체적인 정보 추출
def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    #링크가 없는 것 때문에 만듦
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = company_anchor.string
    else:
        company = company.string

    location = html.find("span", {"class": "location"}).string

    job_id = html["data-jk"]

    return {
        'title':
        title,
        'company':
        company,
        'location':
        location,
        'link':
        f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}&tk"
    }

#최대 페이지 수만큼 request 만드는 두 번째 단계/마지막 for문을 통해 2-1 함수에 모든 request의 정보들을 추출함
def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
