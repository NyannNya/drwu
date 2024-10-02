import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def web_dr_wu_details(url):
    response = requests.get(url, headers={"User-Agent": UserAgent().random})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.select_one('p.Product-summary')
        description = description.text.strip() if description else "Description not found"
        image_urls = [img['data-src'] for img in soup.select('div[style="text-align: center;"] img')]     
        return {
            "description": description,
            "image_urls": image_urls
        }
    else:
        return {
            "status_code": response.status_code       
        }