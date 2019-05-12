import requests
from bs4 import BeautifulSoup

def get_one_page(url, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) ' 
            'Chrome/74.0.3729.131 Safari/537.36'
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def get_one_page_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='s_position_list').find_all('li', 'con_list_item')
    urls = []
    for item in items:
        urls.append(item.find('a')['href'])
    print(len(urls))
    return urls


def get_all_pages_urls(url):
    urls = []
    pageSize = 30;
    params = {}

    for i in range(1, pageSize):
        curUrl = url + str(i) + '/'
        print(curUrl)
        html = get_one_page(curUrl, params)
        urls = list(set(urls + get_one_page_urls(html)))
    return urls



def main():
    url = 'https://www.lagou.com/zhaopin/C/'
    
    get_all_pages_urls(url)


if __name__ == '__main__':
    main()

