from bs4 import BeautifulSoup
import requests


def get_website_status_code(url_name):
    status_code = ''
    try:
        status_code = requests.get(url_name, timeout=1.0).status_code
        return status_code

    except requests.exceptions.RequestException:
        return status_code


def get_website_content(url):
    content = requests.get(url, timeout=1.0).text

    return content


def get_seo_data(content):
    soup = BeautifulSoup(content, 'html.parser')

    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    meta_tag = soup.find('meta', attrs={"name": "description"})

    if h1_tag:
        h1_tag = h1_tag.getText()
    if title_tag:
        title_tag = title_tag.getText()
    if meta_tag:
        meta_tag = meta_tag.get("content")

    return h1_tag, title_tag, meta_tag
